# Run 1, stage 3 (smoke run) on Kaggle: Paradee with our 8 rows, trained from the stage-2 teacher, exported, then checked
# exactly the way the phone uses it: misaki-g2p sounds → ids → ONNX Runtime (int8 file) → Whisper.
import glob, json, os, subprocess, sys, time, traceback
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=30):
    log("$ " + c[:160]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines(); [print("   " + l) for l in out[-tail:]]
    if p.returncode: raise RuntimeError(f"failed: {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
steps = []; report = ["# Run 1 · stage 3: Paradee with Sam and Maya's 8 rows (smoke run)", ""]
def step(n, ok, note=""): steps.append((n, ok, note)); log(f"STEP {n}: {'OK' if ok else 'FAILED'} {note}")
try:
    find = lambda name: (glob.glob(f"/kaggle/input/**/{name}", recursive=True) or [None])[0]
    teacher, sam, maya = find("kokoro_run1.pth"), find("sam_voicepack.pt"), find("maya_voicepack.pt")
    if not all((teacher, sam, maya)): raise RuntimeError("stage-2 outputs not found")
    step("stage-2 teacher + voicepacks found", True)
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=2)
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/lex", tail=1)
    sh("git clone -q --depth 1 https://github.com/sahilmahendrakar/paradee", cwd=TMP)
    sh("pip install -q --no-deps --ignore-requires-python 'kokoro==0.9.4' && pip install -q attrs loguru onnx onnxruntime", tail=2)
    from huggingface_hub import hf_hub_download
    kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    step("tools installed", True)
    t = time.time()
    sh(f"python paradee_run1.py --paradee {TMP}/paradee --teacher {teacher} --kconfig {kc} --pack sam={sam} --pack maya={maya} "
       f"--g2p {TMP}/mb/misaki-g2p-cli --lex {TMP}/lex --out {TMP}/p3 --sents 300 --text-steps 600 --dec-steps 600 --bs 16 --device cuda", cwd=os.getcwd(), tail=20)   # paradee_run1.py is written next to us at start
    st = json.load(open(f"{TMP}/p3/stage3.json"))
    step("Paradee text half trained (600 steps)", True, f"held-out loss {sum(st['text_before']):.3f} → {sum(st['text_after']):.3f}")
    step("Paradee decoder trained (600 steps)", True, f"held-out loss {st['dec_before']:.3f} → {st['dec_after']:.3f}; {(time.time()-t)/60:.1f} min for stage 3 training, {st['n_rows']} teacher readings")
    onnx = f"{TMP}/p3/onnx/paradee_int8.onnx"; step("exported as one int8 ONNX file", st["export_ok"] and os.path.exists(onnx), f"{os.path.getsize(onnx)/1e6:.1f} MB" if os.path.exists(onnx) else "")
    for f in ("config.json", "export_log.txt", "stage3.json"): sh(f"cp {TMP}/p3/{f} {W}/paradee_{f}")
    sh(f"cp {onnx} {W}/paradee_run1_int8.onnx")

    # ---- the phone's way: sounds → ids → ONNX Runtime; then Whisper
    import numpy as np, onnxruntime as ort, soundfile as sf, torch
    cfg = json.load(open(f"{TMP}/p3/config.json")); vocab = cfg["vocab"]; rows = cfg["voices"]
    so = ort.SessionOptions(); so.intra_op_num_threads = 1; sess = ort.InferenceSession(onnx, so)
    lines = {"sam_normal": "So, how was your weekend? Did you do anything fun?", "sam_bright": "No way! That's amazing!",
             "maya_normal": "Hmm, interesting. Tell me more about it.", "maya_low": "Oh… I'm so sorry. Take your time."}
    p = subprocess.run([f"{TMP}/mb/misaki-g2p-cli", "--lex", f"{TMP}/lex"], input="\n".join(lines.values()) + "\n", capture_output=True, text=True, check=True)
    phs = [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
    from transformers import pipeline as hfp
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda")
    pieces = []; heard = []; tt = 0; au = 0
    for (row, text), ph in zip(lines.items(), phs):
        ids = np.array([[0, *[vocab[c] for c in ph if c in vocab], 0]], np.int64)
        t = time.time(); y = sess.run(None, {"input_ids": ids, "speed": np.ones(1, np.float32), "voice": np.array([rows.index(row)], np.int64)})[0][0]; tt += time.time() - t; au += len(y) / 24000
        h = asr(y.astype(np.float32).copy(), generate_kwargs={"language": "en"})["text"].strip()
        heard.append(f"- {row}: “{text}” → heard “{h}”"); pieces += [y, np.zeros(16800, np.float32)]
    sf.write(f"{TMP}/l.wav", np.clip(np.concatenate(pieces), -1, 1), 24000); sh(f"ffmpeg -loglevel error -y -i {TMP}/l.wav -b:a 64k {W}/run1_paradee_listen.mp3")
    step("the phone's way works (misaki-g2p → ONNX Runtime int8)", True, f"{au/tt:.1f}× real time on one CPU thread")
    report += ["## What the trained Paradee file said (Whisper)", ""] + heard + [""]
except Exception:
    tb = traceback.format_exc(); print(tb); step("ERROR", False); report += ["```", tb[-3000:], "```", ""]
report[2:2] = ["| step | result | note |", "|---|---|---|"] + [f"| {n} | {'✅' if ok else '❌'} | {note} |" for n, ok, note in steps] + [""]
report += ["RESULT: " + ("PASS" if steps and all(ok for _, ok, _ in steps) else "FAIL"), "", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

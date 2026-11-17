# Run 6 · IndexTTS-2.5 diagnostic: the same 12 sentences × 4 moods × 3 takes, Maya's voice cloned from one calm normal clip
# (m3n42_r2 from run5_rec_a), mood from IndexTTS's emotion vector, low also a little slower (duration_factor, diag.py).
# IndexTTS runs in its own uv environment (Python 3.11); the Whisper word check runs afterwards in Kaggle's Python.
import csv, glob, inspect, json, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from diag import SENTS, MOODS, EMO
T0 = time.time(); LOG = []; W = "/kaggle/working"; R = "/kaggle/tmp/index-tts"
os.makedirs(f"{W}/takes", exist_ok=True); os.makedirs("/kaggle/tmp", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, ok_fail=False):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True, cwd=cwd)
    out = (p.stdout + p.stderr)[-3000:]
    if p.returncode and not ok_fail: raise RuntimeError(c[:100] + "\n" + out)
    return p.returncode, out
report = ["# Run 6 · IndexTTS-2.5 diagnostic (12 sentences × 4 moods × 3 takes)", ""]
GEN = r'''
import inspect, json, sys, os
cfg = json.load(open(sys.argv[1]))
try:
    from indextts.infer_v2_5 import IndexTTS2
    print("module indextts.infer_v2_5")
except Exception as e:
    print("infer_v2_5 import failed:", e); from indextts.infer_v2 import IndexTTS2; print("module indextts.infer_v2")
cp = inspect.signature(IndexTTS2.__init__).parameters; print("init params:", list(cp))
kw = dict(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
for k, v in (("use_fp16", True), ("use_bf16", False), ("use_cuda_kernel", False), ("use_deepspeed", False)):
    if k in cp: kw[k] = v
tts = IndexTTS2(**kw)
ip = inspect.signature(tts.infer).parameters; print("infer params:", list(ip))
for j in cfg["jobs"]:
    a = dict(spk_audio_prompt=cfg["ref"], text=j["text"], output_path=j["out"])
    if "lang" in ip: a["lang"] = "EN"
    if "emo_vector" in ip: a["emo_vector"] = j["emo"]
    if "duration_factor" in ip: a["duration_factor"] = j["dur"]
    if "verbose" in ip: a["verbose"] = False
    try: tts.infer(**a); print("ok", j["out"], flush=True)
    except Exception as e: print("fail", j["out"], repr(e)[:300], flush=True)
'''
try:
    ref = glob.glob("/kaggle/input/**/takes/m3n42_r2.wav", recursive=True)
    if not ref: raise RuntimeError("reference clip m3n42_r2.wav not found in run5_rec_a outputs")
    ref = ref[0]; log(f"reference {ref}")
    sh(f"git clone -q https://github.com/index-tts/index-tts.git {R}")
    sh("pip install -q -U uv huggingface_hub")
    rc, out = sh("uv sync", cwd=R, ok_fail=True)
    if rc: log("uv sync failed, trying --all-extras:\n" + out[-800:]); sh("uv sync --all-extras", cwd=R)
    sh("hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints", cwd=R)
    jobs = []
    for sid, text in SENTS:
        for m in MOODS:
            for k in range(3):
                jobs.append(dict(id=f"{sid}{m[0]}", sent=sid, row=m, text=text, emo=EMO[m][0], dur=EMO[m][1], out=f"{W}/takes/{sid}{m[0]}_{k}.wav"))
    json.dump(dict(ref=ref, jobs=jobs), open("/kaggle/tmp/gen.json", "w")); open(f"{R}/gen.py", "w").write(GEN)
    t = time.time()
    p = subprocess.run("uv run python gen.py /kaggle/tmp/gen.json", shell=True, capture_output=True, text=True, cwd=R)
    gl = (p.stdout + p.stderr).splitlines()
    log(f"generation {len(jobs)} clips in {(time.time()-t)/60:.1f} min, exit {p.returncode}")
    for l in gl:
        if l.startswith(("module", "init params", "infer params", "fail", "infer_v2_5")): log(l[:300])
    if p.returncode: log("\n".join(gl[-40:]))
    # ---- Whisper word check (Kaggle's own Python)
    sh("pip install -q 'transformers==4.57.6' jiwer soundfile librosa")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:0")
    _wn = asr.tokenizer.normalize
    wn = lambda s: [w for w in _wn(s).split() if re.search(r"[a-z0-9]", w)]
    rows = []; bad = 0
    for j in jobs:
        if not os.path.exists(j["out"]): continue
        y, sr = sf.read(j["out"], dtype="float32")
        if y.ndim > 1: y = y.mean(1)
        if sr != 24000: y = librosa.resample(y, orig_sr=sr, target_sr=24000); sf.write(j["out"], y, 24000)
        y, _ = librosa.effects.trim(y, top_db=40); y = np.concatenate([np.zeros(2400), y, np.zeros(2400)]).astype(np.float32); sf.write(j["out"], y, 24000)
        heard = asr(librosa.resample(y, orig_sr=24000, target_sr=16000), generate_kwargs={"language": "en"})["text"]
        ok = jiwer.wer(" ".join(wn(j["text"])), " ".join(wn(heard)) or "x") == 0
        bad += not ok
        rows.append([j["id"], j["sent"], j["row"], j["out"].replace(W + "/", ""), j["text"], int(ok), heard.strip()])
    with open(f"{W}/takes.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["id", "sent", "row", "file", "text", "words_ok", "heard"]); w.writerows(rows)
    report += [f"clips made {len(rows)} of {len(jobs)} · words exact {len(rows) - bad}", "", "| mood | clips | words exact |", "|---|---|---|"]
    for m in MOODS:
        r = [x for x in rows if x[2] == m]; report.append(f"| {m} | {len(r)} | {sum(x[5] for x in r)} |")
    report += ["", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

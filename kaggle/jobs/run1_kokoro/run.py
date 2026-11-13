# Run 1, stage 2 (smoke run): retrain Kokoro-82M (the teacher) on the stage-1 Orpheus clips, with the
# kikiri-tts recipe (patched StyleTTS2): Stage 1 (acoustic) → Stage 2 (prosody) → voicepacks for Sam and Maya
# → Kokoro speaks test lines → Whisper check. A few epochs only: this proves the code, not the quality.
# Sounds (phonemes) come from misaki-g2p, the SAME C++ code the phone uses, plus our TextPrep (times, names).
import csv, glob, json, os, re, shutil, subprocess, sys, time, traceback
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=40):
    log("$ " + c[:160])
    p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    for l in out[-tail:]: print("   " + l)
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
report = ["# Run 1 · stage 2: Kokoro retraining (smoke run)", ""]; steps = []
def step(name, ok, note=""):
    steps.append((name, ok, note)); log(f"STEP {name}: {'OK' if ok else 'FAILED'} {note}")

# ---- TextPrep: must match the app's TextPrep (Paradee.kt) exactly
NAMES = {"Thenuka": "tˈɛnʊkə", "Kavi": "kˈʌvi", "Nimal": "nˈɪməl", "Priya": "pɹˈiə", "Galle": "ɡˈɑl", "kottu": "kˈOtu",
         "Peradeniya": "pˌɛɹədˈɛnijə",
         # provisional, not yet in the app list (add there before training for real)
         "Paati": "pˈɑti", "Paati's": "pˈɑtiz", "Madurai": "mˈɑdʊɹI", "Chennai": "ʧɛnˈI", "Jaffna": "ʤˈɑfnə"}
def prepare(t):
    def tm(m):
        h, mm = m.group(1), m.group(2)
        return f"{h} o'clock" if mm == "00" else (f"{h} oh {mm[1]}" if mm[0] == "0" else f"{h} {mm}")
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", tm, t)
    names = sorted(NAMES, key=len, reverse=True)
    return re.sub(r"\b(" + "|".join(map(re.escape, names)) + r")(?![\w'])", lambda m: f"[{m.group(1)}](/{NAMES[m.group(1)]}/)", t)

try:
    # ---- inputs from stage 1
    man = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)
    if not man: raise RuntimeError("stage-1 outputs not found under /kaggle/input")
    src = os.path.dirname(man[0]); rows = [r for r in csv.DictReader(open(man[0])) if r.get("kept") == "True"]
    log(f"stage-1 clips: {len(rows)} kept, from {src}")

    # ---- misaki-g2p (same code as the phone) + its dictionary
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=3)
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex", tail=2)
    def phon(texts):
        p = subprocess.run([f"{TMP}/mb/misaki-g2p-cli", "--lex", f"{TMP}/misaki-en-us.lex"], input="\n".join(prepare(t) for t in texts) + "\n", capture_output=True, text=True, check=True)
        return [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
    ph = phon([r["text"] for r in rows])
    for r, p in zip(rows, ph): r["ph"] = p
    step("words → sounds (misaki-g2p)", True, f"{len(ph)} lines; e.g. {rows[0]['text']} → {ph[0]}")

    # ---- the recipe
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=5)
    import torch
    log(f"torch {torch.__version__}, GPUs {torch.cuda.device_count()}")
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    step("recipe + tools installed", True)

    # ---- base weights: Kokoro-82M → StyleTTS2 format
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    raw = torch.load(kp, map_location="cpu", weights_only=False)
    strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")
    step("Kokoro base weights converted", True)

    # ---- data lists (wav|sounds|speaker) ; 2 clips held back for validation
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True)
    for who in ("sam", "maya"): os.makedirs(f"{TMP}/by/{who}", exist_ok=True)
    lines = []
    for r in rows:
        f = os.path.basename(r["file"]); shutil.copy(f"{src}/{r['file']}", f"{AUD}/{f}"); shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['who']}/{f}")
        lines.append(f"{f}|{r['ph']}|0")
    val = [lines[1], lines[-2]]; train = [l for l in lines if l not in val]
    open(f"{K}/training/train_list.txt", "w").write("\n".join(train) + "\n")
    open(f"{K}/training/val_list.txt", "w").write("\n".join(val) + "\n")
    open(f"{K}/training/OOD_texts.txt", "w").write("\n".join(r["ph"] for r in rows) + "\n")

    import yaml
    cfg = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    cfg.update(batch_size=2, epochs=2, epochs_1st=2, epochs_2nd=2, save_freq=1, max_len=200,
               pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=f"{TMP}/logs/run1", load_only_params=True)
    cfg["data_params"].update(train_data=f"{K}/training/train_list.txt", val_data=f"{K}/training/val_list.txt",
                              root_path=AUD, OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
    cfg["loss_params"]["joint_epoch"] = 1          # run the adversarial (SLM) part too, so its code is tested
    yaml.safe_dump(cfg, open(f"{K}/configs/run1.yml", "w"), sort_keys=False)

    # ---- Stage 1 (acoustic) and Stage 2 (prosody)
    t = time.time(); sh(f"python train_first.py --config_path {K}/configs/run1.yml", cwd=S, tail=25)
    c1 = sorted(glob.glob(f"{TMP}/logs/run1/epoch_1st_*.pth")); step("Kokoro stage 1 (acoustic)", bool(c1), f"{(time.time()-t)/60:.1f} min, GPU peak {torch.cuda.max_memory_allocated()/1e9:.1f} GB")
    t = time.time(); sh(f"python train_second.py --config_path {K}/configs/run1.yml", cwd=S, tail=25)
    c2 = sorted(glob.glob(f"{TMP}/logs/run1/epoch_2nd_*.pth")); step("Kokoro stage 2 (prosody + adversarial)", bool(c2), f"{(time.time()-t)/60:.1f} min")
    for f in glob.glob(f"{TMP}/logs/run1/train.log"): shutil.copy(f, f"{W}/kokoro_train_log.txt")

    # ---- voicepacks per character
    for who in ("sam", "maya"):
        sh(f"python scripts/extract_voicepack.py --model {c2[-1]} --style-encoder-model {c1[-1]} --audio-dir {TMP}/by/{who} --output {W}/{who}_voicepack.pt --device cuda", cwd=K, tail=6)
    step("voicepacks (Sam, Maya)", all(os.path.exists(f"{W}/{w}_voicepack.pt") for w in ("sam", "maya")))

    # ---- Kokoro-format weights + speak test lines (KModel only; misaki stubbed, we pass sounds directly)
    kw = {k: {("module." + a if not a.startswith("module.") else a): b for a, b in torch.load(c2[-1], map_location="cpu", weights_only=False)["net"][k].items()} for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}
    torch.save(kw, f"{TMP}/kokoro_run1.pth")
    # the kokoro package imports misaki (Python <3.13 only) for its text pipeline; we pass sounds directly, so stub it
    import types
    mk = types.ModuleType("misaki"); mk.en = types.ModuleType("misaki.en"); mk.espeak = types.ModuleType("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro", tail=2)
    sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    km = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f"{TMP}/kokoro_run1.pth").to("cuda").eval()
    import numpy as np, soundfile as sf
    tests = {"sam": ["Hey! How was your day? Did you watch the match?", "Oh no… I'm so sorry. That's really sad."],
             "maya": ["Hmm, interesting. Tell me more about it.", "Wait, really? I didn't know that!"]}
    pieces = []; heard = []
    from transformers import pipeline as hfp
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda")
    for who, ls in tests.items():
        vp = torch.load(f"{W}/{who}_voicepack.pt", map_location="cpu", weights_only=True)
        for text, p in zip(ls, phon(ls)):
            with torch.no_grad(): out = km(p, vp[len(p) - 1], 1.0)
            a = (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()
            h = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip()
            heard.append(f"- {who}: “{text}” → heard “{h}” ({len(a)/24000:.1f} s)")
            pieces += [a, np.zeros(16800, dtype=np.float32)]
    sf.write(f"{TMP}/l.wav", np.concatenate(pieces), 24000)
    sh(f"ffmpeg -loglevel error -y -i {TMP}/l.wav -b:a 64k {W}/run1_kokoro_listen.mp3")
    step("retrained Kokoro speaks (Sam, Maya)", True)
    report += ["## What the retrained Kokoro said (Whisper)", ""] + heard + [""]
except Exception:
    tb = traceback.format_exc(); print(tb); step("ERROR", False, ""); report += ["```", tb[-3000:], "```", ""]

report[2:2] = ["| step | result | note |", "|---|---|---|"] + [f"| {n} | {'✅' if ok else '❌'} | {note} |" for n, ok, note in steps] + [""]
report += ["RESULT: " + ("PASS" if steps and all(ok for _, ok, _ in steps) else "FAIL"), "", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

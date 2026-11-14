# Run 3 · real stage 2 (joint phase: decoder + MPD/MSD + WavLM adversarial) in parts of 2 epochs, each its own fresh process.
# Recipe fixes from the probes (14 Nov): transformers 4.57.6 (5.x changes the WavLM layer count in train mode);
# slmadv batch_percentage 1.0 (with batch 2 and 0.5 the SLM step never runs); crop 200 frames, SLM max_len 500 (recipe defaults;
# probe v5 peak 8.8 / 6.6 GB of 14.5); joint phase from step 1; GPU cache cleared at each epoch start.
# Data: the same 291 kept clips and 10 held-out clips as try 2 (old text with option-B v1 marks): this answers
# "does the full stage 2 improve Maya?" and gives the working recipe; the real teacher v0.2 is trained on the new recordings later.
# Quick check at the end: the 10 held-out clips, try-2 teacher vs this part, words / naturalness / voice; short blind listening.
import csv, glob, json, os, random, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
EPOCHS_1, EPOCHS_2, JOINT = 10, 2, 0
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"   # 13 Nov: stage 2 ran out of memory (T4, SLM adversarial)
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh_log(c, cwd, logfile):
    """Long training: stream everything to a file in /kaggle/working (kept even if it fails); return code."""
    log("$ " + c[:160] + f"  (log: {os.path.basename(logfile)})")
    with open(logfile, "w") as fh: rc = subprocess.run(c, shell=True, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    tail = open(logfile).read().splitlines()[-15:]; [print("   " + l) for l in tail]
    ep = [l for l in open(logfile).read().splitlines() if "Epoch [" in l]
    if ep: log("last progress: " + ep[-1][:160])
    return rc
def sh(c, cwd=None, tail=40):
    log("$ " + c[:160])
    p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    for l in out[-tail:]: print("   " + l)
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
report = ["# Run 3 · stage 2 part", ""]; steps = []
def step(name, ok, note=""):
    steps.append((name, ok, note)); log(f"STEP {name}: {'OK' if ok else 'FAILED'} {note}")


# ---- TextPrep: must match the app's TextPrep (Paradee.kt)
NAMES = {"Thenuka": "tˈɛnʊkə", "Kavi": "kˈʌvi", "Nimal": "nˈɪməl", "Priya": "pɹˈiə", "Galle": "ɡˈɑl", "kottu": "kˈOtu",
         "Peradeniya": "pˌɛɹədˈɛnijə",
         # provisional, not yet in the app list
         "Paati": "pˈɑti", "Paati's": "pˈɑtiz", "Madurai": "mˈɑdʊɹI", "Chennai": "ʧɛnˈI", "Jaffna": "ʤˈɑfnə"}
def prepare(t):
    def tm(m):
        h, mm = m.group(1), m.group(2)
        return f"{h} o'clock" if mm == "00" else (f"{h} oh {mm[1]}" if mm[0] == "0" else f"{h} {mm}")
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", tm, t)
    names = sorted(NAMES, key=len, reverse=True)
    return re.sub(r"\b(" + "|".join(map(re.escape, names)) + r")(?![\w'])", lambda m: f"[{m.group(1)}](/{NAMES[m.group(1)]}/)", t)

try:
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)
    if not tr: raise RuntimeError("run3_maya_rejudge outputs not found under /kaggle/input")
    src = os.path.dirname(tr[0]); rows = list(csv.DictReader(open(tr[0])))
    log(f"kept clips: {len(rows)} from {src}")

    # ---- misaki-g2p (same code as the phone)
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=3)
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex", tail=2)
    def phon(texts):
        p = subprocess.run([f"{TMP}/mb/misaki-g2p-cli", "--lex", f"{TMP}/misaki-en-us.lex"], input="\n".join(prepare(t) for t in texts) + "\n", capture_output=True, text=True, check=True)
        return [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
    for r, p in zip(rows, phon([r["text_b"] for r in rows])): r["ph"] = p
    step("words → sounds (misaki-g2p)", True, f"{len(rows)} lines")

    # ---- recipe
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=5)
    import torch
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    raw = torch.load(kp, map_location="cpu", weights_only=False)
    strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")
    step("recipe + Kokoro base ready", True, f"torch {torch.__version__}")

    # ---- data lists; 10 clips (spread over rows) held back for validation
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True)
    for row in ROWS: os.makedirs(f"{TMP}/by/{row}", exist_ok=True)
    lines = []
    for r in rows:
        f = os.path.basename(r["file"]); shutil.copy(f"{src}/{r['file']}", f"{AUD}/{f}"); shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['row']}/{f}")
        lines.append(f"{f}|{r['ph']}|0")
    val = lines[::29][:10]; train = [l for l in lines if l not in val]
    open(f"{K}/training/train_list.txt", "w").write("\n".join(train) + "\n")
    open(f"{K}/training/val_list.txt", "w").write("\n".join(val) + "\n")
    open(f"{K}/training/OOD_texts.txt", "w").write("\n".join(r["ph"] for r in rows) + "\n")
    import yaml
    cfg = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    cfg.update(batch_size=2, epochs=EPOCHS_2, epochs_1st=EPOCHS_1, epochs_2nd=EPOCHS_2, save_freq=2, max_len=200,
               pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=f"{TMP}/logs/run3", load_only_params=True)
    cfg["data_params"].update(train_data=f"{K}/training/train_list.txt", val_data=f"{K}/training/val_list.txt",
                              root_path=AUD, OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
    cfg["loss_params"]["joint_epoch"] = JOINT
    cfg["save_freq"] = 1
    cfg.setdefault("slmadv_params", {}).update(max_len=250, batch_percentage=0.5)   # was 500: out of memory on a T4
    yaml.safe_dump(cfg, open(f"{K}/configs/run3.yml", "w"), sort_keys=False)

    from part import PART
    EPOCHS_PER_PART = 1   # part 1 took >4 h for 2 epochs: 1 epoch per job keeps jobs short
    report[0] = f"# Run 3 · stage 2, part {PART} ({EPOCHS_PER_PART} epoch, resumed from part {PART-1})"
    sh("pip install -q 'transformers==4.57.6'", tail=2)
    st1 = glob.glob("/kaggle/input/**/kokoro_maya_v01_stage1.pth", recursive=True)[0]
    prev = glob.glob(f"/kaggle/input/**/s2_part{PART-1}.pth", recursive=True) if PART > 1 else []
    if PART > 1 and not prev: raise RuntimeError(f"part {PART-1} checkpoint not found")
    ld = f"{TMP}/logs/s2"; os.makedirs(ld, exist_ok=True); shutil.copy(st1, f"{ld}/first_stage.pth")
    cfg.update(epochs=99, epochs_2nd=99, log_dir=ld, save_freq=1, max_len=200, batch_size=2)
    cfg["loss_params"]["joint_epoch"] = 0
    cfg["slmadv_params"].update(max_len=500, batch_percentage=1.0)
    if prev: cfg.update(second_stage_load_pretrained=True, pretrained_model=prev[0], load_only_params=False)
    yaml.safe_dump(cfg, open(f"{K}/configs/s2.yml", "w"), sort_keys=False)
    tsrc = open(f"{S}/train_second.py").read()
    a1 = "    for epoch in range(start_epoch, epochs):\n"; a2 = "            torch.save(state, save_path)\n"
    assert tsrc.count(a1) == 1 and tsrc.count(a2) == 1, "patch anchors not found"
    tsrc = tsrc.replace(a1, a1 + "        torch.cuda.empty_cache(); [torch.cuda.reset_peak_memory_stats(d) for d in range(torch.cuda.device_count())]\n")
    tsrc = tsrc.replace(a2, a2 + """            globals()["_DONE"] = globals().get("_DONE", 0) + 1
            print("PEAK_GB", [round(torch.cuda.max_memory_allocated(d) / 2**30, 2) for d in range(torch.cuda.device_count())], "saved", save_path, flush=True)
            if globals()["_DONE"] >= EPOCHS_PER_PART: __import__("os")._exit(0)
""").replace("import ", f"EPOCHS_PER_PART = {EPOCHS_PER_PART}\nimport ", 1)
    open(f"{S}/train_second_part.py", "w").write(tsrc)
    t = time.time(); rc = sh_log(f"python train_second_part.py --config_path {K}/configs/s2.yml", S, f"{W}/train_second_log.txt")
    lg = open(f"{W}/train_second_log.txt").read()
    c2 = sorted(glob.glob(f"{ld}/epoch_2nd_*.pth"), key=os.path.getmtime)
    peaks = [l for l in lg.splitlines() if l.startswith("PEAK_GB")]
    ep = [l for l in lg.splitlines() if "Epoch [" in l]
    gl = [float(x) for x in re.findall(r"GenLM Loss: ([0-9.]+)", lg)]; dl = [float(x) for x in re.findall(r"DiscLM Loss: ([0-9.]+)", lg)]
    gen = [float(x) for x in re.findall(r"Gen Loss: ([0-9.]+)", lg)]
    step(f"stage 2 part {PART} ({EPOCHS_PER_PART} epochs)", rc == 0 and len(c2) >= EPOCHS_PER_PART and "OutOfMemory" not in lg,
         f"{(time.time()-t)/60:.1f} min; peaks {peaks}; log lines with GenLM>0: {sum(1 for x in gl if x > 0)}/{len(gl)}, Gen>0: {sum(1 for x in gen if x > 0)}/{len(gen)}")
    if not c2: raise RuntimeError("no stage-2 checkpoint")
    shutil.copy(c2[-1], f"{W}/s2_part{PART}.pth")
    report += [f"Checkpoint: {os.path.basename(c2[-1])} → s2_part{PART}.pth", "", "Last training log lines:", "```", *[l[:260] for l in ep[-4:]], "```", ""]

    # ---- quick check: the 10 held-out clips (never trained on), try-2 teacher vs this part
    T2 = glob.glob("/kaggle/input/**/kokoro_maya_v01.pth", recursive=True)[0]; T2d = os.path.dirname(T2)
    kw = {k: {("module." + a if not a.startswith("module.") else a): b for a, b in torch.load(c2[-1], map_location="cpu", weights_only=False)["net"][k].items()} for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}
    torch.save(kw, f"{TMP}/part.pth")
    for row in ROWS:
        sh(f"python scripts/extract_voicepack.py --model {c2[-1]} --style-encoder-model {st1} --audio-dir {TMP}/by/{row} --output {TMP}/vp_{row}.pt --device cuda", cwd=K, tail=2)
    import types
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro", tail=2); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    import numpy as np, soundfile as sf, librosa, jiwer
    models = {"try-2 teacher": (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=T2).to("cuda").eval(),
                                {r: torch.load(f"{T2d}/maya_{r}_voicepack.pt", map_location="cpu", weights_only=True) for r in ROWS}),
              f"stage 2 part {PART}": (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f"{TMP}/part.pth").to("cuda").eval(),
                                {r: torch.load(f"{TMP}/vp_{r}.pt", map_location="cpu", weights_only=True) for r in ROWS})}
    byfile = {os.path.basename(r["file"]): r for r in rows}
    VAL = [byfile[l.split("|")[0]] for l in val]
    def say(km, p, vp):
        p = p[:510]
        with torch.no_grad(): out = km(p, vp[len(p) - 1], 1.0)
        return (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()
    from transformers import pipeline as hfp, AutoFeatureExtractor, WavLMForXVector
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda")
    _wnorm = asr.tokenizer.normalize
    SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        s = re.sub(r"(\d)-(?=\d)", r"\1", s); t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wnorm(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w)]
    LOWNAMES = {n.lower() for n in NAMES} | {"wellawatte", "bambalapitiya", "kollupitiya", "thusitha", "dhananjaya", "chathurika", "thilini",
                "appam", "idiyappam", "pittu", "ayubowan", "kohomada", "arun", "appa", "amma", "nuwara", "eliya", "haputale", "silva", "fernando", "perera"}
    def errs(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]
        if not ref: return 0, 0
        o = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in LOWNAMES for j in (i - 1, i, i + 1)}
        for a in o.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad, len(ref)
    utmos = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True).to("cuda").eval()
    def mos(a16):
        with torch.no_grad(): return float(utmos(torch.tensor(a16)[None].cuda(), 16000).item())
    fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xv = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").cuda().eval()
    def spk(a16):
        with torch.no_grad():
            x = fe(a16, sampling_rate=16000, return_tensors="pt").to("cuda"); v = torch.nn.functional.normalize(xv(**x).embeddings, dim=-1)[0]
        return v.cpu().numpy()

    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    real = {os.path.basename(r["file"]): sf.read(f"{src}/{r['file']}", dtype="float32")[0] for r in VAL}
    tcen = np.mean([spk(r16(a)) for a in real.values()], 0); tcen /= np.linalg.norm(tcen)
    res = {}; clips = {}
    for name, (km, vps) in models.items():
        B = N = 0; M = []; S_ = []
        for r in VAL:
            a = say(km, r["ph"], vps[r["row"]]); clips[(name, r["file"])] = a
            h = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip(); b, n = errs(r["text"], h); B += b; N += n
            M.append(mos(r16(a))); S_.append(float(spk(r16(a)) @ tcen))
        res[name] = (100 * B / max(N, 1), np.mean(M), np.mean(S_))
    tara_m = np.mean([mos(r16(a)) for a in real.values()])
    report += ["## Quick check (10 held-out clips)", "", "| | word error | naturalness (UTMOS) | sounds like tara |", "|---|---|---|---|"]
    report += [f"| {k} | {v[0]:.1f}% | {v[1]:.2f} | {v[2]:.3f} |" for k, v in res.items()] + [f"| tara (the real clips) | – | {tara_m:.2f} | – |", ""]
    random.seed(PART); pick = random.sample(VAL, 5); items = []
    for r in pick:
        items += [("tara", real[os.path.basename(r["file"])], r)] + [(k, clips[(k, r["file"])], r) for k in models]
    random.shuffle(items); pieces = []
    for _, a, _ in items: pieces += [a.astype(np.float32), np.zeros(24000, dtype=np.float32)]
    sf.write(f"{TMP}/l.wav", np.concatenate(pieces), 24000)
    sh(f"ffmpeg -loglevel error -y -i {TMP}/l.wav -b:a 64k {W}/s2_part{PART}_listen.mp3")
    open(f"{W}/s2_part{PART}_listen_key.md", "w").write("# Key (read AFTER listening)\n\n| # | voice | mood | line |\n|---|---|---|---|\n" +
        "".join(f"| {i} | {k} | {r['row']} | {r['text']} |\n" for i, (k, _, r) in enumerate(items, 1)))
    step("quick check + listening pack (15 clips)", True)
except Exception:
    tb = traceback.format_exc(); print(tb); step("ERROR", False, ""); report += ["```", tb[-3000:], "```", ""]
report[2:2] = ["| step | result | note |", "|---|---|---|"] + [f"| {n} | {'✅' if ok else '❌'} | {note} |" for n, ok, note in steps] + [""]
report += ["## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

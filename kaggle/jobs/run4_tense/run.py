# Run 4 · step A: tense-only fine-tune (GPT review + mentor, 16 Nov). Does training keep a mood the actor gives?
# 1) Re-run teacher B's stage 2 (no adversarial, 1 epoch, all moods) from run4_t1's stage 1 and SAVE the full checkpoint
#    (the first run kept only the Kokoro-format modules, so it can't be fine-tuned further).
# 2) From that checkpoint: tense clips only, predictor trainable, everything else frozen (decoder, encoders, text side),
#    learning rate 1/10 (1e-5), 3 epochs, a checkpoint each epoch. Fresh process each phase.
# 3) Judge on the 30 matched sentences (same words, never trained on): normal (B) vs tense (B) vs tense (each epoch):
#    pitch level / range, pace, spectral tilt (energy above 1 kHz vs below, a voice-quality proxy); normal-vs-tense
#    told apart from those (cross-validated, chance 50%); word error, naturalness, same voice. The actor's own normal vs tense
#    gap on the training clips is measured the same way, as the target. Named clips for the mentor.
import csv, glob, os, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from test_data import TEST
from textprep import prepare_all
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True); os.makedirs(f"{W}/listen", exist_ok=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
ROWS = ["normal", "bright", "low", "tense"]; MOOD = "tense"; EP2 = 3
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=20):
    log("$ " + c[:160]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines(); [print("   " + l) for l in out[-tail:]]
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
def sh_log(c, cwd, logfile):
    log("$ " + c[:160] + f"  (log: {os.path.basename(logfile)})")
    with open(logfile, "w") as fh: rc = subprocess.run(c, shell=True, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    [print("   " + l) for l in open(logfile).read().splitlines()[-12:]]; return rc
report = [f"# Run 4 · step A: {MOOD}-only fine-tune (predictor only, LR 1e-5) from a re-run of teacher B", ""]
try:
    sh("pip install -q 'transformers==4.57.6'", tail=2)
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)[0]; src = os.path.dirname(tr); rows = list(csv.DictReader(open(tr)))
    st1 = glob.glob("/kaggle/input/**/kokoro_maya_v02_stage1.pth", recursive=True)[0]; L1 = os.path.dirname(st1)
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer librosa torchcrepe scikit-learn", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=3)
    import torch
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    raw = torch.load(kp, map_location="cpu", weights_only=False); strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True); ROW = {}
    for row in ROWS: os.makedirs(f"{TMP}/by/{row}", exist_ok=True)
    for r in rows:
        f = os.path.basename(r["file"]); shutil.copy(f"{src}/{r['file']}", f"{AUD}/{f}"); ROW[f] = r["row"]
        if r["split"] == "train": shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['row']}/{f}")
    for name in ("train_list.txt", "val_list.txt", "OOD_texts.txt"): shutil.copy(f"{L1}/{name}", f"{K}/training/{name}")
    full = open(f"{K}/training/train_list.txt").read().strip().splitlines()
    mood_list = [l for l in full if ROW.get(l.split("|")[0]) == MOOD]
    open(f"{K}/training/train_{MOOD}.txt", "w").write("\n".join(mood_list) + "\n")
    report += [f"Training lists: all moods {len(full)} entries; {MOOD} only {len(mood_list)} entries", ""]
    # ---- patches: loader strips "module."; don't overwrite a trained predictor_encoder when resuming; freeze; stop after N epochs
    msrc = open(f"{S}/models.py").read(); la = "            model[key].load_state_dict(params[key], strict=False)\n"
    assert msrc.count(la) == 1
    open(f"{S}/models.py", "w").write(msrc.replace(la, """            _sd = {(k[7:] if k.startswith("module.") else k): v for k, v in params[key].items()}
            _tgt = model[key].module if hasattr(model[key], "module") else model[key]
            _res = _tgt.load_state_dict(_sd, strict=False)
            print("LOADCHECK %s missing %d unexpected %d" % (key, len(_res.missing_keys), len(_res.unexpected_keys)), flush=True)
"""))
    t0 = open(f"{S}/train_second.py").read()
    a1 = "    for epoch in range(start_epoch, epochs):\n"; a2 = "            torch.save(state, save_path)\n"
    a3 = "            start_ds = True\n"; a4 = "                slm_out = slmadv(\n"
    a5 = "        # (predictor_encoder is not trained in Stage 1)\n        model.predictor_encoder = copy.deepcopy(model.style_encoder)\n"; a6 = "    n_down = model.text_aligner.n_down\n"
    for a in (a1, a2, a3, a4, a5, a6): assert t0.count(a) == 1, f"anchor missing: {a!r}"
    def make(epochs, freeze, resume_s2):
        t = t0.replace(a1, a1 + "        torch.cuda.empty_cache()\n")
        t = t.replace(a2, a2 + """            globals()["_DONE"] = globals().get("_DONE", 0) + 1
            print("SAVED", save_path, flush=True)
            if globals()["_DONE"] >= EPOCHS_PER_PART: __import__("os")._exit(0)
""")
        t = t.replace(a3, "            start_ds = False\n")
        t = t.replace(a4, "                slm_out = (torch.zeros(()).cuda(), torch.zeros((), requires_grad=True).cuda(), None) if True else slmadv(\n")
        if resume_s2: t = t.replace(a5, "        pass  # resume from a trained stage 2: keep its predictor_encoder\n")
        if freeze:
            t = t.replace(a6, a6 + """    for _k in model:
        if _k != "predictor":
            for _p in model[_k].parameters(): _p.requires_grad = False
    print("TRAINABLE", {k: sum(p.numel() for p in model[k].parameters() if p.requires_grad) for k in model}, flush=True)
""")
        return t.replace("import ", f"EPOCHS_PER_PART = {epochs}\nimport ", 1)
    import yaml
    base = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    def cfg_for(name, train_file, logdir, extra):
        c = yaml.safe_load(yaml.safe_dump(base)); os.makedirs(logdir, exist_ok=True)
        c.update(batch_size=2, epochs=99, epochs_1st=5, epochs_2nd=99, save_freq=1, max_len=200,
                 pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=logdir, load_only_params=True)
        c["data_params"].update(train_data=f"{K}/training/{train_file}", val_data=f"{K}/training/val_list.txt", root_path=AUD,
                                OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
        c["loss_params"]["joint_epoch"] = 0; c.setdefault("slmadv_params", {}).update(max_len=500, batch_percentage=1.0)
        c.update(extra); yaml.safe_dump(c, open(f"{K}/configs/{name}.yml", "w"), sort_keys=False)
    # ---- phase 1: teacher B again, full checkpoint kept
    ld1 = f"{TMP}/logs/b"; os.makedirs(ld1, exist_ok=True); shutil.copy(st1, f"{ld1}/first_stage.pth")
    cfg_for("b", "train_list.txt", ld1, {})
    open(f"{S}/train_b.py", "w").write(make(1, False, False))
    t = time.time(); rc = sh_log(f"python train_b.py --config_path {K}/configs/b.yml", S, f"{W}/train_b_log.txt")
    cb = sorted(glob.glob(f"{ld1}/epoch_2nd_*.pth"), key=os.path.getmtime)
    if not cb: raise RuntimeError(f"phase 1 failed (rc {rc})")
    ckB = torch.load(cb[-1], map_location="cpu", weights_only=False)
    torch.save({"net": {k: v for k, v in ckB["net"].items() if k not in ("mpd", "msd", "wd")}, "epoch": 0, "iters": 0}, f"{W}/s2B_full.pth")
    report += [f"Phase 1 (teacher B re-run, all moods, 1 epoch): {(time.time()-t)/60:.1f} min → s2B_full.pth (full modules, for future fine-tunes)"]
    # ---- phase 2: mood only, predictor only, LR 1e-5
    ld2 = f"{TMP}/logs/m"
    cfg_for("m", f"train_{MOOD}.txt", ld2, dict(second_stage_load_pretrained=True, pretrained_model=f"{W}/s2B_full.pth", load_only_params=True,
                                                optimizer_params=dict(lr=1e-5, bert_lr=1e-6, ft_lr=1e-5)))
    open(f"{S}/train_m.py", "w").write(make(EP2, True, True))
    t = time.time(); rc = sh_log(f"python train_m.py --config_path {K}/configs/m.yml", S, f"{W}/train_m_log.txt")
    lg = open(f"{W}/train_m_log.txt").read()
    cm = sorted(glob.glob(f"{ld2}/epoch_2nd_*.pth"), key=os.path.getmtime)
    lc = [l for l in lg.splitlines() if l.startswith("LOADCHECK")]; trn = [l for l in lg.splitlines() if l.startswith("TRAINABLE")]
    report += [f"Phase 2 ({MOOD} only): {len(cm)} checkpoints in {(time.time()-t)/60:.1f} min, rc {rc}", f"- {trn[:1]}",
               f"- load: {sum(1 for l in lc if l.endswith('missing 0 unexpected 0'))}/{len(lc)} modules clean", ""]
    if not cm: raise RuntimeError("phase 2 produced no checkpoint; see train_m_log.txt")
    # ---- export Kokoro-format + voicepacks (B: normal, tense; each epoch: tense)
    def export(ckpt, out):
        n = torch.load(ckpt, map_location="cpu", weights_only=False)["net"]
        torch.save({k: {("module." + a if not a.startswith("module.") else a): b for a, b in n[k].items()} for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}, out)
    export(cb[-1], f"{TMP}/B.pth")
    for row in ("normal", MOOD):
        sh(f"python scripts/extract_voicepack.py --model {cb[-1]} --style-encoder-model {st1} --audio-dir {TMP}/by/{row} --output {TMP}/vpB_{row}.pt --device cuda", cwd=K, tail=2)
    for i, c in enumerate(cm, 1):
        export(c, f"{TMP}/M{i}.pth")
        sh(f"python scripts/extract_voicepack.py --model {c} --style-encoder-model {st1} --audio-dir {TMP}/by/{MOOD} --output {TMP}/vpM{i}.pt --device cuda", cwd=K, tail=2)
    shutil.copy(f"{TMP}/M{len(cm)}.pth", f"{W}/kokoro_maya_{MOOD}_e{len(cm)}.pth"); shutil.copy(f"{TMP}/vpM{len(cm)}.pt", f"{W}/maya_{MOOD}_e{len(cm)}_voicepack.pt")
    # ---- judge
    import numpy as np, soundfile as sf, librosa, jiwer, types
    import marks as MK
    MK.setup("cuda")
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro"); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    Mg = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {Mg} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=2)
    sh(f"python {Mg}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex", tail=2)
    MT = [t for t in TEST if t[2] == "matched" and t[1] in ("normal", MOOD)]
    _, ph = prepare_all([t[3] for t in MT], f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex"); PH = dict(zip([t[0] for t in MT], ph))
    VOICES = {"B normal": (f"{TMP}/B.pth", f"{TMP}/vpB_normal.pt", "normal"), f"B {MOOD}": (f"{TMP}/B.pth", f"{TMP}/vpB_{MOOD}.pt", MOOD)}
    for i in range(1, len(cm) + 1): VOICES[f"{MOOD} e{i}"] = (f"{TMP}/M{i}.pth", f"{TMP}/vpM{i}.pt", MOOD)
    from transformers import pipeline as hfp, AutoFeatureExtractor, WavLMForXVector
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda"); _wn = asr.tokenizer.normalize
    wn = lambda s: [w for w in _wn(s.replace("…", " ").replace("—", " ")).split() if re.search(r"[a-z0-9]", w)]
    utmos = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True).to("cuda").eval()
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xv = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").cuda().eval()
    def spk(a):
        with torch.no_grad():
            x = fe(r16(a), sampling_rate=16000, return_tensors="pt").to("cuda"); return torch.nn.functional.normalize(xv(**x).embeddings, dim=-1)[0].cpu().numpy()
    def tilt(a):
        S_ = np.abs(librosa.stft(a, n_fft=1024, hop_length=256)) ** 2; f = librosa.fft_frequencies(sr=24000, n_fft=1024)
        return float(10 * np.log10(S_[f >= 1000].sum() / max(S_[f < 1000].sum(), 1e-9)))
    def feats(a, text):
        m = MK.measure(a, text)
        return None if not m else dict(body=m["body"], rng=m["rng"], wps=len(text.split()) / max(len(a) / 24000, .1), tilt=tilt(a))
    R, AUDS = {}, {}
    for name, (mp, vp, row) in VOICES.items():
        km = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=mp).to("cuda").eval(); pack = torch.load(vp, map_location="cpu", weights_only=True)
        for tid, trow, kind, text in MT:
            if trow != row: continue
            p = PH[tid][:510]
            with torch.no_grad(): out = km(p, pack[len(p) - 1].to("cuda"), 1.0)
            a = (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy(); AUDS[(name, tid)] = a
            h = asr(a.copy(), generate_kwargs={"language": "en"})["text"]; ref, hyp = wn(text), wn(h) or ["x"]
            bad = sum(max(x.ref_end_idx - x.ref_start_idx, x.hyp_end_idx - x.hyp_start_idx) for x in jiwer.process_words(" ".join(ref), " ".join(hyp)).alignments[0] if x.type != "equal")
            with torch.no_grad(): ms = float(utmos(torch.tensor(r16(a))[None].cuda(), 16000).item())
            R[(name, tid)] = dict(f=feats(a, text), bad=bad, n=len(ref), mos=ms, spk=spk(a))
        del km; torch.cuda.empty_cache(); log(f"judged {name}")
    # actor target: training clips normal vs tense
    act = {"normal": [], MOOD: []}
    for r in rows:
        if r["split"] == "train" and r["row"] in act:
            a = sf.read(f"{src}/{r['file']}", dtype="float32")[0]
            try:
                f_ = feats(a, r["text"])
                if f_: act[r["row"]].append(f_)
            except Exception: pass
    from sklearn.linear_model import LogisticRegression; from sklearn.model_selection import cross_val_score; from sklearn.preprocessing import StandardScaler; from sklearn.pipeline import make_pipeline
    K4 = ["body", "rng", "wps", "tilt"]
    med = lambda xs, k: float(np.median([x[k] for x in xs])) if xs else float("nan")
    def sep(A, B_):
        X = np.array([[x[k] for k in K4] for x in A + B_]); y = np.array([0] * len(A) + [1] * len(B_))
        return 100 * cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=5).mean()
    report += ["## The actor (training clips): normal vs tense", "", "| | pitch level | range | pace | tilt dB |", "|---|---|---|---|---|"]
    for row in ("normal", MOOD): report.append(f"| actor {row} | {med(act[row],'body'):.1f} | {med(act[row],'rng'):.1f} | {med(act[row],'wps'):.2f} | {med(act[row],'tilt'):.1f} |")
    report += ["", f"Actor normal vs {MOOD} told apart from these 4 measures: {sep(act['normal'], act[MOOD]):.0f}% (chance 50%; different sentences, so words also differ)", "",
               f"## Teacher on the 30 matched sentences (same words, never trained on)", "",
               "| voice | pitch level | range | pace | tilt dB | vs B normal: told apart | word error | naturalness | same voice as B normal |", "|---|---|---|---|---|---|---|---|---|"]
    bn = [R[k]["f"] for k in R if k[0] == "B normal" and R[k]["f"]]
    cen = np.mean([R[k]["spk"] for k in R if k[0] == "B normal"], 0); cen /= np.linalg.norm(cen)
    for name in VOICES:
        xs = [R[k] for k in R if k[0] == name]; fs = [x["f"] for x in xs if x["f"]]
        sp = "–" if name == "B normal" else f"{sep(bn, fs):.0f}%"
        we = 100 * sum(x["bad"] for x in xs) / max(sum(x["n"] for x in xs), 1)
        report.append(f"| {name} | {med(fs,'body'):.1f} | {med(fs,'rng'):.1f} | {med(fs,'wps'):.2f} | {med(fs,'tilt'):.1f} | {sp} | {we:.1f}% | {np.mean([x['mos'] for x in xs]):.2f} | {np.mean([x['spk'] @ cen for x in xs]):.3f} |")
    # clips: 3 sentences × (B normal, B tense, last epoch tense)
    bases = sorted({t[0][:-1] for t in MT})[:3]
    for b in bases:
        for name, tag in [("B normal", "normal_B"), (f"B {MOOD}", f"{MOOD}_B"), (f"{MOOD} e{len(cm)}", f"{MOOD}_new")]:
            tid = b + ("n" if name == "B normal" else MOOD[0])
            if (name, tid) in AUDS:
                sf.write(f"{TMP}/c.wav", AUDS[(name, tid)], 24000); sh(f"ffmpeg -loglevel error -y -i {TMP}/c.wav -b:a 64k {W}/listen/{b}_{tag}.mp3")
    texts = {t[0][:-1]: t[3] for t in MT}
    report += ["", "Clips: listen/<sentence>_normal_B / _tense_B (teacher B, as before) / _tense_new (tense-only fine-tune):"] + [f"- {b}: “{texts[b]}”" for b in bases]
    report += ["", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

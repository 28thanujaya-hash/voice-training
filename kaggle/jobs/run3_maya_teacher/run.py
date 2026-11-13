# Run 3 (Maya pilot, voice v0.1), stage 2: fine-tune Kokoro-82M (the teacher) on Maya's kept Orpheus clips
# (run3_maya_rejudge/train.csv; training text = text_b, the option-B marks), kikiri-tts recipe (patched StyleTTS2).
# One voicepack per row: maya_normal, maya_bright, maya_low, maya_tense (style from that row's clips).
# Then G2 on the 200 held-out test lines (never trained on), all by machines:
#   words (Whisper, normalised) · naturalness (UTMOS) · rows told apart (emotion2vec embeddings, nearest-centroid trained on
#   tara's own clips) · still Maya (WavLM speaker similarity to tara) · baseline = stock Kokoro af_heart on the same lines.
# Listening pack: 10 test lines, each by the teacher and by the baseline, shuffled (blind) + key.
import csv, glob, json, os, random, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from test_data import TEST
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
EPOCHS_1, EPOCHS_2, JOINT = 10, 8, 4
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=40):
    log("$ " + c[:160])
    p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    for l in out[-tail:]: print("   " + l)
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
report = ["# Run 3 · Maya pilot (voice v0.1) · stage 2: Kokoro teacher + G2", ""]; steps = []
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
    yaml.safe_dump(cfg, open(f"{K}/configs/run3.yml", "w"), sort_keys=False)

    t = time.time(); sh(f"python train_first.py --config_path {K}/configs/run3.yml", cwd=S, tail=25)
    c1 = sorted(glob.glob(f"{TMP}/logs/run3/epoch_1st_*.pth")); step("Kokoro stage 1 (acoustic)", bool(c1), f"{EPOCHS_1} epochs, {(time.time()-t)/60:.1f} min")
    t = time.time(); sh(f"python train_second.py --config_path {K}/configs/run3.yml", cwd=S, tail=25)
    c2 = sorted(glob.glob(f"{TMP}/logs/run3/epoch_2nd_*.pth")); step("Kokoro stage 2 (prosody + adversarial)", bool(c2), f"{EPOCHS_2} epochs, {(time.time()-t)/60:.1f} min")
    for f in glob.glob(f"{TMP}/logs/run3/train.log"): shutil.copy(f, f"{W}/kokoro_train_log.txt")

    for row in ROWS:
        sh(f"python scripts/extract_voicepack.py --model {c2[-1]} --style-encoder-model {c1[-1]} --audio-dir {TMP}/by/{row} --output {W}/maya_{row}_voicepack.pt --device cuda", cwd=K, tail=4)
    step("voicepacks (4 rows)", all(os.path.exists(f"{W}/maya_{r}_voicepack.pt") for r in ROWS))
    kw = {k: {("module." + a if not a.startswith("module.") else a): b for a, b in torch.load(c2[-1], map_location="cpu", weights_only=False)["net"][k].items()} for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}
    torch.save(kw, f"{W}/kokoro_maya_v01.pth")   # the teacher, for stage 3

    # ---- speak: teacher (row voicepacks) and baseline (stock Kokoro af_heart) read the test set
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
    teacher = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f"{W}/kokoro_maya_v01.pth").to("cuda").eval()
    stock = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=kp).to("cuda").eval()
    vps = {r: torch.load(f"{W}/maya_{r}_voicepack.pt", map_location="cpu", weights_only=True) for r in ROWS}
    heart = torch.load(hf_hub_download("hexgrad/Kokoro-82M", "voices/af_heart.pt"), map_location="cpu", weights_only=True)
    tph = phon([t[3] for t in TEST]); os.makedirs(f"{W}/test", exist_ok=True)
    def say(km, p, vp):
        p = p[:510]
        with torch.no_grad(): out = km(p, vp[len(p) - 1], 1.0)
        return (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()
    gen = {}
    for (tid, row, kind, text), p in zip(TEST, tph):
        gen[(tid, "teacher")] = say(teacher, p, vps[row]); gen[(tid, "baseline")] = say(stock, p, heart)
    step("teacher and baseline read the 200 test lines", True)

    # ---- judges
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
    from funasr import AutoModel as FunModel
    e2v = FunModel(model="emotion2vec/emotion2vec_plus_large", hub="hf", disable_update=True)
    def emb(a16): return np.asarray(e2v.generate(a16, granularity="utterance", extract_embedding=True)[0]["feats"]).reshape(-1)
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)

    # references: tara's own kept clips (row centroids for emotion embeddings, voice centroid, naturalness ceiling)
    ref = {r: [] for r in ROWS}; tara_spk = []; tara_mos = []
    for r in rows:
        a16 = r16(sf.read(f"{src}/{r['file']}", dtype="float32")[0]); ref[r["row"]].append(emb(a16)); tara_spk.append(spk(a16)); tara_mos.append(mos(a16))
    nz = lambda v: v / (np.linalg.norm(v) + 1e-9)
    # leave-one-out on tara: how well can the rows be told apart in the source itself (the ceiling)
    allref = [(r, v) for r in ROWS for v in ref[r]]; loo_ok = 0
    for i, (r, v) in enumerate(allref):
        cen = {q: nz(np.mean([u for j, (qq, u) in enumerate(allref) if qq == q and j != i], 0)) for q in ROWS}
        loo_ok += max(ROWS, key=lambda q: nz(v) @ cen[q]) == r
    cen = {q: nz(np.mean(ref[q], 0)) for q in ROWS}; tcen = nz(np.mean(tara_spk, 0))
    res = []
    for tid, row, kind, text in TEST:
        for who in ("teacher", "baseline"):
            a = gen[(tid, who)]; a16 = r16(a)
            h = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip(); b, n = errs(text, h)
            e = emb(a16); guess = max(ROWS, key=lambda q: nz(e) @ cen[q])
            res.append(dict(id=tid, row=row, kind=kind, who=who, text=text, heard=h, bad=b, n=n, mos=round(mos(a16), 2),
                            spk=round(float(spk(a16) @ tcen), 3), row_guess=guess, secs=round(len(a) / 24000, 2)))
            sf.write(f"{W}/test/{tid}_{who}.wav", a, 24000)
    with open(f"{W}/g2_results.csv", "w", newline="") as fh:
        wtr = csv.DictWriter(fh, list(res[0])); wtr.writeheader(); [wtr.writerow(x) for x in res]
    step("G2 judged (Whisper, UTMOS, emotion2vec, WavLM)", True)

    def summary(sel):
        n = sum(x["n"] for x in sel); b = sum(x["bad"] for x in sel)
        return b / max(n, 1), np.mean([x["mos"] for x in sel]), np.mean([x["spk"] for x in sel])
    T = [x for x in res if x["who"] == "teacher"]; Bl = [x for x in res if x["who"] == "baseline"]
    wt, mt, st = summary(T); wb, mb, sb = summary(Bl)
    rows_ok = sum(x["row_guess"] == x["row"] for x in T) / len(T)
    report += ["## G2 (draft standard: word error < 3%, naturalness ≥ 4.0, rows told apart ≥ 80%)", "",
               "| | word error | naturalness (UTMOS, /5) | sounds like tara (similarity) | rows told apart |", "|---|---|---|---|---|",
               f"| **teacher (v0.1)** | **{100*wt:.1f}%** | **{mt:.2f}** | **{st:.3f}** | **{100*rows_ok:.0f}%** |",
               f"| baseline (stock Kokoro af_heart) | {100*wb:.1f}% | {mb:.2f} | {sb:.3f} | – |",
               f"| tara's own clips (the source) | – | {np.mean(tara_mos):.2f} | {np.mean([nz(v) @ tcen for v in tara_spk]):.3f} | {100*loo_ok/len(allref):.0f}% (ceiling) |", "",
               "Rows told apart = an emotion2vec nearest-centroid judge, trained on tara's kept clips, names the row of each teacher line.", "",
               "### Teacher by row", "", "| row | word error | naturalness | told apart |", "|---|---|---|---|"]
    for row in ROWS:
        s = [x for x in T if x["row"] == row]; w_, m_, _ = summary(s)
        report.append(f"| {row} | {100*w_:.1f}% | {m_:.2f} | {sum(x['row_guess']==row for x in s)}/{len(s)} |")
    report += ["", "### Teacher by kind", "", "| kind | lines | word error | naturalness |", "|---|---|---|---|"]
    for k in ("lesson", "live", "gen", "hard"):
        s = [x for x in T if x["kind"] == k]
        if s: w_, m_, _ = summary(s); report.append(f"| {k} | {len(s)} | {100*w_:.1f}% | {m_:.2f} |")
    report += ["", "### Teacher lines with word errors", ""] + [f"- {x['id']} ({x['kind']}): “{x['text']}” → “{x['heard']}”" for x in T if x["bad"]]

    # ---- blind listening pack: 10 lines (mixed rows/kinds), each by teacher and baseline, shuffled
    random.seed(3); pick = []
    for row in ROWS: pick += random.sample([t for t in TEST if t[1] == row and t[2] != "hard"], 2)
    pick += random.sample([t for t in TEST if t[2] == "hard" and len(t[3].split()) > 3], 2)
    clips = [(t, w) for t in pick for w in ("teacher", "baseline")]; random.shuffle(clips); pieces = []
    for t, w in clips: pieces += [gen[(t[0], w)], np.zeros(24000, dtype=np.float32)]
    sf.write(f"{TMP}/l.wav", np.concatenate(pieces), 24000)
    sh(f"ffmpeg -loglevel error -y -i {TMP}/l.wav -b:a 64k {W}/run3_g2_listen.mp3")
    key = ["# Key to run3_g2_listen.mp3 (read AFTER listening)", "", "| # | voice | row | line |", "|---|---|---|---|"]
    key += [f"| {i} | {'NEW (Maya teacher v0.1)' if w == 'teacher' else 'old (stock Kokoro)'} | {t[1]} | {t[3]} |" for i, (t, w) in enumerate(clips, 1)]
    open(f"{W}/g2_listen_key.md", "w").write("\n".join(key) + "\n")
    step("blind listening pack (20 clips)", True)
except Exception:
    tb = traceback.format_exc(); print(tb); step("ERROR", False, ""); report += ["```", tb[-3000:], "```", ""]

report[2:2] = ["| step | result | note |", "|---|---|---|"] + [f"| {n} | {'✅' if ok else '❌'} | {note} |" for n, ok, note in steps] + [""]
report += ["RESULT: " + ("DONE" if steps and all(ok for _, ok, _ in steps) else "FAIL"), "", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

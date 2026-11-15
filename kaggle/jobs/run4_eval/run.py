# Run 4 · step 12 (G2) for teacher v0.2: A (stage 2 with adversarial) vs B (without) vs stock Kokoro (af_heart).
# Validation set (39 recordings with real tara takes, never trained on) = for CHOOSING A or B.
# Test set (620 lines, never recorded/trained) = for REPORTING only.
# Measures: word error (Whisper, normalised) · naturalness (UTMOS) · sounds like tara (WavLM x-vector) · marks (same
# measurement and thresholds as the actor audit, per mark × mood) · marks v2: marked minus plain on the same sentence ·
# moods on matched lines (pitch level / range per row; mood guessed from pitch features, cross-validated).
# Listening: 10 items (6 marks, 4 matched-mood) by A and B as named clips X/Y; key separate.
import csv, glob, os, random, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from test_data import TEST
from textprep import prepare_all
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True); os.makedirs(f"{W}/listen", exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]
KINDS = ["q", "qx", "ex", "dots", "dash", "caps"]; KN = {"q": "? (yes/no)", "qx": "?!", "ex": "!", "dots": "…", "dash": "—", "caps": "CAPS"}
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=20):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 4 · G2: teacher v0.2 A (with adversarial) vs B (without) vs stock Kokoro", ""]
try:
    sh("pip install -q 'transformers==4.57.6' jiwer soundfile librosa torchcrepe scikit-learn")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    import marks as MK
    MK.setup("cuda")
    # ---- misaki + kokoro
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4")
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex")
    cli, lex = f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex"
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP); K = f"{TMP}/kt"
    import types
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro"); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    heart = torch.load(hf_hub_download("hexgrad/Kokoro-82M", "voices/af_heart.pt"), map_location="cpu", weights_only=True)
    models = {}
    for tag in ("A", "B"):
        f = glob.glob(f"/kaggle/input/**/kokoro_maya_v02_{tag}.pth", recursive=True)
        if not f: log(f"model {tag} missing"); continue
        d = os.path.dirname(f[0])
        models[tag] = (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f[0]).to("cuda").eval(),
                       {r: torch.load(f"{d}/maya_{r}_voicepack.pt", map_location="cpu", weights_only=True) for r in ROWS})
    models["stock"] = (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=kp).to("cuda").eval(), {r: heart for r in ROWS})
    def say(tag, p, row):
        km, vps = models[tag]; p = p[:510]
        with torch.no_grad(): out = km(p, vps[row][len(p) - 1], 1.0)
        return (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()

    # ---- sets
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)[0]; src = os.path.dirname(tr); arows = list(csv.DictReader(open(tr)))
    VAL = [(r["id"], r["row"], "val", r["text"]) for r in arows if r["split"] == "val"]
    real = {r["id"]: sf.read(f"{src}/{r['file']}", dtype="float32")[0] for r in arows if r["split"] == "val"}
    SETS = {"val": VAL, "test": [tuple(t) for t in TEST]}
    allt = [t for s in SETS.values() for t in s]
    _, ph = prepare_all([t[3] for t in allt], cli, lex); PH = {(t[0], t[3]): p for t, p in zip(allt, ph)}
    log(f"validation {len(VAL)} · test {len(TEST)} · models {list(models)}")

    # ---- judges
    from transformers import pipeline as hfp, AutoFeatureExtractor, WavLMForXVector
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda")
    _wn = asr.tokenizer.normalize
    SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        s = re.sub(r"(\d)-(?=\d)", r"\1", s); t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wn(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w)]
    NAMES = {"thenuka", "kavi", "nimal", "priya", "galle", "kottu", "peradeniya", "paati", "madurai", "chennai", "jaffna", "wellawatte", "bambalapitiya",
             "kollupitiya", "thusitha", "dhananjaya", "chathurika", "thilini", "appam", "idiyappam", "pittu", "ayubowan", "kohomada", "arun", "appa",
             "amma", "nuwara", "eliya", "haputale", "silva", "fernando", "perera", "colombo", "kandy", "ella", "dosa", "bruno"}
    def errs(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]
        if not ref: return 0, 0
        o = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in o.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad, len(ref)
    utmos = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True).to("cuda").eval()
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    def mos(a):
        with torch.no_grad(): return float(utmos(torch.tensor(r16(a))[None].cuda(), 16000).item())
    fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xv = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").cuda().eval()
    def spk(a):
        with torch.no_grad():
            x = fe(r16(a), sampling_rate=16000, return_tensors="pt").to("cuda"); return torch.nn.functional.normalize(xv(**x).embeddings, dim=-1)[0].cpu().numpy()
    tcen = np.mean([spk(sf.read(f"{src}/{r['file']}", dtype="float32")[0]) for r in arows[::4]], 0); tcen /= np.linalg.norm(tcen)

    # ---- run everything
    R = {}; AUD = {}
    who = list(models) + ["tara"]
    for sname, items in SETS.items():
        for tid, row, kind, text in items:
            for tag in who:
                if tag == "tara" and sname != "val": continue
                a = real[tid] if tag == "tara" else say(tag, PH[(tid, text)], row)
                AUD[(sname, tid, tag)] = a
                h = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip(); b, n = errs(text, h)
                try: m = MK.measure(a, text)
                except Exception as e: m = None
                R[(sname, tid, tag)] = dict(set=sname, id=tid, row=row, kind=kind, who=tag, text=text, heard=h, bad=b, n=n, mos=mos(a),
                                            spk=float(spk(a) @ tcen), wps=len(re.findall(r"[A-Za-z0-9']+", text)) / max(len(a) / 24000, 0.1), m=m)
        log(f"{sname} done")
    # "!" judged against the same model's plain lines in the same row (as in the audit)
    for tag in who:
        for sname in SETS:
            ref = {}
            for row in ROWS:
                xs = [x["m"] for x in R.values() if x["who"] == tag and x["set"] == sname and x["row"] == row and x["m"] and "!" not in x["text"]]
                ref[row] = (np.median([m["body"] for m in xs]) if xs else 0, np.median([m["rng"] for m in xs]) if xs else 0)
            for x in R.values():
                if x["who"] != tag or x["set"] != sname or not x["m"]: continue
                x["m"]["marks"] = [(k, i, round(max(x["m"]["rng"] - ref[x["row"]][1], x["m"]["body"] - ref[x["row"]][0]), 2), None) if k == "ex" else (k, i, v, o)
                                   for k, i, v, o in x["m"]["marks"]]
                x["m"]["marks"] = [(k, i, v, (v >= 1.0) if k == "ex" and v is not None else o) for k, i, v, o in x["m"]["marks"]]
    def summ(sel):
        n = sum(x["n"] for x in sel); b = sum(x["bad"] for x in sel)
        return 100 * b / max(n, 1), np.mean([x["mos"] for x in sel]), np.mean([x["spk"] for x in sel])
    def marks_rate(sel):
        ok = tot = 0
        for x in sel:
            for k, i, v, o in (x["m"]["marks"] if x["m"] else []):
                if k in KINDS and o is not None: tot += 1; ok += bool(o)
        return f"{ok}/{tot}" + (f" ({100*ok/tot:.0f}%)" if tot else "")
    def mood_acc(sel):
        from sklearn.linear_model import LogisticRegression; from sklearn.model_selection import cross_val_score
        xs = [x for x in sel if x["m"]]
        if len(xs) < 20: return "–"
        X = np.array([[x["m"]["body"], x["m"]["rng"], x["wps"]] for x in xs]); Y = np.array([ROWS.index(x["row"]) for x in xs])
        return f"{100*cross_val_score(LogisticRegression(max_iter=1000), X, Y, cv=5).mean():.0f}%"
    for sname in ("val", "test"):
        report += [f"## {'Validation (choosing)' if sname == 'val' else 'Test (reporting only)'}", "",
                   "| | word error | naturalness | sounds like tara | marks shown | mood from pitch+pace |", "|---|---|---|---|---|---|"]
        for tag in who:
            sel = [x for x in R.values() if x["set"] == sname and x["who"] == tag]
            if not sel: continue
            w_, m_, s_ = summ(sel)
            mood_sel = [x for x in sel if x["kind"] == "matched"] if sname == "test" else sel
            report.append(f"| {tag} | {w_:.1f}% | {m_:.2f} | {s_:.3f} | {marks_rate(sel)} | {mood_acc(mood_sel)} |")
        report.append("")
    # marks per mark × mood on the test set
    for tag in [t for t in who if t != "tara"]:
        report += [f"### Test, {tag}: shows the mark (same thresholds as the actor audit)", "", "| mark | normal | bright | low | tense |", "|---|---|---|---|---|"]
        for k in KINDS:
            cells = []
            for row in ROWS:
                v = [o for x in R.values() if x["set"] == "test" and x["who"] == tag and x["row"] == row and x["m"] for kk, i, vv, o in x["m"]["marks"] if kk == k and o is not None]
                cells.append(f"{sum(v)}/{len(v)}" if v else "–")
            report.append(f"| {KN[k]} | " + " | ".join(cells) + " |")
        report.append("")
    # marks v2: marked minus plain (same sentence, same row)
    def first(m, k):
        for kk, i, v, o in (m["marks"] if m else []):
            if kk == k: return v
    report += ["### Marks v2: marked minus plain, same sentence and mood (median over 5 sentences × 4 moods)", "",
               "| mark | measure | " + " | ".join(t for t in who if t != "tara") + " |", "|---|---|" + "---|" * len([t for t in who if t != "tara"])]
    pairs = {}
    for tid, row, kind, text in TEST:
        if kind.startswith("marks2"): pairs.setdefault((tid[:-1] if tid[-1] in "pm" else tid, row, kind.split(":")[1]), {})["p" if "plain" in kind else "m"] = (tid, text)
    def pairdiff(tag, mark):
        out = []
        for (base, row, mk_), pm in pairs.items():
            if mk_ != mark or len(pm) != 2: continue
            xm, xp = R.get(("test", pm["m"][0], tag)), R.get(("test", pm["p"][0], tag))
            if not xm or not xp or not xm["m"] or not xp["m"]: continue
            if mark in ("?", "?!"):
                a_, b_ = xm["m"]["marks"], xp["m"]["marks"]
                va = [v for k, i, v, o in a_ if k in ("q", "qx") and v is not None]; vb = [v for k, i, v, o in b_ if k in ("q", "qx") and v is not None]
                if va and vb: out.append(va[-1] - vb[-1])
            elif mark == "!": out.append(max(xm["m"]["rng"] - xp["m"]["rng"], xm["m"]["body"] - xp["m"]["body"]))
            elif mark in ("…", "—"):
                k = "dots" if mark == "…" else "dash"; v = first(xm["m"], k)
                if v is not None: out.append(v)
            elif mark == "CAPS":
                v = first(xm["m"], "caps")
                if v is not None: out.append(v)
        return (f"{np.median(out):+.2f} (n {len(out)})" if out else "–")
    meas = {"?": "end rise vs plain (st)", "?!": "end rise vs plain ? (st)", "!": "livelier vs plain (st)", "…": "pause or drawn-out (s / ×)", "—": "pause (s)", "CAPS": "stressed word vs others (st)"}
    for mark in ["?", "?!", "!", "…", "—", "CAPS"]:
        report.append(f"| {mark} | {meas[mark]} | " + " | ".join(pairdiff(t, mark) for t in who if t != "tara") + " |")
    report += ["", "### Moods on the matched lines (30 sentences × 4 moods): median pitch level / range (st)", "",
               "| model | normal | bright | low | tense |", "|---|---|---|---|---|"]
    for tag in [t for t in who if t != "tara"]:
        cells = []
        for row in ROWS:
            xs = [x["m"] for x in R.values() if x["set"] == "test" and x["who"] == tag and x["kind"] == "matched" and x["row"] == row and x["m"]]
            cells.append(f"{np.median([m['body'] for m in xs]):.1f} / {np.median([m['rng'] for m in xs]):.1f}" if xs else "–")
        report.append(f"| {tag} | " + " | ".join(cells) + " |")
    with open(f"{W}/g2_results.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["set", "id", "row", "kind", "who", "bad", "n", "mos", "spk", "marks", "text", "heard"])
        for x in R.values(): w.writerow([x["set"], x["id"], x["row"], x["kind"], x["who"], x["bad"], x["n"], round(x["mos"], 2), round(x["spk"], 3),
                                         ";".join(f"{k}:{v}:{o}" for k, i, v, o in (x["m"]["marks"] if x["m"] else [])), x["text"], x["heard"]])
    errs_ = [x for x in R.values() if x["set"] == "test" and x["who"] in ("A", "B") and x["bad"]]
    report += ["", "### Test lines with word errors (A and B)", ""] + [f"- {x['who']} {x['id']}: “{x['text']}” → “{x['heard']}”" for x in errs_[:60]]

    # ---- listening: X/Y = A/B in random order per item
    if "A" in models and "B" in models:
        random.seed(12); items = []
        m2 = [(t, mk_) for t in TEST if t[2].startswith("marks2:") for mk_ in [t[2].split(":")[1]]]
        for i, mark in enumerate(["?", "?!", "!", "…", "—", "CAPS"]):
            c = [t for t, mk_ in m2 if mk_ == mark and t[1] == ROWS[i % 4]] or [t for t, mk_ in m2 if mk_ == mark]
            items.append((random.choice(c), {"?": "question", "?!": "surprise-qx", "!": "exclaim", "…": "dots", "—": "dash", "CAPS": "CAPS"}[mark]))
        mt = [t for t in TEST if t[2] == "matched"]; base = random.choice(sorted({t[0][:-1] for t in mt}))
        items += [(t, "mood") for t in mt if t[0][:-1] == base]
        key = ["# Key: which of X / Y is which (read AFTER listening)", "", "| clip | text | X | Y |", "|---|---|---|---|"]
        for n, (t, lab) in enumerate(items, 1):
            order = random.sample(["A", "B"], 2)
            for xy, tag in zip("XY", order):
                fn = f"{n:02d}_{lab}_{t[1]}_{xy}"
                sf.write(f"{TMP}/c.wav", AUD[("test", t[0], tag)], 24000); sh(f"ffmpeg -loglevel error -y -i {TMP}/c.wav -b:a 64k {W}/listen/{fn}.mp3")
            key.append(f"| {n:02d}_{lab}_{t[1]} | {t[3]} | {order[0]} | {order[1]} |")
        open(f"{W}/listen_key_AB.md", "w").write("\n".join(key) + "\n\nA = with adversarial · B = without\n")
        lines = ["# Listening: A vs B (blind)", "", "Each item has X and Y: the same line by the two teachers. Which sounds better (clearer, more natural, mark and mood right)?", "",
                 "| clip | text | better: X / Y / same |", "|---|---|---|"] + [f"| {n:02d}_{lab}_{t[1]} | {t[3]} | ☐ X ☐ Y ☐ same |" for n, (t, lab) in enumerate(items, 1)]
        open(f"{W}/listen_sheet_AB.md", "w").write("\n".join(lines) + "\n")
    report += ["", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

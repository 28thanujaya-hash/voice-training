# Run 5 · measure: every Maya clip we have (main takes, added lines, both retake rounds) measured with the new mood measures
# from GPT's acoustic review (17 Nov). CPU only, no recording, no GPU hours.
# Per clip: syllables/s (speech rate + articulation rate), pauses (count, total, share, where the first one falls),
# pitch (median, spread, 90-10 range, phrase slope, final slope, final drop), loudness (LUFS, spread, final drop),
# voice quality (CPP, HNR, H1-H2, tilt). Then: per-mood profile, how well each measure tells moods apart (AUC),
# old measures vs new measures as a mood classifier (cross-validated by sentence), the GPT mood-bundle checks per sentence
# group, and a provisional "fits its mood" score for every clip (used later to re-sort and select).
import csv, glob, hashlib, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from lines5 import build
T0 = time.time(); LOG = []; W = "/kaggle/working"
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 5 · measure: all clips against the new mood measures (GPT review, 17 Nov)", ""]
try:
    sh("pip install -q praat-parselmouth pyloudnorm soundfile librosa cmudict num2words scikit-learn")
    import numpy as np, soundfile as sf, librosa, pyloudnorm, parselmouth, cmudict
    from num2words import num2words
    LINES = {l[0]: l for l in build()}
    CMU = cmudict.dict()
    def syllables(text):
        t = re.sub(r"(\d[\d,]*)", lambda m: " " + num2words(int(m.group(1).replace(",", ""))) + " ", text)
        n = 0
        for w in re.findall(r"[a-zA-Z']+", t.lower()):
            if w in CMU: n += sum(ch[-1].isdigit() for ch in CMU[w][0])
            else: n += max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))
        return n
    # ---- every clip once
    clips = []; seen = set()
    for f in glob.glob("/kaggle/input/**/takes.csv", recursive=True):
        base = os.path.dirname(f)
        for r in csv.DictReader(open(f)):
            clips.append(dict(id=r["id"], path=f"{base}/{r['file']}", src="take", old_pitch=r["pitch"], old_range=r["range"], old_move=r["move"],
                              old_pace=r["pace"], old_lufs=r["lufs"], old_tilt=r["tilt"]))
    for f in sorted(glob.glob("/kaggle/input/**/retakes/*.wav", recursive=True)):
        clips.append(dict(id=os.path.basename(f).split("_x")[0], path=f, src="retake"))
    out = []
    for c in clips:
        if c["id"] not in LINES or not os.path.exists(c["path"]): continue
        h = hashlib.md5(open(c["path"], "rb").read()).hexdigest()
        if h in seen: continue
        seen.add(h); out.append(c)
    clips = out
    log(f"{len(clips)} distinct clips for {len({c['id'] for c in clips})} lines")
    meter = pyloudnorm.Meter(24000)
    st = lambda f: 12 * np.log2(f / 100.0)
    def cpp_h1h2(y, sr, t_f0):
        # CPP (cepstral peak prominence) and H1-H2 on voiced 40 ms frames; uncorrected H1-H2
        N = int(0.04 * sr); win = np.hanning(N); cpps, hh = [], []
        q = np.arange(N) / sr
        for t, f0 in t_f0:
            a = int(t * sr - N / 2)
            if a < 0 or a + N > len(y): continue
            fr = y[a:a + N] * win
            if np.max(np.abs(fr)) < 1e-4: continue
            spec = np.abs(np.fft.rfft(fr, 4 * N)); ldb = 20 * np.log10(spec + 1e-9)
            cep = np.fft.irfft(ldb); cep = cep[:N]; cdb = 20 * np.log10(np.abs(cep) + 1e-9)
            lo, hi = int(sr / 600), int(sr / 75); qs = np.arange(lo, hi)
            pk = qs[np.argmax(cdb[lo:hi])]
            k = np.arange(int(0.001 * sr), N // 2); p = np.polyfit(q[k], cdb[k], 1)
            cpps.append(cdb[pk] - np.polyval(p, q[pk]))
            fbin = sr / (4 * N)
            def amp(f):
                i0, i1 = int(f * 0.9 / fbin), int(f * 1.1 / fbin) + 1
                return np.max(ldb[i0:i1]) if i1 < len(ldb) else np.nan
            hh.append(amp(f0) - amp(2 * f0))
        return (float(np.nanmedian(cpps)) if cpps else np.nan, float(np.nanmedian(hh)) if hh else np.nan)
    def measure(c):
        y, sr = sf.read(c["path"], dtype="float32")
        if y.ndim > 1: y = y.mean(1)
        text = LINES[c["id"]][3]; syl = syllables(text)
        iv = librosa.effects.split(y, top_db=30, frame_length=1024, hop_length=240)
        s0, s1 = iv[0][0] / sr, iv[-1][1] / sr; span = max(s1 - s0, 0.1)
        gaps = [(iv[i][0] - iv[i - 1][1]) / sr for i in range(1, len(iv))]
        starts = [iv[i - 1][1] / sr for i in range(1, len(iv))]
        P = [(g, s) for g, s in zip(gaps, starts) if g >= 0.15]
        ptot = sum(g for g, _ in P)
        snd = parselmouth.Sound(y.astype(np.float64), sr)
        pt = snd.to_pitch_ac(time_step=0.01, pitch_floor=100, pitch_ceiling=600)
        f0 = pt.selected_array["frequency"]; tt = pt.xs()
        v = (f0 > 0) & (tt >= s0) & (tt <= s1)
        d = dict(id=c["id"], src=c["src"], file=c["path"].replace("/kaggle/input/", ""), syl=syl, dur=round(span, 3),
                 syl_s=syl / span, artic=syl / max(span - ptot, 0.1), pauses=len(P), pause_s=ptot, pause_share=ptot / span,
                 first_pause=((P[0][1] - s0) / span) if P else np.nan)
        if v.sum() >= 10:
            s = st(f0[v]); t = tt[v]; n = len(s); k = max(3, n // 5)
            d.update(f0_med=np.median(s), f0_sd=np.std(s), f0_rng=np.percentile(s, 90) - np.percentile(s, 10),
                     slope=np.polyfit(t, s, 1)[0], final_drop=np.median(s[-k:]) - np.median(s[:-k]))
            fin = t >= t[-1] - 0.4
            d["final_slope"] = np.polyfit(t[fin], s[fin], 1)[0] if fin.sum() >= 5 else np.nan
            d["cpp"], d["h1h2"] = cpp_h1h2(y, sr, list(zip(t, f0[v])))
        it = snd.to_intensity(minimum_pitch=100); idb = it.values[0]; ti = it.xs(); m = (ti >= s0) & (ti <= s1) & (idb > idb.max() - 30)
        if m.sum() >= 10:
            x = idb[m]; k = max(3, len(x) // 5)
            d.update(int_sd=np.std(x), int_drop=np.mean(x[-k:]) - np.mean(x[:-k]))
        hn = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=100).values[0]; hn = hn[hn > -100]
        d["hnr"] = float(np.median(hn)) if len(hn) else np.nan
        try: d["lufs"] = meter.integrated_loudness(np.pad(y, (0, max(0, int(0.5 * sr) - len(y)))))
        except Exception: d["lufs"] = np.nan
        S = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / sr)
        d["tilt"] = 10 * np.log10(S[fr > 1000].sum() / max(S[(fr > 60) & (fr <= 1000)].sum(), 1e-12))
        for k in ("old_pitch", "old_range", "old_move", "old_pace", "old_lufs", "old_tilt"): d[k] = float(c[k]) if k in c else np.nan
        return d
    R = []
    for i, c in enumerate(clips):
        try: d = measure(c)
        except Exception as e: log(f"skip {c['path']}: {e}"); continue
        l = LINES[c["id"]]; d.update(row=l[1], group=l[2] or "", split=l[4], text=l[3]); R.append(d)
        if i % 300 == 0: log(f"measured {i}/{len(clips)}")
    log(f"measured {len(R)} clips")
    NEW = ["syl_s", "artic", "pauses", "pause_share", "f0_med", "f0_sd", "f0_rng", "slope", "final_slope", "final_drop",
           "lufs", "int_sd", "int_drop", "cpp", "hnr", "h1h2", "tilt"]
    OLD = ["old_pitch", "old_range", "old_move", "old_pace", "old_lufs", "old_tilt"]
    NAME = dict(syl_s="syllables/s", artic="articulation rate (syl/s without pauses)", pauses="pauses ≥150 ms", pause_share="pause share of time",
                f0_med="pitch (st re 100 Hz)", f0_sd="pitch spread (SD st)", f0_rng="pitch range 90-10 (st)", slope="phrase slope (st/s)",
                final_slope="final 400 ms slope (st/s)", final_drop="end pitch vs body (st)", lufs="loudness (LUFS)", int_sd="loudness spread (dB SD)",
                int_drop="end loudness vs body (dB)", cpp="CPP (higher = clearer, firmer voice)", hnr="HNR (dB, lower = breathier/rougher)",
                h1h2="H1-H2 (dB, higher = breathier)", tilt="tilt (>1 kHz vs <1 kHz, dB)")
    A = {k: np.array([r.get(k, np.nan) for r in R], float) for k in NEW + OLD + ["first_pause"]}
    lab = np.array([r["row"] for r in R]); ids = np.array([r["id"] for r in R])
    # ---- 1. per-mood profile
    report += [f"Clips measured: {len(R)} (" + ", ".join(f"{m} {int((lab == m).sum())}" for m in ROWS) + f"), lines: {len(set(ids))}", "",
               "## 1. Per-mood profile (median, with middle half in brackets)", "", "| measure | " + " | ".join(ROWS) + " |", "|---|" + "---|" * 4]
    for k in NEW + ["first_pause"]:
        cells = []
        for m in ROWS:
            x = A[k][(lab == m) & ~np.isnan(A[k])]
            cells.append(f"{np.median(x):.2f} ({np.percentile(x, 25):.2f}…{np.percentile(x, 75):.2f})" if len(x) else "–")
        report.append(f"| {NAME.get(k, 'first pause at (share of line)')} | " + " | ".join(cells) + " |")
    # ---- 2. which measures tell which moods apart (AUC: 0.5 = no help, 1.0 = perfect; shown as distance from 0.5 ×2)
    from sklearn.metrics import roc_auc_score
    PAIRS = [("low", "normal"), ("normal", "tense"), ("normal", "bright"), ("tense", "bright"), ("low", "tense")]
    report += ["", "## 2. How well each measure alone separates two moods", "AUC 0.50 = no help, 1.00 = perfect. Arrow = which way the second mood goes.", "",
               "| measure | " + " | ".join(f"{a}→{b}" for a, b in PAIRS) + " |", "|---|" + "---|" * len(PAIRS)]
    for k in NEW + OLD:
        cells = []
        for a, b in PAIRS:
            m = np.isin(lab, [a, b]) & ~np.isnan(A[k])
            try: au = roc_auc_score(lab[m] == b, A[k][m])
            except Exception: cells.append("–"); continue
            cells.append(f"{max(au, 1 - au):.2f} {'↑' if au >= .5 else '↓'}")
        report.append(f"| {NAME.get(k, k)} | " + " | ".join(cells) + " |")
    # ---- 3. old vs new measures as a mood classifier, cross-validated by sentence (a line never trains and tests at once)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold, cross_val_predict
    gkey = np.array([r["group"] or r["id"] for r in R])
    def clf(keys):
        X = np.column_stack([A[k] for k in keys]); X[np.isinf(X)] = np.nan
        p = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=2000, C=0.5))
        pr = cross_val_predict(p, X, lab, groups=gkey, cv=GroupKFold(5), method="predict_proba")
        cls = sorted(set(lab)); pred = np.array(cls)[pr.argmax(1)]
        return pr, cls, pred
    res = {}
    for nm, keys in (("old 6 measures", [k for k in OLD]), ("new measures", NEW), ("new without pitch/loudness level", [k for k in NEW if k not in ("f0_med", "lufs")])):
        okk = [k for k in keys if np.isfinite(A[k]).mean() > 0.5]
        pr, cls, pred = clf(okk); res[nm] = (pr, cls)
        acc = (pred == lab).mean()
        report += ["", f"## 3. Mood classifier — {nm}: {acc*100:.0f}% of clips land on their intended mood (chance 25%)", "",
                   "| intended ↓ / measured as → | " + " | ".join(ROWS) + " |", "|---|" + "---|" * 4]
        for m in ROWS:
            x = pred[lab == m]; report.append(f"| {m} | " + " | ".join(f"{(x == n).mean()*100:.0f}%" for n in ROWS) + " |")
    # ---- 4. GPT bundle checks inside each 4-mood sentence group (median of that mood's clips in the group)
    rules = [("low slower than normal (syl/s)", "low", "normal", "syl_s", -1), ("low more pause time than normal", "low", "normal", "pause_share", 1),
             ("low lower pitch than normal", "low", "normal", "f0_med", -1), ("low quieter than normal", "low", "normal", "lufs", -1),
             ("low end weakens more than normal (loudness)", "low", "normal", "int_drop", -1), ("low breathier than normal (H1-H2)", "low", "normal", "h1h2", 1),
             ("low less clear voice than normal (CPP)", "low", "normal", "cpp", -1),
             ("bright higher than normal", "bright", "normal", "f0_med", 1), ("bright more pitch movement than normal (SD)", "bright", "normal", "f0_sd", 1),
             ("bright more pitch movement than tense (SD)", "bright", "tense", "f0_sd", 1), ("bright higher than tense", "bright", "tense", "f0_med", 1),
             ("tense firmer voice than normal (CPP)", "tense", "normal", "cpp", 1), ("tense less breathy than low (H1-H2)", "tense", "low", "h1h2", -1),
             ("tense falls more at the end than bright", "tense", "bright", "final_slope", -1), ("tense more loudness contrast than normal", "tense", "normal", "int_sd", 1),
             ("tense louder than normal", "tense", "normal", "lufs", 1), ("normal faster than low, slower than bright", None, None, None, 0)]
    G = {}
    for r in R:
        if r["group"]: G.setdefault(r["group"], {}).setdefault(r["row"], []).append(r)
    G = {g: v for g, v in G.items() if all(m in v for m in ROWS)}
    gm = lambda g, m, k: np.nanmedian([x.get(k, np.nan) for x in G[g][m]])
    report += ["", f"## 4. GPT mood bundles, checked inside each sentence group ({len(G)} groups with all four moods)", "", "| check | groups passing |", "|---|---|"]
    for name, a, b, k, sgn in rules:
        if k is None:
            n = sum(gm(g, "low", "syl_s") < gm(g, "normal", "syl_s") < gm(g, "bright", "syl_s") for g in G)
        else:
            n = sum(((gm(g, a, k) - gm(g, b, k)) * sgn) > 0 for g in G)
        report.append(f"| {name} | {n}/{len(G)} |")
    # ---- 5. provisional fit score per clip = probability (new-measure classifier, sentence held out) of its intended mood
    pr, cls = res["new measures"]
    for i, r in enumerate(R): r["fit"] = float(pr[i][cls.index(r["row"])]); r["measured_as"] = cls[int(pr[i].argmax())]
    best = {}
    for r in R:
        if r["id"] not in best or r["fit"] > best[r["id"]]["fit"]: best[r["id"]] = r
    report += ["", "## 5. Best clip per line by the new measures (provisional, before the 12-sentence diagnostic sets the targets)", "",
               "| mood | lines | best clip measured as its own mood | median fit |", "|---|---|---|---|"]
    for m in ROWS:
        b = [r for r in best.values() if r["row"] == m]
        report.append(f"| {m} | {len(b)} | {sum(r['measured_as'] == m for r in b)} | {np.median([r['fit'] for r in b]):.2f} |")
    cols = ["id", "row", "group", "split", "src", "file", "text", "fit", "measured_as", "syl", "dur"] + NEW + ["first_pause"] + OLD
    with open(f"{W}/measures.csv", "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
        for r in sorted(R, key=lambda r: (r["id"], -r["fit"])):
            w.writerow({k: (round(v, 3) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})
    log("done")
except Exception:
    report += ["", "## ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report))

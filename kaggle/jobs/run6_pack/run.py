# Run 6 · pack: measure the diagnostic clips (Orpheus run6_orph, IndexTTS run6_idx) with the new measures, choose one take per
# source × sentence × mood by a within-sentence mood-bundle score, compare the two sources, and build blind test 5
# (96 clips + 12 hidden repeats, two sessions of 54, confidence 1-5, key separate). No processing of the audio (mentor 13:03).
import csv, glob, os, random, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from diag import SENTS, MOODS
T0 = time.time(); LOG = []; W = "/kaggle/working"
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 6 · diagnostic pack: Orpheus (new lead-ins) vs IndexTTS-2.5 on 12 sentences × 4 moods", ""]
try:
    sh("pip install -q praat-parselmouth pyloudnorm soundfile librosa cmudict num2words")
    import numpy as np, newm
    TEXT = dict(SENTS); R = []
    for src in ("orph", "idx"):
        for f in glob.glob(f"/kaggle/input/**/se-run6-{src}/takes.csv", recursive=True) + glob.glob(f"/kaggle/input/se-run6-{src}/takes.csv"):
            base = os.path.dirname(f)
            for r in csv.DictReader(open(f)):
                if r.get("words_ok", "1") != "1": continue
                p = f"{base}/{r['file']}"
                if not os.path.exists(p) or any(x["path"] == p for x in R): continue
                try: d = newm.measure(dict(path=p, text=r["text"]))
                except Exception as e: log(f"skip {p}: {e}"); continue
                d.update(src=src, sent=r["sent"], row=r["row"], path=p, text=r["text"]); R.append(d)
    log(f"measured {len(R)} clips: " + ", ".join(f"{s} {sum(r['src'] == s for r in R)}" for s in ("orph", "idx")))
    K = ["syl_s", "pause_share", "f0_med", "f0_sd", "final_slope", "lufs", "int_sd", "int_drop", "cpp", "hnr", "h1h2"]
    NAME = dict(syl_s="syllables/s", pause_share="pause share", f0_med="pitch (st)", f0_sd="pitch movement (SD)", final_slope="end fall (st/s)",
                lufs="loudness (LUFS)", int_sd="loudness contrast (dB)", int_drop="end loudness drop (dB)", cpp="CPP (clear/firm)", hnr="HNR",
                h1h2="H1-H2 (breathy)")
    g = lambda r, k: float(r.get(k, np.nan))
    # ---- within-sentence z (per source, across all four moods' takes), then a bundle score per mood (GPT's descriptions)
    for src in ("orph", "idx"):
        for sid, _ in SENTS:
            rs = [r for r in R if r["src"] == src and r["sent"] == sid]
            if len(rs) < 2: continue
            for k in K:
                v = np.array([g(r, k) for r in rs]); mu, sd = np.nanmean(v), np.nanstd(v) + 1e-6
                for r, x in zip(rs, v): r["z_" + k] = 0.0 if np.isnan(x) else (x - mu) / sd
    def score(r):
        z = lambda k: r.get("z_" + k, 0.0)
        m = r["row"]
        if m == "low": return -z("syl_s") + z("pause_share") - z("f0_med") - z("lufs") + 0.5 * z("h1h2") - 0.5 * z("f0_sd") - 0.5 * z("int_drop")
        if m == "bright": return z("f0_med") + z("f0_sd") + 0.5 * z("lufs")
        if m == "tense": return z("lufs") + z("int_sd") - 0.5 * z("h1h2") - 0.5 * z("final_slope") - 0.3 * z("f0_med")
        return -(abs(z("f0_med")) + abs(z("lufs")) + abs(z("syl_s")) + 0.5 * abs(z("f0_sd")))
    for r in R: r["score"] = score(r)
    pick = {}
    for r in R:
        key = (r["src"], r["sent"], r["row"])
        if key not in pick or r["score"] > pick[key]["score"]: pick[key] = r
    report += [f"Clips measured: {len(R)} · chosen (one per source × sentence × mood): {len(pick)} of 96", ""]
    # ---- 1. profile per source × mood (chosen takes)
    for src, nm in (("orph", "Orpheus tara, new lead-ins"), ("idx", "IndexTTS-2.5, Maya cloned, emotion vector")):
        report += [f"## 1. {nm}: chosen takes, median", "", "| measure | " + " | ".join(MOODS) + " |", "|---|" + "---|" * 4]
        for k in K:
            cells = []
            for m in MOODS:
                x = [g(r, k) for r in pick.values() if r["src"] == src and r["row"] == m]
                cells.append(f"{np.nanmedian(x):.2f}" if x else "–")
            report.append(f"| {NAME[k]} | " + " | ".join(cells) + " |")
        report.append("")
    # ---- 2. GPT bundle checks per sentence (chosen takes)
    rules = [("low slower than normal", "low", "normal", "syl_s", -1), ("low more pause than normal", "low", "normal", "pause_share", 1),
             ("low lower than normal", "low", "normal", "f0_med", -1), ("low quieter than normal", "low", "normal", "lufs", -1),
             ("low breathier than normal", "low", "normal", "h1h2", 1), ("bright higher than normal", "bright", "normal", "f0_med", 1),
             ("bright more pitch movement than normal", "bright", "normal", "f0_sd", 1), ("bright higher than tense", "bright", "tense", "f0_med", 1),
             ("tense louder than normal", "tense", "normal", "lufs", 1), ("tense more loudness contrast than normal", "tense", "normal", "int_sd", 1),
             ("tense less breathy than normal", "tense", "normal", "h1h2", -1), ("tense falls more at the end than normal", "tense", "normal", "final_slope", -1),
             ("normal between low and bright in pitch", None, None, "f0_med", 0), ("normal between low and tense in loudness", None, None, "lufs", 0)]
    report += ["## 2. Mood bundle checks, sentence by sentence (12 sentences)", "", "| check | Orpheus | IndexTTS |", "|---|---|---|"]
    for name, a, b, k, sgn in rules:
        cells = []
        for src in ("orph", "idx"):
            n = t = 0
            for sid, _ in SENTS:
                P = {m: pick.get((src, sid, m)) for m in MOODS}
                if sgn == 0:
                    hi = "bright" if k == "f0_med" else "tense"
                    if not (P["low"] and P["normal"] and P[hi]): continue
                    t += 1; n += g(P["low"], k) < g(P["normal"], k) < g(P[hi], k)
                else:
                    if not (P[a] and P[b]): continue
                    t += 1; n += (g(P[a], k) - g(P[b], k)) * sgn > 0
            cells.append(f"{n}/{t}")
        report.append(f"| {name} | " + " | ".join(cells) + " |")
    # ---- 3. blind test 5
    clips = list(pick.values()); random.seed(17); random.shuffle(clips)
    A, B = clips[: len(clips) // 2], clips[len(clips) // 2:]
    A2 = A + random.sample(B, 6); B2 = B + random.sample(A, 6); random.shuffle(A2); random.shuffle(B2)
    os.makedirs(f"{W}/blind5", exist_ok=True); key = []; n = 0
    for sess, L in (("A", A2), ("B", B2)):
        for r in L:
            n += 1; name = f"blind5_{n:03d}.mp3"
            sh(f"ffmpeg -loglevel error -y -i '{r['path']}' -codec:a libmp3lame -b:a 96k {W}/blind5/{name}")
            first = next((k for k in key if k[2] == r["path"]), None)
            key.append([n, sess, r["path"], r["src"], r["sent"], r["row"], r["text"], first[0] if first else ""])
    with open(f"{W}/blind5_key.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["clip", "session", "path", "source", "sentence", "mood", "text", "repeat_of"])
        w.writerows([k[:2] + [os.path.basename(k[2])] + k[3:] for k in key])
    sheet = ["# Blind test 5 — answer sheet", "", "Listen to one clip at a time. For each: the mood you hear (N normal · B bright · L low · T tense) and how sure you are (1 = guess … 5 = certain).",
             "Session A = clips 1–54, session B = clips 55–108. Some clips appear twice.", ""]
    for sess, a0, a1 in (("A", 1, 54), ("B", 55, len(key))):
        sheet += [f"## Session {sess}", "", "| clip | text | mood (N/B/L/T) | sure (1–5) |", "|---|---|---|---|"]
        sheet += [f"| {k[0]} | {k[6]} | | |" for k in key if k[1] == sess]
        sheet.append("")
    open(f"{W}/blind5_sheet.md", "w").write("\n".join(sheet))
    with open(f"{W}/measures6.csv", "w", newline="") as f:
        cols = ["src", "sent", "row", "chosen", "score", "path", "text", "syl", "dur", "syl_s", "artic", "pauses", "pause_share", "first_pause", "f0_med", "f0_sd",
                "f0_rng", "slope", "final_slope", "final_drop", "lufs", "int_sd", "int_drop", "cpp", "hnr", "h1h2", "tilt"]
        w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
        for r in R:
            r["chosen"] = int(pick.get((r["src"], r["sent"], r["row"])) is r)
            w.writerow({k: (round(float(v), 3) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})
    report += ["", f"Blind test 5: {len(key)} clips (96 + 12 hidden repeats), sessions A {len(A2)} / B {len(B2)}; sheet blind5_sheet.md, key blind5_key.csv", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

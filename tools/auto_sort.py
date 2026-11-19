"""Auto-sort full-run takes by the measured numbers (no listening).

Usage: python3 tools/auto_sort.py <out.csv> <run> [<run> ...]

For every right-word take:
  1. Quality: drop hiss > 0.3 s (0.15 caught normal s-sounds), a monotone hold > 0.8 s, or a mid-line gap
     > 1.0 s (1.5 s on lines with "…" or "—").
  2. Mood strength vs F's normal voice (the d_* columns):
       bright = loud + speed/10;              drop when speed < −25 %
       tense  = loud + 0.5·pitch;             drop when loud < +1 dB and pitch < +1.5 st
       low    = −loud − speed/10 + 0.3·breath; drop when pitch ≥ +2.5 st (not on plain "?" questions)
     every mood: drop when speed < −50 % (sounded odd)
  3. Per line, keep the 2 strongest survivors. If none survive, keep the best take
     and flag the line "check".
Decisions: keep / spare (passed, but not in the top 2) / drop-quality / drop-flat.
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = 2
f = lambda r, k: float(r[k] or 0)


def strength(r, mood):
    if mood == "bright": return f(r, "d_lufs") + f(r, "speed_pct") / 10
    if mood == "tense": return f(r, "d_lufs") + 0.5 * f(r, "d_f0_med")
    return -f(r, "d_lufs") - f(r, "speed_pct") / 10 + 0.3 * f(r, "d_h1h2")


def flat(r, mood):
    # check1 (19 Nov, 36 clips by ear): >50% slower sounded odd 3 of 4; bright slower than -10% was never bright;
    # low with pitch >= +2.5 st (shocked "?!" lines) sounded normal/odd 3 of 3; faster/louder low was still low.
    if f(r, "speed_pct") < -50: return True
    # check2 (25 more clips): bright down to -25% was still bright; plain "?" low questions rise and still sounded low.
    if mood == "bright": return f(r, "speed_pct") < -25
    if mood == "tense": return f(r, "d_lufs") < 1 and f(r, "d_f0_med") < 1.5
    t = r["text"].rstrip()
    return f(r, "d_f0_med") >= 2.5 and not (t.endswith("?") and not t.endswith("?!"))


def quality(r):
    long_ok = 1.5 if ("…" in r["text"] or "—" in r["text"] or "..." in r["text"]) else 1.0
    bad = []
    if f(r, "hiss") > 0.3: bad.append("hiss")
    if f(r, "hold") > 0.8: bad.append("hold")
    if f(r, "gap") > long_ok: bad.append("gap")
    return bad


out, runs = sys.argv[1], sys.argv[2:]
rows_out = []
for run in runs:
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "results", run, "takes.csv")))
            if r["status"] in ("PASS", "fail")
            and os.path.exists(os.path.join(ROOT, "results", run, "takes", f"{r['id']}_{r['var']}_{r['take']}.mp3"))]
    ids = list(dict.fromkeys(r["id"] for r in rows))
    for lid in ids:
        rs = [r for r in rows if r["id"] == lid]
        for r in rs:
            r["run"], r["score"], r["q"] = run, strength(r, r["mood"]), quality(r)
            r["decision"] = "drop-quality" if r["q"] else ("drop-flat" if flat(r, r["mood"]) else "ok")
        ok = sorted([r for r in rs if r["decision"] == "ok"], key=lambda r: -r["score"])
        for i, r in enumerate(ok): r["decision"] = "keep" if i < KEEP else "spare"
        if not ok:
            best = max([r for r in rs if not r["q"]] or rs, key=lambda r: r["score"])
            best["decision"] = "keep-check"
        rows_out += rs

cols = ["run", "id", "mood", "var", "take", "decision", "score", "q", "speed_pct", "d_lufs", "d_f0_med", "d_f0_sd",
        "d_h1h2", "gap", "hold", "hiss", "text", "heard"]
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader()
    for r in rows_out: w.writerow({**r, "score": f"{r['score']:.2f}", "q": " ".join(r["q"])})
from collections import Counter
print(Counter(r["decision"] for r in rows_out), len(set(r["id"] for r in rows_out)), "lines")

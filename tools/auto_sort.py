"""Auto-sort full-run takes by the measured numbers (no listening).

Usage: python3 tools/auto_sort.py <out.csv> <run> [<run> ...]

For every right-word take:
  1. Quality: drop hiss > 0.3 s (0.15 caught normal s-sounds), a monotone hold > 0.8 s, or a mid-line gap
     > 1.0 s (1.5 s on lines with "…" or "—").
  2. Mood strength vs F's normal voice (the d_* columns):
       bright = loud;                         no mood cut; keep the 2 loudest per line (checks 1-4)
       tense  = loud + 0.5·pitch;             drop when loud < +1 dB and pitch < +1.5 st
       low    = −loud − speed/10 + 0.3·breath; drop when pitch ≥ +2.5 st (not on plain "?" questions)
       normal = closeness to F's normal voice; drop when |loud| > 3 dB or |pitch| > 2.5 st
     every mood: drop when speed < −50 % (sounded odd)
  3. Per line, keep the 2 strongest survivors. If none survive, keep the best take
     and flag the line "check".
Decisions: keep / spare (passed, but not in the top 2) / drop-quality / drop-flat.
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = 2
# Bright lines written as amused / ironic stories ("actually", "for once", a punchline) or split by "—":
# heard as F's normal dry humour (check 1-4: 9 of 11 normal marks on chuckle/laugh lines). User 19 Nov 07:27:
# move them to normal (mentor should know). Their takes are sorted with the normal rule (closest to her normal voice).
MOVE_TO_NORMAL = {"m3b55", "m3b73", "m3b64", "m3b72", "m3b53", "m3b18", "m3b67", "m3t09", "m3b20",
                  "m3xb24", "m3xb08", "m3xb12", "m3xb15"}
f = lambda r, k: float(r[k] or 0)


def strength(r, mood):
    # check4 (19 Nov): how the last word ends did NOT predict bright (ends-on-top 3/10 bright); loudness did best:
    # over 54 marked clips, takes >= +3 dB were bright 22/30 vs 32/54 overall. So bright keeps the 2 loudest per line.
    if mood == "bright": return f(r, "d_lufs")
    if mood == "tense": return f(r, "d_lufs") + 0.5 * f(r, "d_f0_med")
    if mood == "normal": return -(abs(f(r, "d_lufs")) / 3 + abs(f(r, "d_f0_med")) / 2.5 + abs(f(r, "speed_pct")) / 30)
    return -f(r, "d_lufs") - f(r, "speed_pct") / 10 + 0.3 * f(r, "d_h1h2")


def flat(r, mood):
    # check1 (19 Nov, 36 clips by ear): >50% slower sounded odd 3 of 4; bright slower than -10% was never bright;
    # low with pitch >= +2.5 st (shocked "?!" lines) sounded normal/odd 3 of 3; faster/louder low was still low.
    if f(r, "speed_pct") < -50 and mood != "bright": return True
    # check2 (25 more clips): bright down to -25% was still bright; plain "?" low questions rise and still sounded low.
    # check3 (19 Nov): 9 of 10 bright takes 25-55% slower were bright; no measure beats keeping all bright takes
    # (35 clips by ear), so bright is cut for quality only and sorted by ear.
    if mood == "bright": return False
    if mood == "tense": return f(r, "d_lufs") < 1 and f(r, "d_f0_med") < 1.5
    if mood == "normal": return abs(f(r, "d_lufs")) > 3 or abs(f(r, "d_f0_med")) > 2.5   # far from her normal voice (not yet checked by ear)
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
    for r in rows:
        if r["mood"] == "bright" and r["id"] in MOVE_TO_NORMAL: r["mood"] = "normal"
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

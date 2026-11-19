"""Original vs actor: for each book line, pick the actor take that sounds closest to the human reader, and build a
listening page with the two side by side.

Usage: python3 tools/book/pair_page.py <run> <human.csv> <human_audio.json> <out_dir>
  human.csv: code, chapter, start, end, text (results/book_anne/director/run18_human.csv)
The take shown is the one the director's own mood rules pick (tools/auto_sort.py scores), never the human recording.
Closeness to the human is only reported afterwards (pairs.md): the human's delivery vs her normal chatting voice, compared with the take's delivery vs F's normal voice:
  speed (%), loudness (dB), pitch (st), pitch movement (st), and how far the last word falls (st, tools/end_word.py).
"""
import base64, csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from end_word import end_features

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
run, hcsv, hjson, out = sys.argv[1:5]
ANNE_NORMAL = dict(rate=22.0, loud=0.35, pitch=0.85, move=1.08)   # Anne's chatting voice vs the reader's narration (ch02/09/37)
book = {}
for ch in ("ch02", "ch09", "ch37"):
    for x in csv.DictReader(open(os.path.join(ROOT, "results/book_anne", f"{ch}.csv"))): book[(ch, x["start"])] = x
H = {}
for r in csv.DictReader(open(hcsv)):
    x = book[(r["chapter"], r["start"])]
    H[r["code"]] = dict(text=r["text"], speed=float(x["rate_rel"]) - ANNE_NORMAL["rate"], loud=float(x["loud_rel"]) - ANNE_NORMAL["loud"],
                        pitch=float(x["pitch_rel"]) - ANNE_NORMAL["pitch"], move=float(x["move_rel"]) - ANNE_NORMAL["move"],
                        fall=float(x["end_fall"] or 0))
hpack = json.load(open(hjson))
takes = [t for t in csv.DictReader(open(os.path.join(ROOT, "results", run, "takes.csv"))) if t["status"] in ("PASS", "fail")]
tdir = os.path.join(ROOT, "results", run, "takes")
os.makedirs(os.path.join(out, "audio"), exist_ok=True)
pairs, pack, report = [], {}, []
for n, (code, h) in enumerate(H.items(), 1):
    best = []
    for t in [t for t in takes if t["id"] == code]:
        fn = os.path.join(tdir, f"{t['id']}_{t['var']}_{t['take']}.mp3")
        if not os.path.exists(fn): continue
        e = end_features(fn) or {}
        a = dict(speed=float(t["speed_pct"]), loud=float(t["d_lufs"]), pitch=float(t["d_f0_med"]), move=float(t["d_f0_sd"]), fall=e.get("end_fall", 0.0))
        d = abs(a["speed"] - h["speed"]) / 20 + abs(a["loud"] - h["loud"]) / 2 + abs(a["pitch"] - h["pitch"]) / 2 + abs(a["move"] - h["move"]) / 1.5 + abs(a["fall"] - h["fall"]) / 4
        own = (a["loud"] if t["mood"] == "bright" else a["loud"] + 0.5 * a["pitch"] if t["mood"] == "tense"
               else -a["loud"] - a["speed"] / 10 + 0.3 * float(t["d_h1h2"] or 0))   # tools/auto_sort.py scores: no human info
        best.append((d, t, a, fn, own))
    best.sort(key=lambda b: -b[4])   # the take the director's own rules pick (an EPUB has no human recording)
    if not best: continue
    d, t, a, fn, _ = best[0]
    pack[f"O{n}"] = hpack[code]; pack[f"A{n}"] = base64.b64encode(open(fn, "rb").read()).decode()
    pairs.append(dict(n=n, code=code, text=h["text"].strip("“”\""), actor=t["text"], var=t["var"]))
    report.append(f"| {n} | {h['text'][:45]} | {t['var']}: {t['text']} | human {h['speed']:+.0f}% {h['loud']:+.1f} dB {h['pitch']:+.1f} st, fall {h['fall']:+.1f} | actor {a['speed']:+.0f}% {a['loud']:+.1f} dB {a['pitch']:+.1f} st, fall {a['fall']:+.1f} | {d:.1f} |")
json.dump(pack, open(os.path.join(out, "audio", "pairs.json"), "w"))
json.dump(pairs, open(os.path.join(out, "pairs.json"), "w"), ensure_ascii=False)
open(os.path.join(ROOT, "results", run, "pairs.md"), "w").write(
    "| # | line | actor version picked | human (vs her chat) | actor (vs F normal) | distance |\n|---|---|---|---|---|---|\n" + "\n".join(report) + "\n")
html = open(os.path.join(os.path.dirname(__file__), "pair_page.html")).read()
open(os.path.join(out, "index.html"), "w").write(html)
print(len(pairs), "pairs")

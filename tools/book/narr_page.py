"""Narration: original paragraph vs the actor's paragraph, joined from pieces with the human's gaps.
Usage: python3 tools/book/narr_page.py <run> <narr_human.csv> <narr_human_audio.json> <out_dir>
A = the director's short units, B = one read per sentence. For each piece the director's own rule picks the take
closest to F's normal voice (no human info). Gaps: 0.3 s after "," / "—", 0.4 s after ";", 0.55 s after a sentence."""
import base64, csv, io, json, os, sys, ast, re
import numpy as np, librosa, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
run, hcsv, hjson, out = sys.argv[1:5]
src = open(os.path.join(ROOT, "kaggle/jobs", run, "pilot.py")).read()
NARR = ast.literal_eval(re.search(r"^NARR = (.*?)\s+#", src, re.M).group(1))
TXT = ast.literal_eval(re.search(r"^TXT = (.*?)\s+#", src, re.M).group(1))
takes = [t for t in csv.DictReader(open(os.path.join(ROOT, "results", run, "takes.csv"))) if t["status"] in ("PASS", "fail")]
tdir = os.path.join(ROOT, "results", run, "takes"); SR = 24000
hum = {r["code"]: r for r in csv.DictReader(open(hcsv))}; hpack = json.load(open(hjson))
def pick(i):
    c = [t for t in takes if t["id"] == i and os.path.exists(os.path.join(tdir, f"{i}_{t['var']}_{t['take']}.mp3"))]
    if not c: return None
    t = min(c, key=lambda t: abs(float(t["d_lufs"])) / 3 + abs(float(t["d_f0_med"])) / 2.5 + abs(float(t["speed_pct"])) / 30)
    y, _ = librosa.load(os.path.join(tdir, f"{i}_{t['var']}_{t['take']}.mp3"), sr=SR); return y
def gap(text): return 0.3 if text.rstrip()[-1] in ",—" else 0.4 if text.rstrip()[-1] == ";" else 0.55
os.makedirs(os.path.join(out, "audio"), exist_ok=True); pack, pairs = {}, []
for n, (p, arms) in enumerate(NARR.items(), 1):
    pack[f"O{n}"] = hpack[p]; item = dict(n=n, code=p, text=hum[p]["text"], versions=[])
    for arm, label in (("A", "short pieces"), ("B", "one read per sentence")):
        parts = []
        for i in arms[arm]:
            y = pick(i)
            if y is None: parts = None; break
            parts += [y, np.zeros(int(gap(TXT[(i, arm)]) * SR), dtype=np.float32)]
        if not parts: continue
        b = io.BytesIO(); sf.write(b, np.concatenate(parts[:-1]), SR, format="WAV", subtype="PCM_16")
        pack[f"{arm}{n}"] = "WAV:" + base64.b64encode(b.getvalue()).decode(); item["versions"].append([arm, label])
    pairs.append(item)
json.dump(pack, open(os.path.join(out, "audio", "pairs.json"), "w")); json.dump(pairs, open(os.path.join(out, "pairs.json"), "w"), ensure_ascii=False)
open(os.path.join(out, "index.html"), "w").write(open(os.path.join(os.path.dirname(__file__), "narr_page.html")).read())
print(len(pairs), "paragraphs")

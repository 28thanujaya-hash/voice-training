"""Blind check sample of auto_sort decisions.

Usage: python3 tools/build_check_page.py <name> <out_dir> <mood.csv> [<mood.csv> ...]
Per mood: 4 kept, 4 dropped as flat, 2 spares, 2 kept takes with s-sound "hiss" 0.15-0.3 s.
Clips are shuffled and numbered C1, C2…; the decision is in key.csv only (not on the page).
"""
import base64, csv, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name, out, csvs = sys.argv[1], sys.argv[2], sys.argv[3:]
rnd = random.Random(name)
N = {"tense": (3, 2, 1, 0), "low": (6, 5, 1, 1), "bright": (6, 5, 1, 1)}   # check2: weight toward low and bright
if os.environ.get("CHECK_N"): N = {k: tuple(v) for k, v in json.loads(os.environ["CHECK_N"]).items()}  # e.g. {"bright":[0,10,0,0]}
os.makedirs(os.path.join(out, "audio"), exist_ok=True)
picked = []
import glob
seen_before = {(k["mood"], k["take"]) for g in glob.glob(os.path.join(ROOT, "results/auto_sort/*_key.csv")) for k in csv.DictReader(open(g))}
for path in csvs:
    rows = list(csv.DictReader(open(path)))
    def take(group, cond, n):
        pool = [r for r in rows if cond(r) and r not in picked
                and (r["mood"], f"{r['id']}_{r['var']}_{r['take']}") not in seen_before]
        rnd.shuffle(pool); seen = set()
        for r in pool:
            if len([p for p in picked if p.get("group") == group and p["mood"] == r["mood"]]) >= n: break
            if r["id"] in seen: continue
            seen.add(r["id"]); r["group"] = group; picked.append(r)
    n = N.get(rows[0]["mood"], (4, 4, 2, 2))
    take("keep", lambda r: r["decision"].startswith("keep") and float(r["hiss"]) <= 0.15, n[0])
    take("drop-flat", lambda r: r["decision"] == "drop-flat", n[1])
    take("spare", lambda r: r["decision"] == "spare", n[2])
    take("s-sound", lambda r: r["decision"] in ("keep", "spare") and 0.15 < float(r["hiss"]) <= 0.3, n[3])
rnd.shuffle(picked)
clips, pack, key = [], {}, []
for i, r in enumerate(picked, 1):
    code = f"C{i}"
    fn = os.path.join(ROOT, "results", r["run"], "takes", f"{r['id']}_{r['var']}_{r['take']}.mp3")
    pack[code] = base64.b64encode(open(fn, "rb").read()).decode()
    clips.append(dict(code=code, mood=r["mood"], line=i, id=r["id"], text=f"{r['text']}  ({r['mood']})", tag="—",
                      run=r["run"], take=f"{r['id']}_{r['var']}_{r['take']}", speed=r["speed_pct"], loud=r["d_lufs"],
                      pitch=r["d_f0_med"], end="", rising=False, reveal=False, heard=r["heard"], pack="audio/check.json"))
    key.append(dict(code=code, mood=r["mood"], group=r["group"], run=r["run"], take=f"{r['id']}_{r['var']}_{r['take']}", text=r["text"]))
json.dump(pack, open(os.path.join(out, "audio", "check.json"), "w"))
json.dump(clips, open(os.path.join(out, "clips.json"), "w"), ensure_ascii=False)
os.makedirs(os.path.join(ROOT, "results", "auto_sort"), exist_ok=True)
with open(os.path.join(ROOT, "results", "auto_sort", f"{name}_key.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(key[0])); w.writeheader(); w.writerows(key)
html = open(os.path.join(ROOT, "tools", "sort_page.html")).read()
html = html.replace("__TITLE__", f"F auto-sort check ({name})").replace("__MOOD__", name)
html = html.replace("F · " + name + ", full run · sort by ear", f"F · auto-sort check · {name}")
html = html.replace("tag: ${c.tag}", "mood asked for: ${c.mood}")
open(os.path.join(out, "index.html"), "w").write(html)
print(len(clips), "clips")

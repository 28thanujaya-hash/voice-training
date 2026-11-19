"""Build a 'sort by ear' page for full-run takes.

Usage: python3 tools/build_sort_page.py <mood> <out_dir> <run> [<run> ...]
  e.g. python3 tools/build_sort_page.py bright /tmp/page full_bright_1 full_bright_2

Writes <out_dir>/index.html, clips.json and audio/<run>.json (base64 mp3 packs),
ready to publish as an artifact. Takes are the cut clips in results/<run>/takes
(right words only). Lines with "…" (reveal lines) list rising-end takes first.
"""
import ast, base64, csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mood, out, runs = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(os.path.join(out, "audio"), exist_ok=True)


def pilot_dict(run, name):
    src = open(os.path.join(ROOT, "kaggle/jobs", run, "pilot.py")).read()
    m = re.search(r"^" + name + r" = (.*?)(\s+#.*)?$", src, re.M)
    return ast.literal_eval(m.group(1)) if m else {}


clips, line_no, letter = [], 0, mood[0].upper()
for run in runs:
    ref_final = pilot_dict(run, "REF").get("final_drop", 0.0)
    txt = pilot_dict(run, "TXT")
    rows = list(csv.DictReader(open(os.path.join(ROOT, "results", run, "takes.csv"))))
    tdir = os.path.join(ROOT, "results", run, "takes")
    pack, order = {}, []
    for r in rows:
        if r["id"] not in order: order.append(r["id"])
    for lid in order:
        rs = [r for r in rows if r["id"] == lid and r["status"] in ("PASS", "fail")
              and os.path.exists(os.path.join(tdir, f"{lid}_{r['var']}_{r['take']}.mp3"))]
        if not rs: continue
        line_no += 1
        actor = txt.get(lid, rs[0]["text"])
        tags = re.findall(r"<(\w+)>", actor)
        reveal = "…" in rs[0]["text"] or "..." in rs[0]["text"]
        if reveal: rs.sort(key=lambda r: -float(r["d_final_drop"] or -99))
        for n, r in enumerate(rs, 1):
            code = f"{letter}{line_no}-{n}"
            fd = float(r["d_final_drop"] or 0) + ref_final
            with open(os.path.join(tdir, f"{lid}_{r['var']}_{r['take']}.mp3"), "rb") as f:
                pack[code] = base64.b64encode(f.read()).decode()
            clips.append(dict(code=code, mood=mood, line=line_no, id=lid, text=rs[0]["text"],
                              tag=", ".join(tags) or "none", run=run, take=f"{lid}_{r['var']}_{r['take']}",
                              speed=r["speed_pct"], loud=r["d_lufs"], pitch=r["d_f0_med"],
                              end=f"{fd:+.1f}", rising=reveal and fd > 0, reveal=reveal,
                              heard=r["heard"], pack=f"audio/{run}.json"))
    json.dump(pack, open(os.path.join(out, "audio", f"{run}.json"), "w"))
json.dump(clips, open(os.path.join(out, "clips.json"), "w"), ensure_ascii=False)

html = open(os.path.join(ROOT, "tools", "sort_page.html")).read()
html = html.replace("__MOOD__", mood).replace("__TITLE__", f"F {mood} (full run): sort by ear")
open(os.path.join(out, "index.html"), "w").write(html)
print(f"{len(clips)} clips, {line_no} lines")

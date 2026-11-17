# Run 6 · ten: 10 IndexTTS-2.5 clips per mood (best within-sentence mood score, one per sentence, words exact), named by mood (mentor 14:03).
import glob, json, os, subprocess
W = "/kaggle/working"; os.makedirs(f"{W}/ten", exist_ok=True)
import sys; sys.path.insert(0, os.getcwd()); from sel import SEL
lines = ["# IndexTTS-2.5 · 10 clips per mood", "", "| clip | text |", "|---|---|"]
for s in SEL:
    f = glob.glob(f"/kaggle/input/**/se-run6-idx/takes/{s['path']}", recursive=True)
    if not f: lines.append(f"| {s['name']} | MISSING {s['path']} |"); continue
    subprocess.run(f"ffmpeg -loglevel error -y -i '{f[0]}' -codec:a libmp3lame -b:a 128k {W}/ten/{s['name']}", shell=True)
    lines.append(f"| {s['name']} | {s['text']} |")
open(f"{W}/report.md", "w").write("\n".join(lines) + "\n")

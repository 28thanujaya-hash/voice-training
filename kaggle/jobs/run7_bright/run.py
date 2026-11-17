# Run 7 · bright: 5 Orpheus bright clips by the new bright rules (mentor 15:20). Selection only, no DSP on the voice.
# Rules vs Maya's normal: ≥6 syllables; pitch ≥ +2.5 st; pitch movement ≥ +0.8; end not quieter (≥ −1 dB); end fall gentle (≥ −5 st);
# not breathier (≤ +1.5 dB). Tier 2 (slightly looser) only if tier 1 runs out. Here: longest gap inside the line ≤ 0.5 s;
# silence before/after the speech trimmed (kept 0.1 s). One clip per line.
import os, sys, glob, subprocess, traceback
sys.path.insert(0, os.getcwd())
from cand import CAND
W = "/kaggle/working"; rep = ["# Run 7 · bright: 5 clips by the new bright rules", "", "| clip | text | longest gap | measures (vs normal) |", "|---|---|---|---|"]
skip = []
try:
    subprocess.run("pip install -q librosa soundfile", shell=True)
    import numpy as np, soundfile as sf, librosa
    n = 0; used = set()
    for c in CAND:
        if n >= 5: break
        if c["id"] in used: continue
        p = "/kaggle/input/" + c["path"]
        if not os.path.exists(p):
            g = glob.glob("/kaggle/input/**/" + os.path.basename(c["path"]), recursive=True)
            if not g: skip.append(f"{c['id']}: file not found"); continue
            p = g[0]
        y, sr = sf.read(p, dtype="float32")
        if y.ndim > 1: y = y.mean(1)
        iv = librosa.effects.split(y, top_db=35, frame_length=1024, hop_length=240)
        gaps = [(iv[i][0] - iv[i-1][1]) / sr for i in range(1, len(iv))]
        g = max(gaps) if gaps else 0.0
        if g > 0.5: skip.append(f"{c['id']} ({c['text']}): gap {g:.2f} s"); continue
        a = max(0, iv[0][0] - int(0.1 * sr)); b = min(len(y), iv[-1][1] + int(0.1 * sr))
        n += 1; used.add(c["id"]); name = f"bright_{n:02d}.mp3"
        sf.write("/tmp/x.wav", y[a:b], sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/x.wav", "-b:a", "128k", f"{W}/{name}"], check=True)
        rep.append(f"| {name} | {c['text']} | {g:.2f} s | {c['note']}{'' if c['tier'] == 1 else ' (tier 2)'} |")
    rep += ["", f"Picked {n}. Skipped:", *[f"- {s}" for s in skip]]
except Exception:
    rep += ["", "## ERROR", "```", traceback.format_exc()[-2000:], "```"]
open(f"{W}/report.md", "w").write("\n".join(rep))

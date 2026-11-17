# Run 7 · low 40: one low clip about 40% slower (mentor 16:33), same checks: gap ≤ 0.5 s, no flat hold > 0.5 s, no hiss > 0.15 s.
# mentor 16:19 "noise dragging 'winner'"). Same bright rules as run7_bright, plus two new checks:
import os, sys, glob, subprocess, traceback
sys.path.insert(0, os.getcwd())
from cand import CAND
W = "/kaggle/working"; rep = ["# Run 7 · low 40: one low clip about 40% slower", "", "| clip | text | longest gap | flat hold | hiss | measures |", "|---|---|---|---|---|---|"]
skip = []
try:
    subprocess.run("pip install -q librosa soundfile", shell=True)
    import numpy as np, soundfile as sf, librosa
    n = 0
    for c in [c for c in CAND if c["id"] != "m3l42"]:
        if n >= 2: break
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
        a = max(0, iv[0][0] - int(0.1 * sr)); b = min(len(y), iv[-1][1] + int(0.1 * sr)); y = y[a:b]
        hop = int(0.01 * sr)
        f0, vf, _ = librosa.pyin(y, fmin=100, fmax=700, sr=sr, frame_length=2048, hop_length=hop)
        st = 12 * np.log2(np.where(vf, f0, np.nan) / 100); flat = 0; run = 0
        for i in range(1, len(st)):
            if np.isfinite(st[i]) and np.isfinite(st[i-1]):
                j = i - run - 1
                run = run + 1 if np.nanmax(st[j:i+1]) - np.nanmin(st[j:i+1]) <= 1.0 else 0
            else: run = 0
            flat = max(flat, run)
        flat_s = flat * hop / sr
        S = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop)) ** 2; fr = librosa.fft_frequencies(sr=sr, n_fft=1024)
        share = S[fr > 4000].sum(0) / np.maximum(S.sum(0), 1e-12); lvl = 10 * np.log10(np.maximum(S.sum(0), 1e-12))
        h = (share > 0.9) & (lvl > lvl.max() - 35); hiss = 0; run = 0
        for x in h: run = run + 1 if x else 0; hiss = max(hiss, run)
        hiss_s = hiss * hop / sr
        why = [w for w, bad in ((f"gap {g:.2f} s", g > 0.5), (f"flat hold {flat_s:.2f} s", flat_s > 0.5), (f"hiss {hiss_s:.2f} s", hiss_s > 0.15)) if bad]
        if why: skip.append(f"{c['id']} ({c['text']}): " + ", ".join(why)); continue
        n += 1; name = "low_40.mp3" if n == 1 else "low_40_spare.mp3"
        sf.write("/tmp/x.wav", y, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/x.wav", "-b:a", "128k", f"{W}/{name}"], check=True)
        rep.append(f"| {name} | {c['text']} | {g:.2f} s | {flat_s:.2f} s | {hiss_s:.2f} s | {c['note']}{'' if c['tier'] == 1 else ' (tier 2)'} |")
    rep += ["", f"Picked {n}. Skipped:", *[f"- {s}" for s in skip]]
except Exception:
    rep += ["", "## ERROR", "```", traceback.format_exc()[-2000:], "```"]
open(f"{W}/report.md", "w").write("\n".join(rep))

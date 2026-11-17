# Run 7 · five: 5 Orpheus clips per mood (normal reference + low, bright, tense), picked from the existing run-5 clips
# by the cues IndexTTS used (results/run7_grey/report.md). No recording, no DSP: clips copied as recorded. CPU only.
#   low    : slower words, ≥2 dB quieter, breathier (H1-H2 ≥ +3 dB) than normal — pitch level not used
#   tense  : ≥2 st higher, not slower, ≥3 dB louder, falling through the phrase
#   bright : ≥3 st higher, more pitch movement
import os, sys, subprocess, traceback
sys.path.insert(0, os.getcwd())
from sel import SEL
W = "/kaggle/working"; rep = ["# Run 7 · five: Orpheus clips picked by the IndexTTS cues (no DSP)", "",
    "Numbers are compared with Maya's normal (median of the clean normal clips).", "", "| clip | text | measures |", "|---|---|---|"]
try:
    for s in SEL:
        src = "/kaggle/input/" + s["path"].split("notebooks/", 1)[-1] if not os.path.exists("/kaggle/input/" + s["path"]) else "/kaggle/input/" + s["path"]
        if not os.path.exists(src):
            import glob; c = glob.glob("/kaggle/input/**/" + os.path.basename(s["path"]), recursive=True); src = c[0] if c else src
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-b:a", "128k", f"{W}/{s['name']}"], check=True)
        rep.append(f"| {s['name']} | {s['text']} | {s['note']} |")
except Exception:
    rep += ["", "## ERROR", "```", traceback.format_exc()[-2000:], "```"]
open(f"{W}/report.md", "w").write("\n".join(rep))

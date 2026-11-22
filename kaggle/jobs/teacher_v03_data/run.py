# teacher_v03_data (CPU): the chosen clips for Kokoro teacher v0.3 (tools/queue/select_teacher.py → results/teacher_v03/train.csv).
# Downloads each take (mp3, raw GitHub) → 24 kHz mono wav in final/, writes train.csv (file,row,text_b,text,split,id) for teacher_v03_t1/t2.
import csv, io, os, subprocess, time, urllib.request
W = "/kaggle/working"; os.makedirs(f"{W}/final", exist_ok=True); T0 = time.time()
src = urllib.request.urlopen("https://raw.githubusercontent.com/28thanujaya-hash/voice-training/main/results/teacher_v03/train.csv").read().decode()
rows = list(csv.DictReader(io.StringIO(src))); ok = []
for r in rows:
    try:
        urllib.request.urlretrieve(r["url"], "/tmp/t.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/t.mp3", "-ar", "24000", "-ac", "1", f"{W}/{r['file']}"], check=True); ok.append(r)
    except Exception as e: print("skip", r["url"], e)
with open(f"{W}/train.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["file", "row", "text_b", "text", "split", "id"], extrasaction="ignore"); w.writeheader(); w.writerows(ok)
from collections import Counter
rep = f"# teacher_v03_data\n\n{len(ok)}/{len(rows)} clips in {(time.time()-T0)/60:.1f} min\n\n{dict(Counter((r['row'], r['split']) for r in ok))}\n\nRESULT: DONE\n"
open(f"{W}/report.md", "w").write(rep); print(rep)

"""Cut listening clips from a LibriVox reading. Usage: python tools/book/clips.py <archive_item> <clips.csv> <out.json>
clips.csv columns: code, chapter (chNN), start, end (seconds in that chapter's mp3). Output: {code: base64 mp3}."""
import base64, csv, json, subprocess, sys, urllib.request
item, src, out = sys.argv[1:4]
UA = {"User-Agent": "voice-training research (github.com/28thanujaya-hash/voice-training)"}
meta = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://archive.org/metadata/{item}", headers=UA)).read())
files = sorted(f["name"] for f in meta["files"] if f["name"].endswith(".mp3") and "64kb" in f["name"])
rows = list(csv.DictReader(open(src))); pack = {}; got = {}
for r in rows:
    n = int(r["chapter"].replace("ch", ""))
    if n not in got:
        got[n] = f"/tmp/ch{n:02d}.mp3"
        urllib.request.urlretrieve(f"https://archive.org/download/{item}/{urllib.request.quote(files[n - 1])}", got[n])
    a, b = max(0, float(r["start"]) - 0.15), float(r["end"]) + 0.3
    o = f"/tmp/{r['code']}.mp3"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.2f}", "-to", f"{b:.2f}", "-i", got[n], "-ac", "1", "-b:a", "64k", o], check=True)
    pack[r["code"]] = base64.b64encode(open(o, "rb").read()).decode()
json.dump(pack, open(out, "w")); print(len(pack), "clips")

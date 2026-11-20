"""Meta superb judge for the old runs (run5/run6 format: takes.csv has id, row (= mood), file (takes/<name>.wav)).
Usage: python tools/judge/superb_old.py <run> <audio_dir>
Writes results/judge/superb_<run>.csv and compact mp3 copies to results/<run>/takes/."""
import csv, os, subprocess, sys, librosa, torch
from transformers import AutoFeatureExtractor, HubertForSequenceClassification
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
run, src = sys.argv[1], sys.argv[2]
NAME = "superb/hubert-large-superb-er"; fe = AutoFeatureExtractor.from_pretrained(NAME)
m = HubertForSequenceClassification.from_pretrained(NAME).eval(); torch.set_num_threads(os.cpu_count() or 2)
LAB = {"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}
labels = [LAB.get(m.config.id2label[i], m.config.id2label[i]) for i in range(len(m.config.id2label))]
files = {}
for dp, _, fs in os.walk(src):
    for f in fs:
        if f.endswith((".wav", ".mp3")): files.setdefault(os.path.splitext(f)[0], os.path.join(dp, f))
out = os.path.join(ROOT, "results", run, "takes"); os.makedirs(out, exist_ok=True); rows = []
for t in csv.DictReader(open(os.path.join(ROOT, "results", run, "takes.csv"))):
    name = os.path.splitext(os.path.basename(t.get("file", "")))[0]; f = files.get(name)
    if not f: continue
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-ac", "1", "-b:a", "48k", f"{out}/{name}.mp3"], check=True)
    y, _ = librosa.load(f, sr=16000); y = librosa.effects.trim(y, top_db=35)[0]
    with torch.no_grad(): p = torch.softmax(m(**fe(y, sampling_rate=16000, return_tensors="pt")).logits[0], -1).numpy()
    rows.append(dict(run=run, mood=t.get("row", ""), var="", id=t["id"], take=name, judged=labels[int(p.argmax())],
                     **{"p_" + k: round(float(v), 3) for k, v in zip(labels, p)}))
with open(os.path.join(ROOT, "results/judge", f"superb_{run}.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
print(run, len(rows), "of", len(files), "audio files judged", flush=True)

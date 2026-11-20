"""Second judge: Meta's HuBERT-large fine-tuned for emotion (superb/hubert-large-superb-er; 4 classes neu/hap/ang/sad, IEMOCAP).
Usage: python tools/judge/superb.py <run> [<run> ...]   → results/judge/superb_<run>.csv (one row per right-word take)."""
import csv, os, sys, numpy as np, librosa, torch
from transformers import AutoFeatureExtractor, HubertForSequenceClassification
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
torch.set_num_threads(max(1, os.cpu_count() or 2))
NAME = "superb/hubert-large-superb-er"
fe = AutoFeatureExtractor.from_pretrained(NAME); m = HubertForSequenceClassification.from_pretrained(NAME).eval()
LAB = {"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}
labels = [LAB.get(m.config.id2label[i], m.config.id2label[i]) for i in range(len(m.config.id2label))]
os.makedirs(os.path.join(ROOT, "results/judge"), exist_ok=True)
for run in sys.argv[1:]:
    tc = os.path.join(ROOT, "results", run, "takes.csv"); td = os.path.join(ROOT, "results", run, "takes"); rows = []
    for t in csv.DictReader(open(tc)):
        if t.get("status") not in ("PASS", "fail"): continue
        name = f"{t['id']}_{t['var']}_{t['take']}"
        f = next((p for p in (f"{td}/{name}.mp3", f"{td}/{name}.wav") if os.path.exists(p)), None)
        if not f: continue
        y, _ = librosa.load(f, sr=16000); y = librosa.effects.trim(y, top_db=35)[0]
        with torch.no_grad(): p = torch.softmax(m(**fe(y, sampling_rate=16000, return_tensors="pt")).logits[0], -1).numpy()
        rows.append(dict(run=run, mood=t.get("mood", ""), var=t["var"], id=t["id"], take=name, judged=labels[int(p.argmax())], **{"p_" + k: round(float(v), 3) for k, v in zip(labels, p)}))
    with open(os.path.join(ROOT, "results/judge", f"superb_{run}.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    print(run, len(rows), {k: sum(r["judged"] == k for r in rows) for k in labels}, flush=True)

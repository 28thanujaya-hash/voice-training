"""Pick the human sad clips the judge is surest about, to use as Orpheus context (run25).
CREMA-D (ODbL), women, sad, >= 2.0 s after trimming; scored by superb/hubert-large-superb-er.
Writes the top clips (one per sentence and per speaker) as mp3 + picks.csv into the output folder.
Usage: python tools/judge/pick_sad_ctx.py <out_dir> [n]"""
import io, os, re, sys, urllib.request, numpy as np, pandas as pd, soundfile as sf, librosa, torch
from transformers import AutoFeatureExtractor, HubertForSequenceClassification
out = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 3; EMO = sys.argv[3] if len(sys.argv) > 3 else "SAD"; os.makedirs(out, exist_ok=True)
KEY = {"SAD": "sad", "HAP": "hap", "ANG": "ang", "NEU": "neu"}[EMO]
TXT = {"IEO": "It's eleven o'clock.", "TIE": "That is exactly what happened.", "IOM": "I'm on my way to the meeting.",
       "IWW": "I wonder what this is about.", "TAI": "The airplane is almost full.", "MTI": "Maybe tomorrow it will be cold.",
       "IWL": "I would like a new alarm clock.", "ITH": "I think I have a doctor's appointment.", "DFA": "Don't forget a jacket.",
       "ITS": "I think I've seen this before.", "TSI": "The surface is slick.", "WSI": "We'll stop in a couple of minutes."}
NAME = "superb/hubert-large-superb-er"; fe = AutoFeatureExtractor.from_pretrained(NAME); m = HubertForSequenceClassification.from_pretrained(NAME).eval()
lab = [m.config.id2label[i] for i in range(len(m.config.id2label))]
demo = pd.read_csv("https://raw.githubusercontent.com/CheyneyComputerScience/CREMA-D/master/VideoDemographics.csv")
fem = set(demo[demo.Sex == "Female"].ActorID.astype(str)); rows = []
for split in ("train", "validation", "test"):
    p = f"/tmp/crema_{split}.parquet"
    if not os.path.exists(p): urllib.request.urlretrieve(f"https://huggingface.co/datasets/confit/cremad-parquet/resolve/main/data/{split}-00000-of-00001.parquet", p)
    for _, r in pd.read_parquet(p).iterrows():
        g = re.search(r"(\d{4})_([A-Z]{3})_([A-Z]{3})_([A-Z]{2})", r.file)
        if not g or g.group(1) not in fem or g.group(3) != EMO: continue
        y, sr = sf.read(io.BytesIO(r.audio["bytes"])); y = y.mean(1) if y.ndim > 1 else y
        y16 = librosa.effects.trim(librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=16000), top_db=35)[0]
        if len(y16) < 32000: continue
        with torch.no_grad(): pr = torch.softmax(m(**fe(y16, sampling_rate=16000, return_tensors="pt")).logits, -1)[0].numpy()
        rows.append(dict(file=g.group(0), spk=g.group(1), item=g.group(2), level=g.group(4), dur=len(y16) / 16000, p_sad=float(pr[lab.index(KEY)]), audio=y, sr=sr))
D = pd.DataFrame(rows).sort_values("p_sad", ascending=False); print(len(D), "female sad clips >= 2 s")
pick, used_i, used_s = [], set(), set()
for _, r in D.iterrows():
    if r.item in used_i or r.spk in used_s: continue
    pick.append(r); used_i.add(r.item); used_s.add(r.spk)
    if len(pick) == N: break
for k, r in enumerate(pick, 1):
    w = f"/tmp/h{k}.wav"; sf.write(w, r.audio, r.sr); os.system(f"ffmpeg -loglevel error -y -i {w} -b:a 128k {out}/human_{k}.mp3")
P = pd.DataFrame([{k: r[k] for k in ("file", "spk", "item", "level", "dur", "p_sad")} for r in pick]); P["text"] = P.item.map(TXT)
P.to_csv(f"{out}/picks_{EMO.lower()}.csv", index=False); print(P.to_string())

"""Mood-judge embeddings (CPU). One set (or one shard of a set) per call.

Usage: python tools/judge/embed.py <set> [<shard>]
  set = crema | ravdess | esd (shard 0-6 = one ESD parquet file) | tara
Writes results/judge/emb/<set>[_<shard>].npz with E (float16, HuBERT-base layers 6/9/12 mean-pooled) and meta columns.

Humans: women only, moods neutral / happy / sad / angry (= our normal / bright / low / tense).
  CREMA-D (ODbL), RAVDESS (non-commercial), ESD English (CC BY-NC): used for judging only, never voice training.
tara: every right-word take of the full F run, the normal batches, and the run13/run14/run15/run9 partner sets.
"""
import glob, io, os, re, sys, csv, urllib.request
import numpy as np, librosa, soundfile as sf, torch
from transformers import AutoFeatureExtractor, HubertModel

SET = sys.argv[1]; SHARD = sys.argv[2] if len(sys.argv) > 2 else None
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "results/judge/emb"); os.makedirs(OUT, exist_ok=True)
HF = "https://huggingface.co/datasets/{}/resolve/main/{}"
MOOD = {"neutral": "neutral", "happy": "happy", "happiness": "happy", "sad": "sad", "sadness": "sad", "angry": "angry", "anger": "angry"}
torch.set_num_threads(max(1, os.cpu_count() or 2))
fe = AutoFeatureExtractor.from_pretrained("facebook/hubert-base-ls960")
hm = HubertModel.from_pretrained("facebook/hubert-base-ls960").eval()


def emb(y):
    with torch.no_grad():
        h = hm(**fe(y, sampling_rate=16000, return_tensors="pt"), output_hidden_states=True).hidden_states
    return torch.stack([h[i][0].mean(0) for i in (6, 9, 12)]).flatten().numpy().astype(np.float16)


def from_bytes(b):
    y, sr = sf.read(io.BytesIO(b)); y = y.mean(1) if y.ndim > 1 else y
    y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=16000)
    return librosa.effects.trim(y, top_db=35)[0]


def fetch(repo, path):
    local = "/tmp/" + path.replace("/", "_")
    if not os.path.exists(local): urllib.request.urlretrieve(HF.format(repo, path), local)
    return local


E, M = [], []
def add(y, **m):
    if len(y) < 1600: return
    E.append(emb(y)); M.append(m)

import pandas as pd
if SET == "crema":
    demo = pd.read_csv("https://raw.githubusercontent.com/CheyneyComputerScience/CREMA-D/master/VideoDemographics.csv")
    fem = set(demo[demo.Sex == "Female"].ActorID.astype(str))
    for split in ("train", "validation", "test"):
        d = pd.read_parquet(fetch("confit/cremad-parquet", f"data/{split}-00000-of-00001.parquet"))
        for _, r in d.iterrows():
            m = re.search(r"(\d{4})_([A-Z]{3})_([A-Z]{3})_([A-Z]{2})", r.file); mood = MOOD.get(str(r.emotion).lower())
            if m and mood and m.group(1) in fem:
                add(from_bytes(r.audio["bytes"]), set="crema", spk=m.group(1), mood=mood, level=m.group(4), item=m.group(2))
elif SET == "ravdess":
    for f in ("train-00000-of-00002-94d632c9f1f51bbe.parquet", "train-00001-of-00002-bcaf733d4b46d6b2.parquet"):
        d = pd.read_parquet(fetch("xbgoose/ravdess", f"data/{f}"))
        d = d[(d.gender == "female") & (d.vocal_channel == "speech")]
        for _, r in d.iterrows():
            mood = MOOD.get(str(r.emotion).lower())
            if mood: add(from_bytes(r.audio["bytes"]), set="ravdess", spk=str(r.actor), mood=mood, level=str(r.emotional_intensity), item=str(r.statement)[:4])
elif SET == "esd":
    d = pd.read_parquet(fetch("jspaulsen/esd", f"data/train-0000{SHARD}-of-00007.parquet"))
    lang = d.language.str.lower(); gen = d.gender.str.lower()
    d = d[lang.str.startswith("en") & gen.str.startswith("f")]
    print("esd shard", SHARD, "english women rows", len(d), d.emotion.value_counts().to_dict(), flush=True)
    for _, r in d.iterrows():
        mood = MOOD.get(str(r.emotion).lower())
        if mood: add(from_bytes(r.audio["bytes"]), set="esd", spk=str(r.speaker_id), mood=mood, level="", item=str(r.transcript)[:40])
elif SET == "tara":
    runs = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(ROOT, "results", "full_*"))) +
            [os.path.join(ROOT, "results", r) for r in ("run9_low", "run13_bright", "run14_tense", "run15_tense")]]
    for run in runs:
        tc = os.path.join(ROOT, "results", run, "takes.csv"); td = os.path.join(ROOT, "results", run, "takes")
        if not os.path.exists(tc): continue
        for t in csv.DictReader(open(tc)):
            if t.get("status") not in ("PASS", "fail"): continue
            name = f"{t['id']}_{t['var']}_{t['take']}"
            f = next((p for p in (f"{td}/{name}.mp3", f"{td}/{name}.wav") if os.path.exists(p)), None)
            if not f: continue
            y, _ = librosa.load(f, sr=16000); add(librosa.effects.trim(y, top_db=35)[0], set="tara", spk=run, mood=t.get("mood", ""), level=t["var"], item=name)
name = SET + (f"_{SHARD}" if SHARD is not None else "")
np.savez_compressed(os.path.join(OUT, name + ".npz"), E=np.array(E), **{k: np.array([m[k] for m in M]) for k in (M[0] if M else {})})
print(name, len(E), "clips", flush=True)

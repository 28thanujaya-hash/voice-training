"""Does a run still sound like tara? Speaker embeddings (SpeechBrain ECAPA, VoxCeleb) vs tara's own takes.
Usage: python tools/judge/voice_match.py <run> <ref_run[,ref_run…]> [<extra_wav_or_mp3>...]  -> results/judge/voice_<run>.csv
Each take: cosine to the centroid of ref_run's takes; extra files (e.g. the context clips) are scored the same way for comparison."""
import glob, os, sys, numpy as np, pandas as pd, torch, librosa
from speechbrain.inference.speaker import EncoderClassifier
run, ref = sys.argv[1], sys.argv[2]; extra = sys.argv[3:]
enc = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb", savedir="/tmp/ecapa", run_opts={"device": "cpu"})
def emb(f):
    y, _ = librosa.load(f, sr=16000); y = librosa.effects.trim(y, top_db=35)[0]
    with torch.no_grad(): e = enc.encode_batch(torch.tensor(y)[None])[0, 0].numpy()
    return e / np.linalg.norm(e)
refs = ref.split(","); n = 60 // len(refs)   # several refs: equal share each (22 Nov: "mix" = 15 takes from each mood's full run)
R = [f for r in refs for f in sorted(glob.glob(f"results/{r}/takes/*.mp3"))[:n]]; c = np.mean([emb(f) for f in R], 0); c /= np.linalg.norm(c)
rows = [dict(file=os.path.basename(f), var=os.path.basename(f).split("_")[1], cos=float(emb(f) @ c)) for f in sorted(glob.glob(f"results/{run}/takes/*.mp3"))]
rows += [dict(file=os.path.basename(f), var="EXTRA", cos=float(emb(f) @ c)) for f in extra]
D = pd.DataFrame(rows); os.makedirs("results/judge", exist_ok=True); D.to_csv(f"results/judge/voice_{run}" + ("_mix" if len(refs) > 1 else "") + ".csv", index=False)
print(D.groupby("var").cos.describe().round(3).to_string()); print(D[D["var"] == "EXTRA"].to_string())

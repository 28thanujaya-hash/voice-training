"""Teacher eval on CPU (GitHub Actions, free) with style-row exaggeration (chat 8, 23 Nov).
Rows are pushed away from the mean of the 4 rows: row' = mean + a * (row - mean).
Arms: 'P<a>' = only the prosody half (dims 128:256, read by the duration/pitch predictor), 'W<a>' = the whole 256-dim style.
Usage: python eval_cpu.py <model.pth> <voicepack dir> <tag> <arms comma list> <n lines>   (run from kaggle/jobs/teacher_v05_eval)
Judge: Meta superb, same pass rule as the Kaggle eval. No Whisper (CPU time)."""
import csv, os, re, sys, time, types
sys.path.insert(0, os.getcwd())
import numpy as np, torch, librosa
from student_data import STUDENT
from textprep import prepare_all
MP, VD, TAG, ARMS, N = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(','), int(sys.argv[5])
TMP = os.environ.get('TMP_DIR', '/tmp/ev'); K = os.environ['KT']
ROWS = ["normal", "bright", "low", "tense"]; KEY = {"normal": "neutral", "bright": "happy", "low": "sad", "tense": "angry"}
torch.set_num_threads(os.cpu_count())
class _Stub(types.ModuleType):
    def __getattr__(self, n):
        if n.startswith("__"): raise AttributeError(n)
        return type(n, (), {})
mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak"); sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
sys.path.insert(0, f"{K}/kokoro")
from kokoro.model import KModel
from huggingface_hub import hf_hub_download
kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
km = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=MP).eval()
VP = {r: torch.load(f"{VD}/f_{r}_voicepack.pt", map_location="cpu", weights_only=True).float() for r in ROWS}
MEAN = sum(VP.values()) / 4
def arm_vp(arm, row):
    if arm == 'base': return VP[row]
    a = float(arm[1:]); v = VP[row].clone(); d = MEAN + a * (VP[row] - MEAN)
    if arm[0] == 'W': return d
    v[..., 128:] = d[..., 128:]; return v
# fixed, balanced subset of held-out lines (every mood), the same for every model and arm
S = sorted(STUDENT, key=lambda s: (s['id']))
pick = []
for m in ROWS:
    L = [s for s in S if s['mood'] == m]; pick += L[:: max(1, len(L) // (N // 4))][: N // 4]
_, PH = prepare_all([s["text"] for s in pick], f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex")
from transformers import AutoFeatureExtractor, HubertForSequenceClassification
J = "superb/hubert-large-superb-er"; jfe = AutoFeatureExtractor.from_pretrained(J); jm = HubertForSequenceClassification.from_pretrained(J).eval()
JL = [{"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}.get(jm.config.id2label[i], jm.config.id2label[i]) for i in range(len(jm.config.id2label))]
rows = []; T0 = time.time()
for arm in ARMS:
    for s, p in zip(pick, PH):
        p2 = p[:510]
        for row in ROWS:
            with torch.no_grad(): out = km(p2, arm_vp(arm, row)[len(p2) - 1], 1.0)
            a = (out.audio if hasattr(out, "audio") else out).squeeze().float().numpy()
            z = librosa.effects.trim(librosa.resample(a, orig_sr=24000, target_sr=16000), top_db=35)[0]
            with torch.no_grad(): pr = torch.softmax(jm(**jfe(z, sampling_rate=16000, return_tensors="pt")).logits[0], -1).tolist()
            P = dict(zip(JL, pr)); judged = max(P, key=P.get)
            ok = (judged == "neutral" or max(P["happy"], P["sad"], P["angry"]) <= .5) if row == "normal" else (judged == KEY[row] and P[KEY[row]] > .5)
            rows.append(dict(model=TAG, arm=arm, id=s["id"], line_mood=s["mood"], row=row, judged=judged, ok=int(ok), secs=round(len(a) / 24000, 2), **{"p_" + k: round(v, 3) for k, v in P.items()}))
    print(f"{arm} done {(time.time()-T0)/60:.1f} min", flush=True)
os.makedirs("out", exist_ok=True)
with open(f"out/eval_{TAG}.csv", "w", newline="") as fh: w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
rep = [f"## {TAG} ({len(pick)} held-out lines, CPU)", "", "| arm | row | pass | judged neutral / happy / sad / angry | mean length s |", "|---|---|---|---|---|"]
for arm in ARMS:
    for row in ROWS:
        x = [r for r in rows if r["arm"] == arm and r["row"] == row]; c = {k: sum(r["judged"] == k for r in x) for k in ("neutral", "happy", "sad", "angry")}
        rep.append(f"| {arm} | {row} | {sum(r['ok'] for r in x)}/{len(x)} | {c['neutral']} / {c['happy']} / {c['sad']} / {c['angry']} | {np.mean([r['secs'] for r in x]):.2f} |")
    rep.append(f"| {arm} | **all** | **{sum(r['ok'] for r in rows if r['arm']==arm)}/{sum(1 for r in rows if r['arm']==arm)}** | | |")
open(f"out/report_{TAG}.md", "w").write("\n".join(rep) + "\n"); print("\n".join(rep))

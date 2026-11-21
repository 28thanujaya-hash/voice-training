"""run29 diagnosis on a free CPU machine (no GPU). run29b lost all 32 takes at decode in 0.3 min: Orpheus stopped right after the scene.
Checks, on 2 low lines with run29b's own recorded scene (results/run29b_prefix/scene_low.wav):
  A  run29b's exact prompt: what are the first generated tokens? (expect 128258 = end of speech at once)
  B  same prompt, end of speech blocked for the first ~1 s (min_new_tokens=84)
  C  as B, but the scene's trailing silence cut off (scene ends right after its last word)
Writes results/diag29/report.md and the B/C takes (mp3) with Whisper words and the Meta superb judge."""
import os, re, subprocess, time, numpy as np, soundfile as sf, librosa, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoFeatureExtractor, HubertForSequenceClassification, pipeline
torch.set_num_threads(os.cpu_count() or 4); torch.manual_seed(0)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); W = f"{ROOT}/results/diag29"; os.makedirs(W, exist_ok=True)
T0 = time.time(); LOG = []
def log(s): s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
SCENE = "Half the time it seems to me that Matthew can't be dead; and the other half it seems as if he must have been dead for a long time, and I've had this horrible dull ache ever since. The tears don't hurt me like that ache did. Oh, just let me cry."
LINES = {"m3l50": "<sigh> Priya's gone home for the weekend, so the flat's empty.", "m3l10": "<sigh> Some nights the flat feels very quiet… and I miss Jaffna."}
tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float32).eval()
from snac import SNAC
snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval(); log("models loaded")
def to_audio(ids):
    ids = [t for t in ids if t != 128258 and t >= 128266]; ids = ids[: len(ids) // 7 * 7]; c = [t - 128266 for t in ids]
    l1, l2, l3 = [], [], []
    for i in range(len(c) // 7):
        l1.append(c[7*i]); l2.append(c[7*i+1] - 4096); l3 += [c[7*i+2] - 2*4096, c[7*i+3] - 3*4096]
        l2.append(c[7*i+4] - 4*4096); l3 += [c[7*i+5] - 5*4096, c[7*i+6] - 6*4096]
    if not l1 or min(l1 + l2 + l3) < 0 or max(l1 + l2 + l3) > 4095: return None
    with torch.inference_mode(): return snac.decode([torch.tensor(x)[None] for x in (l1, l2, l3)]).squeeze().float().numpy()
def encode(y):
    with torch.inference_mode(): c = snac.encode(torch.tensor(y, dtype=torch.float32)[None, None])
    l1, l2, l3 = [x[0].tolist() for x in c]; out = []
    for i in range(len(l1)):
        out += [l1[i] + 128266, l2[2*i] + 128266 + 4096, l3[4*i] + 128266 + 2*4096, l3[4*i+1] + 128266 + 3*4096,
                l2[2*i+1] + 128266 + 4*4096, l3[4*i+2] + 128266 + 5*4096, l3[4*i+3] + 128266 + 6*4096]
    return out
y, _ = librosa.load(f"{ROOT}/results/run29b_prefix/scene_low.wav", sr=24000)
full = encode(y)
e = librosa.feature.rms(y=y, frame_length=1200, hop_length=600)[0]; last = np.where(20*np.log10(e + 1e-9) > -45)[0][-1]
trim = encode(y[: (last + 2) * 600]); log(f"scene codes: full {len(full)//7} frames, trimmed {len(trim)//7} frames ({len(y)/24000:.2f} s → {(last+2)*600/24000:.2f} s)")
def gen(line, codes, mn, mx):
    p = [128259] + tok(f"tara: {SCENE} {line}").input_ids + [128009, 128260, 128261, 128257] + codes
    ids = torch.tensor([p])
    with torch.inference_mode():
        g = om.generate(ids, attention_mask=torch.ones_like(ids), min_new_tokens=mn, max_new_tokens=mx, do_sample=True, temperature=0.6, top_p=0.95,
                        repetition_penalty=1.1, eos_token_id=128258, pad_token_id=128263)
    return g[0, len(p):].tolist()
asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", device="cpu")
NAME = "superb/hubert-large-superb-er"; jfe = AutoFeatureExtractor.from_pretrained(NAME); jm = HubertForSequenceClassification.from_pretrained(NAME).eval()
JL = [{"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}.get(jm.config.id2label[i], jm.config.id2label[i]) for i in range(len(jm.config.id2label))]
def judge(a):
    z = librosa.effects.trim(librosa.resample(a, orig_sr=24000, target_sr=16000), top_db=35)[0]
    with torch.no_grad(): p = torch.softmax(jm(**jfe(z, sampling_rate=16000, return_tensors="pt")).logits[0], -1).tolist()
    return dict(zip(JL, p))
rows = ["| arm | line | new tokens | first tokens | seconds | heard | judge |", "|---|---|---|---|---|---|---|"]
for lid, line in LINES.items():
    for arm, codes, mn, mx in [("A", full, 0, 30), ("B", full, 84, 700), ("C", trim, 84, 700)]:
        t = gen(line, codes, mn, mx); first = " ".join(str(x) for x in t[:8])
        ends = t.index(128258) if 128258 in t else len(t)
        a = to_audio(t[:ends]) if ends >= 7 else None; heard = jd = ""; sec = 0
        if a is not None:
            sec = len(a) / 24000; sf.write("/tmp/t.wav", a, 24000)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/t.wav", "-b:a", "96k", f"{W}/{lid}_{arm}.mp3"])
            heard = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip(); j = judge(a); k = max(j, key=j.get); jd = f"{k} {j[k]:.2f}"
        rows.append(f"| {arm} | {lid} | {ends} | {first} | {sec:.1f} | {heard} | {jd} |"); log(rows[-1])
open(f"{W}/report.md", "w").write("# run29 diagnosis (CPU)\n\nA = run29b prompt as is; B = end of speech blocked for 84 tokens (~1 s); C = B + scene trailing silence cut. 128258 = end of speech.\n\n"
                                   + "\n".join(rows) + "\n\n## Log\n```\n" + "\n".join(LOG) + "\n```\n")

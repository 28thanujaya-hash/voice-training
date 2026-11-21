# run29c_fix (21 Nov): why run29b lost every take, and a fix. Same 8 low lines and the same recorded scene as run29b (scene_low.wav).
#   A  run29b's exact prompt, 30 tokens: the first generated tokens (expect 128258 = end of speech at once)
#   B  same prompt, end of speech blocked for the first ~1 s (min_new_tokens=84)
#   C  as B, but the scene's trailing silence cut off
# B and C: 4 takes per line; sigh cut off before the first word (Whisper word times); Whisper word check; Meta superb judge (low passes: sad > 0.5).
import os, re, sys, time, subprocess, csv
T0 = time.time(); LOG = []; W = "/kaggle/working"; os.makedirs(f"{W}/takes", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
subprocess.run("pip install -q 'transformers==4.57.6' snac soundfile librosa jiwer", shell=True)
import numpy as np, soundfile as sf, librosa, torch, urllib.request, jiwer
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoFeatureExtractor, HubertForSequenceClassification, pipeline
dev = "cuda:0"; DT = torch.float16
RAW = "https://raw.githubusercontent.com/28thanujaya-hash/voice-training/main/"
SCENE = "Half the time it seems to me that Matthew can't be dead; and the other half it seems as if he must have been dead for a long time, and I've had this horrible dull ache ever since. The tears don't hurt me like that ache did. Oh, just let me cry."
src = urllib.request.urlopen(RAW + "kaggle/jobs/run29b_prefix/pilot.py").read().decode()
ns = {}; exec(src, ns); LINES = {i: ns["TXT"][(i, "P")] for i in ns["LINES"]["low"]}
urllib.request.urlretrieve(RAW + "results/run29b_prefix/scene_low.wav", "/tmp/scene.wav")
tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=DT).to(dev).eval()
from snac import SNAC
snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=DT, device=dev)
NAME = "superb/hubert-large-superb-er"; jfe = AutoFeatureExtractor.from_pretrained(NAME); jm = HubertForSequenceClassification.from_pretrained(NAME).eval().to(dev)
JL = [{"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}.get(jm.config.id2label[i], jm.config.id2label[i]) for i in range(len(jm.config.id2label))]
log("models loaded")
def to_audio(ids):
    if 128258 in ids: ids = ids[:ids.index(128258)]
    ids = [t for t in ids if t >= 128266]; ids = ids[: len(ids) // 7 * 7]; c = [t - 128266 for t in ids]
    l1, l2, l3 = [], [], []
    for i in range(len(c) // 7):
        l1.append(c[7*i]); l2.append(c[7*i+1] - 4096); l3 += [c[7*i+2] - 2*4096, c[7*i+3] - 3*4096]
        l2.append(c[7*i+4] - 4*4096); l3 += [c[7*i+5] - 5*4096, c[7*i+6] - 6*4096]
    if not l1 or min(l1 + l2 + l3) < 0 or max(l1 + l2 + l3) > 4095: return None
    with torch.inference_mode(): return snac.decode([torch.tensor(x, device=dev)[None] for x in (l1, l2, l3)]).squeeze().float().cpu().numpy()
def encode(y):
    with torch.inference_mode(): c = snac.encode(torch.tensor(y, device=dev, dtype=torch.float32)[None, None])
    l1, l2, l3 = [x[0].tolist() for x in c]; out = []
    for i in range(len(l1)):
        out += [l1[i] + 128266, l2[2*i] + 128266 + 4096, l3[4*i] + 128266 + 2*4096, l3[4*i+1] + 128266 + 3*4096,
                l2[2*i+1] + 128266 + 4*4096, l3[4*i+2] + 128266 + 5*4096, l3[4*i+3] + 128266 + 6*4096]
    return out
y, _ = librosa.load("/tmp/scene.wav", sr=24000); full = encode(y)
e = librosa.feature.rms(y=y, frame_length=1200, hop_length=600)[0]; last = np.where(20*np.log10(e + 1e-9) > -45)[0][-1]
trim = encode(y[: (last + 2) * 600]); log(f"scene: full {len(full)//7} frames, trimmed {len(trim)//7} frames")
def gen(line, codes, mn, mx, n):
    p = [128259] + tok(f"tara: {SCENE} {line}").input_ids + [128009, 128260, 128261, 128257] + codes
    ids = torch.tensor([p], device=dev)
    with torch.inference_mode():
        g = om.generate(ids, attention_mask=torch.ones_like(ids), min_new_tokens=mn, max_new_tokens=mx, do_sample=True, temperature=0.6, top_p=0.95,
                        repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
    return [x[len(p):].tolist() for x in g]
def norm(s): return re.sub(r"[^a-z' ]", " ", s.lower().replace("…", " ").replace("’", "'")).split()
def judge(a):
    z = librosa.effects.trim(librosa.resample(a, orig_sr=24000, target_sr=16000), top_db=35)[0]
    with torch.no_grad(): p = torch.softmax(jm(**jfe(z, sampling_rate=16000, return_tensors="pt").to(dev)).logits.float()[0], -1).tolist()
    return dict(zip(JL, p))
rows = []; firsts = []
for lid, line in LINES.items():
    t = gen(line, full, 0, 30, 1)[0]; firsts.append(f"| {lid} | {' '.join(map(str, t[:6]))} | {'yes' if t and t[0] == 128258 else 'no'} |")
    text = re.sub(r"<[^>]+>\s*", "", line)
    for arm, codes in (("B", full), ("C", trim)):
        outs = []
        for k in range(2): outs += gen(line, codes, 84, 900, 2)
        for k, ids in enumerate(outs):
            r = dict(id=lid, mood="low", var=arm, take=k, text=text, status="decode", sec="", heard="", judged="", p_sad="")
            rows.append(r); a = to_audio(ids)
            if a is None: continue
            o = asr(a.copy(), return_timestamps="word", generate_kwargs={"language": "en"}); ch = o.get("chunks") or []
            st = max(0.0, (ch[0]["timestamp"][0] or 0) - 0.05) if ch else 0.0; a = a[int(st * 24000):]
            r["heard"] = o["text"].strip(); r["sec"] = round(len(a) / 24000, 2)
            sf.write("/tmp/t.wav", a, 24000); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/t.wav", "-b:a", "96k", f"{W}/takes/{lid}_{arm}_{k}.mp3"])
            if jiwer.wer(" ".join(norm(text)), " ".join(norm(r["heard"])) or "x") > 0.0: r["status"] = "words"; continue
            j = judge(a); r["judged"] = max(j, key=j.get); r["p_sad"] = round(j["sad"], 3)
            r["status"] = "PASS" if r["judged"] == "sad" and j["sad"] > 0.5 else "fail"
    log(f"{lid} done")
with open(f"{W}/takes.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
rep = ["# run29c_fix · why run29b lost every take, and a fix", "", "## A: first tokens of run29b's exact prompt (128258 = end of speech)", "",
       "| line | first tokens | ends at once |", "|---|---|---|"] + firsts + ["", "## B (end blocked ~1 s) and C (B + scene silence cut): Meta superb, low passes at sad > 0.5", "",
       "| arm | takes | decoded | right words | PASS | lines with ≥1 PASS |", "|---|---|---|---|---|---|"]
for arm in "BC":
    R = [r for r in rows if r["var"] == arm]
    rep.append(f"| {arm} | {len(R)} | {sum(r['status'] != 'decode' for r in R)} | {sum(r['status'] in ('PASS', 'fail') for r in R)} | {sum(r['status'] == 'PASS' for r in R)} | {len({r['id'] for r in R if r['status'] == 'PASS'})}/{len(LINES)} |")
open(f"{W}/report.md", "w").write("\n".join(rep) + "\n\n## Log\n```\n" + "\n".join(LOG) + "\n```\n")
log("done")

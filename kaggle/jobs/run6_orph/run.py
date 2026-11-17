# Run 6 · Orpheus diagnostic: 12 sentences × 4 moods × 6 takes with the new lead-ins (diag.py), cut by CTC alignment,
# natural loudness. Gate: Whisper words exact, not clipped, 1-3 words 0.3-2.5 s, else 1.0-4.0 words/s (wide: the diagnostic
# wants to see the pace). Keeps every usable take; run6_pack measures them with the new measures and builds blind test 5.
import csv, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from diag import SENTS, MOODS, LEAD
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"
for d in (TMP, f"{W}/takes"): os.makedirs(d, exist_ok=True)
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 6 · Orpheus diagnostic (12 sentences × 4 moods, new lead-ins)", ""]
try:
    sh("pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe")
    import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
    import marks as MK
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    MK.setup(dev2)
    LINES = [(f"{sid}{m[0]}", m, sid, text, "diag") for sid, text in SENTS for m in MOODS]
    log(f"{len(LINES)} lines")
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev2)
    def to_audio(ids):
        ids = ids.tolist()
        if 128258 in ids: ids = ids[:ids.index(128258)]
        if 128257 in ids: ids = ids[len(ids) - ids[::-1].index(128257):]
        ids = [t for t in ids if t >= 128266]; ids = ids[: len(ids) // 7 * 7]; c = [t - 128266 for t in ids]
        l1, l2, l3 = [], [], []
        for i in range(len(c) // 7):
            l1.append(c[7*i]); l2.append(c[7*i+1] - 4096); l3 += [c[7*i+2] - 2*4096, c[7*i+3] - 3*4096]
            l2.append(c[7*i+4] - 4*4096); l3 += [c[7*i+5] - 5*4096, c[7*i+6] - 6*4096]
        if not l1 or min(l1 + l2 + l3) < 0 or max(l1 + l2 + l3) > 4095: return None
        with torch.inference_mode(): return snac.decode([torch.tensor(x, device=dev)[None] for x in (l1, l2, l3)]).squeeze().float().cpu().numpy()
    def record(texts, n, B=4):
        res = []
        for i in range(0, len(texts), B):
            tx = texts[i:i + B]
            prompts = [[128259] + tok(f"tara: {s}").input_ids + [128009, 128260] for s in tx]; L = max(map(len, prompts))
            ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = om.generate(ids, attention_mask=att, max_new_tokens=2000, do_sample=True, temperature=0.6, top_p=0.95,
                                repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
            outs = [to_audio(x[L:]) for x in g]; res += [outs[k * n:(k + 1) * n] for k in range(len(tx))]
        return res
    _wn = asr.tokenizer.normalize; SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        s = re.sub(r"(\d)-(?=\d)", r"\1", s); t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wn(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w)]
    def word_errors(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]; o = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in o.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad
    meter = pyloudnorm.Meter(24000); nw = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))
    def cut(a, lead, line):
        a16 = librosa.resample(a, orig_sr=24000, target_sr=16000)
        lw, _ = MK.parse(lead); xw, _ = MK.parse(line)
        if not xw: return None, "no words"
        al = MK.align(a16, lw + xw)
        if al is None: return None, "align"
        spans, T = al; e = spans[len(lw) - 1]; s = spans[len(lw)]
        if not e or not s or s[0] <= e[1] + 2: return None, "no gap"
        rms = librosa.feature.rms(y=a, frame_length=960, hop_length=480)[0]
        lo, hi = e[1] + 2, min(s[0], len(rms) - 1)
        if hi <= lo: return None, "no gap"
        k = lo + int(np.argmin(rms[lo:hi])); y, _ = librosa.effects.trim(a[k * 480:], top_db=40)
        return np.concatenate([np.zeros(2400), y, np.zeros(2400)]).astype(np.float32), "ok"
    def tilt(a):
        S_ = np.abs(librosa.stft(a, n_fft=1024, hop_length=256)) ** 2; f = librosa.fft_frequencies(sr=24000, n_fft=1024)
        return float(10 * np.log10(S_[f >= 1000].sum() / max(S_[f < 1000].sum(), 1e-9)))
    def loud(a):
        try: return float(meter.integrated_loudness(a)) if len(a) > 0.45 * 24000 else float(20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9) - 0.7)
        except Exception: return float("nan")
    import torchcrepe
    def contour(a):
        a16 = librosa.resample(a, orig_sr=24000, target_sr=16000)
        with torch.inference_mode():
            f0, per = torchcrepe.predict(torch.tensor(a16)[None].to(dev2), 16000, hop_length=320, fmin=70, fmax=600, model="tiny",
                                         return_periodicity=True, batch_size=2048, device=dev2)
        f0, per = f0[0].cpu().numpy(), per[0].cpu().numpy(); v = 12 * np.log2(np.maximum(f0[per > 0.45], 1) / 100)
        if len(v) < 6: return None
        n = len(v); return float(np.median(v[-max(3, n // 5):]) - np.median(v[:max(3, n // 5)]))
    def judge(a, mood, text):
        if a is None: return None, "decode"
        y, st = cut(a, LEAD[mood], text)
        if y is None: return None, st
        if np.abs(y).max() >= 0.99: return None, "clipped"
        dur = len(y) / 24000 - 0.2; n = nw(text)
        heard = asr(y.copy(), generate_kwargs={"language": "en"})["text"]
        if word_errors(text, heard): return None, "words"
        hi = 4.0
        if (n <= 3 and not 0.3 <= dur <= 2.5) or (n > 3 and not 1.0 <= n / dur <= hi): return None, "pace"
        try: m = MK.measure(y, text)
        except Exception: m = None
        if not m: return None, "measure"
        mv = contour(y)
        return dict(a=y, body=m["body"], rng=m["rng"], move=mv if mv is not None else 0.0, wps=n / dur, lufs=loud(y), tilt=tilt(y), heard=heard), "ok"
    T = {l[0]: [] for l in LINES}; why = {}
    def run_round(lines, n):
        t = time.time(); raw = record([f"{LEAD[l[1]]} {l[3]}" for l in lines], n)
        for l, takes in zip(lines, raw):
            for a in takes:
                x, st = judge(a, l[1], l[3])
                if x: T[l[0]].append(x)
                else: why[st] = why.get(st, 0) + 1
        log(f"round: {len(lines)} lines × {n} in {(time.time()-t)/60:.1f} min")
    run_round(LINES, 6)
    again = [l for l in LINES if len(T[l[0]]) < 3]
    if again: run_round(again, 6)
    rows_out = []
    for lid, mood, sid, text, _ in LINES:
        for k, x in enumerate(T[lid]):
            f = f"takes/{lid}_{k}.wav"; sf.write(f"{W}/{f}", x["a"], 24000)
            rows_out.append([lid, sid, mood, f, text, round(x["wps"], 2), round(x["lufs"], 1), x["heard"]])
    with open(f"{W}/takes.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["id", "sent", "row", "file", "text", "wps", "lufs", "heard"]); w.writerows(rows_out)
    report += [f"usable takes {len(rows_out)} · rejected {why}", "", "| mood | sentences with a take | takes |", "|---|---|---|"]
    for m in MOODS:
        report.append(f"| {m} | {sum(1 for l in LINES if l[1] == m and T[l[0]])}/12 | {sum(len(T[l[0]]) for l in LINES if l[1] == m)} |")
    report += ["", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

# Run 9 · low only: other ways than lead-ins (lead-ins dropped after run 8). Orpheus tara, the 12 run-8 low lines × 4 arms × 2 takes = 96:
#   C  plain line (control)          S  "<sigh>" before the line
#   A  the mentor-approved low take (run7_five low_01, text + its own audio codes) given as an earlier turn, then the line
#   AS A + S
# Everything before the line's first word (the sigh) is cut off by alignment, the same way in every arm. Then word check (Whisper),
# run-5 measures, quality checks and the low rules. Sigh arms also keep the uncut take (full/) for listening.
import csv, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from lines5 import build
from pilot import LINES as PL, REF, CTX, ARMS
T0 = time.time(); LOG = []; W = "/kaggle/working"
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 9 · low: approved low clip as context, <sigh>, control", ""]
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal", "batman"}
try:
    sh("pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    import marks as MK, meas as ME
    GPU = torch.cuda.is_available()   # 18 Nov: also runs on Kaggle CPU (GPU quota used up): float32, time guard below
    dev = "cuda:0" if GPU else "cpu"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    DT = torch.float16 if GPU else torch.float32; STOP_H = 10.5   # Kaggle sessions end at 12 h: stop recording in time to write the report
    log(f"device {dev}/{dev2}, {torch.get_num_threads()} CPU threads" if not GPU else f"device {dev}/{dev2}")
    MK.setup(dev2)
    L = {l[0]: l for l in build()}
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=DT).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=DT, device=dev2)
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
    def encode(path):   # audio -> Orpheus audio tokens (7 per SNAC frame, same layout to_audio reads back)
        y, _ = librosa.load(path, sr=24000)
        with torch.inference_mode(): c = snac.encode(torch.tensor(y, device=dev, dtype=torch.float32)[None, None])
        l1, l2, l3 = [x[0].tolist() for x in c]; out = []
        for i in range(len(l1)):
            out += [l1[i] + 128266, l2[2*i] + 128266 + 4096, l3[4*i] + 128266 + 2*4096, l3[4*i+1] + 128266 + 3*4096,
                    l2[2*i+1] + 128266 + 4*4096, l3[4*i+2] + 128266 + 5*4096, l3[4*i+3] + 128266 + 6*4096]
        return out
    CTX_IDS = None
    def turn(text): return [128259] + tok(f"tara: {text}").input_ids + [128009, 128260]
    def record(texts, n, B=4, ctx=False):
        res = []
        for i in range(0, len(texts), B):
            tx = texts[i:i + B]
            pre = CTX_IDS if ctx else []
            prompts = [pre + turn(s) for s in tx]; Lm = max(map(len, prompts))
            ids = torch.tensor([[128263] * (Lm - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (Lm - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = om.generate(ids, attention_mask=att, max_new_tokens=2000, do_sample=True, temperature=0.6, top_p=0.95,
                                repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
            outs = [to_audio(x[Lm:]) for x in g]; res += [outs[k * n:(k + 1) * n] for k in range(len(tx))]
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
    def cut(a, line):   # drop everything before the line's first word (a sigh, a breath), at the quietest frame just before it
        a16 = librosa.resample(a, orig_sr=24000, target_sr=16000)
        xw, _ = MK.parse(line)
        if not xw: return None, "no words"
        al = MK.align(a16, xw)
        if al is None: return None, "align"
        spans, T = al; s = spans[0]
        if not s: return None, "align"
        rms = librosa.feature.rms(y=a, frame_length=960, hop_length=480)[0]
        lo, hi = max(0, s[0] - 25), min(s[0], len(rms) - 1)
        k = lo + int(np.argmin(rms[lo:hi])) if hi > lo else 0; y, _ = librosa.effects.trim(a[k * 480:], top_db=40)
        return np.concatenate([np.zeros(2400), y, np.zeros(2400)]).astype(np.float32), "ok"
    os.makedirs(f"{W}/takes", exist_ok=True); os.makedirs(f"{W}/pass", exist_ok=True); os.makedirs(f"{W}/full", exist_ok=True)
    CTX_IDS = turn(CTX["text"]) + [128261, 128257] + encode(CTX["file"]) + [128258, 128262]; log(f"context: {len(CTX_IDS)} tokens")
    rows = []
    mood = "low"; ids = PL
    for var, arm in ARMS.items():
            if time.time() - T0 > STOP_H * 3600: log(f"time guard: {var} not recorded"); continue
            texts = [L[i][3] for i in ids]
            raw = record([("<sigh> " if arm["sigh"] else "") + t for t in texts], 2, ctx=arm["ctx"]); log(f"recorded {var}")
            for i, takes in zip(ids, raw):
                text = L[i][3]
                for k, a in enumerate(takes):
                    r = dict(id=i, mood=mood, var=var, take=k, text=text, status="", fails="", heard="")
                    rows.append(r)
                    if a is None: r["status"] = "decode"; continue
                    if arm["sigh"]:   # uncut take, sigh included, as mp3 for listening
                        sf.write("/tmp/full.wav", a, 24000); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/full.wav", "-b:a", "96k", f"{W}/full/{i}_{var}_{k}.mp3"])
                    y, st = cut(a, text)
                    if y is None: r["status"] = st; continue
                    if np.abs(y).max() >= 0.99: r["status"] = "clipped"; continue
                    r["heard"] = asr(y.copy(), generate_kwargs={"language": "en"})["text"].strip()
                    if word_errors(text, r["heard"]): r["status"] = "words"; continue
                    try:
                        y2, q = ME.quality(y); d = ME.measure(y, text); f, sp = ME.rules(d, q, REF, mood)
                    except Exception as e: r["status"] = f"measure: {e}"[:80]; continue
                    r.update({k2: round(float(v), 3) for k2, v in {**d, **q}.items()}); r["speed_pct"] = round(sp, 1)
                    for k2 in ("lufs", "f0_med", "f0_sd", "h1h2", "slope", "int_drop", "final_drop"):
                        if k2 in d: r["d_" + k2] = round(float(d[k2] - REF[k2]), 2)
                    r["fails"] = "; ".join(f); r["status"] = "PASS" if not f else "fail"
                    nm = f"{i}_{var}_{k}"
                    sf.write(f"{W}/takes/{nm}.wav", y2, 24000)
                    if not f: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/takes/{nm}.wav", "-b:a", "128k", f"{W}/pass/{mood}_{nm}.mp3"])
    log(f"{len(rows)} takes done")
    cols = ["id", "mood", "var", "take", "text", "status", "fails", "speed_pct", "d_lufs", "d_f0_med", "d_f0_sd", "d_h1h2", "d_slope", "d_int_drop",
            "d_final_drop", "gap", "hold", "hiss", "syl", "dur", "heard"]
    with open(f"{W}/takes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in rows]
    from collections import Counter
    report += ["Arms: C = plain line; S = \"<sigh>\" before the line; A = approved low take \"" + CTX["text"] + "\" (run7_five low_01) given as an earlier turn; AS = A + S.",
               "Everything before the line's first word is cut off in every arm.", "",
               "## Pass rate (all low rules + quality checks; a take counts only if its words are right)", "",
               "| arm | takes | words OK | PASS | lines with ≥1 PASS |", "|---|---|---|---|---|"]
    for var in ARMS:
        s_ = [r for r in rows if r["var"] == var]; ok = [r for r in s_ if r["status"] in ("PASS", "fail")]; p = [r for r in s_ if r["status"] == "PASS"]
        report.append(f"| {var} | {len(s_)} | {len(ok)} | {len(p)} | {len({r['id'] for r in p})}/12 |")
    report += ["", "## Which rules fail most (takes with right words that failed)", "", "| arm | rule: times failed |", "|---|---|"]
    for var in ARMS:
        c = Counter(x for r in rows if r["var"] == var and r["status"] == "fail" for x in r["fails"].split("; "))
        report.append(f"| {var} | " + ", ".join(f"{k}: {v}" for k, v in c.most_common()) + " |")
    report += ["", "## Medians of right-word takes (vs normal). Low needs speed −15 to −40 %, loudness ≤ −2 dB, breathiness ≥ +3 dB", "",
               "| arm | speed % | loudness dB | pitch st | movement | breathiness dB | end loudness dB | gap s | slow+quiet+breathy (all 3) |", "|---|---|---|---|---|---|---|---|---|"]
    for var in ARMS:
        s_ = [r for r in rows if r["var"] == var and r["status"] in ("PASS", "fail")]
        md = lambda k: np.nanmedian([r.get(k, np.nan) for r in s_]) if s_ else np.nan
        three = sum(1 for r in s_ if r.get("speed_pct", 0) <= -15 and r.get("d_lufs", 0) <= -2 and r.get("d_h1h2", 0) >= 3)
        report.append(f"| {var} | {md('speed_pct'):+.0f} | {md('d_lufs'):+.1f} | {md('d_f0_med'):+.1f} | {md('d_f0_sd'):+.1f} | {md('d_h1h2'):+.1f} | {md('d_int_drop'):+.1f} | {md('gap'):.2f} | {three}/{len(s_)} |")
    other = Counter(r["status"] for r in rows if r["status"] not in ("PASS", "fail"))
    report += ["", "Lost before measuring: " + (", ".join(f"{k} {v}" for k, v in other.most_common()) or "none")]
except Exception:
    report += ["", "## ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report))

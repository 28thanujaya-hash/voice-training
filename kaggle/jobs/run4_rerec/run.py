# Run 4 · step B: re-record pilot for the weak moods (mentor's blind test, 16 Nov: only bright is clear; low heard in 3/9,
# tense sometimes sounds like normal or low). Orpheus tara with a mood-setting lead-in that is cut off afterwards.
#  - the 35 same-line group lines (all 4 moods, same words as the first blind test) + 21 low + 22 tense training lines
#  - 6 takes per line; cut with CTC forced alignment (wav2vec2) at the quietest point between the lead-in and the line
#  - natural loudness kept (no levelling); clipped takes rejected
#  - checks: Whisper hears exactly the line (no lead-in words left), pace / length rules as in Gate 1 v2
#  - choose per line the take that measures most clearly in its mood (z-scores within the line's takes):
#      low  : lower pitch, slower, quieter, darker (less energy above 1 kHz)
#      tense: louder, brighter (more energy above 1 kHz), a little faster
#      bright: higher pitch, wider range · normal: the most central take
#  - blind pack 2: the 35 group lines, new takes, shuffled; key separate (compare with blind test 1)
import csv, glob, os, random, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"
for d in (TMP, f"{W}/new", f"{W}/blind2"): os.makedirs(d, exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]; TAKES = 6
LEAD = {"normal": "Okay, so here is the plan.", "bright": "Oh wow, this is the best news ever!",
        "low": "I feel so sad and lonely today…", "tense": "I am really angry about this. Listen to me."}
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 4 · step B: re-record pilot (low + tense), lead-in cut by forced alignment, natural loudness", ""]
try:
    sh("pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe")
    import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
    import marks as MK
    MK.setup("cuda:1" if torch.cuda.device_count() > 1 else "cuda:0")
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)[0]; src = os.path.dirname(tr); rows = list(csv.DictReader(open(tr)))
    random.seed(7)
    groups = [r for r in rows if r.get("group")]
    nw = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))
    extra = []
    for mood, n in (("low", 21), ("tense", 22)):
        c = [r for r in rows if r["row"] == mood and not r.get("group") and r["split"] == "train" and 4 <= nw(r["text"]) <= 10 and not re.search(r"\d", r["text"])]
        extra += random.sample(c, n)
    LINES = [(r["id"], r["row"], r["text"], r.get("group", ""), r["file"]) for r in groups + extra]
    log(f"{len(LINES)} lines: {len(groups)} group lines + {len(extra)} extra")
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
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
    def record(texts, n, B=8):
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
    t = time.time(); RAW = record([f"{LEAD[m]} {txt}" for _, m, txt, _, _ in LINES], TAKES)
    log(f"recorded {len(LINES)} × {TAKES} in {(time.time()-t)/60:.1f} min"); del om; torch.cuda.empty_cache()
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev)
    _wn = asr.tokenizer.normalize; SPELL = {"mum": "mom", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        return [SPELL.get(w, w) for w in _wn(s).split() if re.search(r"[a-z0-9]", w)]
    def word_errors(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]; o = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in o.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad
    meter = pyloudnorm.Meter(24000)
    def cut(a, lead, line):
        a16 = librosa.resample(a, orig_sr=24000, target_sr=16000)
        lw, _ = MK.parse(lead); xw, _ = MK.parse(line)
        al = MK.align(a16, lw + xw)
        if al is None: return None, "align"
        spans, T = al; e = spans[len(lw) - 1]; s = spans[len(lw)]
        if not e or not s or s[0] <= e[1] + 2: return None, "no gap"
        rms = librosa.feature.rms(y=a, frame_length=960, hop_length=480)[0]   # 20 ms frames at 24 kHz
        lo, hi = e[1] + 2, min(s[0], len(rms) - 1)
        if hi <= lo: return None, "no gap"
        k = lo + int(np.argmin(rms[lo:hi])); y = a[k * 480:]
        y, _ = librosa.effects.trim(y, top_db=40); return np.concatenate([np.zeros(2400), y, np.zeros(2400)]).astype(np.float32), "ok"
    def tilt(a):
        S_ = np.abs(librosa.stft(a, n_fft=1024, hop_length=256)) ** 2; f = librosa.fft_frequencies(sr=24000, n_fft=1024)
        return float(10 * np.log10(S_[f >= 1000].sum() / max(S_[f < 1000].sum(), 1e-9)))
    def loud(a):
        try: return float(meter.integrated_loudness(a)) if len(a) > 0.45 * 24000 else float(20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9) - 0.7)
        except Exception: return float("nan")
    J = []; why = {}
    for (lid, mood, text, grp, oldf), takes in zip(LINES, RAW):
        for k, a in enumerate(takes):
            if a is None: why["decode"] = why.get("decode", 0) + 1; continue
            y, st = cut(a, LEAD[mood], text)
            if y is None: why[st] = why.get(st, 0) + 1; continue
            if np.abs(y).max() >= 0.99: why["clipped"] = why.get("clipped", 0) + 1; continue
            heard = asr(y.copy(), generate_kwargs={"language": "en"})["text"]; dur = len(y) / 24000 - 0.2; n = nw(text)
            bad = word_errors(text, heard)
            ok = bad == 0 and ((0.3 <= dur <= 2.5) if n <= 3 else (1.0 <= n / dur <= 3.2))
            if not ok: why["words/pace"] = why.get("words/pace", 0) + 1; continue
            try: m = MK.measure(y, text)
            except Exception: m = None
            if not m: why["measure"] = why.get("measure", 0) + 1; continue
            J.append(dict(id=lid, mood=mood, text=text, group=grp, take=k + 1, a=y, body=m["body"], rng=m["rng"], wps=n / dur, lufs=loud(y), tilt=tilt(y), heard=heard))
    log(f"{len(J)} usable takes; rejected: {why}")
    # old takes of the same lines, same measures (old were levelled to -20 LUFS, so loudness isn't comparable)
    OLD = {}
    for lid, mood, text, grp, oldf in LINES:
        a = sf.read(f"{src}/{oldf}", dtype="float32")[0]
        try: m = MK.measure(a, text)
        except Exception: m = None
        if m: OLD[lid] = dict(body=m["body"], rng=m["rng"], wps=nw(text) / max(len(a) / 24000 - 0.2, .1), tilt=tilt(a))
    best = {}
    for lid, mood, text, grp, oldf in LINES:
        tk = [x for x in J if x["id"] == lid]
        if not tk: continue
        def z(k): v = np.array([x[k] for x in tk]); return (v - v.mean()) / (v.std() + 1e-6)
        if mood == "low": sc = -z("body") - z("wps") - z("lufs") - z("tilt")
        elif mood == "tense": sc = z("lufs") + z("tilt") + 0.5 * z("wps")
        elif mood == "bright": sc = z("body") + z("rng")
        else: sc = -(np.abs(z("body")) + np.abs(z("rng")) + np.abs(z("wps")))
        best[lid] = tk[int(np.argmax(sc))]
    with open(f"{W}/new_takes.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["id", "row", "group", "take", "file", "text", "pitch", "range", "pace", "lufs", "tilt"])
        for lid, x in best.items():
            f = f"new/{lid}_lead_t{x['take']}.wav"; sf.write(f"{W}/{f}", x["a"], 24000)
            w.writerow([lid, x["mood"], x["group"], x["take"], f, x["text"], round(x["body"], 2), round(x["rng"], 2), round(x["wps"], 2), round(x["lufs"], 1), round(x["tilt"], 1)])
    med = lambda xs, k: float(np.nanmedian([x[k] for x in xs])) if xs else float("nan")
    report += [f"Lines {len(LINES)} · takes {len(LINES) * TAKES} · usable {len(J)} · lines with a kept take {len(best)} · rejected: {why}", "",
               "## Chosen new takes vs the old takes of the same lines (median)", "",
               "| mood | lines | pitch old → new | range old → new | pace old → new | tilt dB old → new | loudness new (LUFS) |", "|---|---|---|---|---|---|---|"]
    for mood in ROWS:
        nx = [best[l[0]] for l in LINES if l[1] == mood and l[0] in best]; ox = [OLD[l[0]] for l in LINES if l[1] == mood and l[0] in OLD and l[0] in best]
        report.append(f"| {mood} | {len(nx)} | {med(ox,'body'):.1f} → {med(nx,'body'):.1f} | {med(ox,'rng'):.1f} → {med(nx,'rng'):.1f} | {med(ox,'wps'):.2f} → {med(nx,'wps'):.2f} | {med(ox,'tilt'):.1f} → {med(nx,'tilt'):.1f} | {med(nx,'lufs'):.1f} |")
    report += ["", "(Old takes were levelled to −20 LUFS; new takes keep their natural loudness.)", ""]
    # blind pack 2: the group lines
    items = [best[r["id"]] for r in groups if r["id"] in best]; random.seed(29); random.shuffle(items)
    key = ["# Blind actor test 2: key (read AFTER listening)", "", "| clip | group | mood | text |", "|---|---|---|---|"]
    sheet = ["# Blind actor test 2: tick sheet", "", "New recordings (lead-in cut off, natural loudness). Same sentences as test 1. Which mood do you hear?", "",
             "| clip | normal | bright | low | tense |", "|---|---|---|---|---|"]
    for i, x in enumerate(items, 1):
        sf.write(f"{TMP}/c.wav", x["a"], 24000); sh(f"ffmpeg -loglevel error -y -i {TMP}/c.wav -b:a 64k {W}/blind2/actor_blind2_{i:02d}.mp3")
        key.append(f"| {i:02d} | {x['group']} | {x['mood']} | {x['text']} |"); sheet.append(f"| {i:02d} | ☐ | ☐ | ☐ | ☐ |")
    open(f"{W}/blind2_key.md", "w").write("\n".join(key) + "\n"); open(f"{W}/blind2_sheet.md", "w").write("\n".join(sheet) + "\n")
    report += [f"Blind pack 2: {len(items)} clips (blind2/, blind2_sheet.md, blind2_key.md)", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

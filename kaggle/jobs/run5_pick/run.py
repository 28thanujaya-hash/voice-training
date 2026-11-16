# Run 5 · pick: choose one take per line across moods (mentor's rules, 16 Nov), re-record lines that fail, build the training
# list, audits and blind pack 3.
# Rules (all kept from before; clip 14 is added as the minimum for low):
#   low    : clip-14 standard vs Maya's normal — pitch ≤ normal −1.5 st, range ≤ 4.5 st, start→end movement within ±2 st,
#            pace ≤ 2.2 words/s, loudness ≤ normal −3 LU (flat, slow, quiet)
#   normal : calm — pace ≤ 2.8, range ≤ normal median +1, pitch and loudness between low and bright/tense
#   tense  : louder than normal (≥ +1 LU) but lower in pitch than bright (≤ bright median −1 st) and range ≤ bright median (firm, not excited)
#   bright : higher than normal (≥ +1 st) and louder than normal (≥ +1 LU)
#   groups : order rule per sentence — pitch low < normal < bright and normal ≤ tense; loudness low < normal < tense and bright;
#            range normal ≤ bright and tense. Best combination of the kept takes.
# Lines with no take meeting their mood's rule get up to 2 rounds × 6 new takes (lead-ins as before); still failing = reported.
import csv, glob, itertools, os, random, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from lines5 import build, LEAD
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"
for d in (TMP, f"{W}/final", f"{W}/blind3"): os.makedirs(d, exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 5 · pick: one take per line, mentor's mood rules, retakes, blind pack 3", ""]
try:
    sh("pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe")
    import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
    import marks as MK
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    MK.setup(dev2)
    LINES = {l[0]: l for l in build()}
    C = {}
    for f in glob.glob("/kaggle/input/**/takes.csv", recursive=True):
        base = os.path.dirname(f)
        for r in csv.DictReader(open(f)):
            for k in ("pitch", "range", "move", "pace", "lufs", "tilt", "score"): r[k] = float(r[k])
            r["path"] = f"{base}/{r['file']}"; C.setdefault(r["id"], []).append(r)
    log(f"takes for {len(C)} of {len(LINES)} lines")
    med = lambda xs: float(np.nanmedian(xs)) if len(xs) else float("nan")
    first = lambda m: [C[i][0] for i in C if LINES[i][1] == m]
    N_P, N_L, N_R = med([r["pitch"] for r in first("normal")]), med([r["lufs"] for r in first("normal")]), med([r["range"] for r in first("normal")])
    B_P, B_R = med([r["pitch"] for r in first("bright")]), med([r["range"] for r in first("bright")])
    report += [f"Reference (best takes): normal pitch {N_P:.1f} st, loudness {N_L:.1f} LUFS, range {N_R:.1f}; bright pitch {B_P:.1f}, range {B_R:.1f}", ""]
    def ok(r, mood):
        if mood == "low": return r["pitch"] <= N_P - 1.5 and r["range"] <= 4.5 and abs(r["move"]) <= 2 and r["pace"] <= 2.2 and r["lufs"] <= N_L - 3
        if mood == "normal": return r["pace"] <= 2.8 and r["range"] <= N_R + 1
        if mood == "tense": return r["lufs"] >= N_L + 1 and r["pitch"] <= B_P - 1 and r["range"] <= B_R
        return r["pitch"] >= N_P + 1 and r["lufs"] >= N_L + 1
    def why_not(r, mood):
        w = []
        if mood == "low":
            if r["pitch"] > N_P - 1.5: w.append("pitch")
            if r["range"] > 4.5: w.append("range")
            if abs(r["move"]) > 2: w.append("movement")
            if r["pace"] > 2.2: w.append("pace")
            if r["lufs"] > N_L - 3: w.append("loud")
        elif mood == "normal":
            if r["pace"] > 2.8: w.append("pace")
            if r["range"] > N_R + 1: w.append("range")
        elif mood == "tense":
            if r["lufs"] < N_L + 1: w.append("not loud")
            if r["pitch"] > B_P - 1: w.append("too high")
            if r["range"] > B_R: w.append("range")
        else:
            if r["pitch"] < N_P + 1: w.append("not high")
            if r["lufs"] < N_L + 1: w.append("not loud")
        return w
    need = [i for i in LINES if not any(ok(r, LINES[i][1]) for r in C.get(i, []))]
    report += [f"Lines with no take meeting the mood rule before retakes: {len(need)} (" + ", ".join(f"{m} {sum(1 for i in need if LINES[i][1] == m)}" for m in ROWS) + ")", ""]
    # ---- retakes
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
    def record(texts, n, B=8):
        res = []
        for i in range(0, len(texts), B):
            tx = texts[i:i + B]
            prompts = [[128259] + tok(f"tara: {s}").input_ids + [128009, 128260] for s in tx]; L = max(map(len, prompts))
            ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = om.generate(ids, attention_mask=att, max_new_tokens=2400, do_sample=True, temperature=0.6, top_p=0.95,
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
        hi = 2.6 if mood == "low" else 3.0
        if (n <= 3 and not 0.3 <= dur <= 2.5) or (n > 3 and not 1.0 <= n / dur <= hi): return None, "pace"
        try: m = MK.measure(y, text)
        except Exception: m = None
        if not m: return None, "measure"
        mv = contour(y)
        return dict(a=y, body=m["body"], rng=m["rng"], move=mv if mv is not None else 0.0, wps=n / dur, lufs=loud(y), tilt=tilt(y), heard=heard), "ok"
    os.makedirs(f"{W}/retakes", exist_ok=True); why = {}
    for rnd in (1, 2):
        if not need: break
        t = time.time(); lines = [LINES[i] for i in need]
        raw = record([f"{LEAD[l[1]]} {l[3]}" for l in lines], 6)
        for l, takes in zip(lines, raw):
            for k, a in enumerate(takes):
                x, st = judge(a, l[1], l[3])
                if not x: why[st] = why.get(st, 0) + 1; continue
                f = f"retakes/{l[0]}_x{rnd}{k}.wav"; sf.write(f"{W}/{f}", x["a"], 24000)
                C.setdefault(l[0], []).append(dict(id=l[0], row=l[1], group=l[2], split=l[4], file=f, path=f"{W}/{f}", text=l[3],
                                                    pitch=x["body"], range=x["rng"], move=x["move"], pace=x["wps"], lufs=x["lufs"], tilt=x["tilt"], score=0.0))
        need = [i for i in need if not any(ok(r, LINES[i][1]) for r in C.get(i, []))]
        log(f"retake round {rnd}: {len(lines)} lines × 6 in {(time.time()-t)/60:.1f} min; still failing {len(need)}; rejects {why}")
    del om; torch.cuda.empty_cache()
    # ---- choose: rule-passing takes first; groups by the order rule
    def cands(i):
        tk = C.get(i, []); p = [r for r in tk if ok(r, LINES[i][1])]
        return p or tk
    chosen = {}
    for i in LINES:
        cs = cands(i)
        if cs: chosen[i] = max(cs, key=lambda r: r["score"])
    G = {}
    for i, l in LINES.items():
        if l[2]: G.setdefault(l[2], {})[l[1]] = i
    def order_ok(sel):
        g = {m: sel[m] for m in sel}; bad = 0
        P = lambda m: g[m]["pitch"]; Lz = lambda m: g[m]["lufs"]; R = lambda m: g[m]["range"]
        def chk(c):
            nonlocal bad
            if not c: bad += 1
        if "low" in g and "normal" in g: chk(P("low") < P("normal")); chk(Lz("low") < Lz("normal"))
        if "normal" in g and "bright" in g: chk(P("normal") < P("bright")); chk(Lz("normal") < Lz("bright")); chk(R("normal") <= R("bright"))
        if "normal" in g and "tense" in g: chk(P("normal") <= P("tense")); chk(Lz("normal") < Lz("tense")); chk(R("normal") <= R("tense"))
        if "tense" in g and "bright" in g: chk(P("tense") < P("bright"))
        return bad
    gstats = []
    for gname, mem in sorted(G.items(), key=lambda x: int(x[0][1:])):
        moods = [m for m in ROWS if m in mem and cands(mem[m])]
        opts = [sorted(cands(mem[m]), key=lambda r: -r["score"])[:4] for m in moods]
        best, bb = None, 99
        for combo in itertools.product(*opts):
            b = order_ok(dict(zip(moods, combo)))
            if b < bb or (b == bb and best is not None and sum(r["score"] for r in combo) > sum(r["score"] for r in best)): best, bb = combo, b
        if best:
            for m, r in zip(moods, best): chosen[mem[m]] = r
        gstats.append((gname, len(moods), bb))
    # ---- outputs
    with open(f"{W}/train.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "row", "text_b", "text", "split", "id", "group", "meets_rule"])
        for i, r in sorted(chosen.items()):
            dst = f"final/{i}.wav"; shutil.copy(r["path"], f"{W}/{dst}"); l = LINES[i]
            w.writerow([dst, l[1], l[3], l[3], l[4], i, l[2], ok(r, l[1])])
    report += [f"Lines with a chosen take: {len(chosen)} of {len(LINES)} · meeting their mood rule: {sum(1 for i, r in chosen.items() if ok(r, LINES[i][1]))}", "",
               "## Per mood (chosen takes, median)", "", "| mood | lines | meet rule | pitch | range | movement | pace | loudness | tilt |", "|---|---|---|---|---|---|---|---|---|"]
    for m in ROWS:
        xs = [r for i, r in chosen.items() if LINES[i][1] == m]
        if xs: report.append(f"| {m} | {len(xs)} | {sum(1 for i, r in chosen.items() if LINES[i][1] == m and ok(r, m))} | " +
                             " | ".join(f"{med([r[k] for r in xs]):.2f}" for k in ("pitch", "range", "move", "pace", "lufs", "tilt")) + " |")
    report += ["", "## Same-line groups: order-rule breaks (0 = all of low < normal < bright/tense, loudness and flatness hold)", "",
               ", ".join(f"{g} ({n} moods): {b}" for g, n, b in gstats), ""]
    fails = [(i, LINES[i][1], LINES[i][3], why_not(min(C[i], key=lambda r: len(why_not(r, LINES[i][1]))), LINES[i][1]) if C.get(i) else ["no usable take"])
             for i in LINES if i not in chosen or not ok(chosen[i], LINES[i][1])]
    report += ["## Lines not meeting their mood rule (kept with their closest take, or missing)", ""] + [f"- {i} ({m}): {t} — {', '.join(w)}" for i, m, t, w in fails[:150]] + [""]
    # ---- blind pack 3: groups G1–G20
    items = [(g, m, chosen[i]) for g, mem in G.items() for m, i in mem.items() if i in chosen]
    random.seed(33); random.shuffle(items)
    key = ["# Blind test 3: key (read AFTER listening)", "", "| clip | group | mood | text |", "|---|---|---|---|"]
    sheet = ["# Blind test 3: tick sheet", "", "Same sentence in different moods (new recordings, natural loudness). Which mood do you hear?", "",
             "| clip | normal | bright | low | tense |", "|---|---|---|---|---|"]
    for n, (g, m, r) in enumerate(items, 1):
        sh(f"ffmpeg -loglevel error -y -i {W}/final/{r['id']}.wav -b:a 64k {W}/blind3/actor_blind3_{n:02d}.mp3")
        key.append(f"| {n:02d} | {g} | {m} | {LINES[r['id']][3]} |"); sheet.append(f"| {n:02d} | ☐ | ☐ | ☐ | ☐ |")
    open(f"{W}/blind3_key.md", "w").write("\n".join(key) + "\n"); open(f"{W}/blind3_sheet.md", "w").write("\n".join(sheet) + "\n")
    report += [f"Blind pack 3: {len(items)} clips", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

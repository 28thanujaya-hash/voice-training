# Run 4 · actor audit (mentor 15 Nov 12:55: "listen to the actor yourself first, for all categories, all 4 rows").
# Every take from run4_record is measured mark by mark, in every mood:
#   yes/no "?" -> pitch at the end of the word rises vs the sentence (≥ +1 st); "?!" ≥ +2 st; wh-questions reported only;
#   "…" mid-line -> silence ≥ 0.30 s; "…" at the end -> last word drawn out (≥ 1.2×) or fading (≥ 3 dB quieter);
#   "—" -> silence ≥ 0.15 s; "," -> silence ≥ 0.10 s (reported only); "!" -> livelier than the same mood's plain lines
#   (pitch range +1 st or pitch level +1 st); CAPS -> the word is higher (+1.5 st) or louder (+3 dB) than the other words.
# Word positions: CTC forced alignment (wav2vec2-large-960h), pauses from the waveform; pitch: torchcrepe.
# Then: per line, the Gate-1-passing take that shows the most marks is kept; lines where no take shows the marks are
# recorded again (2 takes × up to 3 rounds), judged by Gate 1 v2 + the mark checks. Outputs: final clips + train.csv,
# a table per mark × mood (before / after), mood measures, and named listening clips (one good + one failing per cell).
import csv, glob, os, re, shutil, subprocess, sys, time, traceback, unicodedata, random
sys.path.insert(0, os.getcwd())
T0 = time.time(); LOG = []; OUT = "/kaggle/working"
for d in ("final", "new", "listen"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
ROWS = ["normal", "bright", "low", "tense"]
KINDS = ["q", "qx", "ex", "dots", "dash", "caps", "q_wh", "comma"]
REQ = {"q", "qx", "ex", "dots", "dash", "caps"}
KNAME = {"q": "? (yes/no)", "qx": "?!", "ex": "!", "dots": "…", "dash": "—", "caps": "CAPS", "q_wh": "? (wh, report only)", "comma": ", (report only)"}
WH = {"what", "where", "when", "why", "who", "whom", "whose", "which", "how"}
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
report = ["# Run 4 · actor audit: every mark in every mood (Orpheus tara)", ""]
try:
    sh("pip install -q snac jiwer pyloudnorm soundfile librosa torchcrepe scikit-learn")
    import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm, torchcrepe
    from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    man = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)[0]; base = os.path.dirname(man)
    takes = list(csv.DictReader(open(man))); log(f"{len(takes)} takes from {base}")
    proc = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
    ctc = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self").to(dev2).eval()
    VOC = proc.tokenizer.get_vocab(); BLANK = VOC[proc.tokenizer.pad_token]; SEP = VOC["|"]
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev2)
    meter = pyloudnorm.Meter(24000)

    # ---------- text -> words + marks
    def clean(w): return re.sub(r"[^A-Z']", "", unicodedata.normalize("NFKD", w).encode("ascii", "ignore").decode().upper())
    def parse(text):
        """align-words (clean, for CTC) and mark instances: (kind, index of the word the mark belongs to)."""
        toks = text.split(); aw = []; last = []; marks = []; clause_start = 0
        for ti, t in enumerate(toks):
            parts = [clean(p) for p in re.split(r"[-–]", t)]; parts = [p for p in parts if p]
            if parts:
                if not aw or (ti and re.search(r"[.!?…]$", toks[ti - 1].rstrip("\"”'"))): clause_start = len(aw)
                aw += parts; last.append(len(aw) - 1)
                letters = re.sub(r"[^A-Za-z]", "", t)
                if len(letters) >= 2 and letters.isupper(): marks.append(("caps", len(aw) - 1, clause_start))
            else: last.append(len(aw) - 1)
            idx = len(aw) - 1
            if idx < 0: continue
            tail = re.sub(r"[\"”'’)]+$", "", t)
            if t.strip() in ("—", "–") or tail.endswith("—"): marks.append(("dash", idx, clause_start))
            elif tail.endswith("?!"): marks.append(("qx", idx, clause_start))
            elif tail.endswith("?"): marks.append(("q_wh" if any(w.lower() in WH for w in aw[clause_start:clause_start + 2]) else "q", idx, clause_start))
            elif tail.endswith("!"): marks.append(("ex", idx, clause_start))
            elif tail.endswith("…") or tail.endswith("..."): marks.append(("dots", idx, clause_start))
            elif tail.endswith(","): marks.append(("comma", idx, clause_start))
        return aw, marks

    def align(a16, words):
        tokens = [SEP]
        for w in words: tokens += [VOC[c] for c in w if c in VOC] + [SEP]
        with torch.inference_mode():
            x = proc(a16, sampling_rate=16000, return_tensors="pt").input_values.to(dev2)
            em = torch.log_softmax(ctc(x).logits[0].float(), -1).cpu()
        T, N = em.size(0), len(tokens)
        if T < N: return None
        tr = torch.zeros((T, N)); tr[1:, 0] = torch.cumsum(em[1:, BLANK], 0); tr[0, 1:] = -float("inf"); tr[-N + 1:, 0] = float("inf")
        tk = torch.tensor(tokens)
        for t in range(T - 1):
            tr[t + 1, 1:] = torch.maximum(tr[t, 1:] + em[t, BLANK], tr[t, :-1] + em[t, tk[1:]])
        t, j = T - 1, N - 1; path = [(j, t)]
        while j > 0 and t > 0:
            st_ = tr[t - 1, j] + em[t - 1, BLANK]; ch = tr[t - 1, j - 1] + em[t - 1, tk[j]]; t -= 1
            if ch > st_: j -= 1
            path.append((j, t))
        first = {}
        for j, t in path: first[j] = min(t, first.get(j, 10**9))
        # word w: first letter's first frame .. last letter's first frame
        spans, j = [], 1
        for w in words:
            n = sum(1 for c in w if c in VOC)
            if n == 0: spans.append(None); j += 1; continue
            spans.append((first.get(j, 0), first.get(j + n - 1, 0))); j += n + 1
        return spans, T

    def frames(a16, T):
        with torch.inference_mode():
            f0, per = torchcrepe.predict(torch.tensor(a16)[None].to(dev2), 16000, hop_length=320, fmin=70, fmax=600, model="tiny",
                                         return_periodicity=True, batch_size=2048, device=dev2)
        f0, per = f0[0].cpu().numpy(), per[0].cpu().numpy()
        rms = librosa.feature.rms(y=a16, frame_length=640, hop_length=320, center=True)[0]; db = 20 * np.log10(rms + 1e-6)
        n = min(T, len(f0), len(db)); f0, per, db = f0[:n], per[:n], db[:n]
        floor = np.percentile(db, 95) - 30
        st = 12 * np.log2(np.maximum(f0, 1) / 100); voiced = (per > 0.45) & (db > floor)
        return st, voiced, db, floor, n

    def measure(a24, text):
        a16 = librosa.resample(a24.astype(np.float32), orig_sr=24000, target_sr=16000)
        words, marks = parse(text)
        if not words or re.search(r"\d", text): return None
        al = align(a16, words)
        if al is None: return None
        spans, T = al; st, voiced, db, floor, n = frames(a16, T)
        clamp = lambda i: max(0, min(n - 1, i))
        spans = [(clamp(s), clamp(e)) if s is not None else None for s, e in ((sp if sp else (None, None)) for sp in spans)]
        vs = st[voiced]
        if len(vs) < 10: return None
        body = float(np.median(vs)); rng = float(np.percentile(vs, 90) - np.percentile(vs, 10))
        def word_end(i):   # last sounding frame of word i (before the next word starts)
            s, e = spans[i]; nxt = spans[i + 1][0] if i + 1 < len(spans) and spans[i + 1] else n
            k = e
            while k + 1 < nxt and db[k + 1] > floor: k += 1
            return k
        def gap_after(i):
            if i + 1 >= len(spans) or not spans[i] or not spans[i + 1]: return None
            s0, s1 = spans[i][1], spans[i + 1][0]
            return float(np.sum(db[s0:s1] < floor) * 0.02)
        res = []
        for kind, i, cs in marks:
            if not spans[i]: res.append((kind, i, None, None)); continue
            final = i == len(words) - 1
            if kind in ("q", "qx", "q_wh"):
                s, e = spans[i][0], word_end(i); v = st[s:e + 1][voiced[s:e + 1]]
                if len(v) < 3: res.append((kind, i, None, None)); continue
                endp = float(np.median(v[-max(3, len(v) * 3 // 10):]))
                val = endp - body; ok = None if kind == "q_wh" else val >= (1.0 if kind == "q" else 2.0)
            elif kind in ("dots", "dash", "comma"):
                if final:
                    if kind != "dots": res.append((kind, i, None, None)); continue
                    s, e = spans[i][0], word_end(i); dur = (e - s + 1) * 0.02
                    per_letter = np.median([((word_end(k) - spans[k][0] + 1) * 0.02) / max(len(words[k]), 1) for k in range(len(words) - 1) if spans[k]] or [0.08])
                    lengthen = dur / max(len(words[i]) * per_letter, 1e-3)
                    fade = float(np.median(db[s:e + 1]) - np.median(db[db > floor]))
                    val = round(lengthen, 2); ok = lengthen >= 1.2 or fade <= -3
                else:
                    g = gap_after(i)
                    if g is None: res.append((kind, i, None, None)); continue
                    val = g; ok = g >= {"dots": 0.30, "dash": 0.15, "comma": 0.10}[kind]
            elif kind == "caps":
                def peak(k):
                    s, e = spans[k][0], word_end(k); v = st[s:e + 1][voiced[s:e + 1]]
                    return (float(np.percentile(v, 90)) if len(v) >= 2 else None), float(np.max(db[s:e + 1]))
                pk = peak(i); others = [peak(k) for k in range(len(words)) if k != i and spans[k]]
                op = [p for p, _ in others if p is not None]; od = [d for _, d in others]
                if pk[0] is None or not op: res.append((kind, i, None, None)); continue
                dp, dd = pk[0] - float(np.median(op)), pk[1] - float(np.median(od))
                val = round(dp, 2); ok = dp >= 1.5 or dd >= 3.0
            elif kind == "ex":
                val, ok = None, None   # judged later against the same mood's plain lines
            res.append((kind, i, val, ok))
        return dict(body=body, rng=rng, marks=res, rise_end=None)

    # ---------- measure every take
    M = {}; t = time.time()
    for k, r in enumerate(takes):
        try:
            a = sf.read(f"{base}/{r['file']}", dtype="float32")[0]; M[(r["id"], r["take"])] = measure(a, r["text"])
        except Exception as e:
            M[(r["id"], r["take"])] = None; print("measure failed", r["file"], e)
    log(f"measured {len(takes)} takes in {(time.time()-t)/60:.1f} min; failed/unmeasurable {sum(1 for v in M.values() if v is None)}")
    # "!" reference per mood: kept takes of lines with no ! / ?!
    def ref_stats(rows_measured):
        ref = {}
        for row in ROWS:
            xs = [m for (r, m) in rows_measured if r["row"] == row and m and not re.search(r"!", r["text"])]
            ref[row] = (float(np.median([m["body"] for m in xs])) if xs else 0, float(np.median([m["rng"] for m in xs])) if xs else 0)
        return ref
    REF = ref_stats([(r, M[(r["id"], r["take"])]) for r in takes if r["kept"] == "True"])
    def finish_ex(r, m):
        if not m: return m
        b, g = REF[r["row"]]; out = []
        for kind, i, val, ok in m["marks"]:
            if kind == "ex":
                val = round(max(m["rng"] - g, m["body"] - b), 2); ok = val >= 1.0
            out.append((kind, i, val, ok))
        m["marks"] = out; return m
    for r in takes: finish_ex(r, M[(r["id"], r["take"])])
    def score(m):
        if not m: return -1, 0
        req = [ok for kind, _, _, ok in m["marks"] if kind in REQ]
        return sum(1 for o in req if o), len(req)

    # ---------- table helper
    def cell_table(sel, title):
        cnt = {(k, r): [0, 0] for k in KINDS for r in ROWS}; vals = {(k, r): [] for k in KINDS for r in ROWS}
        for r, m in sel:
            if not m: continue
            for kind, _, val, ok in m["marks"]:
                if val is not None: vals[(kind, r["row"])].append(val)
                if ok is None: continue
                cnt[(kind, r["row"])][1] += 1; cnt[(kind, r["row"])][0] += bool(ok)
        out = [f"### {title}", "", "| mark | normal | bright | low | tense |", "|---|---|---|---|---|"]
        for k in KINDS:
            cells = []
            for row in ROWS:
                a_, n_ = cnt[(k, row)]; v = vals[(k, row)]
                med = f" · med {np.median(v):+.2f}" if v else ""
                cells.append(f"{a_}/{n_}{med}" if n_ else (f"– {med}" if v else "–"))
            out.append(f"| {KNAME[k]} | " + " | ".join(cells) + " |")
        return out + [""], cnt
    kept0 = [(r, M[(r["id"], r["take"])]) for r in takes if r["kept"] == "True"]
    t1, cnt0 = cell_table(kept0, "Before: the takes run4_record kept (shows the mark / measured)")

    # ---------- reselect: among Gate-1-passing takes, most marks shown
    LINES = {}
    for r in takes: LINES.setdefault(r["id"], []).append(r)
    chosen = {}; need = []
    for lid, rs in LINES.items():
        # Gate 1 without run4_record's "mark not heard" (it used Whisper-turbo word times, unreliable; marks are re-measured here)
        okr = [r for r in rs if not (set(r["why"].split(",")) - {"mark not heard", ""})] or [r for r in rs if r["kept"] == "True"]
        if not okr: continue
        best = max(okr, key=lambda r: (score(M[(r["id"], r["take"])])[0], r["kept"] == "True"))
        chosen[lid] = ("old", best, M[(best["id"], best["take"])])
        s, n = score(chosen[lid][2])
        if n and s < n: need.append(lid)
    swapped = sum(1 for lid, (_, r, _) in chosen.items() if r["kept"] != "True")
    log(f"reselection: {swapped} lines swapped to another take; {len(need)} lines still missing a mark")
    t2, _ = cell_table([(r, m) for _, r, m in chosen.values()], "After choosing the best existing take per line")

    # ---------- retakes with Orpheus
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from snac import SNAC
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
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
    def record(texts, n=2, B=12):
        res = []
        for i in range(0, len(texts), B):
            tx = texts[i:i + B]
            prompts = [[128259] + tok(f"tara: {s}").input_ids + [128009, 128260] for s in tx]; L = max(map(len, prompts))
            ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = om.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True, temperature=0.6, top_p=0.95,
                                repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
            outs = [to_audio(x[L:]) for x in g]; res += [outs[k * n:(k + 1) * n] for k in range(len(tx))]
        return res
    _wn = asr.tokenizer.normalize
    SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        s = re.sub(r"(\d)-(?=\d)", r"\1", s); t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wn(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w)]
    def word_errors(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]
        o = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in o.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad
    nwords = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))
    def gate1(a, text):
        a, _ = librosa.effects.trim(a, top_db=40); a = np.concatenate([np.zeros(2400), a, np.zeros(2400)]).astype(np.float32)
        dur = len(a) / 24000; lufs = meter.integrated_loudness(a) if dur > 0.5 else -70
        if lufs > -60: a = pyloudnorm.normalize.loudness(a, lufs, -20.0)
        a = np.clip(a, -1, 1).astype(np.float32)
        heard = asr(a.copy(), generate_kwargs={"language": "en"})["text"]; nw = nwords(text); wps = nw / max(dur - 0.2, 0.1)
        ok = word_errors(text, heard) == 0 and (0.3 <= dur - 0.2 <= 2.5 if nw <= 3 else 1.0 <= wps <= 3.2)
        return a, ok, heard
    TXT = {lid: rs[0]["text"] for lid, rs in LINES.items()}; ROW = {lid: rs[0]["row"] for lid, rs in LINES.items()}
    new_n = 0; rounds = []
    for rnd in range(1, 4):
        if not need: break
        t = time.time(); recs = record([TXT[l] for l in need]); fixed = 0
        for lid, aa in zip(need, recs):
            for x in aa:
                if x is None or len(x) < 2400: continue
                a, ok, heard = gate1(x, TXT[lid]); new_n += 1
                if not ok: continue
                fake = dict(id=lid, row=ROW[lid], text=TXT[lid]); m = finish_ex(fake, measure(a, TXT[lid]))
                if score(m)[0] > score(chosen[lid][2])[0]:
                    f = f"new/{lid}_r{rnd}_{new_n}.wav"; sf.write(f"{OUT}/{f}", a, 24000)
                    old = chosen[lid][1]
                    chosen[lid] = ("new", dict(old, file=f, take=f"r{rnd}", text_b=TXT[lid]), m)
        need = [l for l in need if score(chosen[l][2])[0] < score(chosen[l][2])[1]]
        rounds.append(f"round {rnd}: {len(recs)} lines × 2 in {(time.time()-t)/60:.1f} min; still missing a mark: {len(need)}"); log(rounds[-1])
    t3, cnt3 = cell_table([(r, m) for _, r, m in chosen.values()], "After re-recording (final)")

    # ---------- final clips + train.csv
    with open(f"{OUT}/train.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "row", "text_b", "text", "split", "id", "group", "source"])
        for lid, (src, r, m) in sorted(chosen.items()):
            dst = f"final/{lid}.wav"
            shutil.copy(f"{OUT}/{r['file']}" if src == "new" else f"{base}/{r['file']}", f"{OUT}/{dst}")
            w.writerow([dst, r["row"], r["text_b"], r["text"], r["split"], lid, r.get("group", ""), f"{src}:{r['take']}"])
    with open(f"{OUT}/audit_marks.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["id", "take", "row", "kind", "word", "value", "ok", "text"])
        for r in takes:
            m = M[(r["id"], r["take"])]
            for kind, i, val, ok in (m["marks"] if m else []): w.writerow([r["id"], r["take"], r["row"], kind, i, val, ok, r["text"]])

    # ---------- moods (kept takes, measured only)
    fin = [(r, m) for _, r, m in chosen.values() if m]
    report += ["## Moods (final takes): pitch level, pitch range (semitones above 100 Hz)", "", "| mood | lines | pitch level | pitch range |", "|---|---|---|---|"]
    X, Y = [], []
    for row in ROWS:
        xs = [m for r, m in fin if r["row"] == row]
        report.append(f"| {row} | {len(xs)} | {np.median([m['body'] for m in xs]):.1f} | {np.median([m['rng'] for m in xs]):.1f} |")
    try:
        from sklearn.linear_model import LogisticRegression; from sklearn.model_selection import cross_val_score
        X = np.array([[m["body"], m["rng"]] for r, m in fin]); Y = np.array([ROWS.index(r["row"]) for r, m in fin])
        acc = cross_val_score(LogisticRegression(max_iter=500), X, Y, cv=5).mean()
        report += ["", f"Mood guessed from pitch level + range alone: {100*acc:.0f}% (chance 25%). Loudness can't be used: every clip was levelled to −20 LUFS.", ""]
    except Exception as e: report += ["", f"(mood classifier failed: {e})", ""]
    report += [f"Takes measured: {len(takes)} · reselection swapped {swapped} lines · new takes recorded {new_n} · " + " · ".join(rounds), ""]
    report += t1 + t2 + t3
    stuck = [lid for lid, (_, r, m) in chosen.items() if score(m)[1] and score(m)[0] < score(m)[1]]
    report += ["## Lines where no take shows every mark (kept anyway)", ""] + [f"- {lid} ({ROW[lid]}): {TXT[lid]}" for lid in sorted(stuck)[:120]] + [""]

    # ---------- listening clips: per mark × mood one that shows the mark (typical) + one that doesn't (if any)
    random.seed(4); nlist = 0
    for k in ["q", "qx", "ex", "dots", "dash", "caps", "q_wh"]:
        for row in ROWS:
            good, bad = [], []
            for lid, (src, r, m) in chosen.items():
                if r["row"] != row or not m: continue
                for kind, i, val, ok in m["marks"]:
                    if kind != k or val is None: continue
                    (good if ok or k == "q_wh" else bad).append((val, lid, r, src))
            picks = []
            if good: good.sort(key=lambda x: x[0]); picks.append(("shows", good[len(good) // 2]))
            if bad and k != "q_wh": picks.append(("missing", random.choice(bad)))
            for tag, (val, lid, r, src) in picks:
                fn = {"q": "question", "qx": "surprise-qx", "ex": "exclaim", "dots": "dots", "dash": "dash", "caps": "CAPS", "q_wh": "wh-question"}[k]
                sh(f"ffmpeg -loglevel error -y -i {OUT}/final/{lid}.wav -b:a 64k {OUT}/listen/actor_{fn}_{row}_{tag}_{lid}.mp3"); nlist += 1
    for row in ROWS:
        plain = [lid for lid, (src, r, m) in chosen.items() if r["row"] == row and m and not m["marks"]]
        if plain:
            lid = random.choice(plain); sh(f"ffmpeg -loglevel error -y -i {OUT}/final/{lid}.wav -b:a 64k {OUT}/listen/actor_plain_{row}_{lid}.mp3"); nlist += 1
    key = ["# Actor listening clips", "", "Name = actor_<mark>_<mood>_<shows|missing>_<line id>. 'shows' = the measurement found the mark; 'missing' = it didn't.", "",
           "| file | text |", "|---|---|"]
    for f in sorted(os.listdir(f"{OUT}/listen")):
        lid = f.rsplit("_", 1)[1][:-4]; key.append(f"| {f} | {TXT.get(lid, '')} |")
    open(f"{OUT}/listen_key.md", "w").write("\n".join(key) + "\n")
    report += [f"Listening clips: {nlist} (listen/, names explain each one; listen_key.md has the text)", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

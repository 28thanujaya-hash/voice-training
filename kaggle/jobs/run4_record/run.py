# Run 4 · Maya pilot v0.2, steps 6–9 (15 Nov): record the 280 top-up lines (+ retakes), Gate 1 v2, option B v2, audits,
# and the mentor's listening grid. Old takes (run 3) are re-judged with the same rules; nothing is silently dropped.
# Gate 1 v2 (pilot-checklist §5.7): line classes by length; 1–3 words = words + duration 0.3–2.5 s only; 4+ words = words, pace
#   (≤ 3.2 words/s, ≥ 1.0), voice similarity only on clips ≥ 2 s; written "…" / "—" must be heard (a pause), else another take;
#   same-line groups must be complete; rushed or failing lines get more takes (max 8 per line); a 10+-word line with no pass keeps
#   its slowest word-correct take (flagged), never dropped. Emotion2vec / mood judge = measured only, used to choose between takes.
# Option B v2: pauses measured on the waveform near Whisper's word boundaries; only "," is ever added (clear pause ≥ 0.35 s,
#   not a breath); marks are never deleted or weakened; words never change. CAPS stay in the text (TextPrep turns them into ↗).
import csv, glob, json, os, random, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from data import LINES
from settings import LEADIN, LEAD
T0 = time.time(); LOG = []; OUT = "/kaggle/working"; os.makedirs(f"{OUT}/clips", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
report = ["# Run 4 · Maya pilot v0.2 · steps 6–9: recording, Gate 1 v2, option B v2, audits, listening grid", ""]
ROWS = ["normal", "bright", "low", "tense"]
MARKS = [("?", r"\?(?!!)"), ("!", r"(?<!\?)!"), ("…", r"…"), ("—", r"—"), ("?!", r"\?!"), ("CAPS", r"\b(?!I\b)[A-Z][A-Z']*[A-Z]\b")]
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "wellawatte", "priya",
         "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
MAX_TAKES = 8
try:
    sh("pip install -q snac jiwer pyloudnorm soundfile librosa funasr modelscope")
    import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoFeatureExtractor, WavLMForXVector
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    model = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev2)
    from funasr import AutoModel as FunModel
    e2v = FunModel(model="emotion2vec/emotion2vec_plus_large", hub="hf", disable_update=True)
    spk_fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv")
    spk = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").to(dev2).eval()
    meter = pyloudnorm.Meter(24000); log("models loaded")

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
    GEN = [0.0]
    def record(texts, n=2, B=12):
        res = []
        for i in range(0, len(texts), B):
            tx = texts[i:i + B]; t = time.time()
            prompts = [[128259] + tok(f"tara: {s}").input_ids + [128009, 128260] for s in tx]; L = max(map(len, prompts))
            ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = model.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True, temperature=0.6, top_p=0.95,
                                   repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
            outs = [to_audio(x[L:]) for x in g]; res += [outs[k * n:(k + 1) * n] for k in range(len(tx))]; GEN[0] += time.time() - t
        return res

    _wn = asr.tokenizer.normalize
    SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        s = re.sub(r"(\d)-(?=\d)", r"\1", s); t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wn(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w)]
    def word_errors(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]
        out = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in out.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad
    nwords = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    nz = lambda v: v / (np.linalg.norm(v) + 1e-9)
    def emb(a): return np.asarray(e2v.generate(r16(a), granularity="utterance", extract_embedding=True)[0]["feats"]).reshape(-1)

    def cut_leadin(a, lead):
        res = asr(a.copy(), return_timestamps="word", generate_kwargs={"language": "en"}); ch = res.get("chunks", [])
        nl = len(wn(lead)); words = []
        for c in ch:
            for w in wn(c["text"]): words.append(c["timestamp"])
        if len(words) <= nl or words[nl][0] is None: return None
        start = words[nl][0]; c0 = max(int((start - 0.12) * 24000), 0); c1 = int(start * 24000)
        rms = librosa.feature.rms(y=a[c0:c1 + 1], frame_length=512, hop_length=64)[0] if c1 > c0 + 512 else None
        cutp = c0 + int(np.argmin(rms)) * 64 if rms is not None and len(rms) else c1
        return a[cutp:]

    def gaps_after_words(a, chunks):
        """Silence after each heard word: longest run below the silence floor between this word's end and the next word's start
        (± 0.15 s), from the waveform. Breaths (above the floor) don't count."""
        rms = librosa.feature.rms(y=a, frame_length=480, hop_length=120)[0]; db = 20 * np.log10(rms + 1e-6)
        floor = np.percentile(db, 95) - 35; hop = 120 / 24000; out = []
        ts = [c["timestamp"] for c in chunks if c.get("timestamp")]
        for k in range(len(ts) - 1):
            e, s = ts[k][1], ts[k + 1][0]
            if e is None or s is None: out.append(0.0); continue
            i0, i1 = max(int((min(e, s) - 0.15) / hop), 0), min(int((max(e, s) + 0.15) / hop), len(db))
            best = cur = 0
            for v in db[i0:i1]:
                cur = cur + 1 if v < floor else 0; best = max(best, cur)
            out.append(best * hop)
        return out
    PAUSE = re.compile(r"(…|\.\.\.|—|[,.!?:;])+[\"”']?$")
    def option_b(text, chunks, a):
        """Returns (text_b, added, missing): commas added where a clear pause has no mark; written … / — not heard -> missing."""
        toks = text.split(); per = [len(wn(t)) for t in toks]; hw = [len(wn(c["text"])) for c in chunks]
        if sum(per) != sum(hw) or not chunks: return text, [], []
        g = gaps_after_words(a, chunks)
        # gap after token i = gap after its last heard word
        ends, k = [], 0
        for c in hw: k += c; ends.append(k - 1)
        word_gap = {}
        for ci, last in enumerate(ends[:-1]): word_gap[last] = g[ci] if ci < len(g) else 0.0
        out, added, missing, k = [], [], [], 0
        for i, t in enumerate(toks):
            k += per[i]; tt = t
            if i < len(toks) - 1 and per[i]:
                gap = word_gap.get(k - 1, 0.0); m = PAUSE.search(t); mark = m.group(0) if m else ""
                if not mark and gap >= 0.35: tt = t + ","; added.append(f"{t}→{tt} ({gap:.2f}s)")
                if mark.startswith("…") and gap < 0.20: missing.append(f"… after '{t}' ({gap:.2f}s)")
                if t.endswith("—") or (i + 1 < len(toks) and toks[i + 1] == "—"):
                    if gap < 0.10: missing.append(f"— after '{t}' ({gap:.2f}s)")
            out.append(tt)
        return " ".join(out), added, missing

    def analyse(a, line, reused):
        lid, row, grp, text = line[:4]
        peak = 0.0 if reused else float(np.abs(a).max()); a, _ = librosa.effects.trim(a, top_db=40)
        a = np.concatenate([np.zeros(2400), a, np.zeros(2400)]).astype(np.float32); dur = len(a) / 24000
        lufs = meter.integrated_loudness(a) if dur > 0.5 else -70
        if lufs > -60: a = pyloudnorm.normalize.loudness(a, lufs, -20.0)
        a = np.clip(a, -1, 1).astype(np.float32)
        res = asr(a.copy(), return_timestamps="word", generate_kwargs={"language": "en"})
        heard = res["text"].strip(); ch = res.get("chunks", [])
        nw = nwords(text); wps = nw / max(dur - 0.2, 0.1); bad = word_errors(text, heard)
        why = []
        if bad: why.append("words")
        if peak >= 0.99: why.append("clipped")
        if nw <= 3:
            if not 0.3 <= dur - 0.2 <= 2.5: why.append("length")
        else:
            if wps > 3.2: why.append("rushed")
            if wps < 1.0: why.append("dragging")
        tb, added, missing = option_b(text, ch, a) if not bad else (text, [], [])
        if missing: why.append("mark not heard")
        with torch.inference_mode():
            x = spk_fe(r16(a), sampling_rate=16000, return_tensors="pt").to(dev2)
            v = torch.nn.functional.normalize(spk(**x).embeddings, dim=-1)[0].cpu().numpy()
        e = emb(a)
        return a, dict(dur=round(dur, 2), wps=round(wps, 2), bad=bad, heard=heard, why=why, text_b=tb, added=added, missing=missing, spkv=v, emb=e)

    LINE = {l[0]: l for l in LINES}
    takes = {}   # id -> list of dict(a=..., reused=bool, how="as written"/"lead-in")
    man = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)[0]; base = os.path.dirname(man); n_old = 0
    for m in sorted(csv.DictReader(open(man)), key=lambda r: (r["id"], int(r["take"]))):
        if m.get("file") and m["id"] in LINE:
            takes.setdefault(m["id"], []).append(dict(a=sf.read(f"{base}/{m['file']}", dtype="float32")[0], reused=True, how="as written (run 3)")); n_old += 1
    log(f"loaded {n_old} run-3 takes")
    def rec_round(ids, n):
        plain = [i for i in ids if not (LEADIN and LINE[i][2])]; lead = [i for i in ids if LEADIN and LINE[i][2]]
        for i, aa in zip(plain, record([LINE[i][3] for i in plain], n)):
            takes.setdefault(i, []).extend(dict(a=x, reused=False, how="as written") for x in aa if x is not None)
        for i, aa in zip(lead, record([LEAD[LINE[i][1]] + " " + LINE[i][3] for i in lead], n)):
            for x in aa:
                c = cut_leadin(x, LEAD[LINE[i][1]]) if x is not None else None
                if c is not None and len(c) > 2400: takes.setdefault(i, []).append(dict(a=c, reused=False, how="lead-in cut"))
    new = [l[0] for l in LINES if l[5] == "topup"] + ([l[0] for l in LINES if l[5] == "pilot" and l[2]] if LEADIN else [])
    t = time.time(); rec_round(new, 2); log(f"round 1: recorded {len(new)} lines x 2 in {(time.time()-t)/60:.1f} min")

    judged = {}   # (id, k) -> result
    def judge_all():
        for lid, tk in takes.items():
            for k, d in enumerate(tk):
                if (lid, k) in judged: continue
                if d["a"] is None or len(d["a"]) < 2400: judged[(lid, k)] = None; continue
                a, r = analyse(d["a"], LINE[lid], d["reused"]); d["a"] = a; judged[(lid, k)] = r
    def passing(lid): return [k for k in range(len(takes.get(lid, []))) if judged.get((lid, k)) and not judged[(lid, k)]["why"]]
    judge_all()
    for rnd in range(2, 5):
        need = [l[0] for l in LINES if not passing(l[0]) and len(takes.get(l[0], [])) < MAX_TAKES]
        if not need: break
        t = time.time(); rec_round(need, 2); judge_all(); log(f"round {rnd}: {len(need)} lines re-recorded in {(time.time()-t)/60:.1f} min")

    # voice drift (clips >= 2 s): similarity to the centroid of passing takes; z < -3 -> fail
    good = [(lid, k) for lid in takes for k in passing(lid)]
    cen = nz(np.mean([judged[x]["spkv"] for x in good], 0)); sims = {x: float(judged[x]["spkv"] @ cen) for x in judged if judged[x]}
    gs = np.array([sims[x] for x in good]); mu, sd = gs.mean(), gs.std() + 1e-6
    for x in good:
        if judged[x]["dur"] >= 2.0 and (sims[x] - mu) / sd < -3: judged[x]["why"].append("voice drift")
    # mood judge centroids: passing takes of non-group lines
    mc = {r: nz(np.mean([judged[(lid, k)]["emb"] for lid in takes for k in passing(lid) if LINE[lid][1] == r and not LINE[lid][2]], 0)) for r in ROWS}
    mood_of = lambda r: max(ROWS, key=lambda q: nz(r["emb"]) @ mc[q])

    chosen = {}; flagged = []
    for l in LINES:
        lid = l[0]; ps = passing(lid)
        if ps:
            chosen[lid] = max(ps, key=lambda k: (mood_of(judged[(lid, k)]) == l[1], -judged[(lid, k)]["wps"]))
        elif nwords(l[3]) >= 10:
            wc = [k for k in range(len(takes.get(lid, []))) if judged.get((lid, k)) and judged[(lid, k)]["bad"] == 0]
            if wc: chosen[lid] = min(wc, key=lambda k: judged[(lid, k)]["wps"]); flagged.append(lid)
    # write clips + lists
    rowsout = []
    for lid, tk in takes.items():
        for k, d in enumerate(tk):
            r = judged.get((lid, k))
            if not r: continue
            f = f"clips/{lid}_t{k+1}.wav"; sf.write(f"{OUT}/{f}", d["a"], 24000)
            rowsout.append(dict(id=lid, row=LINE[lid][1], group=LINE[lid][2], split=LINE[lid][4], take=k + 1, how=d["how"], kept=(chosen.get(lid) == k),
                                ok=not r["why"], why=",".join(r["why"]), seconds=r["dur"], words_per_s=r["wps"], word_errors=r["bad"],
                                mood_judge=mood_of(r), spk_sim=round(sims.get((lid, k), 0), 3), file=f, text=LINE[lid][3], text_b=r["text_b"],
                                added="; ".join(r["added"]), missing="; ".join(r["missing"]), heard=r["heard"]))
    keys = list(rowsout[0])
    with open(f"{OUT}/manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); [w.writerow(x) for x in rowsout]
    kept = [x for x in rowsout if x["kept"]]
    with open(f"{OUT}/train.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "row", "text_b", "text", "split", "id", "group"])
        [w.writerow([x["file"], x["row"], x["text_b"], x["text"], x["split"], x["id"], x["group"]]) for x in kept]

    # ---- audits
    def cnt(lines, field="text"):
        return {(m, r): sum(1 for x in lines if x["row"] == r and re.search(rx, x[field])) for m, rx in MARKS for r in ROWS}
    W = [dict(row=l[1], text=l[3], split=l[4]) for l in LINES]; Wt = [x for x in W if x["split"] == "train"]
    Kt = [x for x in kept if x["split"] == "train"]
    cw, ck, cb = cnt(Wt), cnt(Kt), cnt(Kt, "text_b")
    report += [f"Takes judged: {len(rowsout)} ({n_old} from run 3) · lines with a kept take: **{len(kept)}/{len(LINES)}** · "
               f"flagged long lines kept without a full pass: {len(flagged)} · recording GPU {GEN[0]/60:.1f} min", "",
               f"Lead-in for same-line groups: {'YES' if LEADIN else 'no'}", "",
               "## Audit 1: marks × moods in training (written → kept); stop rule: a cell > 10% below written or below 8", "",
               "| mark | normal | bright | low | tense |", "|---|---|---|---|---|"]
    stop = []
    for m, _ in MARKS:
        cells = []
        for r in ROWS:
            a_, b_ = cw[(m, r)], ck[(m, r)]; cells.append(f"{a_} → {b_}")
            if b_ < min(8, a_) or (a_ and b_ < 0.9 * a_): stop.append(f"{m}/{r}: {a_} → {b_}")
        report.append(f"| {m} | " + " | ".join(cells) + " |")
    report += ["", "Below the rule: " + ("; ".join(stop) if stop else "none"), "", "## Audit 2: length classes (written → kept, training)", "", "| class | written | kept |", "|---|---|---|"]
    for nm, lo, hi in [("1–3 words", 1, 3), ("4–9 words", 4, 9), ("10+ words", 10, 99)]:
        report.append(f"| {nm} | {sum(lo <= nwords(x['text']) <= hi for x in Wt)} | {sum(lo <= nwords(x['text']) <= hi for x in Kt)} |")
    groups = sorted({l[2] for l in LINES if l[2]}, key=lambda g: int(g[1:]))
    gmiss = [f"{g}: " + ", ".join(l[1] for l in LINES if l[2] == g and l[0] not in chosen) for g in groups if any(l[0] not in chosen for l in LINES if l[2] == g)]
    report += ["", "## Audit 3: same-line groups complete", "", ("All complete." if not gmiss else "Incomplete: " + "; ".join(gmiss)), "",
               "## Audit 4: option B v2 (marks before → after; may only go up)", "", "| mark | before | after |", "|---|---|---|"]
    down = []
    for m, _ in MARKS:
        b_ = sum(ck[(m, r)] for r in ROWS); a_ = sum(cb[(m, r)] for r in ROWS); report.append(f"| {m} | {b_} | {a_} |")
        if a_ < b_: down.append(m)
    report += ["", f"Commas added on {sum(1 for x in kept if x['added'])} kept lines; words changed: {sum(1 for x in kept if wn(x['text']) != wn(x['text_b']))}; counts that went down: {down or 'none'}", ""]
    from collections import Counter
    report += ["## Reject reasons (all takes)", "", ", ".join(f"{k} {v}" for k, v in Counter(w for x in rowsout if not x['ok'] for w in x['why'].split(',') if w).most_common()), "",
               "## Mood judge on kept takes (measured only)", "", "| mood | judged as intended |", "|---|---|"]
    for r in ROWS:
        kk = [x for x in kept if x["row"] == r]; report.append(f"| {r} | {sum(1 for x in kk if x['mood_judge'] == r)}/{len(kk)} |")
    nok = [l for l in LINES if l[0] not in chosen]
    report += ["", "## Lines with no kept take", ""] + ([f"- {l[0]} ({l[1]}): {l[3]}" for l in nok] or ["(none)"])
    report += ["", "## Flagged long lines (kept: slowest word-correct take)", ""] + ([f"- {lid}: {LINE[lid][3]}" for lid in flagged] or ["(none)"])

    # ---- step 9: listening grid (2 kept clips per mark × mood, two packs) + tick sheet
    random.seed(9); grid = []
    for m, rx in MARKS:
        for r in ROWS:
            c = [x for x in kept if x["row"] == r and re.search(rx, x["text"]) and x["split"] == "train"]
            grid += [(m, r, x) for x in random.sample(c, min(2, len(c)))]
    rpool = [x for x in rowsout if not x["ok"] and x["why"] != "words"]; rej = random.sample(rpool, min(5, len(rpool)))
    packs = [[g for g in grid if g[0] in ("?", "!", "…")], [g for g in grid if g[0] in ("—", "?!", "CAPS")] + [("(check)", x["row"], x) for x in rej]]
    sheet = ["# Listening grid: tick sheet", "", "For each clip: does the mark sound right **in this mood**? Does the mood sound right (tense = firm, not angry)?", ""]
    keyl = ["# Key: which clips were rejected takes (read AFTER listening)", ""]
    for pi, pk in enumerate(packs, 1):
        random.shuffle(pk); pieces = []
        for _, _, x in pk: pieces += [sf.read(f"{OUT}/{x['file']}", dtype="float32")[0], np.zeros(24000, dtype=np.float32)]
        sf.write(f"{OUT}/p.wav", np.concatenate(pieces), 24000); sh(f"ffmpeg -loglevel error -y -i {OUT}/p.wav -b:a 64k {OUT}/grid_pack{pi}.mp3 && rm {OUT}/p.wav")
        sheet += [f"## Pack {pi} (grid_pack{pi}.mp3)", "", "| # | mood | line | mark right? | mood right? |", "|---|---|---|---|---|"]
        sheet += [f"| {i} | {r} | {x['text']} | ☐ yes ☐ no | ☐ yes ☐ no |" for i, (m, r, x) in enumerate(pk, 1)] + [""]
        keyl += [f"- pack {pi} #{i}: REJECTED take ({x['why']})" for i, (m, r, x) in enumerate(pk, 1) if m == "(check)"]
    open(f"{OUT}/grid_tick_sheet.md", "w").write("\n".join(sheet) + "\n"); open(f"{OUT}/grid_key.md", "w").write("\n".join(keyl) + "\n")
    report += ["", "RESULT: " + ("PASS" if not stop and not gmiss and not down else "CHECK (see audits)")]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

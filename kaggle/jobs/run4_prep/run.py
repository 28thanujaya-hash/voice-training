# Run 4 · pilot steps 3 + 5 (15 Nov).
# Step 3 (free check): do tara's recorded same-line groups G1–G5 really differ between moods? pitch, range, loudness, pace,
#   pauses, end rise per member + a Maya-trained mood judge (emotion2vec embeddings, centroids from tara's kept non-group clips).
# Step 5 (lead-in test): 20 neutral lines x 4 moods, recorded (A) as written (marks only) and (B) with a mood-setting lead-in
#   sentence that is cut off afterwards at the Whisper word boundary. Does B separate the moods better, and are the cuts clean?
# Outputs: report.md (tables + recommendation), group_listen.mp3, leadin_listen.mp3 + key, clips/ (kept on Kaggle).
import csv, glob, json, os, random, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from data import PILOT, NEUTRAL
T0 = time.time(); LOG = []; OUT = "/kaggle/working"; os.makedirs(f"{OUT}/clips", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
report = ["# Run 4 · pilot steps 3 + 5: same-line groups and the lead-in test", ""]
ROWS = ["normal", "bright", "low", "tense"]
MARK = {"normal": ".", "bright": "!", "low": "…", "tense": "."}
LEAD = {"normal": "Okay, so here is the plan.", "bright": "Oh wow, this is the best news ever!",
        "low": "I feel so sad and lonely today…", "tense": "I am really angry about this. Listen to me."}
try:
    sh("pip install -q snac jiwer soundfile librosa funasr modelscope")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    model = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev2)
    from funasr import AutoModel as FunModel
    e2v = FunModel(model="emotion2vec/emotion2vec_plus_large", hub="hf", disable_update=True)
    log("models loaded")

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
            prompts = [[128259] + tok(f"tara: {t}").input_ids + [128009, 128260] for t in tx]; L = max(map(len, prompts))
            ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
            att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
            with torch.inference_mode():
                g = model.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True, temperature=0.6, top_p=0.95,
                                   repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
            outs = [to_audio(x[L:]) for x in g]; res += [outs[k * n:(k + 1) * n] for k in range(len(tx))]
        return res

    _wn = asr.tokenizer.normalize
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))
        return [w for w in _wn(s).split() if re.search(r"[a-z0-9]", w)]
    def same_words(text, heard): return wn(text) == wn(heard)
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    def emb(a): return np.asarray(e2v.generate(r16(a), granularity="utterance", extract_embedding=True)[0]["feats"]).reshape(-1)
    nz = lambda v: v / (np.linalg.norm(v) + 1e-9)
    def feats(a):
        a, _ = librosa.effects.trim(a, top_db=40); dur = len(a) / 24000
        f0, vf, _ = librosa.pyin(a, fmin=75, fmax=500, sr=24000, frame_length=1024)
        v = f0[vf] if vf is not None and vf.any() else np.array([np.nan])
        st = 12 * np.log2(v / 100.0)
        rms = librosa.feature.rms(y=a, frame_length=1024, hop_length=256)[0]; db = 20 * np.log10(rms + 1e-6)
        tail = st[int(len(st) * 0.75):] if len(st) > 8 else st; mid = st[int(len(st) * 0.25):int(len(st) * 0.75)] if len(st) > 8 else st
        sil = db < (np.percentile(db, 95) - 35); runs, cur = [], 0
        for s_ in sil[5:-5]:
            cur = cur + 1 if s_ else (runs.append(cur) or 0)
        runs.append(cur)
        return dict(dur=round(dur, 2), pitch=round(float(np.nanmedian(st)), 2), range=round(float(np.nanpercentile(st, 90) - np.nanpercentile(st, 10)), 2),
                    loud=round(float(np.percentile(db, 90)), 1), end_rise=round(float(np.nanmedian(tail) - np.nanmedian(mid)), 2),
                    pause=round(max(runs) * 256 / 24000, 2))

    # ---- the Maya mood judge: emotion2vec centroids from tara's kept clips that are NOT in a same-line group
    man = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)[0]; base = os.path.dirname(man)
    M = list(csv.DictReader(open(man))); grp = {p[0]: p[2] for p in PILOT}
    ref = {r: [] for r in ROWS}
    for m in M:
        if m.get("kept") == "True" and not grp.get(m["id"]):
            ref[m["row"]].append(emb(sf.read(f"{base}/{m['file']}", dtype="float32")[0]))
    cen = {r: nz(np.mean(ref[r], 0)) for r in ROWS}
    judge = lambda a: max(ROWS, key=lambda q: nz(emb(a)) @ cen[q])
    log(f"judge centroids from {sum(len(v) for v in ref.values())} kept non-group clips")

    # ---- step 3: G1–G5 as recorded
    report += ["## Step 3: tara's recorded same-line groups (G1–G5)", "",
               "| group | mood | text | taken from | judge says | pitch (st) | range (st) | loudness (dB) | end rise (st) | longest pause (s) | length (s) |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
    gok = gn = 0; gpieces = []
    for g in ["G1", "G2", "G3", "G4", "G5"]:
        for pid, row, gg, text in [p for p in PILOT if p[2] == g]:
            takes = [m for m in M if m["id"] == pid and m.get("file")]
            best = ([m for m in takes if m.get("kept") == "True"] or [m for m in takes if m.get("ok") == "True"] or takes or [None])[0]
            if not best:
                report.append(f"| {g} | {row} | {text} | no take | – | | | | | | |"); continue
            a = sf.read(f"{base}/{best['file']}", dtype="float32")[0]; f = feats(a); j = judge(a); gn += 1; gok += (j == row)
            src = "kept" if best.get("kept") == "True" else ("passing" if best.get("ok") == "True" else "rejected take")
            report.append(f"| {g} | {row} | {text} | {src} | {j}{' ✓' if j == row else ''} | {f['pitch']} | {f['range']} | {f['loud']} | {f['end_rise']} | {f['pause']} | {f['dur']} |")
            gpieces += [a, np.zeros(12000, dtype=np.float32)]
        gpieces.append(np.zeros(24000, dtype=np.float32))
    report += ["", f"Judge names the intended mood for **{gok}/{gn}** group members (chance ≈ 25%).", ""]
    sf.write(f"{OUT}/g.wav", np.concatenate(gpieces), 24000); sh(f"ffmpeg -loglevel error -y -i {OUT}/g.wav -b:a 64k {OUT}/group_listen.mp3 && rm {OUT}/g.wav")

    # ---- step 5: lead-in test
    items = [(s, r) for s in NEUTRAL for r in ROWS]
    textA = [s.rstrip(".!?…") + MARK[r] for s, r in items]
    textB = [LEAD[r] + " " + t for (s, r), t in zip(items, textA)]
    t = time.time(); recA = record(textA); recB = record(textB); log(f"recorded {len(items)} x 2 versions x 2 takes in {(time.time()-t)/60:.1f} min")
    def cut_leadin(a, lead, target):
        res = asr(a.copy(), return_timestamps="word", generate_kwargs={"language": "en"}); ch = res.get("chunks", [])
        nl = len(wn(lead)); words = []
        for c in ch:
            for w in wn(c["text"]): words.append((w, c["timestamp"]))
        if len(words) <= nl or words[nl][1][0] is None: return None, "no boundary"
        start = words[nl][1][0]; c0 = max(int((start - 0.12) * 24000), 0); c1 = int(start * 24000)
        rms = librosa.feature.rms(y=a[c0:c1 + 1], frame_length=512, hop_length=64)[0] if c1 > c0 + 512 else None
        cutp = c0 + int(np.argmin(rms)) * 64 if rms is not None and len(rms) else c1
        out = a[cutp:]; out, _ = librosa.effects.trim(out, top_db=40)
        h = asr(out.copy(), generate_kwargs={"language": "en"})["text"]
        return out, ("ok" if same_words(target, h) else f"words: {h.strip()[:60]}")
    rowsA = []; rowsB = []
    for (s, r), ta, tb, aa, bb in zip(items, textA, textB, recA, recB):
        ca = [x for x in aa if x is not None and len(x) > 4800]
        ga = [x for x in ca if same_words(ta, asr(x.copy(), generate_kwargs={"language": "en"})["text"])]
        a = (ga or ca or [None])[0]
        b = None; why = "no audio"
        for x in [x for x in bb if x is not None and len(x) > 4800]:
            b, why = cut_leadin(x, LEAD[r], ta)
            if why == "ok": break
        rowsA.append((s, r, a, bool(ga))); rowsB.append((s, r, b, why))
    accA = [judge(a) == r for s, r, a, _ in rowsA if a is not None]; accB = [judge(b) == r for s, r, b, w in rowsB if b is not None and w == "ok"]
    cutok = sum(1 for *_, w in rowsB if w == "ok")
    def spread(rws):
        f = {r: [feats(a) for s, rr, a, *_ in rws if rr == r and a is not None] for r in ROWS}
        return {r: {k: round(float(np.mean([x[k] for x in v])), 2) for k in ("pitch", "range", "loud", "end_rise", "pause", "dur")} for r, v in f.items() if v}
    sA, sB = spread(rowsA), spread([(s, r, b, w) for s, r, b, w in rowsB if w == "ok"])
    report += ["## Step 5: lead-in test (20 neutral lines × 4 moods)", "",
               f"Lead-ins: normal “{LEAD['normal']}” · bright “{LEAD['bright']}” · low “{LEAD['low']}” · tense “{LEAD['tense']}”", "",
               "| | judge names the intended mood | clips judged |", "|---|---|---|",
               f"| A: line alone (marks only) | **{100*np.mean(accA):.0f}%** | {len(accA)} |",
               f"| B: lead-in + line, lead-in cut off | **{100*np.mean(accB) if accB else 0:.0f}%** | {len(accB)} |", "",
               f"Clean cuts (Whisper hears exactly the target words after the cut): **{cutok}/{len(rowsB)}**", "",
               "Average voice measures per mood (A → B):", "", "| mood | pitch (st) | range (st) | loudness (dB) | end rise (st) | longest pause (s) | length (s) |", "|---|---|---|---|---|---|---|"]
    for r in ROWS:
        if r in sA and r in sB:
            report.append(f"| {r} | " + " | ".join(f"{sA[r][k]} → {sB[r][k]}" for k in ("pitch", "range", "loud", "end_rise", "pause", "dur")) + " |")
    bad = [f"{s} ({r}): {w}" for s, r, b, w in rowsB if w != "ok"]
    report += ["", "Cuts that failed: " + ("; ".join(bad[:20]) if bad else "none"), ""]
    better = accB and np.mean(accB) - np.mean(accA) >= 0.15 and cutok >= 0.9 * len(rowsB)
    report += ["**Recommendation:** " + ("use the lead-in for all neutral (same-line) lines: clearly better mood separation with clean cuts." if better else
               "keep recording neutral lines as written (the lead-in did not clearly help, or the cuts were not clean enough)."), ""]
    # blind pack: 12 (line, mood) pairs, A and B in random order
    random.seed(5); pick = random.sample([i for i in range(len(items)) if rowsA[i][2] is not None and rowsB[i][3] == "ok"], min(12, cutok))
    clips = []
    for i in pick:
        pair = [("A (as written)", rowsA[i][2]), ("B (lead-in cut)", rowsB[i][2])]; random.shuffle(pair)
        clips += [(items[i], *p) for p in pair]
    pieces = []
    for _, _, a in clips: pieces += [a.astype(np.float32), np.zeros(24000, dtype=np.float32)]
    sf.write(f"{OUT}/l.wav", np.concatenate(pieces), 24000); sh(f"ffmpeg -loglevel error -y -i {OUT}/l.wav -b:a 64k {OUT}/leadin_listen.mp3 && rm {OUT}/l.wav")
    open(f"{OUT}/leadin_listen_key.md", "w").write("# Key to leadin_listen.mp3 (read AFTER listening)\n\n| # | version | mood | line |\n|---|---|---|---|\n" +
        "".join(f"| {k} | {v} | {it[1]} | {it[0]} |\n" for k, (it, v, _) in enumerate(clips, 1)))
    for (s, r, a, _), (_, _, b, w) in zip(rowsA, rowsB):
        n = re.sub(r"\W+", "_", s.lower())[:30]
        if a is not None: sf.write(f"{OUT}/clips/A_{r}_{n}.wav", a, 24000)
        if b is not None and w == "ok": sf.write(f"{OUT}/clips/B_{r}_{n}.wav", b, 24000)
    report += ["RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

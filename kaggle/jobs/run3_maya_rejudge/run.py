# Run 3 (Maya pilot, voice v0.1), stage 1b: RE-JUDGE the takes recorded by run3_maya_record with a fixed Gate 1, then record more
# takes only for lines that still have none. Fixes: (1) word check uses Whisper's own English normaliser on both sides (British vs
# American spelling, café/cafe, numbers as digits) and forgives dropped fillers (hmm, um, oh, ah); (2) emotion recogniser replaced
# (superb ER called 724/732 takes "angry"): emotion2vec+ large, falling back to a wav2vec2 model trained on acted speech.
# Gate 1 (rejects): words exact (names forgiven) · no clipping · not too short · not rushed (pace band) · voice drift (speaker outlier).
# Measured, not rejecting yet (thresholds set from this run): emotion recogniser agreement with the row.
# Option B v1: pauses heard in the acting correct the pause marks (… ,) in the training text -> text_b.
# Outputs: clips/ (kept + rejected), manifest.csv, train.csv (kept: file|row|text_b), report.md, spot-listen pack (20 kept + 5 rejected).
import csv, glob, json, os, random, shutil, re, subprocess, time, traceback
import sys; sys.path.insert(0, os.getcwd())
from lines_data import LINES
T0 = time.time(); LOG = []; OUT = "/kaggle/working"; os.makedirs(f"{OUT}/clips", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
sh("pip install -q snac jiwer pyloudnorm soundfile librosa")
try: sh("pip install -q funasr modelscope"); HAVE_FUNASR = True
except Exception: HAVE_FUNASR = False
import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoFeatureExtractor, WavLMForXVector
VOICE = "tara"; TAKES = 2; RETRY_TAKES = 3; B = 12
PACE_MAX = 3.2      # words/s above this = rushed (tara's audition mean was 2.18); PACE_MIN catches stretched/garbled takes
PACE_MIN = 1.0
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu",
         "wellawatte", "priya", "priya's", "arun", "appa", "amma", "amma's", "kavi", "nimal", "peradeniya", "kandy", "dosa", "ella", "tuk", "dal"}
EMO = {"normal": "neu", "bright": "hap", "low": "sad", "tense": "ang"}
report = ["# Run 3 · Maya pilot (voice v0.1) · stage 1b: re-judged Gate 1 (+ more takes where needed)", ""]; dev = "cuda:0"; dev2 = "cuda:1" if torch.cuda.device_count() > 1 else dev
try:
    tok = model = snac = None
    def load_orpheus():
        global tok, model, snac
        if model is not None: return
        tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
        model = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
        from snac import SNAC
        snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev); log("Orpheus loaded")
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device=dev2)
    EMO_NAME = None; e2v = emo = None
    if HAVE_FUNASR:
        try:
            from funasr import AutoModel as FunModel
            e2v = FunModel(model="emotion2vec/emotion2vec_plus_large", hub="hf", disable_update=True); EMO_NAME = "emotion2vec+ large"
        except Exception as ex: log(f"emotion2vec failed: {str(ex)[:150]}")
    if e2v is None:
        emo = pipeline("audio-classification", "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition", device=dev2); EMO_NAME = "wav2vec2 xlsr (RAVDESS)"
    log(f"emotion model: {EMO_NAME}")
    # our 4 rows <- the model's labels
    EMO_MAP = {"neutral": "neu", "calm": "neu", "happy": "hap", "surprised": "hap", "sad": "sad", "fearful": "sad", "angry": "ang", "disgusted": "ang", "disgust": "ang", "fear": "sad", "surprise": "hap"}
    def emotions(a16):
        global e2v, emo, EMO_NAME
        try: return _emotions(a16) or {"neu": 0.0}
        except Exception as ex:
            if e2v is None: raise
            log(f"emotion2vec failed at run time ({str(ex)[:120]}); switching to the wav2vec2 model")
            e2v = None; emo = pipeline("audio-classification", "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition", device=dev2)
            EMO_NAME = "wav2vec2 xlsr (RAVDESS)"; return _emotions(a16) or {"neu": 0.0}
    def _emotions(a16):
        if e2v is not None:
            r = e2v.generate(a16, granularity="utterance", extract_embedding=False)[0]
            out = {}
            for lab, sc in zip(r["labels"], r["scores"]):
                k = EMO_MAP.get(lab.split("/")[-1].strip().lower())
                if k: out[k] = out.get(k, 0) + float(sc)
            return out
        out = {}
        for d in emo(a16.copy(), top_k=8):
            k = EMO_MAP.get(d["label"].lower())
            if k: out[k] = out.get(k, 0) + d["score"]
        return out
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
    def record_batch(texts, n):
        prompts = [[128259] + tok(f"{VOICE}: {t}").input_ids + [128009, 128260] for t in texts]; L = max(map(len, prompts))
        ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
        att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
        with torch.inference_mode():
            g = model.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True, temperature=0.6, top_p=0.95,
                               repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
        outs = [to_audio(x[L:]) for x in g]; return [outs[i * n:(i + 1) * n] for i in range(len(texts))]

    norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split()
    FILLERS = {"hmm", "hm", "um", "uh", "oh", "ah", "mm"}
    try: _wnorm = asr.tokenizer.normalize; _wnorm("Colours, 7.30")
    except Exception:
        from transformers.models.whisper.english_normalizer import BasicTextNormalizer; _wnorm = BasicTextNormalizer(); log("WARNING: basic normaliser only")
    SPELL = {"mum": "mom", "mums": "moms", "mum's": "mom's", "grey": "gray", "practise": "practice"}
    def wn(s):
        s = re.sub(r"(?i)\b(hmm+|hm|um+|uh+|oh|ah|mm+)\b", " ", s.replace("…", " ").replace("—", " "))   # fillers out first ("oh" -> "0")
        s = re.sub(r"(\d)-(?=\d)", r"\1", s)
        t = re.sub(r"(\d)[.:](\d)", r"\1\2", _wnorm(s))
        return [SPELL.get(w, w) for w in t.split() if re.search(r"[a-z0-9]", w) and w not in FILLERS]
    def word_errors(text, heard):
        ref, hyp = wn(text), wn(heard) or ["x"]
        out = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {j for i, w in enumerate(ref) if w in NAMES for j in (i - 1, i, i + 1)}
        for a in out.alignments[0]:
            if a.type == "equal": continue
            if set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1))) & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad / max(len(ref), 1)

    PAUSE = re.compile(r"(…|\.\.\.|—|[,.!?:;])+[\"”']?$")
    def option_b(text, chunks):
        """Pause marks follow the acting. Returns (text_b, changes). Only when Whisper's words line up with ours."""
        toks = text.split(); per = [len(norm(t)) for t in toks]; words = []
        for c in chunks:
            ts = c.get("timestamp") or (None, None)
            for w in norm(c["text"]): words.append(ts)
        if len(words) != sum(per) or any(t[0] is None or t[1] is None for t in words): return text, []
        out, changes, k = [], [], 0
        for i, t in enumerate(toks):
            k += per[i]; tt = t
            if i < len(toks) - 1 and per[i] and k < len(words):
                gap = words[k][0] - words[k - 1][1]; m = PAUSE.search(t); mark = m.group(0) if m else ""
                if not mark and gap >= 0.8: tt = t + "…"
                elif not mark and gap >= 0.35: tt = t + ","
                elif mark.startswith(",") and gap >= 0.8: tt = t[:-1] + "…"
                elif mark.startswith("…") and gap < 0.15: tt = t[: -len(mark)] + "," + mark[1:]
                if tt != t: changes.append(f"{t}→{tt} ({gap:.2f}s)")
            out.append(tt)
        return " ".join(out), changes

    def analyse(a, reused=False):
        peak = 0.0 if reused else float(np.abs(a).max()); a, _ = librosa.effects.trim(a, top_db=40)
        a = np.concatenate([np.zeros(2400), a, np.zeros(2400)]).astype(np.float32); dur = len(a) / 24000
        lufs = meter.integrated_loudness(a) if dur > 0.5 else -70
        if lufs > -60: a = pyloudnorm.normalize.loudness(a, lufs, -20.0)
        a = np.clip(a, -1, 1).astype(np.float32); a16 = librosa.resample(a, orig_sr=24000, target_sr=16000)
        try: res = asr(a.copy(), return_timestamps="word", generate_kwargs={"language": "en"})
        except Exception as ex:
            log(f"word timestamps failed ({str(ex)[:80]}); plain transcript"); res = asr(a.copy(), generate_kwargs={"language": "en"})
        e = emotions(a16)
        with torch.inference_mode():
            x = spk_fe(a16, sampling_rate=16000, return_tensors="pt").to(dev2)
            v = torch.nn.functional.normalize(spk(**x).embeddings, dim=-1)[0].cpu().numpy()
        return a, dict(peak=peak, dur=dur, lufs=lufs, heard=res["text"].strip(), chunks=res.get("chunks", []), emo=e, emb=v)

    takes = {}; gen_s = 0; audio_s = 0
    def run_round(ids, n, tag):
        global gen_s
        load_orpheus()
        for i in range(0, len(ids), B):
            b = ids[i:i + B]; t = time.time(); got = record_batch([TEXT[l] for l in b], n); gen_s += time.time() - t
            for lid, aa in zip(b, got): takes.setdefault(lid, []).extend(aa)
            log(f"{tag}: batch {i // B + 1}/{(len(ids) + B - 1) // B} in {time.time() - t:.0f} s")
    TEXT = {l[0]: l[3] for l in LINES}; ROW = {l[0]: l[2] for l in LINES}
    # takes from run3_maya_record (already trimmed and loudness-normalised; none were clipped there)
    man = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)
    if not man: raise RuntimeError("run3_maya_record outputs not found under /kaggle/input")
    base = os.path.dirname(man[0]); REUSED = set(); n_old = 0
    for r in sorted(csv.DictReader(open(man[0])), key=lambda r: (r["id"], int(r["take"]))):
        if not r.get("file"): continue
        a, _ = sf.read(f"{base}/{r['file']}", dtype="float32"); takes.setdefault(r["id"], []).append(a)
        REUSED.add((r["id"], len(takes[r["id"]]))); n_old += 1
    log(f"loaded {n_old} earlier takes from {base}")

    rows = []
    def judge(lid):
        global audio_s
        out = []
        for k, a in enumerate(takes[lid]):
            if any(r["id"] == lid and r["take"] == k + 1 for r in rows): continue
            r = dict(id=lid, row=ROW[lid], take=k + 1, text=TEXT[lid])
            if a is None or len(a) < 2400: r.update(ok=False, why="no audio"); rows.append(r); continue
            a, m = analyse(a, reused=(lid, k + 1) in REUSED); audio_s += m["dur"]; e = word_errors(TEXT[lid], m["heard"]); wps = len(norm(TEXT[lid])) / max(m["dur"] - 0.2, 0.1)
            f = f"clips/{lid}_t{k+1}.wav"; sf.write(f"{OUT}/{f}", a, 24000)
            why = [w for w, bad in (("words", e > 0), ("clipped", m["peak"] >= 0.99), ("too short", m["dur"] <= 0.5),
                                     ("rushed", wps > PACE_MAX), ("dragging", wps < PACE_MIN)) if bad]
            tb, ch = option_b(TEXT[lid], m["chunks"]) if not why else (TEXT[lid], [])
            want = EMO[ROW[lid]]
            r.update(ok=not why, why=",".join(why), file=f, seconds=round(m["dur"], 2), words_per_s=round(wps, 2), wer=round(e, 3),
                     emo_top=max(m["emo"], key=m["emo"].get), emo_want=want, emo_p=round(m["emo"].get(want, 0), 3),
                     text_b=tb, b_changes="; ".join(ch), heard=m["heard"], _emb=m["emb"])
            rows.append(r)
    for l in LINES: judge(l[0])
    failed = [l[0] for l in LINES if not any(r["id"] == l[0] and r["ok"] for r in rows)]
    log(f"re-judged: {len(LINES) - len(failed)}/{len(LINES)} lines have a passing take; recording {len(failed)} again with {RETRY_TAKES} more takes")
    if failed:
        run_round(failed, RETRY_TAKES, "retry")
        for lid in failed: judge(lid)

    # voice drift: similarity to the centroid of all passing takes; outliers (z < -3) are rejected
    good = [r for r in rows if r.get("ok")]
    cen = np.mean([r["_emb"] for r in good], 0); cen /= np.linalg.norm(cen)
    for r in rows:
        if "_emb" in r: r["spk_sim"] = round(float(r["_emb"] @ cen), 3)
    sims = np.array([r["spk_sim"] for r in good]); mu, sd = sims.mean(), sims.std() + 1e-6
    for r in good:
        if (r["spk_sim"] - mu) / sd < -3: r.update(ok=False, why="voice drift", text_b=r["text"], b_changes="")
    # keep per line: passing take with the highest emotion agreement, then the slower pace
    for l in LINES:
        c = [r for r in rows if r["id"] == l[0] and r.get("ok")]
        if c: max(c, key=lambda r: (r["emo_p"], -r["words_per_s"]))["kept"] = True

    keys = ["id", "row", "take", "kept", "ok", "why", "seconds", "words_per_s", "wer", "emo_want", "emo_top", "emo_p", "spk_sim", "file", "text", "text_b", "b_changes", "heard"]
    with open(f"{OUT}/manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in rows]
    kept = [r for r in rows if r.get("kept")]
    with open(f"{OUT}/train.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "row", "text_b", "text"]); [w.writerow([r["file"], r["row"], r["text_b"], r["text"]]) for r in kept]

    # spot-listen pack: 20 random kept + 5 random rejected, shuffled (blind); key in listen_key.md
    random.seed(13); rej = [r for r in rows if not r.get("ok") and "file" in r]
    pack = random.sample(kept, min(20, len(kept))) + random.sample(rej, min(5, len(rej))); random.shuffle(pack)
    pieces = []
    for r in pack: pieces += [sf.read(f"{OUT}/{r['file']}")[0], np.zeros(int(24000 * 1.0))]
    sf.write(f"{OUT}/p.wav", np.concatenate(pieces).astype(np.float32), 24000)
    sh(f"ffmpeg -loglevel error -y -i {OUT}/p.wav -b:a 64k {OUT}/run3_spot_listen.mp3 && rm {OUT}/p.wav")
    key = ["# Key to run3_spot_listen.mp3 (read AFTER listening)", "", "| # | kept? | row | why rejected | text |", "|---|---|---|---|---|"]
    key += [f"| {i} | {'kept' if r.get('kept') else 'REJECTED'} | {r['row']} | {r.get('why','')} | {r['text']} |" for i, r in enumerate(pack, 1)]
    open(f"{OUT}/listen_key.md", "w").write("\n".join(key) + "\n")

    report += [f"Voice: **{VOICE}** · lines: {len(LINES)} · earlier takes re-judged: {n_old} · new takes only for lines with none passing ({RETRY_TAKES} each)",
               f"Recording: {gen_s/60:.1f} min for {audio_s/60:.1f} min of audio ({audio_s/max(gen_s,1):.2f}× real time)",
               f"Lines with a kept take: **{len(kept)}/{len(LINES)}** · kept audio: {sum(r['seconds'] for r in kept)/60:.1f} min", "",
               "## Per row", "", "| row | kept | takes made | rejected | reject rate | pace kept (words/s, mean · max) | emotion model agrees (kept) |",
               "|---|---|---|---|---|---|---|"]
    for row in EMO:
        rr = [r for r in rows if r["row"] == row]; kk = [r for r in kept if r["row"] == row]; made = [r for r in rr if "file" in r]
        rj = [r for r in rr if not r.get("ok")]; p = [r["words_per_s"] for r in kk]
        agree = sum(1 for r in kk if r["emo_top"] == r["emo_want"])
        report.append(f"| {row} | {len(kk)}/75 | {len(rr)} | {len(rj)} | {100*len(rj)/max(len(rr),1):.0f}% | {np.mean(p) if p else 0:.2f} · {max(p) if p else 0:.2f} | {agree}/{len(kk)} |")
    from collections import Counter
    report += ["", "Reasons for rejection: " + ", ".join(f"{k} {v}" for k, v in Counter(w for r in rows if not r.get("ok") for w in r.get("why", "").split(",") if w).most_common()), "",
               f"Speaker similarity (passing takes): mean {mu:.3f}, sd {sd:.3f}, min {sims.min():.3f}; drift-rejected: {sum(1 for r in rows if r.get('why') == 'voice drift')}",
               f"Emotion recogniser: {EMO_NAME}; measured only (no rejections); it picks between passing takes.", "",
               f"Option B v1 (pause marks follow the acting): {sum(1 for r in kept if r.get('b_changes'))}/{len(kept)} kept lines changed; "
               f"{sum(1 for r in kept if r.get('b_changes') == '' and r['text_b'] == r['text'])} unchanged.", "",
               "## Lines with no kept take", ""]
    report += [f"- {l[0]} ({l[2]}): {l[3]}" for l in LINES if not any(r["id"] == l[0] and r.get("kept") for r in rows)] or ["(none)"]
    report += ["", "## Option B changes (kept lines)", ""] + [f"- {r['id']}: {r['b_changes']}" for r in kept if r.get("b_changes")]
    report += ["", "## Emotion model disagreements (kept lines)", ""] + [f"- {r['id']} want {r['emo_want']} got {r['emo_top']} ({r['emo_p']}): {r['text']}" for r in kept if r["emo_top"] != r["emo_want"]]
    report += ["", "RESULT: PASS" if len(kept) >= 0.8 * len(LINES) else "RESULT: FAIL (fewer than 80% of lines kept)"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

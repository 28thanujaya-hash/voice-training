# Run 2: the audition. Orpheus reads the 20 persona lines: Sam's 10 in leo and zac, Maya's 10 in tara and leah, 2 takes each.
# Gate 1 keeps the best passing take (Whisper words, clipping; names Whisper doesn't know are forgiven).
# One listening file: each voice introduces itself, then says its 10 lines. The mentor picks one voice per character.
import csv, json, os, re, subprocess, time, traceback
T0 = time.time(); LOG = []; OUT = "/kaggle/working"; os.makedirs(f"{OUT}/clips", exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
sh("pip install -q snac jiwer pyloudnorm soundfile librosa")
import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
LINES = json.loads(r'''[["s01", "sam", "bright", "No way! He's here! I have a little brother! His name is Thenuka!"], ["s02", "sam", "normal", "So, how was your weekend? Did you do anything fun?"], ["s03", "sam", "bright", "You cooked? Okay… but did you burn the rice? Like me?"], ["s04", "sam", "low", "He cried all night… But then he smiled at me. Worth it."], ["s05", "sam", "low", "Bruno died last night. He was old. I'm okay. Just… quiet today."], ["s06", "sam", "tense", "I failed. The parking. Again. Don't laugh."], ["s07", "sam", "bright", "Wait. Seriously? He skipped the whole queue?"], ["s08", "sam", "low", "Hey… I'm really sorry, Maya. That's not fair."], ["s09", "sam", "normal", "Um… I don't know. Maybe I'm not that clever."], ["s10", "sam", "bright", "I can't believe it!"], ["m01", "maya", "normal", "The sea at Galle Face is so pretty tonight, and the air is cool. You should see it."], ["m02", "maya", "normal", "Okay, tell me everything. What happened next?"], ["m03", "maya", "normal", "Marvel again? That's so you."], ["m04", "maya", "bright", "So… I'm shift leader now. Me. Can you believe it?"], ["m05", "maya", "bright", "First Chennai, and then Madurai. I've been saving for a whole year!"], ["m06", "maya", "low", "He shouted at me in front of everyone, so I went to the back and cried."], ["m07", "maya", "tense", "No. That was not okay. You don't speak to people like that."], ["m08", "maya", "low", "Paati's in hospital, and I'm so far away… I just want to be there."], ["m09", "maya", "low", "Oh, Sam… Bruno was family. Take your time."], ["m10", "maya", "normal", "When I think about it, Colombo taught me to be brave."]]''')
CANDIDATES = {"sam": ["leo", "zac"], "maya": ["tara", "leah"]}
NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu", "leo", "zac", "tara", "leah"}
report = ["# Run 2 · the audition", ""]; dev = "cuda:0"
try:
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    model = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:1" if torch.cuda.device_count() > 1 else dev)
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
    def record_batch(items, n=2):
        prompts = [[128259] + tok(f"{v}: {t}").input_ids + [128009, 128260] for t, v in items]; L = max(map(len, prompts))
        ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
        att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
        with torch.inference_mode():
            g = model.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True, temperature=0.6, top_p=0.95,
                               repetition_penalty=1.1, num_return_sequences=n, eos_token_id=128258, pad_token_id=128263)
        outs = [to_audio(x[L:]) for x in g]; return [outs[i * n:(i + 1) * n] for i in range(len(items))]
    norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split()
    def word_errors(text, heard):
        """Word error rate, forgiving errors on a name or right next to one (Whisper doesn't know our names)."""
        ref, hyp = norm(text), norm(heard) or ["x"]
        out = jiwer.process_words(" ".join(ref), " ".join(hyp)); bad = 0
        near = {i for i, w in enumerate(ref) if w in NAMES for i in (i - 1, i, i + 1)}
        for a in out.alignments[0]:
            if a.type == "equal": continue
            span = set(range(a.ref_start_idx, max(a.ref_end_idx, a.ref_start_idx + 1)))
            if span & near: continue
            bad += max(a.ref_end_idx - a.ref_start_idx, a.hyp_end_idx - a.hyp_start_idx)
        return bad / max(len(ref), 1)

    jobs = [(lid, who, row, text, v) for lid, who, row, text in LINES for v in CANDIDATES[who]]
    jobs += [(f"intro_{v}", who, "intro", f"Hi! This is {v.capitalize()}.", v) for who, vs in CANDIDATES.items() for v in vs]
    results = {}; gen_s = 0
    for i in range(0, len(jobs), 8):
        b = jobs[i:i + 8]; t = time.time(); got = record_batch([(j[3], j[4]) for j in b]); gen_s += time.time() - t
        for j, takes in zip(b, got): results[(j[0], j[4])] = takes
        log(f"batch {i // 8 + 1}/{(len(jobs) + 7) // 8} in {time.time() - t:.0f} s")
    rows = []; audio_s = 0
    for lid, who, row, text, v in jobs:
        best = None
        for k, a in enumerate(results[(lid, v)]):
            r = dict(id=lid, who=who, voice=v, row=row, take=k + 1, text=text)
            if a is None or len(a) < 2400: r.update(ok=False, why="no audio"); rows.append(r); continue
            peak = float(np.abs(a).max()); a, _ = librosa.effects.trim(a, top_db=40)
            a = np.concatenate([np.zeros(2400), a, np.zeros(2400)]).astype(np.float32); dur = len(a) / 24000; audio_s += dur
            lufs = meter.integrated_loudness(a) if dur > 0.5 else -70
            if lufs > -60: a = pyloudnorm.normalize.loudness(a, lufs, -20.0)
            heard = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip(); e = word_errors(text, heard)
            wps = len(norm(text)) / max(dur - 0.2, 0.1); f = f"clips/{lid}_{v}_t{k+1}.wav"; sf.write(f"{OUT}/{f}", np.clip(a, -1, 1), 24000)
            ok = e == 0 and peak < 0.99
            r.update(ok=ok, why="" if ok else ("words" if e else "clipped"), file=f, seconds=round(dur, 2), words_per_s=round(wps, 2), wer=round(e, 3), heard=heard)
            rows.append(r)
            if ok and (best is None or r["wer"] < best["wer"] or (r["wer"] == best["wer"] and r["words_per_s"] < best["words_per_s"])): best = r
        if best is None:   # nothing passed: keep the closest take anyway so every line can be heard (marked in the report)
            cands = [r for r in rows if r["id"] == lid and r["voice"] == v and "file" in r]
            if cands: best = min(cands, key=lambda r: r["wer"]); best["fallback"] = True
        if best: best["kept"] = True

    keys = ["id", "who", "voice", "row", "take", "kept", "fallback", "ok", "why", "seconds", "words_per_s", "wer", "file", "text", "heard"]
    with open(f"{OUT}/manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in rows]

    # listening file: Sam (leo, zac), then Maya (tara, leah); each voice: intro, then its 10 lines
    pieces = []; order = []; summary = []
    for who, vs in CANDIDATES.items():
        for n, v in enumerate(vs, 1):
            kept = {r["id"]: r for r in rows if r.get("kept") and r["voice"] == v}
            seq = [f"intro_{v}"] + [l[0] for l in LINES if l[1] == who]
            for lid in seq:
                if lid in kept: pieces += [sf.read(f"{OUT}/{kept[lid]['file']}")[0], np.zeros(int(24000 * 0.8))]
            pieces.append(np.zeros(24000 * 2))
            lines_kept = [kept[l[0]] for l in LINES if l[1] == who and l[0] in kept]
            passed = sum(1 for r in lines_kept if not r.get("fallback"))
            pace = np.mean([r["words_per_s"] for r in lines_kept]) if lines_kept else 0
            summary.append(f"| {who.capitalize()} {n} | **{v}** | {passed}/10 | {pace:.2f} | {sum(r['seconds'] for r in lines_kept):.0f} s |")
            order.append(f"{who.capitalize()} voice {n}: {v}")
    sf.write(f"{OUT}/a.wav", np.concatenate(pieces).astype(np.float32), 24000)
    sh(f"ffmpeg -loglevel error -y -i {OUT}/a.wav -b:a 64k {OUT}/audition_listen.mp3 && rm {OUT}/a.wav")
    report += ["Order in audition_listen.mp3: " + " → ".join(order) + " (each starts with “Hi! This is …”, 2 s gap between voices).", "",
               "| | voice | lines passed Gate 1 | pace (words/s) | total |", "|---|---|---|---|---|", *summary, "",
               f"Recording: {gen_s/60:.1f} min for {audio_s/60:.1f} min of audio ({audio_s/max(gen_s, 1):.2f}× real time).", "",
               "## Lines kept although no take passed (closest take)", ""]
    report += [f"- {r['voice']} {r['id']}: “{r['text']}” → heard “{r['heard']}”" for r in rows if r.get("fallback")] or ["(none)"]
    report += ["", "## All failed takes", ""] + [f"- {r['voice']} {r['id']} t{r['take']}: {r.get('why')} · “{r.get('heard', '')}”" for r in rows if not r.get("ok")]
    report += ["", "RESULT: PASS"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

# Run 1, stage 1 (smoke run): Orpheus records 20 lines (Sam = leo, Maya = tara), 2 takes each,
# then the automatic Gate 1 checks: Whisper words, pace, clipping, loudness, silence trim.
# Quality doesn't matter in run 1: this proves the code and measures time and GPU memory.
import json, os, re, subprocess, sys, time, traceback
T0 = time.time(); LOG = []
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c): subprocess.run(c, shell=True, check=True)
sh("pip install -q snac jiwer pyloudnorm soundfile librosa")
import numpy as np, torch, soundfile as sf, librosa, jiwer, pyloudnorm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
lines = json.loads(r'''[
 ["s01","sam","bright","No way! He's here! I have a little brother! His name is Thenuka!"],
 ["s02","sam","normal","So, how was your weekend? Did you do anything fun?"],
 ["s03","sam","bright","You cooked? Okay… but did you burn the rice? Like me?"],
 ["s04","sam","low","He cried all night… But then he smiled at me. Worth it."],
 ["s05","sam","low","Bruno died last night. He was old. I'm okay. Just… quiet today."],
 ["s06","sam","tense","I failed. The parking. Again. Don't laugh."],
 ["s07","sam","bright","Wait. Seriously? He skipped the whole queue?"],
 ["s08","sam","low","Hey… I'm really sorry, Maya. That's not fair."],
 ["s09","sam","normal","Um… I don't know. Maybe I'm not that clever."],
 ["s10","sam","bright","I can't believe it!"],
 ["m01","maya","normal","The sea at Galle Face is so pretty tonight, and the air is cool. You should see it."],
 ["m02","maya","normal","Okay, tell me everything. What happened next?"],
 ["m03","maya","normal","Marvel again? That's so you."],
 ["m04","maya","bright","So… I'm shift leader now. Me. Can you believe it?"],
 ["m05","maya","bright","First Chennai, and then Madurai. I've been saving for a whole year!"],
 ["m06","maya","low","He shouted at me in front of everyone, so I went to the back and cried."],
 ["m07","maya","tense","No. That was not okay. You don't speak to people like that."],
 ["m08","maya","low","Paati's in hospital, and I'm so far away… I just want to be there."],
 ["m09","maya","low","Oh, Sam… Bruno was family. Take your time."],
 ["m10","maya","normal","When I think about it, Colombo taught me to be brave."]
]''')
VOICE = {"sam": "leo", "maya": "tara"}
OUT = "/kaggle/working"; os.makedirs(f"{OUT}/clips", exist_ok=True)
report = ["# Run 1 · stage 1: Orpheus recording + Gate 1 (smoke run)", ""]
dev = "cuda:0"
try:
    log("loading Orpheus (unsloth/orpheus-3b-0.1-ft, fp16) + SNAC")
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    model = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to(dev).eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(dev)
    log(f"loaded; GPU memory {torch.cuda.memory_allocated(0)/1e9:.1f} GB")

    def to_audio(ids):
        ids = ids.tolist()
        if 128258 in ids: ids = ids[:ids.index(128258)]          # stop at the end-of-speech token (padding follows)
        if 128257 in ids: ids = ids[len(ids) - ids[::-1].index(128257):]
        ids = [t for t in ids if t >= 128266]
        ids = ids[: len(ids) // 7 * 7]
        c = [t - 128266 for t in ids]
        l1, l2, l3 = [], [], []
        for i in range(len(c) // 7):
            l1.append(c[7*i]); l2.append(c[7*i+1] - 4096)
            l3 += [c[7*i+2] - 2*4096, c[7*i+3] - 3*4096]
            l2.append(c[7*i+4] - 4*4096)
            l3 += [c[7*i+5] - 5*4096, c[7*i+6] - 6*4096]
        if not l1 or min(l1 + l2 + l3) < 0 or max(l1 + l2 + l3) > 4095: return None
        codes = [torch.tensor(x, device=dev).unsqueeze(0) for x in (l1, l2, l3)]
        with torch.inference_mode(): return snac.decode(codes).squeeze().float().cpu().numpy()

    def record_batch(items, n=2):
        """items: list of (text, voice). Returns, per item, n audio arrays (or None)."""
        prompts = []
        for text, voice in items:
            p = tok(f"{voice}: {text}").input_ids
            prompts.append([128259] + p + [128009, 128260])
        L = max(map(len, prompts))
        ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device=dev)
        att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device=dev)
        with torch.inference_mode():
            g = model.generate(ids, attention_mask=att, max_new_tokens=1600, do_sample=True,
                               temperature=0.6, top_p=0.95, repetition_penalty=1.1, num_return_sequences=n,
                               eos_token_id=128258, pad_token_id=128263)
        outs = [to_audio(x[L:]) for x in g]
        return [outs[i * n:(i + 1) * n] for i in range(len(items))]

    log("loading Whisper large-v3-turbo")
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:1" if torch.cuda.device_count() > 1 else dev)
    meter = pyloudnorm.Meter(24000)
    norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split()
    NAMES = {"thenuka", "galle", "paati", "paati's", "madurai", "chennai", "colombo", "bruno", "maya", "sam", "jaffna", "kottu"}
    plain = lambda s: [w for w in norm(s) if w not in NAMES]

    rows = []; gen_s = 0.0; audio_s = 0.0
    B = 8; batches = [lines[i:i + B] for i in range(0, len(lines), B)]
    results = {}
    for b in batches:
        t = time.time(); got = record_batch([(text, VOICE[who]) for _, who, _, text in b]); gen = time.time() - t; gen_s += gen
        log(f"batch of {len(b)} lines × 2 takes in {gen:.0f} s")
        for line, takes in zip(b, got): results[line[0]] = takes
    for lid, who, row, text in lines:
        takes = results[lid]
        best = None
        for k, a in enumerate(takes):
            r = dict(id=lid, who=who, row=row, take=k + 1, text=text)
            if a is None or len(a) < 2400: r.update(ok=False, why="no audio"); rows.append(r); continue
            peak = float(np.abs(a).max())
            a, _ = librosa.effects.trim(a, top_db=40)
            a = np.concatenate([np.zeros(2400), a, np.zeros(2400)]).astype(np.float32)   # 0.1 s each end
            dur = len(a) / 24000; audio_s += dur
            lufs = meter.integrated_loudness(a) if dur > 0.5 else -70
            a = pyloudnorm.normalize.loudness(a, lufs, -20.0) if lufs > -60 else a
            heard = asr(a.copy(), generate_kwargs={"language": "en"})["text"].strip()
            wer = jiwer.wer(" ".join(plain(text)), " ".join(plain(heard)) or "x")   # names aside (Whisper doesn't know them)
            names_heard = [w for w in norm(text) if w in NAMES and w not in norm(heard)]
            wps = len(norm(text)) / max(dur - 0.2, 0.1)
            f = f"clips/{lid}_t{k+1}.wav"; sf.write(f"{OUT}/{f}", np.clip(a, -1, 1), 24000)
            ok = wer == 0 and peak < 0.99 and dur > 0.5
            why = [] if ok else [w for w, bad in (("words", wer > 0), ("clipped", peak >= 0.99), ("too short", dur <= 0.5)) if bad]
            r.update(ok=ok, why=",".join(why), names_misheard=" ".join(names_heard), file=f, seconds=round(dur, 2), words_per_s=round(wps, 2), peak=round(peak, 3), lufs_before=round(lufs, 1), wer=round(wer, 3), heard=heard)
            rows.append(r)
            if ok and (best is None or abs(wps - 2.5) < abs(best["words_per_s"] - 2.5)): best = r
        if best: best["kept"] = True
        log(f"{lid} {who}/{row}: {'kept take ' + str(best['take']) if best else 'NONE passed'}")

    # manifest + report + listening file (kept takes, in order)
    import csv
    keys = ["id", "who", "row", "take", "kept", "ok", "why", "names_misheard", "seconds", "words_per_s", "wer", "peak", "lufs_before", "file", "text", "heard"]
    with open(f"{OUT}/manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in rows]
    kept = [r for r in rows if r.get("kept")]
    takes_n = sum(1 for r in rows if "file" in r); passed = sum(1 for r in rows if r.get("ok"))
    pieces = []
    for r in kept:
        pieces += [sf.read(f"{OUT}/{r['file']}")[0], np.zeros(int(24000 * 0.7))]
    if pieces:
        sf.write(f"{OUT}/listen.wav", np.concatenate(pieces).astype(np.float32), 24000)
        sh(f"ffmpeg -loglevel error -y -i {OUT}/listen.wav -b:a 64k {OUT}/run1_orpheus_listen.mp3 && rm {OUT}/listen.wav")
    sam = [r["words_per_s"] for r in kept if r["who"] == "sam"]; maya = [r["words_per_s"] for r in kept if r["who"] == "maya"]
    report += [f"- Lines: {len(lines)} · takes made: {takes_n} · passed Gate 1 (words exact, no clipping): **{passed}** · lines with a kept take: **{len(kept)}/{len(lines)}**",
               f"- Recording time: {gen_s/60:.1f} min for {audio_s/60:.1f} min of audio ({audio_s/max(gen_s,1):.2f}× real time on one T4, 8 lines × 2 takes per batch)",
               f"- Pace (words per second, kept): Sam {np.mean(sam) if sam else 0:.2f} · Maya {np.mean(maya) if maya else 0:.2f}",
               f"- GPU memory peak: {torch.cuda.max_memory_allocated(0)/1e9:.1f} GB (GPU 0)", "",
               "## Failed takes", ""]
    report += [f"- {r['id']} take {r.get('take')}: {r.get('why')} · heard: “{r.get('heard','')}”" for r in rows if not r.get("ok")] or ["(none)"]
    report += ["", "## Names Whisper heard differently (not counted as failures)", ""]
    report += [f"- {r['id']} take {r['take']}: {r['names_misheard']} · heard: “{r['heard']}”" for r in rows if r.get("names_misheard")] or ["(none)"]
    report += ["", "## Kept", "", "| id | who | row | s | words/s | text |", "|---|---|---|---|---|---|"]
    report += [f"| {r['id']} | {r['who']} | {r['row']} | {r['seconds']} | {r['words_per_s']} | {r['text']} |" for r in kept]
    report += ["", "RESULT: PASS (stage 1 code works)" if kept else "RESULT: FAIL (no clip passed)"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc(), "```"]
    print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{OUT}/report.md", "w").write("\n".join(report) + "\n")

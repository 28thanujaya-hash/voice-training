# Same measures as run5_measure (so numbers compare with the 1,661 run-5 clips) + the quality checks (gap, flat hold, hiss)
# and the agreed mood rules (claude/mood-rules.md, 17 Nov).
import re, numpy as np, librosa, parselmouth, pyloudnorm, cmudict
from num2words import num2words
CMU = cmudict.dict(); SR = 24000; meter = pyloudnorm.Meter(SR)
def syllables(text):
    t = re.sub(r"(\d[\d,]*)", lambda m: " " + num2words(int(m.group(1).replace(",", ""))) + " ", text); n = 0
    for w in re.findall(r"[a-zA-Z']+", t.lower()):
        if w in CMU: n += sum(ch[-1].isdigit() for ch in CMU[w][0])
        else: n += max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))
    return n
def cpp_h1h2(y, sr, t_f0):
    N = int(0.04 * sr); win = np.hanning(N); cpps, hh = [], []; q = np.arange(N) / sr
    for t, f0 in t_f0:
        a = int(t * sr - N / 2)
        if a < 0 or a + N > len(y): continue
        fr = y[a:a + N] * win
        if np.max(np.abs(fr)) < 1e-4: continue
        spec = np.abs(np.fft.rfft(fr, 4 * N)); ldb = 20 * np.log10(spec + 1e-9)
        cep = np.fft.irfft(ldb)[:N]; cdb = 20 * np.log10(np.abs(cep) + 1e-9)
        lo, hi = int(sr / 600), int(sr / 75); pk = np.arange(lo, hi)[np.argmax(cdb[lo:hi])]
        k = np.arange(int(0.001 * sr), N // 2); p = np.polyfit(q[k], cdb[k], 1); cpps.append(cdb[pk] - np.polyval(p, q[pk]))
        fbin = sr / (4 * N)
        def amp(f):
            i0, i1 = int(f * 0.9 / fbin), int(f * 1.1 / fbin) + 1
            return np.max(ldb[i0:i1]) if i1 < len(ldb) else np.nan
        hh.append(amp(f0) - amp(2 * f0))
    return (float(np.nanmedian(cpps)) if cpps else np.nan, float(np.nanmedian(hh)) if hh else np.nan)
def measure(y, text):
    sr = SR; st = lambda f: 12 * np.log2(f / 100.0); syl = syllables(text)
    iv = librosa.effects.split(y, top_db=30, frame_length=1024, hop_length=240)
    s0, s1 = iv[0][0] / sr, iv[-1][1] / sr; span = max(s1 - s0, 0.1)
    gaps = [(iv[i][0] - iv[i - 1][1]) / sr for i in range(1, len(iv))]
    P = [g for g in gaps if g >= 0.15]; ptot = sum(P)
    snd = parselmouth.Sound(y.astype(np.float64), sr)
    pt = snd.to_pitch_ac(time_step=0.01, pitch_floor=100, pitch_ceiling=600)
    f0 = pt.selected_array["frequency"]; tt = pt.xs(); v = (f0 > 0) & (tt >= s0) & (tt <= s1)
    d = dict(syl=syl, dur=span, artic=syl / max(span - ptot, 0.1), pause_share=ptot / span)
    if v.sum() >= 10:
        s = st(f0[v]); t = tt[v]; k = max(3, len(s) // 5)
        d.update(f0_med=np.median(s), f0_sd=np.std(s), slope=np.polyfit(t, s, 1)[0], final_drop=np.median(s[-k:]) - np.median(s[:-k]))
        d["cpp"], d["h1h2"] = cpp_h1h2(y, sr, list(zip(t, f0[v])))
    it = snd.to_intensity(minimum_pitch=100); idb = it.values[0]; ti = it.xs(); m = (ti >= s0) & (ti <= s1) & (idb > idb.max() - 30)
    if m.sum() >= 10:
        x = idb[m]; k = max(3, len(x) // 5); d["int_drop"] = np.mean(x[-k:]) - np.mean(x[:-k])
    try: d["lufs"] = meter.integrated_loudness(np.pad(y, (0, max(0, int(0.5 * sr) - len(y)))))
    except Exception: d["lufs"] = np.nan
    return d
def quality(y):
    sr = SR; hop = int(0.01 * sr)
    iv = librosa.effects.split(y, top_db=35, frame_length=1024, hop_length=240)
    gaps = [(iv[i][0] - iv[i-1][1]) / sr for i in range(1, len(iv))]
    a = max(0, iv[0][0] - int(0.1 * sr)); b = min(len(y), iv[-1][1] + int(0.1 * sr)); y = y[a:b]
    f0, vf, _ = librosa.pyin(y, fmin=100, fmax=700, sr=sr, frame_length=2048, hop_length=hop)
    st = 12 * np.log2(np.where(vf, f0, np.nan) / 100); flat = run = 0
    for i in range(1, len(st)):
        if np.isfinite(st[i]) and np.isfinite(st[i-1]):
            j = i - run - 1; run = run + 1 if np.nanmax(st[j:i+1]) - np.nanmin(st[j:i+1]) <= 1.0 else 0
        else: run = 0
        flat = max(flat, run)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop)) ** 2; fr = librosa.fft_frequencies(sr=sr, n_fft=1024)
    share = S[fr > 4000].sum(0) / np.maximum(S.sum(0), 1e-12); lvl = 10 * np.log10(np.maximum(S.sum(0), 1e-12))
    h = (share > 0.9) & (lvl > lvl.max() - 35); hiss = run = 0
    for x in h: run = run + 1 if x else 0; hiss = max(hiss, run)
    return y, dict(gap=max(gaps) if gaps else 0.0, hold=flat * hop / sr, hiss=hiss * hop / sr)
def rules(d, q, ref, mood):
    """list of failed rules (empty = pass). Numbers vs Maya's clean normal."""
    g = lambda k: d.get(k, np.nan) - ref[k]
    sp = (d["artic"] - ref["artic"]) / ref["artic"] * 100
    R = {"low": [("speed 15-40% slower", -40 <= sp <= -15), ("≥2 dB quieter", g("lufs") <= -2), ("breathier ≥+3 dB", g("h1h2") >= 3)],
         "tense": [("pitch ≥+2 st", g("f0_med") >= 2), ("≥10% faster", sp >= 10), ("≥3 dB louder", g("lufs") >= 3),
                   ("falls through line", g("slope") < 0), ("end ≥3 dB quieter", g("int_drop") <= -3)],
         "bright": [("≥6 syllables", d["syl"] >= 6), ("pitch ≥+2.5 st", g("f0_med") >= 2.5), ("movement ≥+0.8", g("f0_sd") >= 0.8),
                    ("end not quieter", g("int_drop") >= -1), ("end fall gentle", g("final_drop") >= -5), ("not breathy", g("h1h2") <= 1.5), ("not slower", sp >= -5)]}[mood]
    R += [("gap ≤0.5 s", q["gap"] <= 0.5), ("no flat hold >0.5 s", q["hold"] <= 0.5), ("no hiss >0.15 s", q["hiss"] <= 0.15)]
    return [n for n, ok in R if not ok], sp

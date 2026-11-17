# New mood measures (GPT acoustic review, 17 Nov), shared by run5_measure and run6_pack. measure(dict(path=..., text=...)).
import re
import numpy as np, soundfile as sf, librosa, pyloudnorm, parselmouth, cmudict
from num2words import num2words
CMU = cmudict.dict()
def syllables(text):
    t = re.sub(r"(\d[\d,]*)", lambda m: " " + num2words(int(m.group(1).replace(",", ""))) + " ", text)
    n = 0
    for w in re.findall(r"[a-zA-Z']+", t.lower()):
        if w in CMU: n += sum(ch[-1].isdigit() for ch in CMU[w][0])
        else: n += max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))
    return n
meter = pyloudnorm.Meter(24000)
st = lambda f: 12 * np.log2(f / 100.0)
def cpp_h1h2(y, sr, t_f0):
    # CPP (cepstral peak prominence) and H1-H2 on voiced 40 ms frames; uncorrected H1-H2
    N = int(0.04 * sr); win = np.hanning(N); cpps, hh = [], []
    q = np.arange(N) / sr
    for t, f0 in t_f0:
        a = int(t * sr - N / 2)
        if a < 0 or a + N > len(y): continue
        fr = y[a:a + N] * win
        if np.max(np.abs(fr)) < 1e-4: continue
        spec = np.abs(np.fft.rfft(fr, 4 * N)); ldb = 20 * np.log10(spec + 1e-9)
        cep = np.fft.irfft(ldb); cep = cep[:N]; cdb = 20 * np.log10(np.abs(cep) + 1e-9)
        lo, hi = int(sr / 600), int(sr / 75); qs = np.arange(lo, hi)
        pk = qs[np.argmax(cdb[lo:hi])]
        k = np.arange(int(0.001 * sr), N // 2); p = np.polyfit(q[k], cdb[k], 1)
        cpps.append(cdb[pk] - np.polyval(p, q[pk]))
        fbin = sr / (4 * N)
        def amp(f):
            i0, i1 = int(f * 0.9 / fbin), int(f * 1.1 / fbin) + 1
            return np.max(ldb[i0:i1]) if i1 < len(ldb) else np.nan
        hh.append(amp(f0) - amp(2 * f0))
    return (float(np.nanmedian(cpps)) if cpps else np.nan, float(np.nanmedian(hh)) if hh else np.nan)
def measure(c):
    y, sr = sf.read(c["path"], dtype="float32")
    if y.ndim > 1: y = y.mean(1)
    text = c["text"]; syl = syllables(text)
    iv = librosa.effects.split(y, top_db=30, frame_length=1024, hop_length=240)
    s0, s1 = iv[0][0] / sr, iv[-1][1] / sr; span = max(s1 - s0, 0.1)
    gaps = [(iv[i][0] - iv[i - 1][1]) / sr for i in range(1, len(iv))]
    starts = [iv[i - 1][1] / sr for i in range(1, len(iv))]
    P = [(g, s) for g, s in zip(gaps, starts) if g >= 0.15]
    ptot = sum(g for g, _ in P)
    snd = parselmouth.Sound(y.astype(np.float64), sr)
    pt = snd.to_pitch_ac(time_step=0.01, pitch_floor=100, pitch_ceiling=600)
    f0 = pt.selected_array["frequency"]; tt = pt.xs()
    v = (f0 > 0) & (tt >= s0) & (tt <= s1)
    d = dict(syl=syl, dur=round(span, 3),
             syl_s=syl / span, artic=syl / max(span - ptot, 0.1), pauses=len(P), pause_s=ptot, pause_share=ptot / span,
             first_pause=((P[0][1] - s0) / span) if P else np.nan)
    if v.sum() >= 10:
        s = st(f0[v]); t = tt[v]; n = len(s); k = max(3, n // 5)
        d.update(f0_med=np.median(s), f0_sd=np.std(s), f0_rng=np.percentile(s, 90) - np.percentile(s, 10),
                 slope=np.polyfit(t, s, 1)[0], final_drop=np.median(s[-k:]) - np.median(s[:-k]))
        fin = t >= t[-1] - 0.4
        d["final_slope"] = np.polyfit(t[fin], s[fin], 1)[0] if fin.sum() >= 5 else np.nan
        d["cpp"], d["h1h2"] = cpp_h1h2(y, sr, list(zip(t, f0[v])))
    it = snd.to_intensity(minimum_pitch=100); idb = it.values[0]; ti = it.xs(); m = (ti >= s0) & (ti <= s1) & (idb > idb.max() - 30)
    if m.sum() >= 10:
        x = idb[m]; k = max(3, len(x) // 5)
        d.update(int_sd=np.std(x), int_drop=np.mean(x[-k:]) - np.mean(x[:-k]))
    hn = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=100).values[0]; hn = hn[hn > -100]
    d["hnr"] = float(np.median(hn)) if len(hn) else np.nan
    try: d["lufs"] = meter.integrated_loudness(np.pad(y, (0, max(0, int(0.5 * sr) - len(y)))))
    except Exception: d["lufs"] = np.nan
    S = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / sr)
    d["tilt"] = 10 * np.log10(S[fr > 1000].sum() / max(S[(fr > 60) & (fr <= 1000)].sum(), 1e-12))
    return d

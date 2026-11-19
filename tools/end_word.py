"""Measure how a take ends (its last word), from the mp3.

Usage (module): end_features(path) -> dict
  end_hi    median pitch of the last 0.25 s of voice, st above the line's own median
  end_peak  highest pitch in the last 0.6 s of voice, st above the line's median
  end_fall  last 0.1 s of voice minus the peak of the last 0.6 s (0 = ends on top, −5 = falls 5 st)
  end_rise  last 0.1 s minus the first 0.1 s of the last 0.6 s
  end_loud  loudness of the last 0.4 s of voice minus the line's median (dB)
  end_len   length of the last unbroken voiced stretch (s): a drawn-out last word is longer
"""
import numpy as np, librosa

SR, HOP = 22050, 256


def end_features(path):
    y, _ = librosa.load(path, sr=SR)
    f0, vf, _ = librosa.pyin(y, fmin=110, fmax=600, sr=SR, hop_length=HOP)
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0][: len(f0)]
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    v = np.where(vf & np.isfinite(f0))[0]
    if len(v) < 10: return None
    st = 12 * np.log2(f0 / 100.0)
    med = np.nanmedian(st[v]); fr = HOP / SR
    last = v[-1]
    tail = v[v >= last - int(0.6 / fr)]; t25 = v[v >= last - int(0.25 / fr)]; t10 = v[v >= last - int(0.1 / fr)]
    head10 = tail[tail <= tail[0] + int(0.1 / fr)]
    run = 1
    for i in range(len(v) - 1, 0, -1):
        if v[i] - v[i - 1] <= 3: run += 1
        else: break
    loud_tail = db[max(0, last - int(0.4 / fr)): last + 1]
    loud_line = db[v[0]: last + 1]
    return dict(end_hi=np.median(st[t25]) - med, end_peak=np.max(st[tail]) - med,
                end_fall=np.median(st[t10]) - np.max(st[tail]), end_rise=np.median(st[t10]) - np.median(st[head10]),
                end_loud=np.median(loud_tail) - np.median(loud_line), end_len=run * fr)

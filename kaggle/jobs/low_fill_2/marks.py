# Mark measurements, copied from run4_audit (same thresholds): CTC alignment (wav2vec2-large-960h) + torchcrepe pitch + energy.
import re, unicodedata, numpy as np, torch, librosa, torchcrepe
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
WH = {"what", "where", "when", "why", "who", "whom", "whose", "which", "how"}
def setup(dev):
    global proc, ctc, VOC, BLANK, SEP, dev2
    dev2 = dev
    proc = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
    ctc = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self").to(dev).eval()
    VOC = proc.tokenizer.get_vocab(); BLANK = VOC[proc.tokenizer.pad_token]; SEP = VOC["|"]
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


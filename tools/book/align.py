"""Line up a LibriVox reading with its Project Gutenberg text, sentence by sentence, and measure how each
sentence was read. Runs on a GitHub CPU machine (tools/book/README in book_align.yml).

Usage: python tools/book/align.py <archive_item> <gutenberg_id> <chapter> [<chapter> ...]
Writes out/ch<NN>.csv (one row per sentence) and out/ch<NN>_words.json (Whisper words with times).

Per sentence: paragraph, dialogue or narration, start/end in the chapter mp3, how much of it Whisper matched,
and measures against the reader's own NARRATION in that chapter (her neutral voice):
  rate      words per second, % vs narration median
  loud      dB vs narration median
  pitch     median pitch, semitones vs narration median
  move      pitch spread (sd), semitones minus narration's
  end_hi / end_fall / end_rise   how the last word ends (as tools/end_word.py)
  pauses    pauses inside the sentence > 0.2 s, with the word before each and the pitch jump after it
"""
import json, os, re, sys, unicodedata, urllib.request, difflib
import numpy as np

ITEM, GID, CHAPTERS = sys.argv[1], sys.argv[2], [int(c) for c in sys.argv[3:]]
os.makedirs("out", exist_ok=True)
UA = {"User-Agent": "voice-training research (github.com/28thanujaya-hash/voice-training)"}


def get(url, path=None):
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=300).read()
    if path: open(path, "wb").write(data)
    return data


# ---------- text: Gutenberg -> chapters -> paragraphs -> sentences ----------
def book_chapters():
    raw = None
    for url in (f"https://www.gutenberg.org/cache/epub/{GID}/pg{GID}.txt", f"https://www.gutenberg.org/files/{GID}/{GID}-0.txt"):
        try: raw = get(url).decode("utf-8", "replace"); break
        except Exception as e: print("text fetch failed", url, e)
    raw = raw.replace("\r\n", "\n")
    s = raw.find("*** START"); e = raw.find("*** END")
    body = raw[raw.find("\n", s) + 1: e if e > 0 else None]
    parts = re.split(r"\n\s*CHAPTER\s+([IVXLC]+)\.?[^\n]*\n", body)
    chaps = {}
    for i in range(1, len(parts) - 1, 2):   # a contents list also matches; keep the longest text per chapter number
        n = roman(parts[i])
        if len(parts[i + 1]) > len(chaps.get(n, "")): chaps[n] = parts[i + 1]
    print("chapters in text:", sorted(chaps)[:5], "…", len(chaps))
    return chaps


def roman(s):
    v = dict(I=1, V=5, X=10, L=50, C=100); t = 0
    for a, b in zip(s, s[1:] + " "):
        t += -v[a] if b != " " and v.get(b, 0) > v[a] else v[a]
    return t


ABBR = re.compile(r"\b(Mr|Mrs|Dr|St|Mt|Jr|Sr)\.")


def sentences(chapter_text):
    out = []
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", chapter_text) if p.strip()]
    for pi, p in enumerate(paras):
        p = p.replace("--", "—").replace("_", "")
        q = ABBR.sub(lambda m: m.group(1) + "\u2024", p)          # protect "Mrs." from splitting
        sents = [m.group(0).strip() for m in re.finditer(r'.+?(?:[.!?]+["”’\']?|$)(?=\s+["“‘\']?[A-Z]|\s*$)', q)]
        inq = False
        for s in sents:
            s = s.replace("\u2024", ".")
            qn = s.count('"') + s.count("“") + s.count("”")
            dialogue = inq or s.startswith(('"', "“"))
            if qn % 2: inq = not inq
            out.append(dict(para=pi, text=s, dialogue=dialogue))
    return out, paras


def norm_words(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace("—", " ")
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", s)


# ---------- audio ----------
def audio_files():
    meta = json.loads(get(f"https://archive.org/metadata/{ITEM}"))
    mp3 = [f["name"] for f in meta["files"] if f["name"].endswith(".mp3") and "64kb" in f["name"]]
    if not mp3: mp3 = [f["name"] for f in meta["files"] if f["name"].endswith(".mp3")]
    mp3.sort(); print("audio files:", len(mp3), mp3[:3])
    return mp3


def main():
    from faster_whisper import WhisperModel
    import librosa
    chaps = book_chapters(); files = audio_files()
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    for ch in CHAPTERS:
        name = files[ch - 1]; path = f"/tmp/ch{ch:02d}.mp3"
        get(f"https://archive.org/download/{ITEM}/{urllib.request.quote(name)}", path)
        segs, _ = model.transcribe(path, word_timestamps=True, beam_size=1, vad_filter=False, language="en")
        W = [dict(w=w.word.strip(), s=w.start, e=w.end) for sg in segs for w in sg.words]
        json.dump(dict(file=name, words=W), open(f"out/ch{ch:02d}_words.json", "w"))
        print(f"ch{ch}: {name}, {len(W)} words heard")
        S, paras = sentences(chaps[ch])
        # word lists with owners
        bw, owner = [], []
        for si, s in enumerate(S):
            for t in norm_words(s["text"]): bw.append(t); owner.append(si)
        aw, ai = [], []
        for k, w in enumerate(W):
            for t in norm_words(w["w"]): aw.append(t); ai.append(k)
        sm = difflib.SequenceMatcher(None, bw, aw, autojunk=False)
        match = {}
        for a, b, n in sm.get_matching_blocks():
            for j in range(n): match[a + j] = ai[b + j]
        # audio features for the whole chapter
        y, sr = librosa.load(path, sr=16000)
        hop = 256; fr = hop / sr
        f0, vf, _ = librosa.pyin(y, fmin=70, fmax=500, sr=sr, frame_length=1024, hop_length=hop)
        st = 12 * np.log2(np.where(vf, f0, np.nan) / 100.0)
        db = 20 * np.log10(np.maximum(librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0][: len(st)], 1e-6))
        rows = []
        for si, s in enumerate(S):
            idx = [k for k, o in enumerate(owner) if o == si]
            got = [match[k] for k in idx if k in match]
            r = dict(chapter=ch, para=s["para"], sent=si, dialogue=int(s["dialogue"]), text=s["text"],
                     words=len(idx), coverage=round(len(got) / max(1, len(idx)), 2))
            if len(got) >= max(2, 0.8 * len(idx)):
                t0, t1 = W[got[0]]["s"], W[got[-1]]["e"]
                a, b = int(t0 / fr), int(t1 / fr) + 1
                v = np.where(np.isfinite(st[a:b]))[0] + a
                r.update(start=round(t0, 2), end=round(t1, 2), rate=round(len(idx) / max(0.2, t1 - t0), 2),
                         loud=round(float(np.median(db[a:b])), 2))
                if len(v) > 8:
                    med = np.median(st[v]); last = v[-1]
                    tail = v[v >= last - int(0.6 / fr)]; t10 = v[v >= last - int(0.1 / fr)]; t25 = v[v >= last - int(0.25 / fr)]
                    h10 = tail[tail <= tail[0] + int(0.1 / fr)]
                    r.update(pitch=round(float(med), 2), move=round(float(np.std(st[v])), 2),
                             end_hi=round(float(np.median(st[t25]) - med), 2),
                             end_fall=round(float(np.median(st[t10]) - np.max(st[tail])), 2),
                             end_rise=round(float(np.median(st[t10]) - np.median(st[h10])), 2))
                # pauses between heard words inside the sentence
                ps = []
                for x, y2 in zip(got, got[1:]):
                    gap = W[y2]["s"] - W[x]["e"]
                    if gap > 0.2:
                        p0, p1 = int(W[x]["e"] / fr), int(W[y2]["s"] / fr)
                        bef = st[max(a, p0 - int(0.3 / fr)):p0]; aft = st[p1:p1 + int(0.3 / fr)]
                        jump = np.nanmedian(aft) - np.nanmedian(bef) if np.isfinite(bef).any() and np.isfinite(aft).any() else np.nan
                        ps.append(f"{W[x]['w']}|{gap:.2f}|{jump:+.1f}")
                r["pauses"] = " ".join(ps)
            rows.append(r)
        # relative to her narration in this chapter
        nar = [r for r in rows if not r["dialogue"] and "rate" in r]
        ref = {k: np.median([r[k] for r in nar if k in r]) for k in ("rate", "loud", "pitch", "move")} if nar else {}
        for r in rows:
            for k in ref:
                if k in r: r[k + "_rel"] = round(r[k] / ref[k] * 100 - 100, 1) if k == "rate" else round(r[k] - ref[k], 2)
        import csv
        cols = ["chapter", "para", "sent", "dialogue", "text", "words", "coverage", "start", "end", "rate", "loud", "pitch", "move",
                "rate_rel", "loud_rel", "pitch_rel", "move_rel", "end_hi", "end_fall", "end_rise", "pauses"]
        with open(f"out/ch{ch:02d}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
        json.dump(paras, open(f"out/ch{ch:02d}_paras.json", "w"))
        ok = sum(1 for r in rows if "rate" in r)
        print(f"ch{ch}: {len(rows)} sentences, {ok} lined up ({ok / max(1, len(rows)):.0%}), dialogue {sum(r['dialogue'] for r in rows)}")


if __name__ == "__main__":
    main()

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
    d = "/".join(GID[:-1]) + "/" + GID if len(GID) > 1 else "0/" + GID   # mirror folder layout: 45 -> 4/45
    urls = [f"https://www.gutenberg.org/cache/epub/{GID}/pg{GID}.txt", f"https://aleph.gutenberg.org/{d}/{GID}-0.txt",
            f"https://gutenberg.pglaf.org/{d}/{GID}-0.txt", f"http://mirrors.xmission.com/gutenberg/{d}/{GID}-0.txt",
            f"https://gutenberg.readingroo.ms/{d}/{GID}-0.txt", f"https://www.gutenberg.org/files/{GID}/{GID}-0.txt",
            f"https://aleph.gutenberg.org/{d}/{GID}.txt", f"https://gutenberg.pglaf.org/{d}/{GID}.txt"]
    import time
    for attempt in range(3):
        for url in urls:
            try: raw = get(url).decode("utf-8", "replace"); print("text from", url); break
            except Exception as e: print("text fetch failed", url, e)
        if raw: break
        time.sleep(30)
    if not raw: raise SystemExit("no book text from any mirror")
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


SAY = r"(?:said|cried|exclaimed|asked|retorted|wailed|pleaded|demanded|whispered|sobbed|answered|replied|murmured|added|repeated|continued|protested|gasped|explained|declared|remarked|returned|interrupted|called|began|went on|admitted|groaned|sighed|laughed|giggled|shrieked|screamed|moaned|snapped|urged|ventured|stammered|faltered|breathed|observed|inquired|suggested|insisted|agreed|said Mrs|confided|announced)"
NAME = r"((?:Mrs\.|Mr\.|Miss|Aunt|Uncle)\s+[A-Z][a-z]+|[A-Z][a-z]+)"
NOT_NAME = {"She", "He", "They", "It", "I", "We", "You", "The", "Then", "But", "And", "Oh", "Well", "Yes", "No"}


def tokens_with_quotes(text, inq):
    """Split a sentence into words, each marked as inside quotes (speech) or not (narration / 'she said')."""
    out = []
    for m in re.finditer(r'["“”]|[^"“”]+', text):
        t = m.group(0)
        if t in '"“”':
            inq = (t == "“") or (t == '"' and not inq)
            if t == "”": inq = False
            continue
        for w in norm_words(t): out.append((w, inq))
    return out, inq


def guess_speaker(narr):
    for pat in (SAY + r"\s+(?:the\s+[a-z]+\s+)?" + NAME, NAME + r"\s+" + SAY, NAME + r"[’']s\s+\w+\s+(?:response|reply|comment|answer)"):
        for m in re.finditer(pat, narr):
            n = [g for g in m.groups() if g and g[0].isupper()]
            if n and n[0] not in NOT_NAME: return n[0].replace("Mrs. ", "Mrs ").replace("Mr. ", "Mr ")
    return ""


def sentences(chapter_text):
    out = []
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", chapter_text) if p.strip()]
    spk_hist = []
    for pi, p in enumerate(paras):
        p = p.replace("--", "—").replace("_", "")
        q = ABBR.sub(lambda m: m.group(1) + "\u2024", p)          # protect "Mrs." from splitting
        sents = [m.group(0).strip().replace("\u2024", ".") for m in re.finditer(r'.+?(?:[.!?]+["”’\']?|$)(?=\s+["“‘\']?[A-Z]|\s*$)', q)]
        has_speech = bool(re.search(r'["“]', p))
        narr = re.sub(r'“[^”]*”|"[^"]*"', " ", p)
        spk, src = (guess_speaker(narr), "tag") if has_speech else ("", "")
        if has_speech and not spk and len(spk_hist) >= 2 and spk_hist[-1] != spk_hist[-2]:
            spk, src = spk_hist[-2], "turns"                       # two people talking: turns alternate
        if has_speech: spk_hist.append(spk or "?")
        inq = False
        for s in sents:
            toks, inq2 = tokens_with_quotes(s, inq)
            speech = [w for w, iq in toks if iq]
            out.append(dict(para=pi, text=s, dialogue=bool(speech), toks=toks, speaker=spk if speech else "", spk_src=src if speech else ""))
            inq = inq2
    return out, paras


def norm_words(s):
    s = re.sub(r"[—–-]", " ", s.replace("’", "'").replace("‘", "'"))   # before ascii: keep apostrophes, split on dashes
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
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
        y, sr = librosa.load(path, sr=16000)   # decode here (faster-whisper's own decoder breaks on newer PyAV)
        segs, _ = model.transcribe(y, word_timestamps=True, beam_size=1, vad_filter=False, language="en")
        W = [dict(w=w.word.strip(), s=w.start, e=w.end) for sg in segs for w in sg.words]
        json.dump(dict(file=name, words=W), open(f"out/ch{ch:02d}_words.json", "w"))
        print(f"ch{ch}: {name}, {len(W)} words heard")
        S, paras = sentences(chaps[ch])
        # word lists with owners
        bw, owner, isq = [], [], []
        for si, s in enumerate(S):
            for t, iq in s["toks"]: bw.append(t); owner.append(si); isq.append(iq)
        aw, ai = [], []
        for k, w in enumerate(W):
            for t in norm_words(w["w"]): aw.append(t); ai.append(k)
        sm = difflib.SequenceMatcher(None, bw, aw, autojunk=False)
        match = {}
        for a, b, n in sm.get_matching_blocks():
            for j in range(n): match[a + j] = ai[b + j]
        # audio features for the whole chapter
        hop = 256; fr = hop / sr
        f0, vf, _ = librosa.pyin(y, fmin=110, fmax=500, sr=sr, frame_length=1024, hop_length=hop)
        st = 12 * np.log2(np.where(vf, f0, np.nan) / 100.0)
        db = 20 * np.log10(np.maximum(librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0][: len(st)], 1e-6))
        def feats(got, nwords):
            """Measures over the given heard words only (speech part, or the whole sentence for narration)."""
            if len(got) < 2: return {}
            runs, cur = [], [got[0]]
            for x, y2 in zip(got, got[1:]):
                if y2 == x + 1 or W[y2]["s"] - W[x]["e"] < 1.5: cur.append(y2)
                else: runs.append(cur); cur = [y2]
            runs.append(cur)
            dur = sum(W[r_[-1]]["e"] - W[r_[0]]["s"] for r_ in runs)
            fidx = np.concatenate([np.arange(int(W[r_[0]]["s"] / fr), int(W[r_[-1]]["e"] / fr) + 1) for r_ in runs])
            fidx = fidx[fidx < len(st)]
            o = dict(start=round(W[got[0]]["s"], 2), end=round(W[got[-1]]["e"], 2), rate=round(nwords / max(0.2, dur), 2),
                     loud=round(float(np.median(db[fidx])), 2))
            v = fidx[np.isfinite(st[fidx])]
            lr = runs[-1]; la, lb = int(W[lr[0]]["s"] / fr), int(W[lr[-1]]["e"] / fr) + 1
            lv = np.where(np.isfinite(st[la:lb]))[0] + la
            if len(v) > 8 and len(lv) > 4:
                med = np.median(st[v]); last = lv[-1]
                tail = lv[lv >= last - int(0.6 / fr)]; t10 = lv[lv >= last - int(0.1 / fr)]; t25 = lv[lv >= last - int(0.25 / fr)]
                h10 = tail[tail <= tail[0] + int(0.1 / fr)]
                o.update(pitch=round(float(med), 2), move=round(float(np.std(st[v])), 2),
                         end_hi=round(float(np.median(st[t25]) - med), 2),
                         end_fall=round(float(np.median(st[t10]) - np.max(st[tail])), 2),
                         end_rise=round(float(np.median(st[t10]) - np.median(st[h10])), 2))
            ps = []
            for r_ in runs:
                for x, y2 in zip(r_, r_[1:]):
                    gap = W[y2]["s"] - W[x]["e"]
                    if gap > 0.2:
                        p0, p1 = int(W[x]["e"] / fr), int(W[y2]["s"] / fr)
                        bef = st[max(0, p0 - int(0.3 / fr)):p0]; aft = st[p1:p1 + int(0.3 / fr)]
                        jump = np.nanmedian(aft) - np.nanmedian(bef) if np.isfinite(bef).any() and np.isfinite(aft).any() else np.nan
                        ps.append(f"{W[x]['w']}|{gap:.2f}|{jump:+.1f}")
            o["pauses"] = " ".join(ps)
            return o

        rows = []
        for si, s in enumerate(S):
            idx = [k for k, o in enumerate(owner) if o == si]
            got = [match[k] for k in idx if k in match]
            sp_idx = [k for k in idx if isq[k]] if s["dialogue"] else idx
            sp_got = [match[k] for k in sp_idx if k in match]
            r = dict(chapter=ch, para=s["para"], sent=si, dialogue=int(s["dialogue"]), speaker=s["speaker"], spk_src=s["spk_src"],
                     text=s["text"], speech=" ".join(w for w, iq in s["toks"] if iq) if s["dialogue"] else "",
                     words=len(sp_idx), coverage=round(len(sp_got) / max(1, len(sp_idx)), 2))
            if len(sp_got) >= max(2, 0.8 * len(sp_idx)): r.update(feats(sp_got, len(sp_idx)))
            rows.append(r)
        # relative to her narration in this chapter
        nar = [r for r in rows if not r["dialogue"] and "rate" in r]
        ref = {k: np.median([r[k] for r in nar if k in r]) for k in ("rate", "loud", "pitch", "move")} if nar else {}
        for r in rows:
            for k in ref:
                if k in r: r[k + "_rel"] = round(r[k] / ref[k] * 100 - 100, 1) if k == "rate" else round(r[k] - ref[k], 2)
        import csv
        cols = ["chapter", "para", "sent", "dialogue", "speaker", "spk_src", "text", "speech", "words", "coverage", "start", "end", "rate", "loud", "pitch", "move",
                "rate_rel", "loud_rel", "pitch_rel", "move_rel", "end_hi", "end_fall", "end_rise", "pauses"]
        with open(f"out/ch{ch:02d}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
        json.dump(paras, open(f"out/ch{ch:02d}_paras.json", "w"))
        ok = sum(1 for r in rows if "rate" in r)
        print(f"ch{ch}: {len(rows)} sentences, {ok} lined up ({ok / max(1, len(rows)):.0%}), dialogue {sum(r['dialogue'] for r in rows)}")


if __name__ == "__main__":
    main()

# Run 4 · mood control experiment (no training). G2 showed the 4 mood rows sound alike on matched lines (same words, 4 moods):
# pitch level/range nearly identical per row. Cause to test: each row's voicepack is an average of many clips' styles, which
# washes the mood out. Settings tried on teacher A and B (30 matched sentences × 4 moods):
#   base   : the trained voicepacks
#   x2     : normal + 2 × (row − normal), whole style vector
#   x3p    : prosody half × 3 (style dims 128–255 drive duration/pitch/energy), acoustic half from the row
#   x5p    : prosody half × 5
# Measured: pitch level / range / pace per row, mood guessed from pitch+pace (cross-validated), word error, naturalness,
# sounds like tara (vs the same model's base normal), cosine between row voicepacks. Named clips of one sentence × 4 moods
# for the best two settings.
import glob, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from test_data import TEST
from textprep import prepare_all
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 4 · mood control experiment (voicepack settings, no training)", ""]
try:
    sh("pip install -q 'transformers==4.57.6' jiwer soundfile librosa torchcrepe scikit-learn loguru munch einops einops-exts nltk pydub accelerate")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    import marks as MK
    MK.setup("cuda")
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4")
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex")
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP); K = f"{TMP}/kt"
    import types
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro"); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    from huggingface_hub import hf_hub_download
    kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    models, packs = {}, {}
    for tag in ("A", "B"):
        f = glob.glob(f"/kaggle/input/**/kokoro_maya_v02_{tag}.pth", recursive=True)[0]; d = os.path.dirname(f)
        models[tag] = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f).to("cuda").eval()
        packs[tag] = {r: torch.load(f"{d}/maya_{r}_voicepack.pt", map_location="cpu", weights_only=True).float() for r in ROWS}
        P = packs[tag]; flat = {r: P[r].reshape(P[r].shape[0], -1).mean(0) for r in ROWS}
        cs = lambda a, b: float(torch.nn.functional.cosine_similarity(a, b, dim=0))
        report += [f"{tag}: voicepack shape {tuple(P['normal'].shape)}; cosine to normal: " + ", ".join(f"{r} {cs(flat[r], flat['normal']):.4f}" for r in ROWS[1:]) +
                   " · prosody half: " + ", ".join(f"{r} {cs(flat[r][128:], flat['normal'][128:]):.4f}" for r in ROWS[1:]) +
                   " · acoustic half: " + ", ".join(f"{r} {cs(flat[r][:128], flat['normal'][:128]):.4f}" for r in ROWS[1:])]
    report.append("")
    def setting(P, row, name):
        n, x = P["normal"], P[row]
        if name == "base" or row == "normal": return x
        if name == "x2": return n + 2 * (x - n)
        k = {"x3p": 3, "x5p": 5}[name]; y = x.clone(); y[..., 128:] = n[..., 128:] + k * (x[..., 128:] - n[..., 128:]); return y
    SETTINGS = ["base", "x2", "x3p", "x5p"]
    MT = [t for t in TEST if t[2] == "matched"]
    _, ph = prepare_all([t[3] for t in MT], f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex"); PH = dict(zip([t[0] for t in MT], ph))
    from transformers import pipeline as hfp, AutoFeatureExtractor, WavLMForXVector
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda"); _wn = asr.tokenizer.normalize
    wn = lambda s: [w for w in _wn(s.replace("…", " ").replace("—", " ")).split() if re.search(r"[a-z0-9]", w)]
    utmos = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True).to("cuda").eval()
    r16 = lambda a: librosa.resample(a.astype(np.float32), orig_sr=24000, target_sr=16000)
    fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv"); xv = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").cuda().eval()
    def spk(a):
        with torch.no_grad():
            x = fe(r16(a), sampling_rate=16000, return_tensors="pt").to("cuda"); return torch.nn.functional.normalize(xv(**x).embeddings, dim=-1)[0].cpu().numpy()
    R = {}; AUD = {}
    for tag in models:
        for sname in SETTINGS:
            for tid, row, kind, text in MT:
                p = PH[tid][:510]; vp = setting(packs[tag], row, sname)
                with torch.no_grad(): out = models[tag](p, vp[len(p) - 1].to("cuda"), 1.0)
                a = (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy(); AUD[(tag, sname, tid)] = a
                h = asr(a.copy(), generate_kwargs={"language": "en"})["text"]; ref, hyp = wn(text), wn(h) or ["x"]
                bad = sum(max(x.ref_end_idx - x.ref_start_idx, x.hyp_end_idx - x.hyp_start_idx) for x in jiwer.process_words(" ".join(ref), " ".join(hyp)).alignments[0] if x.type != "equal")
                with torch.no_grad(): ms = float(utmos(torch.tensor(r16(a))[None].cuda(), 16000).item())
                try: m = MK.measure(a, text)
                except Exception: m = None
                R[(tag, sname, tid)] = dict(row=row, bad=bad, n=len(ref), mos=ms, spk=spk(a), m=m, wps=len(text.split()) / max(len(a) / 24000, .1))
            log(f"{tag} {sname} done")
    from sklearn.linear_model import LogisticRegression; from sklearn.model_selection import cross_val_score
    report += ["## Matched lines: per setting", "", "| model | setting | normal | bright | low | tense | mood from pitch+pace | word error | naturalness | same voice |",
               "|---|---|---|---|---|---|---|---|---|---|"]
    best = []
    for tag in models:
        cen = np.mean([R[(tag, "base", t[0])]["spk"] for t in MT if t[1] == "normal"], 0); cen /= np.linalg.norm(cen)
        for sname in SETTINGS:
            xs = [(t, R[(tag, sname, t[0])]) for t in MT]
            cells = []
            for row in ROWS:
                v = [x for t, x in xs if t[1] == row and x["m"]]
                cells.append(f"{np.median([x['m']['body'] for x in v]):.1f} / {np.median([x['m']['rng'] for x in v]):.1f} / {np.median([x['wps'] for x in v]):.2f}")
            v = [x for t, x in xs if x["m"]]
            acc = cross_val_score(LogisticRegression(max_iter=1000), np.array([[x["m"]["body"], x["m"]["rng"], x["wps"]] for x in v]),
                                  np.array([ROWS.index(x["row"]) for x in v]), cv=5).mean()
            we = 100 * sum(x["bad"] for t, x in xs) / max(sum(x["n"] for t, x in xs), 1); mo = np.mean([x["mos"] for t, x in xs]); sv = np.mean([x["spk"] @ cen for t, x in xs])
            report.append(f"| {tag} | {sname} | " + " | ".join(cells) + f" | {100*acc:.0f}% | {we:.1f}% | {mo:.2f} | {sv:.3f} |")
            if we < 6 and mo > 3.5: best.append((acc, tag, sname))
    report += ["", "Cells: pitch level / pitch range (semitones) / pace (words per second). Chance for the mood guess = 25%.", ""]
    best.sort(reverse=True); pick = best[:2] if best else [(0, "B", "base")]
    report += ["Best settings that keep words and naturalness (word error < 6%, naturalness > 3.5): " + ", ".join(f"{t} {s} ({100*a:.0f}%)" for a, t, s in pick), ""]
    os.makedirs(f"{W}/listen", exist_ok=True)
    sent = sorted({t[0][:-1] for t in MT})[3]
    for _, tag, sname in pick + [(0, pick[0][1], "base")]:
        for row in ROWS:
            tid = sent + row[0]
            sf.write(f"{TMP}/c.wav", AUD[(tag, sname, tid)], 24000); sh(f"ffmpeg -loglevel error -y -i {TMP}/c.wav -b:a 64k {W}/listen/mood_{tag}_{sname}_{row}.mp3")
    report += [f"Clips: listen/mood_<model>_<setting>_<mood>.mp3 — sentence: “{[t[3] for t in MT if t[0].startswith(sent)][0]}”", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

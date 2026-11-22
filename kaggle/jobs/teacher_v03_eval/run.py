# teacher v0.3 · eval: do the 4 style rows sound like 4 moods? Student lines (held out, never trained; split.csv) are spoken in
# EVERY row by teacher v0.3 (and stock Kokoro af_heart as a baseline). Judge: Meta superb (pass rule as for the actor), Whisper words.
# Main number: per row, share judged as that row's mood (normal: neutral or mild). Teacher v0.2 failed here (rows alike).
import csv, glob, os, re, subprocess, sys, time, traceback, types
sys.path.insert(0, os.getcwd())
from student_data import STUDENT
from textprep import prepare_all
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True); os.makedirs(f"{W}/clips", exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]; KEY = {"normal": "neutral", "bright": "happy", "low": "sad", "tense": "angry"}
def log(s): s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if p.returncode: raise RuntimeError((p.stdout + p.stderr)[-2000:])
report = ["# teacher v0.3 · eval: rows vs moods on held-out student lines", ""]
try:
    sh("pip install -q 'transformers==4.57.6' jiwer soundfile librosa loguru munch einops einops-exts nltk pydub accelerate")
    import numpy as np, torch, soundfile as sf, librosa, jiwer
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4")
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex")
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP); K = f"{TMP}/kt"
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak"); sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro"); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    heart = torch.load(hf_hub_download("hexgrad/Kokoro-82M", "voices/af_heart.pt"), map_location="cpu", weights_only=True)
    f = glob.glob("/kaggle/input/**/kokoro_f_v03_*.pth", recursive=True)[0]; d = os.path.dirname(f); log(f"model {f}")
    models = {"v03": (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f).to("cuda").eval(), {r: torch.load(f"{d}/f_{r}_voicepack.pt", map_location="cpu", weights_only=True) for r in ROWS}),
              "stock": (KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=kp).to("cuda").eval(), {r: heart for r in ROWS})}
    _, PH = prepare_all([s["text"] for s in STUDENT], f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex")
    from transformers import pipeline as hfp, AutoFeatureExtractor, HubertForSequenceClassification
    asr = hfp("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda")
    N = "superb/hubert-large-superb-er"; jfe = AutoFeatureExtractor.from_pretrained(N); jm = HubertForSequenceClassification.from_pretrained(N).eval().to("cuda")
    JL = [{"neu": "neutral", "hap": "happy", "sad": "sad", "ang": "angry"}.get(jm.config.id2label[i], jm.config.id2label[i]) for i in range(len(jm.config.id2label))]
    norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("…", " ").replace("—", " ")).split()
    rows = []
    for tag, (km, vps) in models.items():
        for s, p in zip(STUDENT, PH):
            for row in ROWS:
                p2 = p[:510]
                with torch.no_grad(): out = km(p2, vps[row][len(p2) - 1], 1.0)
                a = (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()
                z = librosa.effects.trim(librosa.resample(a, orig_sr=24000, target_sr=16000), top_db=35)[0]
                with torch.no_grad(): pr = torch.softmax(jm(**jfe(z, sampling_rate=16000, return_tensors="pt").to("cuda")).logits.float()[0], -1).tolist()
                P = dict(zip(JL, pr)); judged = max(P, key=P.get)
                ok = (judged == "neutral" or max(P["happy"], P["sad"], P["angry"]) <= .5) if row == "normal" else (judged == KEY[row] and P[KEY[row]] > .5)
                heard = asr(a.copy(), generate_kwargs={"language": "en"})["text"]; wer = jiwer.wer(" ".join(norm(s["text"])), " ".join(norm(heard)) or "x")
                rows.append(dict(model=tag, id=s["id"], line_mood=s["mood"], row=row, judged=judged, ok=int(ok), wer=round(wer, 3), **{"p_" + k: round(v, 3) for k, v in P.items()}))
                if tag == "v03" and len([r for r in rows if r["model"] == "v03" and r["row"] == row]) <= 12: sf.write(f"{W}/clips/{s['id']}_{row}.wav", a, 24000)
        log(f"{tag} done")
    with open(f"{W}/eval.csv", "w", newline="") as fh: w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    report += ["| model | row | pass | judged neutral / happy / sad / angry | word error |", "|---|---|---|---|---|"]
    for tag in models:
        for row in ROWS:
            x = [r for r in rows if r["model"] == tag and r["row"] == row]; c = {k: sum(r["judged"] == k for r in x) for k in ("neutral", "happy", "sad", "angry")}
            report.append(f"| {tag} | {row} | {sum(r['ok'] for r in x)}/{len(x)} | {c['neutral']} / {c['happy']} / {c['sad']} / {c['angry']} | {np.mean([r['wer'] for r in x]):.2f} |")
    report += ["", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]; open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

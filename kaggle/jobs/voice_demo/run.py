# Voice demo (15 Nov, user ask): one sentence per expression mark, new sentences (never trained on).
# For each: Orpheus tara (the actor, = what the training data sounds like) then the current best teacher (Kokoro, stage 2 part 1,
# trained on run-3 data). The CAPS line is also rendered with the new ↗ emphasis rule (teacher never trained on it yet).
import glob, os, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from textprep import prepare_all, g2p_raw, _names, _times
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
LINES = [("plain", "normal", "I usually take the bus to class in the morning."),
         ("?", "normal", "Did you finish your homework before dinner?"),
         ("!", "bright", "We won the match last night!"),
         ("…", "low", "I waited for him all evening… but he never came."),
         ("—", "tense", "Listen to me — you cannot leave the door open."),
         ("?!", "bright", "You ate the whole cake by yourself?!"),
         ("CAPS", "tense", "I said the RED bag, not the blue one.")]
ROWS = ["normal", "bright", "low", "tense"]
report = ["# Voice demo: one sentence per expression", ""]
try:
    sh("pip install -q 'transformers==4.57.6' snac soundfile librosa")
    import torch, numpy as np, soundfile as sf, librosa, shutil, csv
    # ---- Orpheus tara (2 takes, keep the first that decodes)
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained("unsloth/orpheus-3b-0.1-ft")
    om = AutoModelForCausalLM.from_pretrained("unsloth/orpheus-3b-0.1-ft", torch_dtype=torch.float16).to("cuda").eval()
    from snac import SNAC
    snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to("cuda")
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
        with torch.inference_mode(): return snac.decode([torch.tensor(x, device="cuda")[None] for x in (l1, l2, l3)]).squeeze().float().cpu().numpy()
    texts = [t for _, _, t in LINES]
    prompts = [[128259] + tok(f"tara: {s}").input_ids + [128009, 128260] for s in texts]; L = max(map(len, prompts))
    ids = torch.tensor([[128263] * (L - len(p)) + p for p in prompts], device="cuda")
    att = torch.tensor([[0] * (L - len(p)) + [1] * len(p) for p in prompts], device="cuda")
    with torch.inference_mode():
        g = om.generate(ids, attention_mask=att, max_new_tokens=1200, do_sample=True, temperature=0.6, top_p=0.95, repetition_penalty=1.1,
                        num_return_sequences=2, eos_token_id=128258, pad_token_id=128263)
    orph = []
    for k in range(len(texts)):
        a = [to_audio(g[2 * k + j][L:]) for j in range(2)]; a = [x for x in a if x is not None]
        orph.append(librosa.effects.trim(a[0], top_db=40)[0] if a else np.zeros(2400, np.float32))
    del om; torch.cuda.empty_cache(); log("Orpheus done")

    # ---- misaki-g2p (same as the phone)
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4")
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex")
    cli, lex = f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex"
    old_ph = g2p_raw([_names(_times(t)) for t in texts], cli, lex)          # how the teacher was trained
    _, new_ph = prepare_all([LINES[-1][2]], cli, lex)                        # CAPS with ↗
    report += ["Sounds given to the teacher:", ""] + [f"- {m}: `{p}`" for (m, _, _), p in zip(LINES, old_ph)] + [f"- CAPS with ↗: `{new_ph[0]}`", ""]

    # ---- teacher: stage 2 part 1 + voicepacks extracted from the kept run-3 clips
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"
    sh("pip install -q munch einops einops-exts nltk pydub accelerate loguru")
    sh(f"pip install -q 'torchaudio=={torch.__version__.split('+')[0]}' || true")
    from huggingface_hub import hf_hub_download
    kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)[0]; src = os.path.dirname(tr)
    for r in csv.DictReader(open(tr)):
        os.makedirs(f"{TMP}/by/{r['row']}", exist_ok=True); shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['row']}/")
    st1 = glob.glob("/kaggle/input/**/kokoro_maya_v01_stage1.pth", recursive=True)[0]
    p1 = glob.glob("/kaggle/input/**/s2_part1.pth", recursive=True)[0]
    for row in ROWS:
        sh(f"python scripts/extract_voicepack.py --model {p1} --style-encoder-model {st1} --audio-dir {TMP}/by/{row} --output {TMP}/vp_{row}.pt --device cuda", cwd=K)
    kw = {k: {("module." + a if not a.startswith("module.") else a): b for a, b in torch.load(p1, map_location="cpu", weights_only=False)["net"][k].items()}
          for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}
    torch.save(kw, f"{TMP}/p1.pth")
    import types
    class _Stub(types.ModuleType):
        def __getattr__(self, n):
            if n.startswith("__"): raise AttributeError(n)
            return type(n, (), {})
    mk = _Stub("misaki"); mk.en = _Stub("misaki.en"); mk.espeak = _Stub("misaki.espeak")
    sys.modules.update({"misaki": mk, "misaki.en": mk.en, "misaki.espeak": mk.espeak})
    sh(f"pip install -q --no-deps -e {K}/kokoro"); sys.path.insert(0, f"{K}/kokoro")
    from kokoro.model import KModel
    km = KModel(repo_id="hexgrad/Kokoro-82M", config=kc, model=f"{TMP}/p1.pth").to("cuda").eval()
    vps = {r: torch.load(f"{TMP}/vp_{r}.pt", map_location="cpu", weights_only=True) for r in ROWS}
    def say(p, row):
        p = p[:510]
        with torch.no_grad(): out = km(p, vps[row][len(p) - 1], 1.0)
        return (out.audio if hasattr(out, "audio") else out).squeeze().float().cpu().numpy()
    teach = [say(p, row) for (_, row, _), p in zip(LINES, old_ph)]
    caps_new = say(new_ph[0], LINES[-1][1])

    # ---- one file: for each line, actor then teacher (CAPS: + teacher with ↗)
    gap = lambda s: np.zeros(int(24000 * s), np.float32)
    pieces = []; key = ["# Voice demo: order of clips", "", "| # | mark | mood | voice | sentence |", "|---|---|---|---|---|"]; n = 0
    for i, (m, row, t) in enumerate(LINES):
        seq = [("Maya: Orpheus actor", orph[i]), ("Maya: teacher (phone voice's parent)", teach[i])]
        if m == "CAPS": seq.append(("teacher with ↗ rule (not trained on it yet)", caps_new))
        for v, a in seq:
            n += 1; pieces += [a.astype(np.float32), gap(0.8)]; key.append(f"| {n} | {m} | {row} | {v} | {t} |")
        pieces.append(gap(0.8))
    sf.write(f"{TMP}/d.wav", np.concatenate(pieces), 24000)
    sh(f"ffmpeg -loglevel error -y -i {TMP}/d.wav -b:a 96k {W}/voice_demo.mp3")
    open(f"{W}/voice_demo_key.md", "w").write("\n".join(key) + "\n")
    report += ["RESULT: OK"]
except Exception:
    report += ["RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

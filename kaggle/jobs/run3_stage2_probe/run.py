
# Run 3 · stage-2 MEMORY PROBE (14 Nov). Why stage 2 runs out of memory on a T4 at the joint epoch, and which setting fits.
# Each setting runs train_second.py from the try-2 stage-1 checkpoint with the joint phase from step 1 (joint_epoch 0),
# for PROBE_STEPS steps, in its own process; peak memory per GPU, time per step and the adversarial losses are logged.
import csv, glob, json, os, random, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
PROBE_STEPS = 20
EPOCHS_1, EPOCHS_2, JOINT = 10, 1, 0
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"   # 13 Nov: stage 2 ran out of memory (T4, SLM adversarial)
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh_log(c, cwd, logfile):
    """Long training: stream everything to a file in /kaggle/working (kept even if it fails); return code."""
    log("$ " + c[:160] + f"  (log: {os.path.basename(logfile)})")
    with open(logfile, "w") as fh: rc = subprocess.run(c, shell=True, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    tail = open(logfile).read().splitlines()[-15:]; [print("   " + l) for l in tail]
    ep = [l for l in open(logfile).read().splitlines() if "Epoch [" in l]
    if ep: log("last progress: " + ep[-1][:160])
    return rc
def sh(c, cwd=None, tail=40):
    log("$ " + c[:160])
    p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    for l in out[-tail:]: print("   " + l)
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
report = ["# Run 3 · stage-2 memory probe v5 (transformers 4.57.6 + SLM step enabled: batch_percentage 1.0)", ""]; steps = []
def step(name, ok, note=""):
    steps.append((name, ok, note)); log(f"STEP {name}: {'OK' if ok else 'FAILED'} {note}")


# ---- TextPrep: must match the app's TextPrep (Paradee.kt)
NAMES = {"Thenuka": "tˈɛnʊkə", "Kavi": "kˈʌvi", "Nimal": "nˈɪməl", "Priya": "pɹˈiə", "Galle": "ɡˈɑl", "kottu": "kˈOtu",
         "Peradeniya": "pˌɛɹədˈɛnijə",
         # provisional, not yet in the app list
         "Paati": "pˈɑti", "Paati's": "pˈɑtiz", "Madurai": "mˈɑdʊɹI", "Chennai": "ʧɛnˈI", "Jaffna": "ʤˈɑfnə"}
def prepare(t):
    def tm(m):
        h, mm = m.group(1), m.group(2)
        return f"{h} o'clock" if mm == "00" else (f"{h} oh {mm[1]}" if mm[0] == "0" else f"{h} {mm}")
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", tm, t)
    names = sorted(NAMES, key=len, reverse=True)
    return re.sub(r"\b(" + "|".join(map(re.escape, names)) + r")(?![\w'])", lambda m: f"[{m.group(1)}](/{NAMES[m.group(1)]}/)", t)

try:
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)
    if not tr: raise RuntimeError("run3_maya_rejudge outputs not found under /kaggle/input")
    src = os.path.dirname(tr[0]); rows = list(csv.DictReader(open(tr[0])))
    log(f"kept clips: {len(rows)} from {src}")

    # ---- misaki-g2p (same code as the phone)
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=3)
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex", tail=2)
    def phon(texts):
        p = subprocess.run([f"{TMP}/mb/misaki-g2p-cli", "--lex", f"{TMP}/misaki-en-us.lex"], input="\n".join(prepare(t) for t in texts) + "\n", capture_output=True, text=True, check=True)
        return [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
    for r, p in zip(rows, phon([r["text_b"] for r in rows])): r["ph"] = p
    step("words → sounds (misaki-g2p)", True, f"{len(rows)} lines")

    # ---- recipe
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=5)
    import torch
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    raw = torch.load(kp, map_location="cpu", weights_only=False)
    strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")
    step("recipe + Kokoro base ready", True, f"torch {torch.__version__}")

    # ---- data lists; 10 clips (spread over rows) held back for validation
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True)
    for row in ROWS: os.makedirs(f"{TMP}/by/{row}", exist_ok=True)
    lines = []
    for r in rows:
        f = os.path.basename(r["file"]); shutil.copy(f"{src}/{r['file']}", f"{AUD}/{f}"); shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['row']}/{f}")
        lines.append(f"{f}|{r['ph']}|0")
    val = lines[::29][:10]; train = [l for l in lines if l not in val]
    open(f"{K}/training/train_list.txt", "w").write("\n".join(train) + "\n")
    open(f"{K}/training/val_list.txt", "w").write("\n".join(val) + "\n")
    open(f"{K}/training/OOD_texts.txt", "w").write("\n".join(r["ph"] for r in rows) + "\n")
    import yaml
    cfg = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    cfg.update(batch_size=2, epochs=EPOCHS_2, epochs_1st=EPOCHS_1, epochs_2nd=EPOCHS_2, save_freq=2, max_len=200,
               pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=f"{TMP}/logs/run3", load_only_params=True)
    cfg["data_params"].update(train_data=f"{K}/training/train_list.txt", val_data=f"{K}/training/val_list.txt",
                              root_path=AUD, OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
    cfg["loss_params"]["joint_epoch"] = JOINT
    cfg["save_freq"] = 1
    cfg.setdefault("slmadv_params", {}).update(max_len=250, batch_percentage=0.5)   # was 500: out of memory on a T4
    yaml.safe_dump(cfg, open(f"{K}/configs/run3.yml", "w"), sort_keys=False)

    st1 = glob.glob("/kaggle/input/**/kokoro_maya_v01_stage1.pth", recursive=True)
    if not st1: raise RuntimeError("try-2 stage-1 checkpoint not found under /kaggle/input")
    log(f"stage-1 checkpoint: {st1[0]}")
    # ---- v4: WavLM diagnosis (probe v3 crashed: the WavLM judge expects 13 layers x 768, got 28416 = 37 x 768)
    DIAG = r"""
import torch, transformers, json
from transformers import AutoModel
m = AutoModel.from_pretrained("microsoft/wavlm-base-plus")
for p in m.parameters(): p.requires_grad = False
m.feature_extractor._requires_grad = False
out = {"transformers": transformers.__version__, "class": type(m).__name__, "num_hidden_layers": m.config.num_hidden_layers}
for mode in ("eval", "train"):
    getattr(m, mode)()
    try:
        ns = [len(m(input_values=torch.randn(2, 29000) * torch.ones(1, requires_grad=True), output_hidden_states=True).hidden_states) for _ in range(8)]
        out[mode] = ns
    except Exception as e: out[mode] = "error: " + str(e)[:200]
print("DIAG " + json.dumps(out))
"""
    open(f"{TMP}/diag.py", "w").write(DIAG)
    def diag(tag):
        o = sh(f"python {TMP}/diag.py", tail=3); d = json.loads([l for l in o.splitlines() if l.startswith("DIAG ")][-1][5:])
        log(f"WavLM diagnosis ({tag}): {d}"); report.extend([f"- WavLM diagnosis ({tag}): `{json.dumps(d)}`"]); return d
    report += ["## WavLM diagnosis", ""]
    # v5: always pin transformers 4.57 (the 2023 recipe's era): 5.x drops layers in train mode (layerdrop) and its hook-based
    # hidden-state capture appears to mix replicas under DataParallel (28416 = 37 x 768 channels in v3/v4)
    sh("pip install -q 'transformers==4.57.6'", tail=3); d = diag("transformers 4.57.6, eval and train mode, 8 calls each")
    ok = lambda d: all(isinstance(d.get(k), list) and set(d[k]) == {13} for k in ("eval", "train"))
    step("WavLM returns 13 layers in eval and train mode", ok(d), f"transformers {d.get('transformers')}")
    if not ok(d): raise RuntimeError("WavLM still does not return 13 hidden states; stopping before the probe (report to the mentor)")
    report.append("")
    # input-shape guard: every WavLM call gets (batch, samples); a (batch, 1, samples) input is flattened. Harmless if already 2-D.
    lsrc = open(f"{S}/losses.py").read()
    lnew = re.sub(r"self\.wavlm\(input_values=([^,]+), output_hidden_states=True\)",
                  lambda m: f"self.wavlm(input_values=({m.group(1)}).reshape(-1, ({m.group(1)}).shape[-1]), output_hidden_states=True)", lsrc)
    log(f"losses.py: {lsrc.count('self.wavlm(input_values=')} WavLM calls; {sum(1 for x, y in zip(lsrc.splitlines(), lnew.splitlines()) if x != y)} lines patched")
    open(f"{S}/losses.py", "w").write(lnew)
    tsrc = open(f"{S}/train_second.py").read()
    # v3 hooks: A right after the main backward (every step), B before iters+=1 (only reached when the SLM step ran)
    anchA = "            g_loss.backward()\n"; anchB = "            iters = iters + 1\n"
    assert tsrc.count(anchA) == 1 and tsrc.count(anchB) == 1, "probe anchors not found"
    rec = """            _pm = [round(torch.cuda.max_memory_allocated(d) / 2**30, 2) for d in range(torch.cuda.device_count())]
            _lv = {k: (float(v) if hasattr(v, "item") else float(v or 0)) for k, v in dict(gen=locals().get("loss_gen_all", 0), slm=locals().get("loss_gen_lm", 0), dslm=locals().get("d_loss_slm", 0), disc=locals().get("d_loss", 0)).items()}
"""
    hookA = anchA + rec + """            globals()["_PSTEP"] = globals().get("_PSTEP", 0) + 1
            print("PROBE " + __import__("json").dumps(dict(where="main", step=globals()["_PSTEP"], peak_gb=_pm, t=__import__("time").time(), **_lv)), flush=True)
            if globals()["_PSTEP"] > PROBE_STEPS: __import__("os")._exit(0)
"""
    hookB = rec + """            print("PROBE " + __import__("json").dumps(dict(where="slm", step=globals().get("_PSTEP", 0), peak_gb=_pm, t=__import__("time").time(), **_lv)), flush=True)
""" + anchB
    open(f"{S}/train_second_probe.py", "w").write(tsrc.replace(anchA, hookA).replace(anchB, hookB).replace("import ", f"PROBE_STEPS = {PROBE_STEPS}\nimport ", 1))
    # v3: batch 2 with slmadv batch_percentage 1.0 (with 0.5 the SLM step needs >1 clip of 0.5*2=1 and always returns None)
    SETTINGS = [("crop200_slm500", 200, 2, 500), ("crop200_slm250", 200, 2, 250), ("crop150_slm250", 150, 2, 250), ("crop120_slm250", 120, 2, 250)]
    results = []
    for name, crop, bs, slmlen in SETTINGS:
        ld = f"{TMP}/logs/{name}"; os.makedirs(ld, exist_ok=True); shutil.copy(st1[0], f"{ld}/first_stage.pth")
        c = json.loads(json.dumps(cfg)); c.update(batch_size=bs, max_len=crop, epochs=1, epochs_2nd=1, log_dir=ld, save_freq=99)
        c["loss_params"]["joint_epoch"] = 0
        c["slmadv_params"].update(max_len=slmlen, batch_percentage=1.0)
        yaml.safe_dump(c, open(f"{K}/configs/{name}.yml", "w"), sort_keys=False)
        t = time.time(); rc = sh_log(f"python train_second_probe.py --config_path {K}/configs/{name}.yml", S, f"{W}/probe_{name}.txt")
        txt = open(f"{W}/probe_{name}.txt").read(); allp = [json.loads(l[6:]) for l in txt.splitlines() if l.startswith("PROBE ")]
        pr = [p for p in allp if p["where"] == "main"]; ps = [p for p in allp if p["where"] == "slm"]
        oom = "OutOfMemoryError" in txt or "out of memory" in txt
        dt = [b["t"] - a["t"] for a, b in zip(pr, pr[1:])]
        r = dict(name=name, crop=crop, batch=bs, rc=rc, oom=oom, steps=len(pr),
                 peak=[max(p["peak_gb"][d] for p in allp) for d in range(len(allp[0]["peak_gb"]))] if allp else None,
                 s_per_step=round(sum(dt) / len(dt), 1) if dt else None,
                 slm_steps=sum(1 for p in ps if p["slm"] != 0), gen_steps=sum(1 for p in pr if p["gen"] != 0),
                 minutes=round((time.time() - t) / 60, 1))
        results.append(r); log(f"PROBE RESULT {r}")
        step(f"probe {name}", rc == 0 and not oom and len(pr) >= PROBE_STEPS, f"{len(pr)} steps, peak GB {r['peak']}, {r['s_per_step']} s/step, adversarial steps {r['slm_steps']}")
    json.dump(results, open(f"{W}/probe_results.json", "w"), indent=1)
    report += ["## Memory probe (joint phase from step 1; T4 = 14.56 GB usable)", "",
               "| setting | crop (frames) | batch | finished | out of memory | steps | peak GB GPU0 / GPU1 | s per step | steps with generator adversarial loss | steps with SLM adversarial loss |",
               "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        report.append(f"| {r['name']} | {r['crop']} | {r['batch']} | {'yes' if r['rc']==0 else 'no'} | {'YES' if r['oom'] else 'no'} | {r['steps']} | {' / '.join(map(str, r['peak'] or []))} | {r['s_per_step']} | {r['gen_steps']} | {r['slm_steps']} |")
    report += ["", "Crop frames: 80 frames ≈ 1 s of speech. Each setting started fresh from the same stage-1 checkpoint."]
except Exception:
    tb = traceback.format_exc(); print(tb); step("ERROR", False, ""); report += ["```", tb[-3000:], "```", ""]
report[2:2] = ["| step | result | note |", "|---|---|---|"] + [f"| {n} | {'✅' if ok else '❌'} | {note} |" for n, ok, note in steps] + [""]
report += ["RESULT: DONE", "", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

# Run 4 · teacher v0.2, part 1: Kokoro stage 1 (acoustic) on the audited Maya takes (run4_audit/train.csv, text_b).
# TextPrep with the CAPS ↗ rule (kaggle/common/textprep.py); split by whole sentence (training / validation from the plan);
# balanced sampling: every mood × mark cell repeated up to 3× towards ~30 entries (over-full cells used once).
# Stage 1: 5 epochs (the balanced list is ~2.3× run 3's, so ≈ the same number of steps as run 3's 10 epochs).
# Outputs: kokoro_maya_v02_stage1.pth + train/val/OOD lists (phonemes) for the stage-2 jobs (A with adversarial, B without).
import csv, glob, os, re, shutil, subprocess, sys, time, traceback
from collections import Counter
sys.path.insert(0, os.getcwd())
from textprep import prepare_all
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
EPOCHS_1 = 5
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None, tail=30):
    log("$ " + c[:160]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines(); [print("   " + l) for l in out[-tail:]]
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
    return "\n".join(out)
def sh_log(c, cwd, logfile):
    log("$ " + c[:160] + f"  (log: {os.path.basename(logfile)})")
    with open(logfile, "w") as fh: rc = subprocess.run(c, shell=True, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    [print("   " + l) for l in open(logfile).read().splitlines()[-15:]]; return rc
def cell(text):
    for k, rx in [("?!", r"\?!"), ("CAPS", r"\b(?!I\b)[A-Z][A-Z']*[A-Z]\b"), ("—", "—"), ("…", "…"), ("?", r"\?"), ("!", "!")]:
        if re.search(rx, text): return k
    return "plain"
report = ["# Run 4 · teacher v0.2 · part 1: stage 1", ""]
try:
    sh("pip install -q 'transformers==4.57.6'", tail=2)
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True)
    if len(tr) != 1: raise RuntimeError(f"expected one train.csv, found {tr}")
    src = os.path.dirname(tr[0]); rows = list(csv.DictReader(open(tr[0])))
    log(f"{len(rows)} clips from {src}: " + str(Counter(r['split'] for r in rows)))
    sh("git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set tools/misaki-g2p", cwd=TMP)
    M = f"{TMP}/llm/tools/misaki-g2p"
    sh(f"cmake -S {M} -B {TMP}/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' && cmake --build {TMP}/mb -j4", tail=3)
    sh(f"python {M}/convert_misaki_lexicon.py --fetch {TMP}/lexc -o {TMP}/misaki-en-us.lex", tail=2)
    prep, ph = prepare_all([r["text_b"] for r in rows], f"{TMP}/mb/misaki-g2p-cli", f"{TMP}/misaki-en-us.lex")
    for r, p in zip(rows, ph): r["ph"] = p
    caps = [r["ph"] for r in rows if re.search(r"\b[A-Z]{2,}\b", r["text_b"]) and "↗" in r["ph"]]
    log(f"phonemes done; CAPS lines carrying ↗: {len(caps)}")

    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    from importlib import util as _u
    spec = _u.spec_from_file_location("ks", f"{S}/kokoro_symbols.py"); ks = _u.module_from_spec(spec); spec.loader.exec_module(ks)
    unknown = Counter(c for r in rows for c in r["ph"] if c not in ks.dicts)
    if unknown: raise RuntimeError(f"phoneme symbols not in Kokoro's table: {unknown}")
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=5)
    import torch
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth")
    raw = torch.load(kp, map_location="cpu", weights_only=False)
    strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")

    # ---- lists: split from the plan; balanced repeats
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True)
    tr_rows = [r for r in rows if r["split"] == "train"]; va_rows = [r for r in rows if r["split"] == "val"]
    for r in rows: shutil.copy(f"{src}/{r['file']}", f"{AUD}/{os.path.basename(r['file'])}")
    n = Counter((r["row"], cell(r["text"])) for r in tr_rows); rep = {c: max(1, min(3, round(30 / k))) for c, k in n.items()}
    train = [f"{os.path.basename(r['file'])}|{r['ph']}|0" for r in tr_rows for _ in range(rep[(r['row'], cell(r['text']))])]
    val = [f"{os.path.basename(r['file'])}|{r['ph']}|0" for r in va_rows]
    for name, L in (("train_list.txt", train), ("val_list.txt", val), ("OOD_texts.txt", [r["ph"] for r in rows])):
        open(f"{K}/training/{name}", "w").write("\n".join(L) + "\n"); shutil.copy(f"{K}/training/{name}", f"{W}/{name}")
    report += ["## Balanced training list (lines → entries per mood × mark)", "", "| mark | normal | bright | low | tense |", "|---|---|---|---|---|"]
    for k in ["plain", "?", "!", "…", "—", "?!", "CAPS"]:
        report.append(f"| {k} | " + " | ".join(f"{n.get((r, k), 0)} → {n.get((r, k), 0) * rep.get((r, k), 1)}" for r in ROWS) + " |")
    report += ["", f"Training: {len(tr_rows)} clips → {len(train)} entries · validation: {len(val)} clips (never trained on)", ""]

    import yaml
    cfg = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    cfg.update(batch_size=2, epochs=EPOCHS_1, epochs_1st=EPOCHS_1, epochs_2nd=1, save_freq=1, max_len=200,
               pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=f"{TMP}/logs/s1", load_only_params=True)
    cfg["data_params"].update(train_data=f"{K}/training/train_list.txt", val_data=f"{K}/training/val_list.txt",
                              root_path=AUD, OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
    yaml.safe_dump(cfg, open(f"{K}/configs/s1.yml", "w"), sort_keys=False)
    t = time.time(); rc = sh_log(f"python train_first.py --config_path {K}/configs/s1.yml", S, f"{W}/train_first_log.txt")
    c1 = sorted(glob.glob(f"{TMP}/logs/s1/epoch_1st_*.pth"), key=os.path.getmtime)
    if not c1: raise RuntimeError(f"stage 1 produced no checkpoint (rc {rc})")
    shutil.copy(c1[-1], f"{W}/kokoro_maya_v02_stage1.pth")
    ep = [l for l in open(f"{W}/train_first_log.txt").read().splitlines() if "Epoch [" in l]
    report += [f"Stage 1: {EPOCHS_1} epochs in {(time.time()-t)/60:.1f} min, rc {rc}; checkpoint {os.path.basename(c1[-1])} → kokoro_maya_v02_stage1.pth", "",
               "```", *[l[:240] for l in ep[-3:]], "```", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

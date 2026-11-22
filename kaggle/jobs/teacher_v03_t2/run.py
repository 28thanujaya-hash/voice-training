# teacher v0.3 · teacher v0.3, part 2: stage 2 joint phase from run4_t1's stage-1 checkpoint, one fresh process, 1 epoch over the
# balanced list (≈ run 3 part 1's 2 epochs in steps). Recipe from 15 Nov: transformers 4.57.6 first; slmadv batch_percentage 1.0,
# SLM max_len 500, crop 200, batch 2, joint from step 1; GPU cache cleared each epoch.
# settings.NOADV: A = False (adversarial on) · B = True (MPD/MSD discriminators off and the SLM adversarial step replaced by
# a zero loss; mel, F0, duration, WavLM feature loss, style and decoder training unchanged).
# Outputs: kokoro_f_v03_<A|B>.pth (Kokoro format) + maya_<row>_voicepack.pt; judged later in run4_eval (validation + test).
import glob, os, re, shutil, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
from settings import NOADV
TAG = "B" if NOADV else "A"
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
ROWS = ["normal", "bright", "low", "tense"]; EPOCHS_PER_PART = 1
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
report = [f"# teacher v0.3 · teacher v0.3 · stage 2 ({TAG}: {'without' if NOADV else 'with'} adversarial)", ""]
try:
    sh("pip install -q 'transformers==4.57.6'", tail=2)
    import csv
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True); src = os.path.dirname(tr[0]); rows = list(csv.DictReader(open(tr[0])))
    st1 = glob.glob("/kaggle/input/**/kokoro_f_v03_stage1.pth", recursive=True)[0]; L1 = os.path.dirname(st1)
    sh("git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    K = f"{TMP}/kt"; S = f"{K}/StyleTTS2"
    sh("pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile", tail=3)
    sh("git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .", cwd=TMP, tail=5)
    import torch
    sh("pip install -q 'torchaudio==%s' 2>&1 | tail -1 || true" % torch.__version__.split("+")[0], tail=2)
    from huggingface_hub import hf_hub_download
    kp = hf_hub_download("hexgrad/Kokoro-82M", "kokoro-v1_0.pth"); kc = hf_hub_download("hexgrad/Kokoro-82M", "config.json")
    raw = torch.load(kp, map_location="cpu", weights_only=False)
    strip = lambda d: {k.replace("module.", ""): v for k, v in d.items()}
    os.makedirs(f"{K}/training", exist_ok=True)
    torch.save({"net": {k: strip(raw[k]) for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}}, f"{K}/training/kokoro_base.pth")
    AUD = f"{TMP}/audio"; os.makedirs(AUD, exist_ok=True)
    for row in ROWS: os.makedirs(f"{TMP}/by/{row}", exist_ok=True)
    for r in rows:
        f = os.path.basename(r["file"]); shutil.copy(f"{src}/{r['file']}", f"{AUD}/{f}")
        if r["split"] == "train": shutil.copy(f"{src}/{r['file']}", f"{TMP}/by/{r['row']}/{f}")
    for name in ("train_list.txt", "val_list.txt", "OOD_texts.txt"): shutil.copy(f"{L1}/{name}", f"{K}/training/{name}")
    import yaml
    cfg = yaml.safe_load(open(f"{K}/configs/config_german_ft.yml"))
    ld = f"{TMP}/logs/s2"; os.makedirs(ld, exist_ok=True); shutil.copy(st1, f"{ld}/first_stage.pth")
    cfg.update(batch_size=2, epochs=99, epochs_1st=5, epochs_2nd=99, save_freq=1, max_len=200,
               pretrained_model=f"{K}/training/kokoro_base.pth", log_dir=ld, load_only_params=True)
    cfg["data_params"].update(train_data=f"{K}/training/train_list.txt", val_data=f"{K}/training/val_list.txt",
                              root_path=AUD, OOD_data=f"{K}/training/OOD_texts.txt", min_length=10, num_workers=2)
    cfg["loss_params"]["joint_epoch"] = 0
    cfg.setdefault("slmadv_params", {}).update(max_len=500, batch_percentage=1.0)
    yaml.safe_dump(cfg, open(f"{K}/configs/s2.yml", "w"), sort_keys=False)
    tsrc = open(f"{S}/train_second.py").read()
    a1 = "    for epoch in range(start_epoch, epochs):\n"; a2 = "            torch.save(state, save_path)\n"
    a3 = "            start_ds = True\n"; a4 = "                slm_out = slmadv(\n"
    for a in (a1, a2, a3, a4): assert tsrc.count(a) == 1, f"patch anchor not found: {a!r}"
    tsrc = tsrc.replace(a1, a1 + "        torch.cuda.empty_cache(); [torch.cuda.reset_peak_memory_stats(d) for d in range(torch.cuda.device_count())]\n")
    tsrc = tsrc.replace(a2, a2 + """            globals()["_DONE"] = globals().get("_DONE", 0) + 1
            print("PEAK_GB", [round(torch.cuda.max_memory_allocated(d) / 2**30, 2) for d in range(torch.cuda.device_count())], "saved", save_path, flush=True)
            if globals()["_DONE"] >= EPOCHS_PER_PART: __import__("os")._exit(0)
""")
    tsrc = tsrc.replace(a3, "            start_ds = not NOADV\n")
    tsrc = tsrc.replace(a4, "                slm_out = (torch.zeros(()).cuda(), torch.zeros((), requires_grad=True).cuda(), None) if NOADV else slmadv(\n")
    tsrc = tsrc.replace("import ", f"EPOCHS_PER_PART = {EPOCHS_PER_PART}\nNOADV = {NOADV}\nimport ", 1)
    open(f"{S}/train_second_part.py", "w").write(tsrc)
    t = time.time(); rc = sh_log(f"python train_second_part.py --config_path {K}/configs/s2.yml", S, f"{W}/train_second_log.txt")
    lg = open(f"{W}/train_second_log.txt").read()
    c2 = sorted(glob.glob(f"{ld}/epoch_2nd_*.pth"), key=os.path.getmtime)
    if not c2 or "OutOfMemory" in lg: raise RuntimeError(f"stage 2 failed (rc {rc}); see train_second_log.txt")
    gen = [float(x) for x in re.findall(r"Gen Loss: ([0-9.]+)", lg)]; glm = [float(x) for x in re.findall(r"GenLM Loss: ([0-9.]+)", lg)]
    ep = [l for l in lg.splitlines() if "Epoch [" in l]; peaks = [l for l in lg.splitlines() if l.startswith("PEAK_GB")]
    report += [f"Stage 2 ({TAG}): {EPOCHS_PER_PART} epoch in {(time.time()-t)/60:.1f} min; {peaks}",
               f"Log lines with Gen>0: {sum(1 for x in gen if x > 0)}/{len(gen)} · GenLM>0: {sum(1 for x in glm if x > 0)}/{len(glm)} "
               f"(expected {'0 and 0' if NOADV else 'all and all'})", "", "```", *[l[:240] for l in ep[-3:]], "```", ""]
    for row in ROWS:
        sh(f"python scripts/extract_voicepack.py --model {c2[-1]} --style-encoder-model {st1} --audio-dir {TMP}/by/{row} --output {W}/f_{row}_voicepack.pt --device cuda", cwd=K, tail=3)
    kw = {k: {("module." + a if not a.startswith("module.") else a): b for a, b in torch.load(c2[-1], map_location="cpu", weights_only=False)["net"][k].items()}
          for k in ["bert", "bert_encoder", "predictor", "text_encoder", "decoder"]}
    torch.save(kw, f"{W}/kokoro_f_v03_{TAG}.pth")
    report += [f"Saved kokoro_f_v03_{TAG}.pth + 4 voicepacks", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

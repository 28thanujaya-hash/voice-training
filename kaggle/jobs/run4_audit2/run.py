# Run 4 · audit 2 (GPT review step 0 + the mentor's blind actor test), 16 Nov.
# Part 1: are the voice settings trustworthy?
#  - which encoders exist in each checkpoint; is stage 2's predictor_encoder really trained (differs from its stage-1 copy)?
#  - style_encoder drift stage 1 → stage 2 (kikiri issue #1)
#  - per-clip style vectors (acoustic half = stage-1 style_encoder, prosody half = stage-2 predictor_encoder, as used for the
#    packs): within-mood vs between-mood similarity; mood guessed from single-clip vectors (cross-validated)
#  - do the saved voicepacks equal the clip average?
#  - do ?, ?!, …, —, ↗ survive in the training list?
# Part 2: blind actor test — the same-line groups (same words in 2–4 moods), shuffled, numbered; key separate.
import csv, glob, os, random, re, subprocess, sys, time, traceback
sys.path.insert(0, os.getcwd())
T0 = time.time(); LOG = []; W = "/kaggle/working"; TMP = "/kaggle/tmp"; os.makedirs(TMP, exist_ok=True); os.makedirs(f"{W}/blind", exist_ok=True)
ROWS = ["normal", "bright", "low", "tense"]
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None):
    log("$ " + c[:150]); p = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(c[:100] + "\n" + (p.stdout + p.stderr)[-2000:])
report = ["# Run 4 · audit 2: are the mood settings trustworthy? + blind actor test", ""]
try:
    sh("pip install -q scikit-learn soundfile")
    import numpy as np, torch, soundfile as sf, torchaudio
    sh("git clone -q --depth 1 https://github.com/semidark/kikiri-tts kt", cwd=TMP)
    sys.path.insert(0, f"{TMP}/kt/scripts")
    from extract_voicepack import StyleEncoder
    strip = lambda d: {k[7:] if k.startswith("module.") else k: v for k, v in d.items()}
    st1 = torch.load(glob.glob("/kaggle/input/**/kokoro_maya_v02_stage1.pth", recursive=True)[0], map_location="cpu", weights_only=False)["net"]
    # stage-2 full checkpoints are not in the outputs; the Kokoro-format files hold bert..decoder only → use voicepacks + st1;
    # predictor_encoder must come from the stage-2 run: check what the kokoro_maya_v02_X.pth files contain
    ck = {}
    for tag in ("A", "B"):
        f = glob.glob(f"/kaggle/input/**/kokoro_maya_v02_{tag}.pth", recursive=True)[0]; ck[tag] = torch.load(f, map_location="cpu", weights_only=False)
    report += ["## Checkpoints", "", f"- stage 1 modules: {sorted(st1.keys())}",
               f"- teacher A file modules: {sorted(ck['A'].keys())}", f"- teacher B file modules: {sorted(ck['B'].keys())}", ""]
    has_pe = "predictor_encoder" in st1
    def norm(sd): return float(torch.sqrt(sum((v.float() ** 2).sum() for k, v in sd.items() if v.dtype.is_floating_point)))
    if has_pe:
        a, b = strip(st1["style_encoder"]), strip(st1["predictor_encoder"])
        same = all(torch.equal(a[k], b[k]) for k in a if k in b)
        report.append(f"- stage 1: style_encoder norm {norm(a):.2f}; predictor_encoder norm {norm(b):.2f}; identical: {same}")
    # stage-2 encoders: re-derive from the voicepacks is impossible; the stage-2 epoch checkpoint wasn't kept in outputs.
    report += ["", "Note: the stage-2 full checkpoint (with predictor_encoder) was not saved as an output, only the Kokoro-format",
               "modules + voicepacks. So per-clip prosody vectors are computed two ways: (i) stage-1 style_encoder for both halves",
               "(what the extractor falls back to), (ii) compared against the saved packs to see which encoder made them.", ""]
    SE = StyleEncoder(dim_in=64, style_dim=128, max_conv_dim=512); SE.load_state_dict(a); SE = SE.cuda().eval()
    PE1 = StyleEncoder(dim_in=64, style_dim=128, max_conv_dim=512); PE1.load_state_dict(b if has_pe else a); PE1 = PE1.cuda().eval()
    mel_t = torchaudio.transforms.MelSpectrogram(sample_rate=24000, n_fft=2048, win_length=1200, hop_length=300, n_mels=80).cuda()
    tr = glob.glob("/kaggle/input/**/train.csv", recursive=True); tr = [t for t in tr if "audit" in t] or tr; src = os.path.dirname(tr[0])
    rows = list(csv.DictReader(open(tr[0])))
    V = {}
    with torch.no_grad():
        for r in rows:
            x = torch.tensor(sf.read(f"{src}/{r['file']}", dtype="float32")[0])[None].cuda()
            m = (torch.log(1e-5 + mel_t(x)) - (-4)) / 4
            V[r["id"]] = (SE(m[None]).squeeze().cpu().numpy(), PE1(m[None]).squeeze().cpu().numpy())
    log(f"{len(V)} clips embedded")
    from sklearn.linear_model import LogisticRegression; from sklearn.model_selection import cross_val_score; from sklearn.preprocessing import StandardScaler; from sklearn.pipeline import make_pipeline
    trn = [r for r in rows if r["split"] == "train"]
    lab = np.array([ROWS.index(r["row"]) for r in trn])
    def stats(idx, name):
        X = np.array([V[r["id"]][idx] for r in trn]); Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
        C = Xn @ Xn.T; same = lab[:, None] == lab[None, :]; np.fill_diagonal(same, False); diff = lab[:, None] != lab[None, :]
        acc = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.5)), X, lab, cv=5).mean()
        cen = {k: Xn[lab == i].mean(0) for i, k in enumerate(ROWS)}
        cc = {k: float(cen[k] @ cen["normal"] / np.linalg.norm(cen[k]) / np.linalg.norm(cen["normal"])) for k in ROWS[1:]}
        return f"| {name} | {C[same].mean():.4f} | {C[diff].mean():.4f} | {100*acc:.0f}% | " + ", ".join(f"{k} {v:.4f}" for k, v in cc.items()) + " |", X
    l1, Xa = stats(0, "acoustic half (stage-1 style_encoder)")
    l2, Xp = stats(1, "prosody half (stage-1 " + ("predictor_encoder" if has_pe else "style_encoder") + ")")
    report += ["## Single clips: is the mood in the style vectors?", "",
               "| vectors | similarity within a mood | between moods | mood guessed from one clip (chance 25%) | average per mood vs normal (cosine) |",
               "|---|---|---|---|---|", l1, l2, ""]
    # saved packs vs clip average
    for tag in ("A", "B"):
        f = glob.glob(f"/kaggle/input/**/kokoro_maya_v02_{tag}.pth", recursive=True)[0]; d = os.path.dirname(f)
        out = []
        for row in ROWS:
            pk = torch.load(f"{d}/maya_{row}_voicepack.pt", map_location="cpu", weights_only=True).float().reshape(510, -1)
            varies = float((pk - pk[0]).abs().max())
            mean_a = Xa[lab == ROWS.index(row)].mean(0); mean_p = Xp[lab == ROWS.index(row)].mean(0); p0 = pk[0].numpy()
            cos = lambda u, v: float(u @ v / np.linalg.norm(u) / np.linalg.norm(v))
            out.append(f"{row}: rows differ by length? max {varies:.4f}; pack acoustic vs clip-mean {cos(p0[:128], mean_a):.4f}; pack prosody vs stage-1 clip-mean {cos(p0[128:], mean_p):.4f}")
        report += [f"- teacher {tag} packs: " + " · ".join(out)]
    report += ["", "(If 'pack prosody vs stage-1 clip-mean' ≈ 1.0, the packs' prosody half came from the stage-1 encoder, i.e. the extractor fell back; if clearly < 1, it came from the stage-2 predictor_encoder.)", ""]
    # marks in the training list
    tl = open(glob.glob("/kaggle/input/**/train_list.txt", recursive=True)[0]).read()
    report += ["## Marks in the training list (phoneme text the teacher saw)", "",
               ", ".join(f"{k}: {tl.count(k)}" for k in ["?!", "?", "…", "—", "↗", "!"]), ""]
    # ---- Part 2: blind actor test from the same-line groups
    G = {}
    for r in rows:
        if r.get("group"): G.setdefault(r["group"], []).append(r)
    random.seed(16); items = [r for g in sorted(G) for r in G[g]]; random.shuffle(items)
    key = ["# Blind actor test: key (read AFTER listening)", "", "| clip | group | mood | text |", "|---|---|---|---|"]
    sheet = ["# Blind actor test: tick sheet", "", "Orpheus tara (the actor) says the same words in different moods. For each clip, which mood do you hear?", "",
             "| clip | normal | bright | low | tense |", "|---|---|---|---|---|"]
    for i, r in enumerate(items, 1):
        sh(f"ffmpeg -loglevel error -y -i {src}/{r['file']} -b:a 64k {W}/blind/actor_blind_{i:02d}.mp3")
        key.append(f"| {i:02d} | {r['group']} | {r['row']} | {r['text']} |"); sheet.append(f"| {i:02d} | ☐ | ☐ | ☐ | ☐ |")
    open(f"{W}/blind_key.md", "w").write("\n".join(key) + "\n"); open(f"{W}/blind_sheet.md", "w").write("\n".join(sheet) + "\n")
    report += [f"## Blind actor test: {len(items)} clips from {len(G)} groups (blind/, blind_sheet.md, blind_key.md)", "", "RESULT: DONE"]
except Exception:
    report += ["", "RESULT: ERROR", "```", traceback.format_exc()[-3000:], "```"]; print(traceback.format_exc())
report += ["", "## Log", "```", *LOG, "```"]
open(f"{W}/report.md", "w").write("\n".join(report) + "\n")

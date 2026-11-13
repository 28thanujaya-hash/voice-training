"""Run 1, stage 3 (smoke run): our retrained Kokoro (teacher) reads sentences in Sam's and Maya's rows; Paradee's two halves
are warm-started from the released 1.3 weights with an 8-row voice table (Sam: normal/bright/low/tense, Maya: same) and trained
a few hundred steps on those readings; exported as ONE int8 ONNX file with the same inputs the phone uses; checked with ONNX Runtime.
Paradee's public trainers are single-voice, so this is our own small multi-voice trainer around Paradee's model code.
usage: paradee_run1.py --paradee REPO --teacher KOKORO.pth --kconfig config.json --pack sam=a.pt --pack maya=b.pt
                       --g2p CLI --lex LEX --out DIR [--sents N] [--text-steps N] [--dec-steps N] [--device cuda]"""
import argparse, json, math, os, random, subprocess, sys, time, types, re
import numpy as np, torch, torch.nn.functional as F
ap = argparse.ArgumentParser()
ap.add_argument("--paradee", required=True); ap.add_argument("--teacher", required=True); ap.add_argument("--kconfig", required=True)
ap.add_argument("--pack", action="append", required=True); ap.add_argument("--g2p", required=True); ap.add_argument("--lex", required=True)
ap.add_argument("--out", required=True); ap.add_argument("--sents", type=int, default=150); ap.add_argument("--text-steps", type=int, default=300)
ap.add_argument("--dec-steps", type=int, default=300); ap.add_argument("--device", default="cuda"); ap.add_argument("--bs", type=int, default=16)
A = ap.parse_args(); DEV = A.device; os.makedirs(A.out, exist_ok=True); T0 = time.time()
def log(s): print(f"[{(time.time()-T0)/60:5.1f} min] {s}", flush=True)

# kokoro's package imports misaki (Python <3.13); we feed sounds directly, so a stub package is enough (also for the exporter)
STUB = os.path.abspath(f"{A.out}/_stub"); os.makedirs(f"{STUB}/misaki", exist_ok=True)
_g = 'def __getattr__(n):\n    if n.startswith("__"): raise AttributeError(n)\n    return type(n, (), {})\n'
open(f"{STUB}/misaki/__init__.py", "w").write("from . import en, espeak\n" + _g)
for m in ("en", "espeak"): open(f"{STUB}/misaki/{m}.py", "w").write(_g)
sys.path.insert(0, STUB)
sys.path.insert(0, os.path.join(A.paradee, "training", "scripts"))
from kokoro.model import KModel
from student import TextStudent, alignment
from vhead import VDecoder
from huggingface_hub import hf_hub_download

ROWS = ["sam_normal", "sam_bright", "sam_low", "sam_tense", "maya_normal", "maya_bright", "maya_low", "maya_tense"]
PACK = dict(p.split("=", 1) for p in A.pack)

# ---- sentences: Paradee's own WikiText sentences (held-out ones skipped) + our lines
wt = json.load(open(os.path.join(A.paradee, "training", "data", "wikitext_sents.json")))[200:200 + A.sents]
ours = ["Hi! I'm Sam. Did you see the new Avengers film?", "Hmm, interesting. Tell me more about it.",
        "Sorry, could you slow down a bit?", "Wait, really? I didn't know that!", "Oh no… I'm so sorry. That's really sad."]
sents = ours + wt
def g2p(texts):
    p = subprocess.run([A.g2p, "--lex", A.lex], input="\n".join(texts) + "\n", capture_output=True, text=True, check=True)
    return [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
phs = g2p(sents); log(f"{len(sents)} sentences → sounds")

# ---- teacher readings (same intermediates as Paradee's gen_teacher.py), Sam → row 0, Maya → row 4
try: km = KModel(repo_id="hexgrad/Kokoro-82M", config=A.kconfig, model=A.teacher)
except TypeError: km = KModel(config=A.kconfig, model=A.teacher)   # older kokoro package
km = km.to(DEV).eval()
packs = {w: torch.load(p, map_location="cpu", weights_only=True) for w, p in PACK.items()}
@torch.no_grad()
def teach(ps, ref):
    m = km; ids = torch.LongTensor([[0, *[m.vocab[c] for c in ps if c in m.vocab], 0]]).to(DEV)
    T = ids.shape[1]; r = ref[T - 3].to(DEV)
    L = torch.full((1,), T, device=DEV); mask = torch.zeros(1, T, dtype=torch.bool, device=DEV)
    bert = m.bert(ids, attention_mask=(~mask).int()); d_en = m.bert_encoder(bert).transpose(-1, -2)
    s = r[:, 128:]; d = m.predictor.text_encoder(d_en, s, L, mask); x, _ = m.predictor.lstm(d)
    dur = torch.sigmoid(m.predictor.duration_proj(x)).sum(-1); pd_ = torch.round(dur).clamp(min=1).long().squeeze(0)
    aln = alignment(pd_)[None]; en = d.transpose(-1, -2) @ aln; F0, Nn = m.predictor.F0Ntrain(en, s)
    t_en = m.text_encoder(ids, L, mask); audio = m.decoder(t_en @ aln, F0, Nn, r[:, :128]).squeeze()
    c = lambda t: t.squeeze(0).cpu()
    return dict(ids=c(ids), dur=c(dur), pred_dur=pd_.cpu(), t_en=c(t_en), F0=c(F0), N=c(Nn), audio=audio.cpu().clamp(-1, 1))
rows = []; secs = 0; t = time.time()
for who, row in (("sam", 0), ("maya", 4)):
    for text, ps in zip(sents, phs):
        if not ps or len(ps) > 400: continue
        r = teach(ps, packs[who]); r.update(text=text, voice=row); rows.append(r); secs += len(r["audio"]) / 24000
log(f"teacher read {len(rows)} sentences, {secs/60:.1f} min of audio in {time.time()-t:.0f} s")
random.seed(0); held = [r for r in rows if r["text"] in ours[:2]]; train = [r for r in rows if r["text"] not in ours[:2]]

# ---- released 1.3 weights, 8-row tables: Sam rows start from am_puck, Maya rows from af_heart
cfg = json.load(open(hf_hub_download("sahilmahendrakar/Paradee-8M-v1.3", "config.json")))
REL = cfg["voices"]; start = [REL.index("am_puck")] * 4 + [REL.index("af_heart")] * 4
def eight(w): return torch.stack([w[i] for i in start])
ts = TextStudent("s+mlp", n_voices=len(REL)); ts.load_state_dict(torch.load(hf_hub_download("sahilmahendrakar/Paradee-8M-v1.3", "pytorch/text_side.pt"), map_location="cpu")["model"])
w = ts.style.data.clone(); ts.style = torch.nn.Parameter(eight(w)); ts = ts.to(DEV)
vd = VDecoder(head="v2", dim=160, blocks=4, n_voices=len(REL)); vd.load_ckpt(hf_hub_download("sahilmahendrakar/Paradee-8M-v1.3", "pytorch/decoder.pt"))
w = vd.style.data.clone(); vd.style = torch.nn.Parameter(eight(w)); vd = vd.to(DEV)
log(f"warm start from Paradee 1.3; rows {ROWS}")

# ---- text half (losses as in Paradee's train_text.py, plus the voice row per sentence)
def collate(batch):
    B = len(batch); T = max(len(r["ids"]) for r in batch); Fm = max(len(r["F0"]) for r in batch) // 2
    ids = torch.zeros(B, T, dtype=torch.long); L = torch.tensor([len(r["ids"]) for r in batch]); dur = torch.zeros(B, T)
    ten = torch.zeros(B, 512, T); aln = torch.zeros(B, T, Fm); F0 = torch.zeros(B, 2 * Fm); N = torch.zeros(B, 2 * Fm); fm = torch.zeros(B, 2 * Fm, dtype=torch.bool)
    for i, r in enumerate(batch):
        t_ = len(r["ids"]); f = len(r["F0"]) // 2
        ids[i, :t_] = r["ids"]; dur[i, :t_] = r["dur"]; ten[i, :, :t_] = r["t_en"]; aln[i, :t_, :f] = alignment(r["pred_dur"], f)
        F0[i, :2 * f] = r["F0"]; N[i, :2 * f] = r["N"]; fm[i, :2 * f] = True
    tm = torch.arange(T)[None] < L[:, None]; v = torch.tensor([r["voice"] for r in batch])
    return [x.to(DEV) for x in (ids, L, dur, ten, aln, F0, N, tm, fm, v)]
def text_losses(b):
    ids, L, dur, ten, aln, F0, N, tm, fm, v = b
    pd_, pF0, pN, pasr = ts(ids, L, aln, voice=v)
    return ((F.l1_loss(torch.log(pd_.clamp_min(1e-3)), torch.log(dur.clamp_min(1e-3)), reduction="none") * tm).sum() / tm.sum(),
            (F.l1_loss(pF0, F0, reduction="none") * fm).sum() / fm.sum() / 100,
            (F.l1_loss(pN, N, reduction="none") * fm).sum() / fm.sum(),
            (F.l1_loss(pasr, ten, reduction="none") * tm[:, None]).sum() / tm.sum() / 512)
opt = torch.optim.AdamW(ts.parameters(), lr=2e-4, weight_decay=0.01); ts.train(); hist = []
with torch.no_grad(): ts.eval(); before = [l.item() for l in text_losses(collate(held))]; ts.train()
for step in range(1, A.text_steps + 1):
    ls = text_losses(collate(random.sample(train, min(A.bs, len(train))))); loss = sum(ls)
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(ts.parameters(), 1.0); opt.step()
    if step % 50 == 0: log(f"text step {step} loss {loss.item():.4f}"); hist.append(loss.item())
with torch.no_grad(): ts.eval(); after = [l.item() for l in text_losses(collate(held))]
log(f"text half held-out losses (dur, f0, n, asr) before {np.round(before, 4).tolist()} after {np.round(after, 4).tolist()}")
torch.save({"model": ts.cpu().state_dict()}, f"{A.out}/text_side.pt"); ts.to(DEV)

# ---- decoder (multi-resolution spectrogram losses on random windows; the full run adds Paradee's GAN + statistic losses)
def stft_loss(y, x):
    l = 0
    for n, h in ((512, 128), (1024, 256), (2048, 512)):
        w = torch.hann_window(n, device=y.device)
        Y = torch.stft(y, n, h, window=w, return_complex=True).abs().clamp_min(1e-5); X = torch.stft(x, n, h, window=w, return_complex=True).abs().clamp_min(1e-5)
        l = l + F.l1_loss(torch.log(Y), torch.log(X)) + (torch.norm(X - Y) / torch.norm(X))
    return l / 3
SEG = 64
def window(r):
    f = len(r["F0"]) // 2; a = random.randint(0, max(0, f - SEG)); n = min(SEG, f)
    aln = alignment(r["pred_dur"], f)
    asr = (r["t_en"] @ aln)[:, a:a + n]; F0 = r["F0"][2 * a:2 * (a + n)]; N = r["N"][2 * a:2 * (a + n)]; au = r["audio"][600 * a:600 * (a + n)]
    return asr, F0, N, au, n
opt = torch.optim.AdamW(vd.parameters(), lr=1e-4); vd.train()
def dec_eval():
    vd.eval(); tot = 0
    with torch.no_grad():
        for r in held:
            f = len(r["F0"]) // 2; asr = (r["t_en"] @ alignment(r["pred_dur"], f))[None].to(DEV)
            y = vd(asr, r["F0"][None].to(DEV), r["N"][None].to(DEV), voice=torch.tensor([r["voice"]], device=DEV))[0]
            k = min(len(y), len(r["audio"])); tot += stft_loss(y[None, :k], r["audio"][None, :k].to(DEV)).item()
    vd.train(); return tot / len(held)
d_before = dec_eval()
for step in range(1, A.dec_steps + 1):
    picks = random.sample(train, min(8, len(train))); b = [window(r) for r in picks]; n = min(x[4] for x in b)
    asr = torch.stack([x[0][:, :n] for x in b]).to(DEV); F0 = torch.stack([x[1][:2 * n] for x in b]).to(DEV); N = torch.stack([x[2][:2 * n] for x in b]).to(DEV)
    au = torch.stack([x[3][:600 * n] for x in b]).to(DEV); v = torch.tensor([r["voice"] for r in picks], device=DEV)
    y = vd(asr, F0, N, voice=v); k = min(y.shape[-1], au.shape[-1]); loss = stft_loss(y[:, :k], au[:, :k])
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(vd.parameters(), 1.0); opt.step()
    if step % 50 == 0: log(f"decoder step {step} loss {loss.item():.4f}")
d_after = dec_eval(); log(f"decoder held-out spectrogram loss before {d_before:.4f} after {d_after:.4f}")
torch.save({"model": vd.cpu().state_dict()}, f"{A.out}/decoder.pt")

# ---- export: Paradee's own exporter, with our 8 rows; our config.json carries the row names
cfg2 = dict(cfg); cfg2.update(voices=ROWS, languages={r: "en-us" for r in ROWS}, model_type="paradee", version="run1-smoke")
json.dump(cfg2, open(f"{A.out}/config.json", "w"), ensure_ascii=False, indent=1)
cwd = os.path.join(A.paradee, "training")
p = subprocess.run([sys.executable, "scripts/export_paradee_v1_2.py", os.path.abspath(f"{A.out}/decoder.pt"), "--text", os.path.abspath(f"{A.out}/text_side.pt"),
                    "--config", os.path.abspath(f"{A.out}/config.json"), "--out", os.path.abspath(f"{A.out}/onnx"), "--voices", ",".join(ROWS)],
                   cwd=cwd, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)})
open(f"{A.out}/export_log.txt", "w").write(p.stdout + p.stderr); log(f"export exit {p.returncode}: " + (p.stdout + p.stderr).strip()[-600:])
json.dump(dict(text_before=before, text_after=after, dec_before=d_before, dec_after=d_after, n_rows=len(rows), audio_min=secs / 60,
               export_ok=p.returncode == 0), open(f"{A.out}/stage3.json", "w"), indent=1)

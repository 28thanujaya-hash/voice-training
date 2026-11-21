# run27: IndexTTS2 in tara's voice, all four moods, three emotion controls (recipe in pilot.py). One GPU try; every step logged into report.md.
import csv, json, os, re, subprocess, sys, time, traceback, urllib.request
sys.path.insert(0, os.getcwd())
from pilot import LINES, VEC, ETXT, CLIP, TAKES
T0 = time.time(); LOG = []; W = "/kaggle/working"; os.makedirs(f"{W}/takes", exist_ok=True)
RAW = "https://raw.githubusercontent.com/28thanujaya-hash/voice-training/main/kaggle/jobs/run27_indextts_all/"
def log(s):
    s = f"[{(time.time()-T0)/60:5.1f} min] {s}"; print(s, flush=True); LOG.append(s)
def sh(c, cwd=None):
    log("$ " + c[:160]); p = subprocess.run(c, shell=True, capture_output=True, text=True, cwd=cwd)
    if p.returncode: raise RuntimeError(c[:120] + "\n" + (p.stdout + p.stderr)[-3000:])
    return p.stdout
rows = []
try:
    for f in ["spk_tara.mp3"] + sorted(set(CLIP.values())):
        urllib.request.urlretrieve(RAW + f, f); sh(f"ffmpeg -loglevel error -y -i {f} -ar 24000 -ac 1 {f[:-4]}.wav")
    sh("git clone -q --depth 1 https://github.com/index-tts/index-tts.git /tmp/itts && cd /tmp/itts && git lfs pull 2>/dev/null; true")
    sh("pip install -q -U uv 'huggingface_hub[cli]'")
    sh("uv sync", cwd="/tmp/itts")
    sh("python -c \"from huggingface_hub import snapshot_download; snapshot_download('IndexTeam/IndexTTS-2', local_dir='/tmp/itts/checkpoints_2')\"")
    ARMS = lambda m: {"V": dict(emo_vector=VEC[m]), "T": dict(use_emo_text=True, emo_text=ETXT[m], emo_alpha=0.6), "A": dict(emo_audio_prompt=os.path.abspath(CLIP[m][:-4] + ".wav"), emo_alpha=0.9)}
    jobs = [dict(mood=m, id=i, arm=a, take=k, text=t, out=f"{W}/raw_{i}_{a}_{k}.wav", kw=kw) for m in LINES for i, t in LINES[m].items() for a, kw in ARMS(m).items() for k in range(TAKES)]
    json.dump(dict(spk=os.path.abspath("spk_tara.wav"), jobs=jobs), open("/tmp/itts/jobs.json", "w"))
    open("/tmp/itts/gen.py", "w").write('''
import json, time, traceback
from indextts.infer_v2 import IndexTTS2
J = json.load(open("jobs.json"))
tts = IndexTTS2(cfg_path="checkpoints_2/config.yaml", model_dir="checkpoints_2", use_fp16=True, use_cuda_kernel=False, use_deepspeed=False)
for j in J["jobs"]:
    t = time.time()
    try: tts.infer(spk_audio_prompt=J["spk"], text=j["text"], output_path=j["out"], verbose=False, **j["kw"]); print("OK", j["out"], round(time.time()-t, 1), flush=True)
    except Exception: print("FAIL", j["out"], traceback.format_exc()[-800:], flush=True)
''')
    out = sh("PYTHONPATH=. uv run python gen.py", cwd="/tmp/itts"); log("generation done: " + str(out.count("OK ")) + " ok, " + str(out.count("FAIL ")) + " failed")
    if "FAIL" in out: log(out[out.index("FAIL"):][:1500])
    sh("pip install -q 'transformers==4.57.6' jiwer librosa soundfile")
    import torch, jiwer
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", "openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:0")
    norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split()
    for j in jobs:
        if not os.path.exists(j["out"]): continue
        name = f"{j['id']}_{j['arm']}_{j['take']}"
        sh(f"ffmpeg -loglevel error -y -i {j['out']} -b:a 96k {W}/takes/{name}.mp3"); os.remove(j["out"])
        heard = asr(f"{W}/takes/{name}.mp3")["text"].strip(); wer = jiwer.wer(" ".join(norm(j["text"])), " ".join(norm(heard)) or "x")
        rows.append(dict(id=j["id"], mood=j["mood"], var=j["arm"], take=j["take"], text=j["text"], status="PASS" if wer <= 0.15 else "fail", heard=heard, wer=round(wer, 3)))
    log(f"{len(rows)} takes, {sum(r['status']=='PASS' for r in rows)} with right words")
except Exception:
    log("ERROR\n" + traceback.format_exc()[-3000:])
if rows:
    with open(f"{W}/takes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
open(f"{W}/report.md", "w").write("# run27 · IndexTTS2 in tara's voice, all moods (recipe in pilot.py)\n\nstatus PASS here = right words only (judge decides the mood)\n\n```\n" + "\n".join(LOG) + "\n```\n")

# Runs on the Colab VM (sent by colab.yml): fetch the repo, run kaggle/jobs/<JOB>/run.py with live output, zip /kaggle/working.
import os, shutil, subprocess, sys, time
JOB = "__JOB__"
os.makedirs("/kaggle/working", exist_ok=True)
subprocess.run("rm -rf /content/vt && git clone -q --depth 1 https://github.com/28thanujaya-hash/voice-training /content/vt", shell=True, check=True)
t0 = time.time()
p = subprocess.Popen([sys.executable, "-u", "run.py"], cwd=f"/content/vt/kaggle/jobs/{JOB}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
with open("/kaggle/working/run.log", "w") as log:
    for line in p.stdout:
        log.write(line); log.flush(); print(line, end="", flush=True)
p.wait()
print(f"\nEXIT {p.returncode} after {(time.time()-t0)/60:.1f} min", flush=True)
shutil.make_archive("/content/out", "zip", "/kaggle/working")
print("ZIP READY", os.path.getsize("/content/out.zip") // 1024, "KB", flush=True)

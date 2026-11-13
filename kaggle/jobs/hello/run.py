# Connection check: GPU, internet, Python packages. Writes report.md.
import subprocess, sys, json, time, urllib.request
r = []
def sh(c):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as e: return f"ERR {e}"
r.append("# Kaggle connection check\n")
r.append("GPU:\n```\n" + sh("nvidia-smi --query-gpu=name,memory.total --format=csv") + "\n```")
r.append("Python: " + sys.version.split()[0])
try:
    import torch; r.append(f"torch {torch.__version__}, cuda {torch.cuda.is_available()}, devices {torch.cuda.device_count()}")
except Exception as e: r.append(f"torch: {e}")
t = time.time()
try:
    urllib.request.urlopen("https://huggingface.co/api/models/hexgrad/Kokoro-82M", timeout=30).read()
    r.append(f"Internet: OK (Hugging Face in {time.time()-t:.1f} s)")
except Exception as e: r.append(f"Internet: FAILED {e}")
r.append("Disk:\n```\n" + sh("df -h /kaggle/working | tail -1") + "\n```")
open("report.md", "w").write("\n".join(r) + "\n")
print("\n".join(r))

import modal
app = modal.App("voice-gpu-check")
img = modal.Image.debian_slim().pip_install("torch")

@app.function(gpu="T4", image=img, timeout=600)
def check():
    import subprocess, torch
    print(subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout)
    return {"cuda": torch.cuda.is_available(), "name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}

@app.local_entrypoint()
def main():
    print("RESULT", check.remote())

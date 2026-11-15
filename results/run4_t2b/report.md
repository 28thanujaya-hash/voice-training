# Run 4 · teacher v0.2 · stage 2 (B: without adversarial)

Stage 2 (B): 1 epoch in 39.3 min; ['PEAK_GB [6.89, 4.47] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth']
Log lines with Gen>0: 0/90 · GenLM>0: 0/90 (expected 0 and 0)

```
INFO:__main__:Epoch [1/99], Step [440/451], Loss: 0.31605, Disc Loss: 0.00000, Dur Loss: 0.92926, CE Loss: 0.05031, Norm Loss: 0.57571, F0 Loss: 3.45930, LM Loss: 1.46956, Gen Loss: 0.00000, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
Epoch [1/99], Step [450/451], Loss: 0.27322, Disc Loss: 0.00000, Dur Loss: 0.71265, CE Loss: 0.04071, Norm Loss: 0.51808, F0 Loss: 1.83653, LM Loss: 1.21128, Gen Loss: 0.00000, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.00000, Ge
INFO:__main__:Epoch [1/99], Step [450/451], Loss: 0.27322, Disc Loss: 0.00000, Dur Loss: 0.71265, CE Loss: 0.04071, Norm Loss: 0.51808, F0 Loss: 1.83653, LM Loss: 1.21128, Gen Loss: 0.00000, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
```

Saved kokoro_maya_v02_B.pth + 4 voicepacks

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.3 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.2 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 41.5 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/se-run4-t1/kokoro_maya_v02_stage1.pth --
[ 41.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/se-run4-t1/kokoro_maya_v02_stage1.pth --
[ 41.9 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/se-run4-t1/kokoro_maya_v02_stage1.pth --
[ 42.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/se-run4-t1/kokoro_maya_v02_stage1.pth --
```

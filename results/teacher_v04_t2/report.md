# teacher v0.4 · teacher v0.4 · stage 2 (A: with adversarial)

Stage 2 (A): 1 epoch in 75.9 min; ['PEAK_GB [10.01, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth']
Log lines with Gen>0: 92/92 · GenLM>0: 92/92 (expected all and all)

```
INFO:__main__:Epoch [1/99], Step [460/485], Loss: 0.33211, Disc Loss: 3.97833, Dur Loss: 1.01175, CE Loss: 0.05513, Norm Loss: 0.35056, F0 Loss: 3.34692, LM Loss: 1.51839, Gen Loss: 2.95854, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
Epoch [1/99], Step [480/485], Loss: 0.64588, Disc Loss: 3.96937, Dur Loss: 0.84189, CE Loss: 0.03764, Norm Loss: 0.67625, F0 Loss: 3.59541, LM Loss: 1.61156, Gen Loss: 2.79051, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.49357, Ge
INFO:__main__:Epoch [1/99], Step [480/485], Loss: 0.64588, Disc Loss: 3.96937, Dur Loss: 0.84189, CE Loss: 0.03764, Norm Loss: 0.67625, F0 Loss: 3.59541, LM Loss: 1.61156, Gen Loss: 2.79051, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
```

Saved kokoro_f_v04_A.pth + 4 voicepacks

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.3 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.5 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 78.4 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 78.6 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 78.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 79.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
```

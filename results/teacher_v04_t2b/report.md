# teacher v0.4 · teacher v0.4 · stage 2 (A: with adversarial)

Stage 2 (A): 3 epoch in 226.0 min; ['PEAK_GB [9.91, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth', 'PEAK_GB [9.82, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth', 'PEAK_GB [9.91, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00002.pth']
Log lines with Gen>0: 282/282 · GenLM>0: 282/282 (expected all and all)

```
INFO:__main__:Epoch [3/99], Step [470/485], Loss: 0.28230, Disc Loss: 4.02248, Dur Loss: 1.02554, CE Loss: 0.04480, Norm Loss: 0.73290, F0 Loss: 2.99401, LM Loss: 1.43992, Gen Loss: 3.27530, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
Epoch [3/99], Step [480/485], Loss: 0.41552, Disc Loss: 3.86577, Dur Loss: 0.85886, CE Loss: 0.04228, Norm Loss: 0.82674, F0 Loss: 4.31863, LM Loss: 1.55626, Gen Loss: 3.80076, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.48372, Ge
INFO:__main__:Epoch [3/99], Step [480/485], Loss: 0.41552, Disc Loss: 3.86577, Dur Loss: 0.85886, CE Loss: 0.04228, Norm Loss: 0.82674, F0 Loss: 4.31863, LM Loss: 1.55626, Gen Loss: 3.80076, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
```

Saved kokoro_f_v04_A.pth + 4 voicepacks

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.2 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.3 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[228.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00002.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[228.7 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00002.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[228.9 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00002.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[229.2 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00002.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
```

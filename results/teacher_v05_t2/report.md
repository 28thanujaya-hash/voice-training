# teacher v0.5 · teacher v0.5 · stage 2 (A: with adversarial)

Stage 2 (A): 1 epoch in 89.1 min; ['PEAK_GB [9.99, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth']
Log lines with Gen>0: 110/110 · GenLM>0: 110/110 (expected all and all)

```
INFO:__main__:Epoch [1/99], Step [550/563], Loss: 0.31943, Disc Loss: 3.93473, Dur Loss: 0.95958, CE Loss: 0.03766, Norm Loss: 0.73290, F0 Loss: 5.25614, LM Loss: 1.54827, Gen Loss: 2.95409, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
Epoch [1/99], Step [560/563], Loss: 0.31711, Disc Loss: 4.00424, Dur Loss: 0.90763, CE Loss: 0.04731, Norm Loss: 1.56983, F0 Loss: 5.02865, LM Loss: 1.86538, Gen Loss: 2.53554, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.57177, Ge
INFO:__main__:Epoch [1/99], Step [560/563], Loss: 0.31711, Disc Loss: 4.00424, Dur Loss: 0.90763, CE Loss: 0.04731, Norm Loss: 1.56983, F0 Loss: 5.02865, LM Loss: 1.86538, Gen Loss: 2.53554, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
```

Saved kokoro_f_v05_A.pth + 4 voicepacks

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.3 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.3 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 91.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 91.6 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 91.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
[ 92.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-teacher
```

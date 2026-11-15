# Run 4 · teacher v0.2 · stage 2 (A: with adversarial)

Stage 2 (A): 1 epoch in 70.6 min; ['PEAK_GB [8.92, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth']
Log lines with Gen>0: 88/88 · GenLM>0: 88/88 (expected all and all)

```
INFO:__main__:Epoch [1/99], Step [430/451], Loss: 0.30212, Disc Loss: 3.96109, Dur Loss: 0.73898, CE Loss: 0.05316, Norm Loss: 0.67753, F0 Loss: 2.73254, LM Loss: 1.38097, Gen Loss: 3.30887, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
Epoch [1/99], Step [440/451], Loss: 0.31451, Disc Loss: 3.97628, Dur Loss: 0.66317, CE Loss: 0.03275, Norm Loss: 0.68946, F0 Loss: 4.10128, LM Loss: 1.58566, Gen Loss: 3.31220, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.41782, Ge
INFO:__main__:Epoch [1/99], Step [440/451], Loss: 0.31451, Disc Loss: 3.97628, Dur Loss: 0.66317, CE Loss: 0.03275, Norm Loss: 0.68946, F0 Loss: 4.10128, LM Loss: 1.58566, Gen Loss: 3.31220, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Los
```

Saved kokoro_maya_v02_A.pth + 4 voicepacks

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.4 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.4 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.2 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.2 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 72.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1
[ 73.0 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1
[ 73.2 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1
[ 73.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1
```

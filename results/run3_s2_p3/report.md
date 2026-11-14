# Run 3 · stage 2, part 3 (1 epoch, resumed from part 1 with the loader fix)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| resume loaded every module completely | ✅ | 13 modules, 0 with missing/unexpected keys |
| stage 2 part 3 (1 epochs) | ✅ | 24.4 min; peaks ['PEAK_GB [9.02, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 28/28, Gen>0: 28/28 |
| quick check + listening pack (15 clips) | ✅ |  |

Resume load check:
```
LOADCHECK bert missing 0 unexpected 0
LOADCHECK bert_encoder missing 0 unexpected 0
LOADCHECK predictor missing 0 unexpected 0
LOADCHECK decoder missing 0 unexpected 0
LOADCHECK text_encoder missing 0 unexpected 0
LOADCHECK predictor_encoder missing 0 unexpected 0
LOADCHECK style_encoder missing 0 unexpected 0
LOADCHECK diffusion missing 0 unexpected 0
LOADCHECK text_aligner missing 0 unexpected 0
LOADCHECK pitch_extractor missing 0 unexpected 0
LOADCHECK mpd missing 0 unexpected 0
LOADCHECK msd missing 0 unexpected 0
LOADCHECK wd missing 0 unexpected 0
```

Checkpoint: epoch_2nd_00001.pth → s2_part3.pth

Last training log lines:
```
Epoch [2/99], Step [130/140], Loss: 0.35780, Disc Loss: 4.05182, Dur Loss: 1.53671, CE Loss: 0.08872, Norm Loss: 0.93532, F0 Loss: 5.00262, LM Loss: 1.64434, Gen Loss: 3.05007, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.54130, GenLM Loss: 0.25735
INFO:__main__:Epoch [2/99], Step [130/140], Loss: 0.35780, Disc Loss: 4.05182, Dur Loss: 1.53671, CE Loss: 0.08872, Norm Loss: 0.93532, F0 Loss: 5.00262, LM Loss: 1.64434, Gen Loss: 3.05007, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.54130, GenLM Lo
Epoch [2/99], Step [140/140], Loss: 0.35441, Disc Loss: 3.97619, Dur Loss: 0.61944, CE Loss: 0.03506, Norm Loss: 0.52817, F0 Loss: 2.56750, LM Loss: 1.43640, Gen Loss: 3.25284, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.50736, GenLM Loss: 0.25514
INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.35441, Disc Loss: 3.97619, Dur Loss: 0.61944, CE Loss: 0.03506, Norm Loss: 0.52817, F0 Loss: 2.56750, LM Loss: 1.43640, Gen Loss: 3.25284, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.50736, GenLM Lo
```

## Quick check (10 held-out clips)

| | word error | naturalness (UTMOS) | sounds like tara |
|---|---|---|---|
| try-2 teacher | 5.7% | 4.03 | 0.967 |
| stage 2 part 3 | 3.3% | 4.23 | 0.957 |
| stage 2 part 1 | 3.3% | 4.25 | 0.962 |
| tara (the real clips) | – | 4.05 | – |

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.3 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.3 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.5 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.5 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.5 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.7 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  1.1 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.9 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.9 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.4 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 26.8 min] last progress: INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.35441, Disc Loss: 3.97619, Dur Loss: 0.61944, CE Loss: 0.03506, Norm Loss: 0.52817, F0 Loss: 2.56750, LM Los
[ 26.8 min] STEP resume loaded every module completely: OK 13 modules, 0 with missing/unexpected keys
[ 26.8 min] STEP stage 2 part 3 (1 epochs): OK 24.4 min; peaks ['PEAK_GB [9.02, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 28/28, Gen>0: 28/28
[ 26.9 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.2 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.4 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.6 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[ 28.0 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.2 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.3 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.4 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 29.7 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/l.wav -b:a 64k /kaggle/working/s2_part3_listen.mp3
[ 29.7 min] STEP quick check + listening pack (15 clips): OK 
```

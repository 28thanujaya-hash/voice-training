# Run 3 · stage 2, part 2 (1 epoch, resumed from part 1)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| stage 2 part 2 (1 epochs) | ✅ | 23.9 min; peaks ['PEAK_GB [9.08, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 26/26, Gen>0: 26/26 |
| quick check + listening pack (15 clips) | ✅ |  |

Checkpoint: epoch_2nd_00001.pth → s2_part2.pth

Last training log lines:
```
Epoch [2/99], Step [130/140], Loss: 0.66681, Disc Loss: 3.83762, Dur Loss: 1.37174, CE Loss: 0.10619, Norm Loss: 1.50834, F0 Loss: 4.50032, LM Loss: 2.65606, Gen Loss: 4.59483, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.67480, GenLM Loss: 0.50624
INFO:__main__:Epoch [2/99], Step [130/140], Loss: 0.66681, Disc Loss: 3.83762, Dur Loss: 1.37174, CE Loss: 0.10619, Norm Loss: 1.50834, F0 Loss: 4.50032, LM Loss: 2.65606, Gen Loss: 4.59483, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.67480, GenLM Lo
Epoch [2/99], Step [140/140], Loss: 0.69623, Disc Loss: 4.10511, Dur Loss: 1.20296, CE Loss: 0.10416, Norm Loss: 1.90644, F0 Loss: 4.68055, LM Loss: 2.71351, Gen Loss: 5.26335, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.23954, GenLM Loss: 0.44938
INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.69623, Disc Loss: 4.10511, Dur Loss: 1.20296, CE Loss: 0.10416, Norm Loss: 1.90644, F0 Loss: 4.68055, LM Loss: 2.71351, Gen Loss: 5.26335, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.23954, GenLM Lo
```

## Quick check (10 held-out clips)

| | word error | naturalness (UTMOS) | sounds like tara |
|---|---|---|---|
| try-2 teacher | 5.7% | 4.01 | 0.967 |
| stage 2 part 2 | 1526.0% | 1.24 | 0.468 |
| stage 2 part 1 | 3.3% | 4.26 | 0.961 |
| tara (the real clips) | – | 4.05 | – |

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.3 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.3 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.5 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.6 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.6 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.7 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  1.2 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  2.0 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.0 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.7 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 26.6 min] last progress: INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.69623, Disc Loss: 4.10511, Dur Loss: 1.20296, CE Loss: 0.10416, Norm Loss: 1.90644, F0 Loss: 4.68055, LM Los
[ 26.6 min] STEP stage 2 part 2 (1 epochs): OK 23.9 min; peaks ['PEAK_GB [9.08, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 26/26, Gen>0: 26/26
[ 26.7 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.0 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 27.4 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[ 27.8 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.0 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.1 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 28.2 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input/notebooks
[ 30.1 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/l.wav -b:a 64k /kaggle/working/s2_part2_listen.mp3
[ 30.1 min] STEP quick check + listening pack (15 clips): OK 
```

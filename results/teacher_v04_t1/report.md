# teacher v0.4 · teacher v0.4 · part 1: stage 1

## Balanced training list (lines → entries per mood × mark)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| plain | 131 → 131 | 13 → 26 | 31 → 31 | 96 → 96 |
| ? | 34 → 34 | 9 → 27 | 9 → 27 | 12 → 24 |
| ! | 5 → 15 | 86 → 86 | 33 → 33 | 22 → 22 |
| … | 5 → 15 | 23 → 23 | 86 → 86 | 23 → 23 |
| — | 6 → 18 | 13 → 26 | 16 → 32 | 14 → 28 |
| ?! | 7 → 21 | 13 → 26 | 0 → 0 | 11 → 33 |
| CAPS | 2 → 6 | 7 → 21 | 16 → 32 | 14 → 28 |

Training: 737 clips → 970 entries · validation: 63 clips (never trained on)

Stage 1: 5 epochs in 107.9 min, rc 0; checkpoint epoch_1st_00004.pth → kokoro_f_v04_stage1.pth

```
Epoch [5/5], Step [460/485], Mel Loss: 0.25026, Gen Loss: 2.44362, Disc Loss: 3.96928, Mono Loss: 0.09876, S2S Loss: 1.69230, SLM Loss: 1.77543
Epoch [5/5], Step [470/485], Mel Loss: 0.25471, Gen Loss: 3.22228, Disc Loss: 3.95843, Mono Loss: 0.10226, S2S Loss: 1.53533, SLM Loss: 1.71112INFO:__main__:[RANK 0] Epoch [5/5], Step [480/485], Mel Loss: 0.27463, Gen Loss: 2.76637, Disc Lo
Epoch [5/5], Step [480/485], Mel Loss: 0.27463, Gen Loss: 2.76637, Disc Loss: 3.95079, Mono Loss: 0.13653, S2S Loss: 1.15033, SLM Loss: 1.79498
```

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.4 min] 800 clips from /kaggle/input/notebooks/thusharajayawardane/se-teacher-v04-data: Counter({'train': 737, 'val': 63})
[  0.4 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.4 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.6 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.7 min] phonemes done; CAPS lines carrying ↗: 47
[  0.7 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.8 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.9 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.8 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.8 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/s1.yml  (log: train_first_log.txt)
```

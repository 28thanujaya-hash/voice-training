# teacher v0.5 · teacher v0.5 · part 1: stage 1

## Balanced training list (lines → entries per mood × mark)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| plain | 131 → 131 | 15 → 30 | 31 → 31 | 143 → 143 |
| ? | 34 → 34 | 13 → 26 | 9 → 27 | 18 → 36 |
| ! | 5 → 15 | 125 → 125 | 33 → 33 | 28 → 28 |
| … | 5 → 15 | 34 → 34 | 86 → 86 | 34 → 34 |
| — | 6 → 18 | 20 → 40 | 16 → 32 | 24 → 24 |
| ?! | 7 → 21 | 18 → 36 | 0 → 0 | 17 → 34 |
| CAPS | 2 → 6 | 11 → 33 | 16 → 32 | 23 → 23 |

Training: 904 clips → 1127 entries · validation: 75 clips (never trained on)

Stage 1: 5 epochs in 123.4 min, rc 0; checkpoint epoch_1st_00004.pth → kokoro_f_v05_stage1.pth

```
Epoch [5/5], Step [540/563], Mel Loss: 0.24985, Gen Loss: 3.15184, Disc Loss: 3.96092, Mono Loss: 0.15961, S2S Loss: 0.70099, SLM Loss: 1.50512
Epoch [5/5], Step [550/563], Mel Loss: 0.23343, Gen Loss: 3.03577, Disc Loss: 3.96145, Mono Loss: 0.15401, S2S Loss: 0.61985, SLM Loss: 1.63120
Epoch [5/5], Step [560/563], Mel Loss: 0.22881, Gen Loss: 2.71824, Disc Loss: 4.00209, Mono Loss: 0.21074, S2S Loss: 1.00860, SLM Loss: 1.16419
```

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] 979 clips from /kaggle/input/notebooks/thusharajayawardane/se-teacher-v05-data: Counter({'train': 904, 'val': 75})
[  0.3 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.3 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.5 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.5 min] phonemes done; CAPS lines carrying ↗: 60
[  0.5 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.6 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.7 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.4 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.6 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/s1.yml  (log: train_first_log.txt)
```

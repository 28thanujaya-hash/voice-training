# Run 4 · teacher v0.2 · part 1: stage 1

## Balanced training list (lines → entries per mood × mark)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| plain | 54 → 54 | 0 → 0 | 21 → 21 | 65 → 65 |
| ? | 19 → 38 | 9 → 27 | 9 → 27 | 9 → 27 |
| ! | 24 → 24 | 61 → 61 | 24 → 24 | 22 → 22 |
| … | 16 → 32 | 17 → 34 | 52 → 52 | 17 → 34 |
| — | 10 → 30 | 10 → 30 | 10 → 30 | 10 → 30 |
| ?! | 10 → 30 | 9 → 27 | 10 → 30 | 11 → 33 |
| CAPS | 10 → 30 | 9 → 27 | 10 → 30 | 11 → 33 |

Training: 539 clips → 902 entries · validation: 38 clips (never trained on)

Stage 1: 5 epochs in 114.3 min, rc 0; checkpoint epoch_1st_00004.pth → kokoro_maya_v02_stage1.pth

```
Epoch [5/5], Step [430/451], Mel Loss: 0.23526, Gen Loss: 2.73072, Disc Loss: 3.96298, Mono Loss: 0.35015, S2S Loss: 0.88819, SLM Loss: 1.32971
Epoch [5/5], Step [440/451], Mel Loss: 0.25827, Gen Loss: 3.40538, Disc Loss: 3.98494, Mono Loss: 0.18623, S2S Loss: 0.60809, SLM Loss: 1.38756
Epoch [5/5], Step [450/451], Mel Loss: 0.26595, Gen Loss: 3.22599, Disc Loss: 3.97267, Mono Loss: 0.11182, S2S Loss: 1.40974, SLM Loss: 1.29710
```

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] 577 clips from /kaggle/input/notebooks/thusharajayawardane/se-run4-audit: Counter({'train': 539, 'val': 38})
[  0.3 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.3 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.5 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.5 min] phonemes done; CAPS lines carrying ↗: 44
[  0.5 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.6 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.7 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.4 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.2 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/s1.yml  (log: train_first_log.txt)
```

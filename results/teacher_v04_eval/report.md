# teacher v0.4 · eval: rows vs moods on held-out student lines

| model | row | pass | judged neutral / happy / sad / angry | word error |
|---|---|---|---|---|
| v04 | normal | 66/148 | 37 / 90 / 16 / 5 | 0.02 |
| v04 | bright | 43/148 | 37 / 62 / 47 / 2 | 0.02 |
| v04 | low | 109/148 | 10 / 18 / 120 / 0 | 0.02 |
| v04 | tense | 56/148 | 5 / 78 / 0 / 65 | 0.02 |
| stock | normal | 48/148 | 34 / 49 / 0 / 65 | 0.04 |
| stock | bright | 45/148 | 33 / 48 / 0 / 67 | 0.04 |
| stock | low | 0/148 | 34 / 48 / 0 / 66 | 0.03 |
| stock | tense | 58/148 | 32 / 48 / 0 / 68 | 0.04 |

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa loguru munch einops einops-exts nltk pydub accelerate
[  0.4 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  0.4 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  0.6 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.6 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.8 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  1.4 min] model /kaggle/input/notebooks/thusharajayawardane/se-teacher-v04-t2/kokoro_f_v04_A.pth
[  7.0 min] v04 done
[ 11.4 min] stock done
```

# teacher v0.5 · eval: rows vs moods on held-out student lines

| model | row | pass | judged neutral / happy / sad / angry | word error |
|---|---|---|---|---|
| v05 | normal | 59/148 | 32 / 99 / 8 / 9 | 0.03 |
| v05 | bright | 67/148 | 26 / 95 / 19 / 8 | 0.02 |
| v05 | low | 81/148 | 6 / 38 / 104 / 0 | 0.03 |
| v05 | tense | 52/148 | 8 / 79 / 0 / 61 | 0.03 |
| stock | normal | 47/148 | 34 / 48 / 0 / 66 | 0.04 |
| stock | bright | 44/148 | 33 / 47 / 0 / 68 | 0.04 |
| stock | low | 0/148 | 33 / 48 / 0 / 67 | 0.04 |
| stock | tense | 57/148 | 34 / 48 / 0 / 66 | 0.04 |

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa loguru munch einops einops-exts nltk pydub accelerate
[  0.4 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  0.4 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  0.6 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.7 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.8 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  1.5 min] model /kaggle/input/notebooks/thusharajayawardane/se-teacher-v05-t2/kokoro_f_v05_A.pth
[  7.2 min] v05 done
[ 11.6 min] stock done
```

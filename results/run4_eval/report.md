# Run 4 · G2: teacher v0.2 A (with adversarial) vs B (without) vs stock Kokoro


RESULT: ERROR
```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 45, in <module>
    from kokoro.model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/__init__.py", line 3, in <module>
    from loguru import logger
ModuleNotFoundError: No module named 'loguru'

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa torchcrepe scikit-learn
[  1.5 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  1.6 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  1.8 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  1.9 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  2.1 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
```

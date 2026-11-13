# Run 1 · stage 2: Kokoro retraining (smoke run)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn? |
| recipe + tools installed | ✅ |  |
| Kokoro base weights converted | ✅ |  |
| Kokoro stage 1 (acoustic) | ✅ | 2.3 min, GPU peak 0.0 GB |
| Kokoro stage 2 (prosody + adversarial) | ✅ | 2.2 min |
| voicepacks (Sam, Maya) | ✅ |  |
| ERROR | ❌ |  |

```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 113, in <module>
    from kokoro.model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/__init__.py", line 23, in <module>
    from .pipeline import KPipeline
  File "/kaggle/tmp/kt/kokoro/kokoro/pipeline.py", line 44, in <module>
    class KPipeline:
    ...<406 lines>...
                        yield self.Result(graphemes=chunk, phonemes=ps, output=output, text_index=graphemes_index)
  File "/kaggle/tmp/kt/kokoro/kokoro/pipeline.py", line 189, in KPipeline
    def tokens_to_ps(tokens: List[en.MToken]) -> str:
                                  ^^^^^^^^^
AttributeError: module 'misaki.en' has no attribute 'MToken'

```

RESULT: FAIL

## Log
```
[  0.0 min] stage-1 clips: 17 kept, from /kaggle/input/notebooks/thusharajayawardane/se-run1-record
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.1 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.3 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.3 min] STEP words → sounds (misaki-g2p): OK 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn?
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.6 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.7 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.5 min] torch 2.11.0+cu130, GPUs 2
[  1.5 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.5 min] STEP recipe + tools installed: OK 
[  1.6 min] STEP Kokoro base weights converted: OK 
[  1.6 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  3.9 min] STEP Kokoro stage 1 (acoustic): OK 2.3 min, GPU peak 0.0 GB
[  3.9 min] $ python train_second.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  6.1 min] STEP Kokoro stage 2 (prosody + adversarial): OK 2.2 min
[  6.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  6.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  6.4 min] STEP voicepacks (Sam, Maya): OK 
[  6.4 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  6.6 min] STEP ERROR: FAILED 
```

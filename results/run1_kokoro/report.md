# Run 1 · stage 2: Kokoro retraining (smoke run)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn? |
| recipe + tools installed | ✅ |  |
| Kokoro base weights converted | ✅ |  |
| Kokoro stage 1 (acoustic) | ✅ | 2.1 min, GPU peak 0.0 GB |
| Kokoro stage 2 (prosody + adversarial) | ✅ | 2.3 min |
| voicepacks (Sam, Maya) | ✅ |  |
| ERROR | ❌ |  |

```
p(
     ~~~~~~~~~~~~~~~~~~~~~~~^
        "_c10d_functional::_wrap_tensor_autograd",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        mutates_args=(),
        ^^^^^^^^^^^^^^^^
        schema="(Tensor input) -> Tensor",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/usr/local/lib/python3.13/dist-packages/torch/_library/custom_ops.py", line 157, in inner
    result = CustomOpDef(namespace, opname, schema_str, fn, tags)
  File "/usr/local/lib/python3.13/dist-packages/torch/_library/custom_ops.py", line 215, in __init__
    self._register_to_dispatcher(self._tags)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/_library/custom_ops.py", line 638, in _register_to_dispatcher
    lib._register_fake(self._name, fake_impl, _stacklevel=4)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/library.py", line 183, in _register_fake
    source = torch._library.utils.get_source(_stacklevel + 1)
  File "/usr/local/lib/python3.13/dist-packages/torch/_library/utils.py", line 45, in get_source
    frame = inspect.getframeinfo(sys._getframe(stacklevel))
  File "/usr/lib/python3.13/inspect.py", line 1707, in getframeinfo
    lines, lnum = findsource(frame)
                  ~~~~~~~~~~^^^^^^^
  File "/usr/lib/python3.13/inspect.py", line 1083, in findsource
    module = getmodule(object, file)
  File "/usr/lib/python3.13/inspect.py", line 1037, in getmodule
    f = getabsfile(module)
  File "/usr/lib/python3.13/inspect.py", line 1005, in getabsfile
    _filename = getsourcefile(object) or getfile(object)
                ~~~~~~~~~~~~~^^^^^^^^
  File "/usr/lib/python3.13/inspect.py", line 977, in getsourcefile
    if any(filename.endswith(s) for s in all_bytecode_suffixes):
       ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/inspect.py", line 977, in <genexpr>
    if any(filename.endswith(s) for s in all_bytecode_suffixes):
           ^^^^^^^^^^^^^^^^^
AttributeError: type object '__file__' has no attribute 'endswith'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/kaggle/src/script.py", line 115, in <module>
    from kokoro.model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/__init__.py", line 22, in <module>
    from .model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/model.py", line 2, in <module>
    from .modules import CustomAlbert, ProsodyPredictor, TextEncoder
  File "/kaggle/tmp/kt/kokoro/kokoro/modules.py", line 4, in <module>
    from transformers import AlbertModel
  File "/usr/local/lib/python3.13/dist-packages/transformers/utils/import_utils.py", line 2688, in __getattr__
    raise ModuleNotFoundError(import_error_message) from e
ModuleNotFoundError: Could not import module 'AlbertModel'. Are this object's requirements defined correctly? Set the logging verbosity to DEBUG for the original import error.

```

RESULT: FAIL

## Log
```
[  0.0 min] stage-1 clips: 17 kept, from /kaggle/input/notebooks/thusharajayawardane/se-run1-record
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.3 min] STEP words → sounds (misaki-g2p): OK 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn?
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.4 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.2 min] torch 2.11.0+cu130, GPUs 2
[  1.2 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.3 min] STEP recipe + tools installed: OK 
[  1.3 min] STEP Kokoro base weights converted: OK 
[  1.4 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  3.4 min] STEP Kokoro stage 1 (acoustic): OK 2.1 min, GPU peak 0.0 GB
[  3.4 min] $ python train_second.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  5.7 min] STEP Kokoro stage 2 (prosody + adversarial): OK 2.3 min
[  5.7 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  5.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  6.0 min] STEP voicepacks (Sam, Maya): OK 
[  6.0 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  6.2 min] STEP ERROR: FAILED 
```

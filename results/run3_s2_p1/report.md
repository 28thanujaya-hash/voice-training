# Run 3 · stage 2, part 1 (epochs 1–2)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| stage 2 part 1 (2 epochs) | ✅ | 44.5 min; peaks ['PEAK_GB [8.88, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth', 'PEAK_GB [8.88, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 56/56, Gen>0: 56/56 |
| ERROR | ❌ |  |

Checkpoint: epoch_2nd_00001.pth → s2_part1.pth

Last training log lines:
```
Epoch [2/99], Step [130/140], Loss: 0.38020, Disc Loss: 3.98472, Dur Loss: 0.82398, CE Loss: 0.04270, Norm Loss: 0.68707, F0 Loss: 4.21564, LM Loss: 1.74600, Gen Loss: 3.64994, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.48908, GenLM Loss: 0.25246
INFO:__main__:Epoch [2/99], Step [130/140], Loss: 0.38020, Disc Loss: 3.98472, Dur Loss: 0.82398, CE Loss: 0.04270, Norm Loss: 0.68707, F0 Loss: 4.21564, LM Loss: 1.74600, Gen Loss: 3.64994, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.48908, GenLM Lo
Epoch [2/99], Step [140/140], Loss: 0.37484, Disc Loss: 3.94137, Dur Loss: 1.13666, CE Loss: 0.07623, Norm Loss: 0.81283, F0 Loss: 3.03467, LM Loss: 1.61685, Gen Loss: 3.39248, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.55961, GenLM Loss: 0.23659
INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.37484, Disc Loss: 3.94137, Dur Loss: 1.13666, CE Loss: 0.07623, Norm Loss: 0.81283, F0 Loss: 3.03467, LM Loss: 1.61685, Gen Loss: 3.39248, Sty Loss: 0.00000, Diff Loss: 0.00000, DiscLM Loss: 0.55961, GenLM Lo
```

```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 154, in <module>
    from kokoro.model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/__init__.py", line 22, in <module>
    from .model import KModel
  File "/kaggle/tmp/kt/kokoro/kokoro/model.py", line 2, in <module>
    from .modules import CustomAlbert, ProsodyPredictor, TextEncoder
  File "/kaggle/tmp/kt/kokoro/kokoro/modules.py", line 4, in <module>
    from transformers import AlbertModel
  File "/usr/local/lib/python3.13/dist-packages/transformers/__init__.py", line 27, in <module>
    from . import dependency_versions_check
  File "/usr/local/lib/python3.13/dist-packages/transformers/dependency_versions_check.py", line 16, in <module>
    from .utils.versions import require_version, require_version_core
  File "/usr/local/lib/python3.13/dist-packages/transformers/utils/__init__.py", line 19, in <module>
    from huggingface_hub import get_full_repo_name  # for backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/huggingface_hub/__init__.py", line 1224, in __getattr__
    delete_space_storage,  # noqa: F401
                     ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/huggingface_hub/hf_api.py", line 56, in <module>
    from ._commit_api import (
    ...<9 lines>...
    )
  File "/usr/local/lib/python3.13/dist-packages/huggingface_hub/_commit_api.py", line 19, in <module>
    from .errors import EntryNotFoundError, HfHubHTTPError, XetAuthorizationError, XetRefreshTokenError
ImportError: cannot import name 'XetAuthorizationError' from 'huggingface_hub.errors' (/usr/local/lib/python3.13/dist-packages/huggingface_hub/errors.py)

```

## Log
```
[  0.0 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.2 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.2 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.4 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  0.8 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.5 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.6 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  1.9 min] $ pip install -q 'transformers==4.57.6'
[  2.2 min] $ python train_second_part.py --config_path /kaggle/tmp/kt/configs/s2.yml  (log: train_second_log.txt)
[ 46.7 min] last progress: INFO:__main__:Epoch [2/99], Step [140/140], Loss: 0.37484, Disc Loss: 3.94137, Dur Loss: 1.13666, CE Loss: 0.07623, Norm Loss: 0.81283, F0 Loss: 3.03467, LM Los
[ 46.7 min] STEP stage 2 part 1 (2 epochs): OK 44.5 min; peaks ['PEAK_GB [8.88, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00000.pth', 'PEAK_GB [8.88, 6.56] saved /kaggle/tmp/logs/s2/epoch_2nd_00001.pth']; log lines with GenLM>0: 56/56, Gen>0: 56/56
[ 46.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 47.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 47.3 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 47.4 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/s2/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run3-ma
[ 47.6 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[ 47.6 min] STEP ERROR: FAILED 
```

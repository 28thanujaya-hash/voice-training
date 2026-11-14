# Run 3 · stage-2 memory probe

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| probe crop200_b2 | ❌ | 0 steps, peak GB None, None s/step, adversarial steps 0 |
| probe crop150_b2 | ❌ | 0 steps, peak GB None, None s/step, adversarial steps 0 |
| probe crop100_b2 | ❌ | 0 steps, peak GB None, None s/step, adversarial steps 0 |
| probe crop200_b1 | ❌ | 0 steps, peak GB None, None s/step, adversarial steps 0 |
| probe crop120_b2 | ❌ | 0 steps, peak GB None, None s/step, adversarial steps 0 |

## Memory probe (joint phase from step 1; T4 = 14.56 GB usable)

| setting | crop (frames) | batch | finished | out of memory | steps | peak GB GPU0 / GPU1 | s per step | steps with generator adversarial loss | steps with SLM adversarial loss |
|---|---|---|---|---|---|---|---|---|---|
| crop200_b2 | 200 | 2 | yes | no | 0 |  | None | 0 | 0 |
| crop150_b2 | 150 | 2 | yes | no | 0 |  | None | 0 | 0 |
| crop100_b2 | 100 | 2 | yes | no | 0 |  | None | 0 | 0 |
| crop200_b1 | 200 | 1 | no | no | 0 |  | None | 0 | 0 |
| crop120_b2 | 120 | 2 | yes | no | 0 |  | None | 0 | 0 |

Crop frames: 80 frames ≈ 1 s of speech. Each setting started fresh from the same stage-1 checkpoint.
RESULT: DONE

## Log
```
[  0.0 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.3 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  0.9 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.6 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.7 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.1 min] stage-1 checkpoint: /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-teacher/kokoro_maya_v01_stage1.pth
[  2.2 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_b2.yml  (log: probe_crop200_b2.txt)
[ 31.3 min] PROBE RESULT {'name': 'crop200_b2', 'crop': 200, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 0, 'peak': None, 's_per_step': None, 'slm_steps': 0, 'gen_steps': 0, 'minutes': 29.1}
[ 31.3 min] STEP probe crop200_b2: FAILED 0 steps, peak GB None, None s/step, adversarial steps 0
[ 31.3 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop150_b2.yml  (log: probe_crop150_b2.txt)
[ 58.5 min] PROBE RESULT {'name': 'crop150_b2', 'crop': 150, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 0, 'peak': None, 's_per_step': None, 'slm_steps': 0, 'gen_steps': 0, 'minutes': 27.2}
[ 58.5 min] STEP probe crop150_b2: FAILED 0 steps, peak GB None, None s/step, adversarial steps 0
[ 58.5 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop100_b2.yml  (log: probe_crop100_b2.txt)
[ 85.0 min] PROBE RESULT {'name': 'crop100_b2', 'crop': 100, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 0, 'peak': None, 's_per_step': None, 'slm_steps': 0, 'gen_steps': 0, 'minutes': 26.5}
[ 85.0 min] STEP probe crop100_b2: FAILED 0 steps, peak GB None, None s/step, adversarial steps 0
[ 85.0 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_b1.yml  (log: probe_crop200_b1.txt)
[ 85.7 min] PROBE RESULT {'name': 'crop200_b1', 'crop': 200, 'batch': 1, 'rc': 1, 'oom': False, 'steps': 0, 'peak': None, 's_per_step': None, 'slm_steps': 0, 'gen_steps': 0, 'minutes': 0.7}
[ 85.7 min] STEP probe crop200_b1: FAILED 0 steps, peak GB None, None s/step, adversarial steps 0
[ 85.7 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop120_b2.yml  (log: probe_crop120_b2.txt)
[112.8 min] PROBE RESULT {'name': 'crop120_b2', 'crop': 120, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 0, 'peak': None, 's_per_step': None, 'slm_steps': 0, 'gen_steps': 0, 'minutes': 27.1}
[112.8 min] STEP probe crop120_b2: FAILED 0 steps, peak GB None, None s/step, adversarial steps 0
```

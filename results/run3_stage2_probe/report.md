# Run 3 · stage-2 memory probe v3 (SLM step enabled: batch_percentage 1.0)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| probe crop200_slm500 | ❌ | 1 steps, peak GB [7.62, 6.53], None s/step, adversarial steps 0 |
| probe crop200_slm250 | ❌ | 1 steps, peak GB [7.62, 6.54], None s/step, adversarial steps 0 |
| probe crop150_slm250 | ❌ | 1 steps, peak GB [6.51, 5.39], None s/step, adversarial steps 0 |
| probe crop120_slm250 | ❌ | 1 steps, peak GB [5.84, 4.73], None s/step, adversarial steps 0 |

## Memory probe (joint phase from step 1; T4 = 14.56 GB usable)

| setting | crop (frames) | batch | finished | out of memory | steps | peak GB GPU0 / GPU1 | s per step | steps with generator adversarial loss | steps with SLM adversarial loss |
|---|---|---|---|---|---|---|---|---|---|
| crop200_slm500 | 200 | 2 | no | no | 1 | 7.62 / 6.53 | None | 1 | 0 |
| crop200_slm250 | 200 | 2 | no | no | 1 | 7.62 / 6.54 | None | 1 | 0 |
| crop150_slm250 | 150 | 2 | no | no | 1 | 6.51 / 5.39 | None | 1 | 0 |
| crop120_slm250 | 120 | 2 | no | no | 1 | 5.84 / 4.73 | None | 1 | 0 |

Crop frames: 80 frames ≈ 1 s of speech. Each setting started fresh from the same stage-1 checkpoint.
RESULT: DONE

## Log
```
[  0.0 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.1 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.3 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  1.0 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.7 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.8 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.2 min] stage-1 checkpoint: /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-teacher/kokoro_maya_v01_stage1.pth
[  2.3 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_slm500.yml  (log: probe_crop200_slm500.txt)
[  4.0 min] PROBE RESULT {'name': 'crop200_slm500', 'crop': 200, 'batch': 2, 'rc': 1, 'oom': False, 'steps': 1, 'peak': [7.62, 6.53], 's_per_step': None, 'slm_steps': 0, 'gen_steps': 1, 'minutes': 1.7}
[  4.0 min] STEP probe crop200_slm500: FAILED 1 steps, peak GB [7.62, 6.53], None s/step, adversarial steps 0
[  4.0 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_slm250.yml  (log: probe_crop200_slm250.txt)
[  4.6 min] PROBE RESULT {'name': 'crop200_slm250', 'crop': 200, 'batch': 2, 'rc': 1, 'oom': False, 'steps': 1, 'peak': [7.62, 6.54], 's_per_step': None, 'slm_steps': 0, 'gen_steps': 1, 'minutes': 0.6}
[  4.6 min] STEP probe crop200_slm250: FAILED 1 steps, peak GB [7.62, 6.54], None s/step, adversarial steps 0
[  4.6 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop150_slm250.yml  (log: probe_crop150_slm250.txt)
[  5.3 min] PROBE RESULT {'name': 'crop150_slm250', 'crop': 150, 'batch': 2, 'rc': 1, 'oom': False, 'steps': 1, 'peak': [6.51, 5.39], 's_per_step': None, 'slm_steps': 0, 'gen_steps': 1, 'minutes': 0.6}
[  5.3 min] STEP probe crop150_slm250: FAILED 1 steps, peak GB [6.51, 5.39], None s/step, adversarial steps 0
[  5.3 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop120_slm250.yml  (log: probe_crop120_slm250.txt)
[  5.9 min] PROBE RESULT {'name': 'crop120_slm250', 'crop': 120, 'batch': 2, 'rc': 1, 'oom': False, 'steps': 1, 'peak': [5.84, 4.73], 's_per_step': None, 'slm_steps': 0, 'gen_steps': 1, 'minutes': 0.6}
[  5.9 min] STEP probe crop120_slm250: FAILED 1 steps, peak GB [5.84, 4.73], None s/step, adversarial steps 0
```

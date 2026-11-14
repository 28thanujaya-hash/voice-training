# Run 3 · stage-2 memory probe v5 (transformers 4.57.6 + SLM step enabled: batch_percentage 1.0)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| WavLM returns 13 layers in eval and train mode | ✅ | transformers 4.57.6 |
| probe crop200_slm500 | ✅ | 21 steps, peak GB [8.84, 6.55], 9.5 s/step, adversarial steps 20 |
| probe crop200_slm250 | ✅ | 21 steps, peak GB [8.81, 6.56], 9.5 s/step, adversarial steps 20 |
| probe crop150_slm250 | ✅ | 21 steps, peak GB [7.77, 5.42], 9.3 s/step, adversarial steps 20 |
| probe crop120_slm250 | ✅ | 21 steps, peak GB [6.98, 4.73], 9.1 s/step, adversarial steps 20 |

## WavLM diagnosis

- WavLM diagnosis (transformers 4.57.6, eval and train mode, 8 calls each): `{"transformers": "4.57.6", "class": "WavLMModel", "num_hidden_layers": 12, "eval": [13, 13, 13, 13, 13, 13, 13, 13], "train": [13, 13, 13, 13, 13, 13, 13, 13]}`

## Memory probe (joint phase from step 1; T4 = 14.56 GB usable)

| setting | crop (frames) | batch | finished | out of memory | steps | peak GB GPU0 / GPU1 | s per step | steps with generator adversarial loss | steps with SLM adversarial loss |
|---|---|---|---|---|---|---|---|---|---|
| crop200_slm500 | 200 | 2 | yes | no | 21 | 8.84 / 6.55 | 9.5 | 21 | 20 |
| crop200_slm250 | 200 | 2 | yes | no | 21 | 8.81 / 6.56 | 9.5 | 21 | 20 |
| crop150_slm250 | 150 | 2 | yes | no | 21 | 7.77 / 5.42 | 9.3 | 21 | 20 |
| crop120_slm250 | 120 | 2 | yes | no | 21 | 6.98 / 4.73 | 9.1 | 21 | 20 |

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
[  0.4 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  0.9 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.8 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.9 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.2 min] stage-1 checkpoint: /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-teacher/kokoro_maya_v01_stage1.pth
[  2.2 min] $ pip install -q 'transformers==4.57.6'
[  2.6 min] $ python /kaggle/tmp/diag.py
[  3.7 min] WavLM diagnosis (transformers 4.57.6, eval and train mode, 8 calls each): {'transformers': '4.57.6', 'class': 'WavLMModel', 'num_hidden_layers': 12, 'eval': [13, 13, 13, 13, 13, 13, 13, 13], 'train': [13, 13, 13, 13, 13, 13, 13, 13]}
[  3.7 min] STEP WavLM returns 13 layers in eval and train mode: OK transformers 4.57.6
[  3.7 min] losses.py: 6 WavLM calls; 6 lines patched
[  3.8 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_slm500.yml  (log: probe_crop200_slm500.txt)
[  7.7 min] last progress: INFO:__main__:Epoch [1/1], Step [20/140], Loss: 0.38491, Disc Loss: 4.95856, Dur Loss: 1.01302, CE Loss: 0.06725, Norm Loss: 1.35104, F0 Loss: 4.95258, LM Loss:
[  7.7 min] PROBE RESULT {'name': 'crop200_slm500', 'crop': 200, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 21, 'peak': [8.84, 6.55], 's_per_step': 9.5, 'slm_steps': 20, 'gen_steps': 21, 'minutes': 4.0}
[  7.7 min] STEP probe crop200_slm500: OK 21 steps, peak GB [8.84, 6.55], 9.5 s/step, adversarial steps 20
[  7.8 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop200_slm250.yml  (log: probe_crop200_slm250.txt)
[ 11.4 min] last progress: INFO:__main__:Epoch [1/1], Step [20/140], Loss: 0.41250, Disc Loss: 4.85716, Dur Loss: 0.96570, CE Loss: 0.06283, Norm Loss: 0.84469, F0 Loss: 4.91634, LM Loss:
[ 11.4 min] PROBE RESULT {'name': 'crop200_slm250', 'crop': 200, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 21, 'peak': [8.81, 6.56], 's_per_step': 9.5, 'slm_steps': 20, 'gen_steps': 21, 'minutes': 3.7}
[ 11.4 min] STEP probe crop200_slm250: OK 21 steps, peak GB [8.81, 6.56], 9.5 s/step, adversarial steps 20
[ 11.4 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop150_slm250.yml  (log: probe_crop150_slm250.txt)
[ 15.0 min] last progress: INFO:__main__:Epoch [1/1], Step [20/140], Loss: 0.44252, Disc Loss: 4.76952, Dur Loss: 1.00377, CE Loss: 0.05971, Norm Loss: 1.74113, F0 Loss: 5.72136, LM Loss:
[ 15.0 min] PROBE RESULT {'name': 'crop150_slm250', 'crop': 150, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 21, 'peak': [7.77, 5.42], 's_per_step': 9.3, 'slm_steps': 20, 'gen_steps': 21, 'minutes': 3.6}
[ 15.0 min] STEP probe crop150_slm250: OK 21 steps, peak GB [7.77, 5.42], 9.3 s/step, adversarial steps 20
[ 15.0 min] $ python train_second_probe.py --config_path /kaggle/tmp/kt/configs/crop120_slm250.yml  (log: probe_crop120_slm250.txt)
[ 18.6 min] last progress: INFO:__main__:Epoch [1/1], Step [20/140], Loss: 0.40951, Disc Loss: 4.97534, Dur Loss: 1.06049, CE Loss: 0.11116, Norm Loss: 0.72301, F0 Loss: 3.73626, LM Loss:
[ 18.6 min] PROBE RESULT {'name': 'crop120_slm250', 'crop': 120, 'batch': 2, 'rc': 0, 'oom': False, 'steps': 21, 'peak': [6.98, 4.73], 's_per_step': 9.1, 'slm_steps': 20, 'gen_steps': 21, 'minutes': 3.5}
[ 18.6 min] STEP probe crop120_slm250: OK 21 steps, peak GB [6.98, 4.73], 9.1 s/step, adversarial steps 20
```

# Run 1 · stage 3: Paradee with Sam and Maya's 8 rows (smoke run)

| step | result | note |
|---|---|---|
| stage-2 teacher + voicepacks found | ✅ |  |
| tools installed | ✅ |  |
| Paradee text half trained (600 steps) | ✅ | held-out loss 6.724 → 0.399 |
| Paradee decoder trained (600 steps) | ✅ | held-out loss 6.643 → 1.457; 7.1 min for stage 3 training, 610 teacher readings |
| exported as one int8 ONNX file | ✅ | 8.5 MB |
| the phone's way works (misaki-g2p → ONNX Runtime int8) | ✅ | 25.5× real time on one CPU thread |

## What the trained Paradee file said (Whisper)

- sam_normal: “So, how was your weekend? Did you do anything fun?” → heard “Okay.”
- sam_bright: “No way! That's amazing!” → heard “. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .”
- maya_normal: “Hmm, interesting. Tell me more about it.” → heard “you”
- maya_low: “Oh… I'm so sorry. Take your time.” → heard “. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .”

RESULT: PASS

## Log
```
[  0.0 min] STEP stage-2 teacher + voicepacks found: OK 
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/lex
[  0.3 min] $ git clone -q --depth 1 https://github.com/sahilmahendrakar/paradee
[  0.3 min] $ pip install -q --no-deps --ignore-requires-python 'kokoro==0.9.4' && pip install -q attrs loguru onnx onnxruntime
[  0.4 min] STEP tools installed: OK 
[  0.4 min] $ python paradee_run1.py --paradee /kaggle/tmp/paradee --teacher /kaggle/input/notebooks/thusharajayawardane/se-run1-kokoro/kokoro_run1.pth --kconfig /root/.cache
[  7.5 min] STEP Paradee text half trained (600 steps): OK held-out loss 6.724 → 0.399
[  7.5 min] STEP Paradee decoder trained (600 steps): OK held-out loss 6.643 → 1.457; 7.1 min for stage 3 training, 610 teacher readings
[  7.5 min] STEP exported as one int8 ONNX file: OK 8.5 MB
[  7.5 min] $ cp /kaggle/tmp/p3/config.json /kaggle/working/paradee_config.json
[  7.5 min] $ cp /kaggle/tmp/p3/export_log.txt /kaggle/working/paradee_export_log.txt
[  7.5 min] $ cp /kaggle/tmp/p3/stage3.json /kaggle/working/paradee_stage3.json
[  7.5 min] $ cp /kaggle/tmp/p3/onnx/paradee_int8.onnx /kaggle/working/paradee_run1_int8.onnx
[  8.1 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/l.wav -b:a 64k /kaggle/working/run1_paradee_listen.mp3
[  8.1 min] STEP the phone's way works (misaki-g2p → ONNX Runtime int8): OK 25.5× real time on one CPU thread
```

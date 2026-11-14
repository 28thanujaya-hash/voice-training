# Run 3 · Maya pilot (voice v0.1) · stage 2: Kokoro teacher + G2

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| Kokoro stage 1 (acoustic) | ✅ | 10 epochs, 69.0 min |
| Kokoro stage 2 (prosody + adversarial) | ❌ | 6 epochs, 259.3 min; 4 checkpoints — FAILED, continuing with the last checkpoint |
| voicepacks (4 rows) | ✅ |  |
| teacher and baseline read the 200 test lines | ✅ |  |
| G2 judged (Whisper, UTMOS, emotion2vec, WavLM) | ✅ |  |
| blind listening pack (20 clips) | ✅ |  |

Teacher = stage-2 checkpoint epoch_2nd_00003.pth

## G2 (draft standard: word error < 3%, naturalness ≥ 4.0, rows told apart ≥ 80%)

| | word error | naturalness (UTMOS, /5) | sounds like tara (similarity) | rows told apart |
|---|---|---|---|---|
| **teacher (v0.1)** | **3.3%** | **3.86** | **0.934** | **44%** |
| baseline (stock Kokoro af_heart) | 4.2% | 4.44 | 0.849 | – |
| tara's own clips (the source) | – | 3.93 | 0.955 | 61% (ceiling) |

Rows told apart = an emotion2vec nearest-centroid judge, trained on tara's kept clips, names the row of each teacher line.

### Teacher by row

| row | word error | naturalness | told apart |
|---|---|---|---|
| normal | 5.3% | 3.93 | 42/78 |
| bright | 3.0% | 3.82 | 13/47 |
| low | 1.4% | 3.75 | 22/40 |
| tense | 0.4% | 3.87 | 12/35 |

### Teacher by kind

| kind | lines | word error | naturalness |
|---|---|---|---|
| lesson | 22 | 3.6% | 3.74 |
| live | 23 | 0.6% | 4.04 |
| gen | 89 | 1.1% | 3.99 |
| hard | 66 | 9.8% | 3.65 |

### Teacher lines with word errors

- mtn05 (lesson): “Late again?” → “Later then,”
- mtn09 (lesson): “Oh, Kandy? What did you do there?” → “Oh Candy, what did you do there?”
- mtn10 (lesson): “Oh, The Dark Knight? How many times have you seen it?” → “Oh, the dark night. How many times have you seen it?”
- mtn12 (lesson): “Say "uh-huh" or "really?" while I'm talking.” → “Say aha, or really, while I'm talking.”
- mtn19 (live): “You said "I go to Kandy yesterday". We say "I went to Kandy yesterday". Can you try it?” → “You said, I go to candy yesterday. We say, I went to candy yesterday. Can you try it?”
- mtn28 (gen): “The café gets really busy after six, when people finish work.” → “but gets really busy after six when people finish work.”
- mtn51 (hard): “Nineteen ninety-nine, two thousand and five, and twenty twenty-six.” → “1999, 2005, and 2026”
- mtn52 (hard): “The meeting is at 3:45 on the 21st of March.” → “The meeting is at 3.45 on the 21st of March.”
- mtn53 (hard): “It costs Rs. 2,500, but students pay only Rs. 1,250.” → “It costs R.S. $2,500, but students pay only R.S. $1,250.”
- mtn54 (hard): “Call me on 077 123 4567 after eight.” → “Call me on 77-123-4567 after 8.”
- mtn64 (hard): “Very well, we'll walk with Vicky to the village.” → “Very well. We'll walk with V.I.C.K.Y. to the village.”
- mtn69 (hard): “The WiFi password is "maya2024", all small letters.” → “The WAFI password is Maya2024, all small letters.”
- mtn75 (hard): “NOT the red one. The GREEN one.” → “N.O.T. the red one, the green one.”
- mtn78 (hard): “One, two, three, four, five, six, seven, eight, nine, ten.” → “1, 2, 3, 4, 5, 6, 7, 8, 9, 10.”
- mtb28 (gen): “It's snowing in the hills? Really? In Sri Lanka?” → “It's snowing in the hills, really, in Sri L.A.N.K.A.”
- mtb29 (gen): “My first pay as shift leader! Dinner's on me!” → “My first pay is shift leader. Dinner's on me.”
- mtb38 (hard): “We fly on the 14th at 6:30 a.m.!” → “We fly on the 14th at 6.30 a.m.”
- mtb45 (hard): “Ha ha! You should see your face!” → “Haha, you should see your face.”
- mtl12 (gen): “I tried my best… but it wasn't enough.” → “I tried my best to, but it wasn't enough.”
- mtl37 (hard): “Is it… is it serious?” → “As in, is it serious?”
- mtl40 (hard): “The last bus left at 10:15… and I missed it.” → “The last bus left at 10.15, and I missed it.”
- mtt27 (hard): “Rs. 4,750 for one shirt? No way.” → “RS, $4,750 for one shirt. No way.”
RESULT: FAIL

## Log
```
[  0.0 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.2 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.2 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.3 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  0.7 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.5 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.5 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.1 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/run3.yml  (log: train_first_log.txt)
[ 71.1 min] last progress: Epoch [10/10], Step [140/140], Mel Loss: 0.30841, Gen Loss: 3.11139, Disc Loss: 4.02968, Mono Loss: 0.11179, S2S Loss: 1.36517, SLM Loss: 1.50233
[ 71.1 min] STEP Kokoro stage 1 (acoustic): OK 10 epochs, 69.0 min
[ 71.1 min] $ python train_second.py --config_path /kaggle/tmp/kt/configs/run3.yml  (log: train_second_log.txt)
[330.4 min] last progress: Epoch [3/6], Step [140/140], Loss: 0.27342, Disc Loss: 0.00000, Dur Loss: 1.28969, CE Loss: 0.05953, Norm Loss: 1.01631, F0 Loss: 3.01696, LM Loss: 830.55908, G
[330.4 min] STEP Kokoro stage 2 (prosody + adversarial): FAILED 6 epochs, 259.3 min; 4 checkpoints — FAILED, continuing with the last checkpoint
[330.4 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run3/epoch_2nd_00003.pth --style-encoder-model /kaggle/tmp/logs/run3/epoch_1st_00009.pth --audio-di
[330.6 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run3/epoch_2nd_00003.pth --style-encoder-model /kaggle/tmp/logs/run3/epoch_1st_00009.pth --audio-di
[330.7 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run3/epoch_2nd_00003.pth --style-encoder-model /kaggle/tmp/logs/run3/epoch_1st_00009.pth --audio-di
[330.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run3/epoch_2nd_00003.pth --style-encoder-model /kaggle/tmp/logs/run3/epoch_1st_00009.pth --audio-di
[331.0 min] STEP voicepacks (4 rows): OK 
[331.0 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[332.5 min] STEP teacher and baseline read the 200 test lines: OK 
[337.6 min] STEP G2 judged (Whisper, UTMOS, emotion2vec, WavLM): OK 
[337.6 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/l.wav -b:a 64k /kaggle/working/run3_g2_listen.mp3
[337.6 min] STEP blind listening pack (20 clips): OK 
```

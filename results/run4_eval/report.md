# Run 4 · G2: teacher v0.2 A (with adversarial) vs B (without) vs stock Kokoro

## Validation (choosing)

| | word error | naturalness | sounds like tara | marks shown | mood from pitch+pace |
|---|---|---|---|---|---|
| A | 0.4% | 3.86 | 0.931 | 18/31 (58%) | 29% |
| B | 0.4% | 3.98 | 0.918 | 20/32 (62%) | 30% |
| stock | 0.0% | 4.45 | 0.831 | 10/27 (37%) | 21% |
| tara | 0.0% | 3.92 | 0.919 | 28/32 (88%) | 16% |

## Test (reporting only)

| | word error | naturalness | sounds like tara | marks shown | mood from pitch+pace |
|---|---|---|---|---|---|
| A | 2.8% | 3.80 | 0.917 | 114/315 (36%) | 34% |
| B | 3.0% | 3.96 | 0.905 | 113/317 (36%) | 33% |
| stock | 2.1% | 4.42 | 0.817 | 84/287 (29%) | 25% |

### Test, A: shows the mark (same thresholds as the actor audit)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| ? (yes/no) | 5/40 | 6/18 | 1/12 | 1/11 |
| ?! | 0/5 | 1/6 | 0/5 | 0/5 |
| ! | 7/18 | 11/69 | 3/7 | 3/6 |
| … | 15/20 | 4/6 | 18/21 | 2/5 |
| — | 9/9 | 6/6 | 5/5 | 6/6 |
| CAPS | 7/17 | 2/7 | 1/5 | 1/6 |

### Test, B: shows the mark (same thresholds as the actor audit)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| ? (yes/no) | 7/41 | 6/18 | 2/13 | 0/11 |
| ?! | 0/5 | 0/6 | 0/5 | 0/5 |
| ! | 3/18 | 13/69 | 1/7 | 2/6 |
| … | 15/20 | 4/6 | 18/21 | 2/5 |
| — | 9/9 | 6/6 | 5/5 | 6/6 |
| CAPS | 6/17 | 4/7 | 2/5 | 2/6 |

### Test, stock: shows the mark (same thresholds as the actor audit)

| mark | normal | bright | low | tense |
|---|---|---|---|---|
| ? (yes/no) | 4/31 | 0/14 | 0/8 | 0/9 |
| ?! | 0/4 | 1/5 | 0/4 | 0/4 |
| ! | 13/18 | 32/68 | 5/6 | 3/5 |
| … | 6/20 | 3/6 | 4/21 | 3/5 |
| — | 0/9 | 0/6 | 0/5 | 0/6 |
| CAPS | 7/16 | 1/6 | 1/5 | 1/6 |

### Marks v2: marked minus plain, same sentence and mood (median over 5 sentences × 4 moods)

| mark | measure | A | B | stock |
|---|---|---|---|---|
| ? | end rise vs plain (st) | – | – | – |
| ?! | end rise vs plain ? (st) | +0.02 (n 20) | -0.30 (n 20) | -0.18 (n 16) |
| ! | livelier vs plain (st) | +0.22 (n 20) | +0.11 (n 20) | +0.14 (n 17) |
| … | pause or drawn-out (s / ×) | +1.16 (n 20) | +1.12 (n 20) | +1.10 (n 20) |
| — | pause (s) | +0.59 (n 20) | +0.42 (n 20) | +0.02 (n 20) |
| CAPS | stressed word vs others (st) | -2.16 (n 20) | -0.31 (n 20) | -2.76 (n 20) |

### Moods on the matched lines (30 sentences × 4 moods): median pitch level / range (st)

| model | normal | bright | low | tense |
|---|---|---|---|---|
| A | 12.1 / 8.2 | 12.5 / 8.3 | 12.1 / 8.2 | 12.1 / 8.1 |
| B | 12.8 / 7.1 | 13.2 / 7.1 | 12.9 / 7.0 | 12.9 / 7.1 |
| stock | 12.0 / 7.8 | 12.0 / 7.8 | 11.8 / 7.7 | 11.9 / 7.8 |

### Test lines with word errors (A and B)

- A mtn05: “Late again?” → “Lead again.”
- B mtn05: “Late again?” → “Read again.”
- A mtn10: “Oh, The Dark Knight? How many times have you seen it?” → “Oh, the dark night. How many times have you seen it?”
- A mtn24: “You can say it in Sinhala if you need to, and I'll help you with the English.” → “You can say it in SINHLA if you need to, and I'll help you with the English.”
- B mtn24: “You can say it in Sinhala if you need to, and I'll help you with the English.” → “You can say it in SINHRLA if you need to, and I'll help you with the English.”
- A mtn28: “The café gets really busy after six, when people finish work.” → “It gets really busy after six, when people finish work.”
- B mtn28: “The café gets really busy after six, when people finish work.” → “But gets really busy after 6, when people finish work.”
- A mtn51: “Nineteen ninety-nine, two thousand and five, and twenty twenty-six.” → “1999, 2005, and 2026.”
- B mtn51: “Nineteen ninety-nine, two thousand and five, and twenty twenty-six.” → “1999, 2005, and 2026.”
- A mtn52: “The meeting is at 3:45 on the 21st of March.” → “The meeting is at 3.45 on the 21st of March.”
- B mtn52: “The meeting is at 3:45 on the 21st of March.” → “The meeting is at 3.45 on the 21st of March.”
- A mtn53: “It costs Rs. 2,500, but students pay only Rs. 1,250.” → “It costs R.S. $2,500, but students pay only R.S. $1,250.”
- B mtn53: “It costs Rs. 2,500, but students pay only Rs. 1,250.” → “It costs R.S. $2,500, but students pay only R.S. $1,250.”
- A mtn54: “Call me on 077 123 4567 after eight.” → “Call me on 77-123-4567 after 8.”
- B mtn54: “Call me on 077 123 4567 after eight.” → “Call me on 77-123-4567 after 8.”
- A mtn64: “Very well, we'll walk with Vicky to the village.” → “Very well. We'll walk with V.I.C.K.Y. to the village.”
- B mtn64: “Very well, we'll walk with Vicky to the village.” → “Very well. We'll walk with V.I.C.K.Y. to the village.”
- A mtn68: “Ayubowan! Kohomada? That's all the Sinhala I know.” → “A-Y-U-B-O-W-U-N K-O-H-M-A-D That's all the S-I-N-H-A-L-A I know.”
- B mtn68: “Ayubowan! Kohomada? That's all the Sinhala I know.” → “That's all the S-I-N-H-R-L-A I know.”
- A mtn69: “The WiFi password is "maya2024", all small letters.” → “The WAFI password is Maya2024, all small letters.”
- B mtn69: “The WiFi password is "maya2024", all small letters.” → “The WFI password is Maya2024. All small letters.”
- A mtn78: “One, two, three, four, five, six, seven, eight, nine, ten.” → “1, 2, 3, 4, 5, 6, 7, 8, 9, 10.”
- B mtn78: “One, two, three, four, five, six, seven, eight, nine, ten.” → “1, 2, 3, 4, 5, 6, 7, 8, 9, 10.”
- A mtb28: “It's snowing in the hills? Really? In Sri Lanka?” → “It's snowing in the hills, really, in Sri Alain Ka.”
- B mtb28: “It's snowing in the hills? Really? In Sri Lanka?” → “It's snowing in the hills, really, in Sri L.A. & K.”
- A mtb29: “My first pay as shift leader! Dinner's on me!” → “My first pay is shift leader. Dinner's on me.”
- B mtb29: “My first pay as shift leader! Dinner's on me!” → “My first pay is shift leader. Dinner's on me.”
- A mtb38: “We fly on the 14th at 6:30 a.m.!” → “We fly on the 14th at 6.30 a.m.”
- B mtb38: “We fly on the 14th at 6:30 a.m.!” → “We fly on the 14th at 6.30 a.m.”
- A mtb45: “Ha ha! You should see your face!” → “Haha, you should see your face.”
- B mtb45: “Ha ha! You should see your face!” → “Haha, you should see your face.”
- A mtl40: “The last bus left at 10:15… and I missed it.” → “The last bus left at 10.15 and I missed it.”
- B mtl40: “The last bus left at 10:15… and I missed it.” → “The last bus left at 10.15 and I missed it.”
- A mtt24: “Enough.” → “Love.”
- B mtt24: “Enough.” → “Love.”
- A mtt34: “Put it back. Now.” → “Put it back. No.”
- A mtm01n: “We're going back to the café after class.” → “We're going back to the after class.”
- B mtm01n: “We're going back to the café after class.” → “We're going back to the after class.”
- A mtm01b: “We're going back to the café after class.” → “We're going back to the after class.”
- B mtm01b: “We're going back to the café after class.” → “We're going back to the after class.”
- A mtm01l: “We're going back to the café after class.” → “We're going back to the after class.”
- B mtm01l: “We're going back to the café after class.” → “We're going back to the after class.”
- A mtm01t: “We're going back to the café after class.” → “We're going back to the after class.”
- B mtm01t: “We're going back to the café after class.” → “We're going back to the after class.”
- A mtm15n: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- B mtm15n: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- A mtm15b: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- B mtm15b: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- A mtm15l: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- B mtm15l: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- A mtm15t: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- B mtm15t: “There's nobody at the café tonight.” → “There's nobody at the tonight.”
- B mtm19n: “They're closing the old bookshop next month.” → “They're closing the old BUOKSHOP next month.”
- A mtm19l: “They're closing the old bookshop next month.” → “They're closing the old BOKSHOP next month.”
- B mtm19l: “They're closing the old bookshop next month.” → “They're closing the old BUOKSHOP next month.”
- A mtm19t: “They're closing the old bookshop next month.” → “They're closing the old BOO-KSHOP next month.”
- A mtp023: “You finished it!” → “You finished that?”
- B mtp113: “SHE bought the red one.” → “She bought the red wine.”
- A mtp142: “He LIVES in Kandy.” → “Hidden lives in candy.”
- B mtq06np: “That's the bus.” → “That's the boss.”

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa torchcrepe scikit-learn loguru munch einops einops-exts nltk pydub accelerate
[  1.1 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  1.3 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  1.5 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  1.5 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  1.6 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  2.0 min] validation 38 · test 620 · models ['A', 'B', 'stock']
[  4.8 min] val done
[ 27.9 min] test done
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/01_question_normal_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/01_question_normal_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/02_surprise-qx_bright_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/02_surprise-qx_bright_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/03_exclaim_low_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/03_exclaim_low_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/04_dots_tense_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/04_dots_tense_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/05_dash_normal_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/05_dash_normal_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/06_CAPS_bright_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/06_CAPS_bright_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/07_mood_normal_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/07_mood_normal_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/08_mood_bright_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/08_mood_bright_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/09_mood_low_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/09_mood_low_Y.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/10_mood_tense_X.mp3
[ 27.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/10_mood_tense_Y.mp3
```

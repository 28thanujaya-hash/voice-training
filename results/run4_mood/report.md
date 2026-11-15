# Run 4 · mood control experiment (voicepack settings, no training)

A: voicepack shape (510, 1, 256); cosine to normal: bright 0.9971, low 0.9996, tense 0.9988 · prosody half: bright 0.9976, low 0.9997, tense 0.9987 · acoustic half: bright 0.9964, low 0.9994, tense 0.9990
B: voicepack shape (510, 1, 256); cosine to normal: bright 0.9974, low 0.9996, tense 0.9990 · prosody half: bright 0.9981, low 0.9997, tense 0.9991 · acoustic half: bright 0.9964, low 0.9994, tense 0.9990

## Matched lines: per setting

| model | setting | normal | bright | low | tense | mood from pitch+pace | word error | naturalness | same voice |
|---|---|---|---|---|---|---|---|---|---|
| A | base | 12.0 / 8.2 / 2.11 | 12.5 / 8.3 / 2.15 | 12.1 / 8.2 / 2.11 | 12.2 / 8.1 / 2.11 | 35% | 1.8% | 3.99 | 0.967 |
| A | x2 | 12.1 / 8.2 / 2.11 | 13.0 / 8.3 / 2.19 | 12.2 / 8.2 / 2.08 | 12.4 / 7.9 / 2.09 | 46% | 1.9% | 4.00 | 0.966 |
| A | x3p | 12.1 / 8.1 / 2.11 | 13.6 / 8.2 / 2.21 | 12.1 / 8.1 / 2.08 | 12.4 / 7.7 / 2.09 | 52% | 2.3% | 4.02 | 0.966 |
| A | x5p | 12.1 / 8.3 / 2.11 | 14.8 / 8.0 / 2.24 | 12.1 / 8.2 / 2.07 | 12.5 / 7.7 / 2.10 | 57% | 1.8% | 4.02 | 0.965 |
| B | base | 12.8 / 7.2 / 2.11 | 13.2 / 7.2 / 2.13 | 12.8 / 7.1 / 2.10 | 12.9 / 7.0 / 2.10 | 32% | 2.8% | 4.18 | 0.967 |
| B | x2 | 12.9 / 7.1 / 2.11 | 13.3 / 7.3 / 2.15 | 13.1 / 7.2 / 2.07 | 13.0 / 6.9 / 2.09 | 35% | 2.9% | 4.18 | 0.964 |
| B | x3p | 12.9 / 7.1 / 2.11 | 13.7 / 7.1 / 2.17 | 13.0 / 7.1 / 2.06 | 12.9 / 6.9 / 2.07 | 42% | 3.1% | 4.18 | 0.967 |
| B | x5p | 12.9 / 7.1 / 2.11 | 14.2 / 6.9 / 2.25 | 13.0 / 7.0 / 2.03 | 13.0 / 6.6 / 2.04 | 48% | 3.0% | 4.18 | 0.966 |

Cells: pitch level / pitch range (semitones) / pace (words per second). Chance for the mood guess = 25%.

Best settings that keep words and naturalness (word error < 6%, naturalness > 3.5): A x5p (57%), A x3p (52%)

Clips: listen/mood_<model>_<setting>_<mood>.mp3 — sentence: “He called me three times last night.”

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa torchcrepe scikit-learn loguru munch einops einops-exts nltk pydub accelerate
[  1.2 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  1.2 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  1.4 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  1.5 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  1.6 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  4.2 min] A base done
[  5.8 min] A x2 done
[  7.3 min] A x3p done
[  8.8 min] A x5p done
[ 10.3 min] B base done
[ 11.9 min] B x2 done
[ 13.4 min] B x3p done
[ 14.9 min] B x5p done
[ 14.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x5p_normal.mp3
[ 14.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x5p_bright.mp3
[ 14.9 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x5p_low.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x5p_tense.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x3p_normal.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x3p_bright.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x3p_low.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_x3p_tense.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_base_normal.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_base_bright.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_base_low.mp3
[ 15.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mood_A_base_tense.mp3
```

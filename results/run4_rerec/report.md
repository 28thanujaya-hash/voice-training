# Run 4 · step B: re-record pilot (low + tense), lead-in cut by forced alignment, natural loudness

Lines 78 · takes 468 · usable 330 · lines with a kept take 71 · rejected: {'words/pace': 131, 'measure': 6, 'no gap': 1}

## Chosen new takes vs the old takes of the same lines (median)

| mood | lines | pitch old → new | range old → new | pace old → new | tilt dB old → new | loudness new (LUFS) |
|---|---|---|---|---|---|---|
| normal | 9 | 10.2 → 9.9 | 5.6 → 3.9 | 1.40 → 2.60 | -11.4 → -10.3 | -26.6 |
| bright | 8 | 14.3 → 14.0 | 10.9 → 8.6 | 1.53 → 2.24 | -8.5 → -10.2 | -20.9 |
| low | 27 | 11.6 → 10.6 | 6.3 → 4.7 | 1.89 → 2.34 | -12.9 → -12.4 | -28.8 |
| tense | 27 | 11.3 → 11.9 | 6.5 → 6.0 | 1.82 → 2.65 | -11.6 → -10.1 | -23.2 |

(Old takes were levelled to −20 LUFS; new takes keep their natural loudness.)

Blind pack 2: 33 clips (blind2/, blind2_sheet.md, blind2_key.md)

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe
[  1.1 min] 78 lines: 35 group lines + 43 extra
[ 20.4 min] recorded 78 × 6 in 18.5 min
[ 24.8 min] 330 usable takes; rejected: {'words/pace': 131, 'measure': 6, 'no gap': 1}
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_01.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_02.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_03.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_04.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_05.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_06.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_07.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_08.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_09.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_10.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_11.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_12.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_13.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_14.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_15.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_16.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_17.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_18.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_19.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_20.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_21.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_22.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_23.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_24.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_25.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_26.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_27.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_28.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_29.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_30.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_31.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_32.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/blind2/actor_blind2_33.mp3
```

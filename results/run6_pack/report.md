# Run 6 · diagnostic pack: Orpheus (new lead-ins) vs IndexTTS-2.5 on 12 sentences × 4 moods

Clips measured: 279 · chosen (one per source × sentence × mood): 85 of 96 (Orpheus 38, IndexTTS 47)

## 1. Orpheus tara, new lead-ins: chosen takes, median

| measure | normal | bright | low | tense |
|---|---|---|---|---|
| syllables/s | 5.16 | 4.72 | 5.17 | 5.26 |
| pause share | 0.00 | 0.00 | 0.00 | 0.00 |
| pitch (st) | 10.19 | 12.88 | 9.45 | 9.74 |
| pitch movement (SD) | 1.43 | 2.96 | 1.31 | 1.61 |
| end fall (st/s) | 4.08 | -2.54 | -0.26 | 0.43 |
| loudness (LUFS) | -27.45 | -26.00 | -28.06 | -26.94 |
| loudness contrast (dB) | 6.39 | 6.55 | 6.33 | 6.67 |
| end loudness drop (dB) | -5.13 | -4.41 | -4.33 | -5.97 |
| CPP (clear/firm) | 18.57 | 18.51 | 18.73 | 18.19 |
| HNR | 15.88 | 14.83 | 17.64 | 14.79 |
| H1-H2 (breathy) | 6.41 | 5.99 | 6.60 | 4.50 |

## 1. IndexTTS-2.5, Maya cloned, emotion vector: chosen takes, median

| measure | normal | bright | low | tense |
|---|---|---|---|---|
| syllables/s | 3.29 | 3.04 | 2.32 | 3.43 |
| pause share | 0.17 | 0.07 | 0.34 | 0.04 |
| pitch (st) | 11.28 | 18.15 | 11.33 | 16.25 |
| pitch movement (SD) | 2.42 | 4.04 | 1.71 | 2.95 |
| end fall (st/s) | -5.51 | -17.22 | -3.21 | -10.03 |
| loudness (LUFS) | -21.93 | -18.80 | -25.94 | -17.89 |
| loudness contrast (dB) | 6.61 | 7.08 | 7.15 | 7.42 |
| end loudness drop (dB) | -2.90 | -0.02 | -1.82 | -4.92 |
| CPP (clear/firm) | 23.04 | 21.59 | 18.49 | 19.56 |
| HNR | 15.62 | 15.82 | 14.11 | 14.58 |
| H1-H2 (breathy) | 4.17 | 5.94 | 9.42 | 8.58 |

## 2. Mood bundle checks, sentence by sentence (12 sentences)

| check | Orpheus | IndexTTS |
|---|---|---|
| low slower than normal | 6/8 | 12/12 |
| low more pause than normal | 1/8 | 12/12 |
| low lower than normal | 6/8 | 7/12 |
| low quieter than normal | 4/8 | 12/12 |
| low breathier than normal | 5/8 | 12/12 |
| bright higher than normal | 8/8 | 11/11 |
| bright more pitch movement than normal | 8/8 | 11/11 |
| bright higher than tense | 7/9 | 8/11 |
| tense louder than normal | 6/8 | 10/12 |
| tense more loudness contrast than normal | 5/8 | 10/12 |
| tense less breathy than normal | 5/8 | 2/12 |
| tense falls more at the end than normal | 5/8 | 7/12 |
| normal between low and bright in pitch | 6/8 | 7/11 |
| normal between low and tense in loudness | 3/8 | 10/12 |

Blind test 5: 97 clips (85 + 12 hidden repeats), sessions A 48 / B 49; sheet blind5_sheet.md, key blind5_key.csv

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q praat-parselmouth pyloudnorm soundfile librosa cmudict num2words
[  1.6 min] measured 279 clips: orph 146, idx 133
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d06l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d10t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d11l_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d06n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d11t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d07l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d09n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d11t_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.6 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d09b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d04t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d10b_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05n_5.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d04b_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d04n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d01n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05l_4.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d08n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d08t_4.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d10n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d01t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d08l_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d02l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d07b_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03l_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d03l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05t_3.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d09b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d08b_4.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d01b_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d11n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d04t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d10l_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d03t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d09t_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d06n_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d06l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d06t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d05l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d02t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d12l_3.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.7 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d05b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d01l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d02n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d01b_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d12n_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d04l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d06b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d02t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d02t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d11b_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05l_4.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d08b_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d02n_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d03b_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05t_3.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d02l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d08b_4.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d12t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d10l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d11b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d01n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d12t_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d08n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d07l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d11n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d02b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d05n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d07n_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d12b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d09n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d08t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d01l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d12n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d02l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.8 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d03n_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d08l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d06t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d05t_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d12l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d01b_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d06b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d11l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d09l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d07t_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d01t_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d04l_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d12b_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d04b_2.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d03n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d05b_5.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d06l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-idx/takes/d04n_1.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/b
[  1.9 min] $ ffmpeg -loglevel error -y -i '/kaggle/input/notebooks/thusharajayawardane/se-run6-orph/takes/d07l_0.wav' -codec:a libmp3lame -b:a 96k /kaggle/working/
```

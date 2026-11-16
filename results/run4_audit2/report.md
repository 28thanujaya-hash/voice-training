# Run 4 · audit 2: are the mood settings trustworthy? + blind actor test

## Checkpoints

- stage 1 modules: ['bert', 'bert_encoder', 'decoder', 'diffusion', 'mpd', 'msd', 'pitch_extractor', 'predictor', 'predictor_encoder', 'style_encoder', 'text_aligner', 'text_encoder', 'wd']
- teacher A file modules: ['bert', 'bert_encoder', 'decoder', 'predictor', 'text_encoder']
- teacher B file modules: ['bert', 'bert_encoder', 'decoder', 'predictor', 'text_encoder']

- stage 1: style_encoder norm 42.95; predictor_encoder norm 41.43; identical: False

Note: the stage-2 full checkpoint (with predictor_encoder) was not saved as an output, only the Kokoro-format
modules + voicepacks. So per-clip prosody vectors are computed two ways: (i) stage-1 style_encoder for both halves
(what the extractor falls back to), (ii) compared against the saved packs to see which encoder made them.

## Single clips: is the mood in the style vectors?

| vectors | similarity within a mood | between moods | mood guessed from one clip (chance 25%) | average per mood vs normal (cosine) |
|---|---|---|---|---|
| acoustic half (stage-1 style_encoder) | 0.9520 | 0.9502 | 38% | bright 0.9965, low 0.9994, tense 0.9990 |
| prosody half (stage-1 predictor_encoder) | 0.9997 | 0.9997 | 42% | bright 1.0000, low 1.0000, tense 1.0000 |

- teacher A packs: normal: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0796 · bright: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0804 · low: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0765 · tense: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0708
- teacher B packs: normal: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0812 · bright: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0809 · low: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0784 · tense: rows differ by length? max 0.0000; pack acoustic vs clip-mean 1.0000; pack prosody vs stage-1 clip-mean 0.0743

(If 'pack prosody vs stage-1 clip-mean' ≈ 1.0, the packs' prosody half came from the stage-1 encoder, i.e. the extractor fell back; if clearly < 1, it came from the stage-2 predictor_encoder.)

## Marks in the training list (phoneme text the teacher saw)

?!: 120, ?: 270, …: 161, —: 123, ↗: 120, !: 402

## Blind actor test: 35 clips from 10 groups (blind/, blind_sheet.md, blind_key.md)

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q scikit-learn soundfile
[  0.2 min] $ git clone -q --depth 1 https://github.com/semidark/kikiri-tts kt
[  1.2 min] 577 clips embedded
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xn50.wav -b:a 64k /kaggle/working/blind/actor_blind_01.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3t13.wav -b:a 64k /kaggle/working/blind/actor_blind_02.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xt52.wav -b:a 64k /kaggle/working/blind/actor_blind_03.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3b25.wav -b:a 64k /kaggle/working/blind/actor_blind_04.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xn47.wav -b:a 64k /kaggle/working/blind/actor_blind_05.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xt51.wav -b:a 64k /kaggle/working/blind/actor_blind_06.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3n37.wav -b:a 64k /kaggle/working/blind/actor_blind_07.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xl47.wav -b:a 64k /kaggle/working/blind/actor_blind_08.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3n38.wav -b:a 64k /kaggle/working/blind/actor_blind_09.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xt49.wav -b:a 64k /kaggle/working/blind/actor_blind_10.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xb38.wav -b:a 64k /kaggle/working/blind/actor_blind_11.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xb34.wav -b:a 64k /kaggle/working/blind/actor_blind_12.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3t15.wav -b:a 64k /kaggle/working/blind/actor_blind_13.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3l20.wav -b:a 64k /kaggle/working/blind/actor_blind_14.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3l19.wav -b:a 64k /kaggle/working/blind/actor_blind_15.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xl49.wav -b:a 64k /kaggle/working/blind/actor_blind_16.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3b23.wav -b:a 64k /kaggle/working/blind/actor_blind_17.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xb37.wav -b:a 64k /kaggle/working/blind/actor_blind_18.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3t14.wav -b:a 64k /kaggle/working/blind/actor_blind_19.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xb36.wav -b:a 64k /kaggle/working/blind/actor_blind_20.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xl46.wav -b:a 64k /kaggle/working/blind/actor_blind_21.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xl45.wav -b:a 64k /kaggle/working/blind/actor_blind_22.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xn48.wav -b:a 64k /kaggle/working/blind/actor_blind_23.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3l18.wav -b:a 64k /kaggle/working/blind/actor_blind_24.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xt48.wav -b:a 64k /kaggle/working/blind/actor_blind_25.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xn46.wav -b:a 64k /kaggle/working/blind/actor_blind_26.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xl48.wav -b:a 64k /kaggle/working/blind/actor_blind_27.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3l17.wav -b:a 64k /kaggle/working/blind/actor_blind_28.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3n39.wav -b:a 64k /kaggle/working/blind/actor_blind_29.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3b22.wav -b:a 64k /kaggle/working/blind/actor_blind_30.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3b24.wav -b:a 64k /kaggle/working/blind/actor_blind_31.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3n40.wav -b:a 64k /kaggle/working/blind/actor_blind_32.m
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xn49.wav -b:a 64k /kaggle/working/blind/actor_blind_33.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xt50.wav -b:a 64k /kaggle/working/blind/actor_blind_34.
[  1.3 min] $ ffmpeg -loglevel error -y -i /kaggle/input/notebooks/thusharajayawardane/se-run4-audit/final/m3xb35.wav -b:a 64k /kaggle/working/blind/actor_blind_35.
```

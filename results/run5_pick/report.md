# Run 5 · pick: one take per line, mentor's mood rules, retakes, blind pack 3

Reference (best takes): normal pitch 11.0 st, loudness -27.2 LUFS, range 5.0; bright pitch 13.8, range 8.0

Lines retaken (no usable take, or low below the clip-14 standard): 267 (normal 52, bright 20, low 155, tense 40)


RESULT: ERROR
```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 202, in <module>
    for gname, mem in sorted(G.items(), key=lambda x: int(x[0][1:])):
                      ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/kaggle/src/script.py", line 202, in <lambda>
    for gname, mem in sorted(G.items(), key=lambda x: int(x[0][1:])):
                                                      ~~~^^^^^^^^^^
ValueError: invalid literal for int() with base 10: "t's Monday again…"

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe
[  1.4 min] takes for 446 of 625 lines
[110.0 min] retake round 1: 267 lines × 6 in 107.7 min; still failing 243; rejects {'pace': 857, 'words': 116, 'no words': 42, 'measure': 222}
```

# Run 5 · pick 3 (mood zones from the mentor's blind test 3; G1 dropped; all takes incl. both retake rounds; no new recording): one take per line, mentor's mood rules, retakes, blind pack 3


RESULT: ERROR
```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 50, in <module>
    N_P, N_L, N_R = med([r["pitch"] for r in first("normal")]), med([r["lufs"] for r in first("normal")]), med([r["range"] for r in first("normal")])
                                             ~~~~~^^^^^^^^^^
  File "/kaggle/src/script.py", line 49, in <lambda>
    first = lambda m: [C[i][0] for i in C if LINES[i][1] == m]
                                             ~~~~~^^^
KeyError: 'm3l17'

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe
[  1.2 min] takes for 475 of 622 lines
```

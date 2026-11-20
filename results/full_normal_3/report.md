# Full run · F normal batch 3/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| normal | T | 172 | 159 | 94 | 33/43 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| normal | T | -2 | +1.5 | +1.6 | +1.0 | +0.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| normal | T | gap ≤0.5 s: 41, no hiss >0.15 s: 31, no flat hold >0.5 s: 5 |

Lost before measuring: words 13

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  2.9 min] context tokens: {}
[  7.4 min] recorded normal T
[ 10.4 min] 172 takes done
```
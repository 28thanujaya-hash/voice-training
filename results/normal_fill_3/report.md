# normal_fill_3 · normal top-up 3, plain (64)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| normal | T | 256 | 227 | 128 | 51/64 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| normal | T | +3 | +0.0 | +0.1 | +0.9 | -1.0 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| normal | T | gap ≤0.5 s: 73, no hiss >0.15 s: 41, no flat hold >0.5 s: 13 |

Lost before measuring: words 29

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cuda:0/cuda:1
[  2.3 min] context tokens: {}
[ 10.9 min] recorded normal T
[ 15.7 min] 256 takes done
```
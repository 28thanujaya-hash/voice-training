# Full run · F normal batch 2/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| normal | T | 172 | 156 | 67 | 28/43 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| normal | T | +13 | +0.4 | +0.3 | +1.0 | -1.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| normal | T | gap ≤0.5 s: 68, no hiss >0.15 s: 39, no flat hold >0.5 s: 9 |

Lost before measuring: words 16

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.1 min] context tokens: {}
[ 10.8 min] recorded normal T
[ 14.6 min] 172 takes done
```
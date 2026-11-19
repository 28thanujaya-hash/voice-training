# Full run · F bright batch 2/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | T | 136 | 124 | 6 | 3/34 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | T | +1 | +3.3 | +2.5 | +1.1 | +0.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | T | pitch ≥+2.5 st: 63, gap ≤0.5 s: 54, movement ≥+0.8: 49, not slower: 48, not breathy: 47, no hiss >0.15 s: 33, end not quieter: 25, end fall gentle: 13, no flat hold >0.5 s: 5 |

Lost before measuring: words 12

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  8.3 min] context tokens: {}
[ 14.8 min] recorded bright T
[ 18.5 min] 136 takes done
```
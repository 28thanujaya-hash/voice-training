# Full run · F bright batch 1/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | T | 136 | 119 | 1 | 1/34 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | T | +4 | +2.5 | +1.4 | +0.9 | -0.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | T | pitch ≥+2.5 st: 83, movement ≥+0.8: 55, gap ≤0.5 s: 42, not slower: 40, not breathy: 37, end not quieter: 35, no hiss >0.15 s: 28, no flat hold >0.5 s: 10, ≥6 syllables: 8, end fall gentle: 7 |

Lost before measuring: words 17

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  3.4 min] context tokens: {}
[ 10.9 min] recorded bright T
[ 14.6 min] 136 takes done
```
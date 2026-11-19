# Full run · F bright batch 3/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | T | 136 | 130 | 1 | 1/34 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | T | -9 | +3.2 | +3.3 | +0.8 | +1.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | T | not slower: 72, not breathy: 69, movement ≥+0.8: 64, end not quieter: 55, pitch ≥+2.5 st: 52, no hiss >0.15 s: 47, gap ≤0.5 s: 35, ≥6 syllables: 31, end fall gentle: 14, no flat hold >0.5 s: 6 |

Lost before measuring: words 6

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  3.3 min] context tokens: {}
[  9.3 min] recorded bright T
[ 12.4 min] 136 takes done
```
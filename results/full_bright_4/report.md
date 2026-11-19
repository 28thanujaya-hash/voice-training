# Full run · F bright batch 4/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | T | 128 | 120 | 0 | 0/32 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | T | -15 | +4.6 | +3.0 | +1.1 | +1.5 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | T | not slower: 75, ≥6 syllables: 70, end not quieter: 67, not breathy: 60, pitch ≥+2.5 st: 48, movement ≥+0.8: 47, end fall gentle: 31, gap ≤0.5 s: 18, no hiss >0.15 s: 15, no flat hold >0.5 s: 6 |

Lost before measuring: words 8

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  2.6 min] context tokens: {}
[  7.0 min] recorded bright T
[  9.5 min] 128 takes done
```
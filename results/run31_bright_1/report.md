# run31_bright_1 · bright / tense line at the end of a full scene (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | K | 16 | 16 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | K | +21 | +0.9 | -0.3 | +0.3 | -1.6 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | K | pitch ≥+2.5 st: 12, movement ≥+0.8: 10, gap ≤0.5 s: 7, end not quieter: 7, no hiss >0.15 s: 6, not breathy: 1, no flat hold >0.5 s: 1, not slower: 1 |

Lost before measuring: none

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.6 min] context tokens: {'A': 199}
[ 15.4 min] recorded bright K
[ 16.0 min] 16 takes done
```
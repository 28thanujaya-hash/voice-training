# run32_bright_calm · bright after a calm scene, plain line (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | C | 16 | 16 | 0 | 0/8 |
| bright | K | 16 | 15 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | C | +24 | +1.2 | -0.1 | +0.8 | -2.6 | +0 | +0.0 | +0.0 | +0.0 |
| bright | K | +26 | -0.5 | -0.3 | -0.1 | -1.3 | +2 | -1.8 | +0.6 | -0.9 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | C | pitch ≥+2.5 st: 15, end not quieter: 11, movement ≥+0.8: 8, gap ≤0.5 s: 8, no hiss >0.15 s: 4, not slower: 1, not breathy: 1 |
| bright | K | pitch ≥+2.5 st: 15, movement ≥+0.8: 14, gap ≤0.5 s: 9, end not quieter: 8, no hiss >0.15 s: 3, not breathy: 1 |

Lost before measuring: words 1

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.0 min] device cuda:0/cuda:1
[  2.5 min] context tokens: {'A': 199}
[  3.1 min] recorded bright C
[ 23.3 min] recorded bright K
[ 23.7 min] 32 takes done
```
# run32_bright_calm_2 · bright after a calm scene, plain line (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | C | 16 | 16 | 0 | 0/8 |
| bright | K | 16 | 15 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | C | +17 | +0.3 | +1.0 | +1.1 | -1.9 | +0 | +0.0 | +0.0 | +0.0 |
| bright | K | +17 | -0.2 | -0.3 | -0.0 | -2.9 | +6 | -1.2 | -0.2 | -0.9 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | C | pitch ≥+2.5 st: 14, gap ≤0.5 s: 12, end not quieter: 9, movement ≥+0.8: 5, no hiss >0.15 s: 4, not breathy: 2, no flat hold >0.5 s: 1, not slower: 1 |
| bright | K | pitch ≥+2.5 st: 15, movement ≥+0.8: 13, gap ≤0.5 s: 6, end not quieter: 6, no hiss >0.15 s: 2, not breathy: 2 |

Lost before measuring: words 1

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'A': 199}
[  3.5 min] recorded bright C
[ 23.1 min] recorded bright K
[ 23.5 min] 32 takes done
```
# bright_calm_fill · bright top-up, calm scene + plain line (30)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | K | 90 | 76 | 0 | 0/30 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | K | +11 | -1.2 | -0.4 | -0.1 | -0.6 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | K | pitch ≥+2.5 st: 71, movement ≥+0.8: 71, end not quieter: 50, ≥6 syllables: 38, not breathy: 26, not slower: 21, gap ≤0.5 s: 20, no hiss >0.15 s: 10, no flat hold >0.5 s: 5 |

Lost before measuring: words 14

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'A': 199}
[ 89.0 min] recorded bright K
[ 90.8 min] 90 takes done
```
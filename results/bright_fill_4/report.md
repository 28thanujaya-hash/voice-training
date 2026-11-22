# bright_fill_4 · bright top-up 4, excited scene / calm scene + laugh (8)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | K | 32 | 29 | 0 | 0/8 |
| bright | L | 32 | 29 | 1 | 1/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | K | +7 | +1.5 | +2.1 | +0.8 | +1.0 | +nan | +nan | +nan | +nan |
| bright | L | +6 | +3.5 | +3.4 | +0.3 | -0.3 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | K | end not quieter: 24, pitch ≥+2.5 st: 16, ≥6 syllables: 15, movement ≥+0.8: 14, not breathy: 12, not slower: 7, gap ≤0.5 s: 3, end fall gentle: 3, no hiss >0.15 s: 2 |
| bright | L | end not quieter: 19, movement ≥+0.8: 17, ≥6 syllables: 16, not slower: 12, pitch ≥+2.5 st: 11, not breathy: 6, end fall gentle: 4, no hiss >0.15 s: 2, gap ≤0.5 s: 2 |

Lost before measuring: words 6

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.5 min] device cuda:0/cuda:1
[  3.1 min] context tokens: {'A': 199}
[ 27.3 min] recorded bright K
[ 57.5 min] recorded bright L
[ 58.4 min] 64 takes done
```
# bright_fill_3 · bright top-up 3, calm scene + script line, tags removed, '!'

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | K | 80 | 69 | 0 | 0/20 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | K | +3 | +2.4 | +2.7 | +0.6 | +1.1 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | K | end not quieter: 45, ≥6 syllables: 43, movement ≥+0.8: 41, not breathy: 34, pitch ≥+2.5 st: 33, not slower: 22, no hiss >0.15 s: 10, gap ≤0.5 s: 7, end fall gentle: 4, no flat hold >0.5 s: 3 |

Lost before measuring: words 11

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.0 min] device cuda:0/cuda:1
[  2.6 min] context tokens: {'A': 199}
[ 67.4 min] recorded bright K
[ 68.9 min] 80 takes done
```
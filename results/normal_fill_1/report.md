# normal_fill_1 · normal top-up, plain as in the full run, lines with <2 passe

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| normal | T | 240 | 220 | 105 | 43/60 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| normal | T | +11 | +0.1 | +0.5 | +1.1 | -0.6 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| normal | T | gap ≤0.5 s: 87, no hiss >0.15 s: 49, no flat hold >0.5 s: 20 |

Lost before measuring: words 20

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cuda:0/cuda:1
[  2.4 min] context tokens: {}
[ 13.1 min] recorded normal T
[ 18.2 min] 240 takes done
```
# normal_fill_2 · normal top-up, plain as in the full run, lines with <2 passe

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| normal | T | 236 | 216 | 174 | 52/59 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| normal | T | -1 | +0.3 | +1.4 | +0.6 | +0.9 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| normal | T | no hiss >0.15 s: 24, gap ≤0.5 s: 16, no flat hold >0.5 s: 10 |

Lost before measuring: words 20

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.3 min] device cuda:0/cuda:1
[  2.5 min] context tokens: {}
[  7.9 min] recorded normal T
[ 11.7 min] 236 takes done
```
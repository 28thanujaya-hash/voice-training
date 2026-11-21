# run23 · writing test (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | O | 24 | 21 | 1 | 1/6 |
| low | R | 24 | 20 | 0 | 0/6 |
| normal | O | 24 | 21 | 6 | 4/6 |
| normal | R | 24 | 22 | 3 | 2/6 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | O | -5 | -1.2 | -0.2 | -0.3 | +3.8 | +nan | +nan | +nan | +nan |
| low | R | +8 | -1.9 | +0.2 | -0.3 | +2.3 | +nan | +nan | +nan | +nan |
| normal | O | +7 | -0.2 | -0.6 | +1.1 | -1.5 | +nan | +nan | +nan | +nan |
| normal | R | +21 | -1.0 | -0.5 | +0.8 | -0.8 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | O | speed 15-40% slower: 19, ≥2 dB quieter: 14, breathier ≥+3 dB: 10, gap ≤0.5 s: 6, no flat hold >0.5 s: 4 |
| low | R | speed 15-40% slower: 19, breathier ≥+3 dB: 12, ≥2 dB quieter: 10, gap ≤0.5 s: 9, no flat hold >0.5 s: 5 |
| normal | O | gap ≤0.5 s: 12, no hiss >0.15 s: 5, no flat hold >0.5 s: 1 |
| normal | R | gap ≤0.5 s: 16, no hiss >0.15 s: 4, no flat hold >0.5 s: 3 |

Lost before measuring: words 12

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.8 min] context tokens: {'low': 199}
[  4.3 min] recorded low O
[  6.4 min] recorded low R
[  8.3 min] recorded normal O
[ 10.5 min] recorded normal R
[ 11.1 min] 96 takes done
```
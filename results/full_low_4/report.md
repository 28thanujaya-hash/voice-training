# Full run · F low batch 4/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | T | 152 | 143 | 4 | 3/38 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | T | +1 | -1.1 | +0.3 | -0.4 | +3.6 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | T | speed 15-40% slower: 117, ≥2 dB quieter: 94, breathier ≥+3 dB: 64, no hiss >0.15 s: 24, no flat hold >0.5 s: 10, gap ≤0.5 s: 1 |

Lost before measuring: words 9

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.3 min] context tokens: {'low': 199}
[  9.5 min] recorded low T
[ 12.2 min] 152 takes done
```
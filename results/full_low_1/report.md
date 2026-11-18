# Full run · F low batch 1/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | T | 156 | 146 | 2 | 2/39 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | T | +5 | -2.0 | -0.4 | -0.2 | +3.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | T | speed 15-40% slower: 127, gap ≤0.5 s: 77, ≥2 dB quieter: 73, breathier ≥+3 dB: 62, no hiss >0.15 s: 30, no flat hold >0.5 s: 27 |

Lost before measuring: words 10

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.5 min] context tokens: {'low': 199}
[ 15.3 min] recorded low T
[ 19.3 min] 156 takes done
```
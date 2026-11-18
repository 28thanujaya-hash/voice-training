# Full run · F low batch 3/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | T | 156 | 146 | 7 | 7/39 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | T | -9 | -0.5 | +0.6 | -0.1 | +4.5 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | T | ≥2 dB quieter: 102, speed 15-40% slower: 93, breathier ≥+3 dB: 60, no hiss >0.15 s: 32, gap ≤0.5 s: 26, no flat hold >0.5 s: 14 |

Lost before measuring: words 10

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  4.0 min] context tokens: {'low': 199}
[ 11.2 min] recorded low T
[ 13.9 min] 156 takes done
```
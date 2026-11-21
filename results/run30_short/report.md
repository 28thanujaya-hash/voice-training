# run30_short · low line after a shorter scene (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | S1 | 32 | 31 | 0 | 0/8 |
| low | S2 | 32 | 26 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | S1 | +6 | -1.0 | -0.9 | -0.3 | -0.1 | +nan | +nan | +nan | +nan |
| low | S2 | +9 | -1.4 | -0.6 | -0.5 | +0.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | S1 | speed 15-40% slower: 31, breathier ≥+3 dB: 26, ≥2 dB quieter: 23, gap ≤0.5 s: 19, no hiss >0.15 s: 5, no flat hold >0.5 s: 4 |
| low | S2 | speed 15-40% slower: 25, breathier ≥+3 dB: 19, ≥2 dB quieter: 18, gap ≤0.5 s: 14, no hiss >0.15 s: 5, no flat hold >0.5 s: 1 |

Lost before measuring: words 7

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  5.0 min] context tokens: {'A': 199}
[ 11.7 min] recorded low S1
[ 23.6 min] recorded low S2
[ 24.5 min] 64 takes done
```
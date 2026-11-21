# run28 · low line at the end of a long scene (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 32 | 30 | 0 | 0/8 |
| low | F | 32 | 27 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | +14 | -1.9 | -1.2 | -0.6 | +0.2 | +nan | +nan | +nan | +nan |
| low | F | +11 | -1.3 | -0.9 | -0.4 | +0.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | speed 15-40% slower: 29, breathier ≥+3 dB: 26, gap ≤0.5 s: 18, ≥2 dB quieter: 15, no hiss >0.15 s: 5, no flat hold >0.5 s: 4 |
| low | F | speed 15-40% slower: 26, breathier ≥+3 dB: 23, ≥2 dB quieter: 17, gap ≤0.5 s: 17, no hiss >0.15 s: 5, no flat hold >0.5 s: 3 |

Lost before measuring: words 7

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.3 min] device cuda:0/cuda:1
[  3.0 min] context tokens: {'A': 199}
[ 26.6 min] recorded low K
[ 51.0 min] recorded low F
[ 52.0 min] 64 takes done
```
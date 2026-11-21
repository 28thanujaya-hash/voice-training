# low_scene_2 · low re-record, full scene (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 76 | 70 | 3 | 3/38 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | -6 | -1.1 | -0.2 | -0.3 | +3.5 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | speed 15-40% slower: 54, ≥2 dB quieter: 47, breathier ≥+3 dB: 30, no hiss >0.15 s: 10, no flat hold >0.5 s: 4 |

Lost before measuring: words 6

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'A': 199}
[ 67.5 min] recorded low K
[ 69.2 min] 76 takes done
```
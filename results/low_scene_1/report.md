# low_scene_1 · low re-record, full scene (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 76 | 68 | 2 | 2/38 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | +11 | -0.8 | +0.3 | -0.1 | +2.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | speed 15-40% slower: 58, ≥2 dB quieter: 45, breathier ≥+3 dB: 38, gap ≤0.5 s: 18, no hiss >0.15 s: 14, no flat hold >0.5 s: 8 |

Lost before measuring: words 8

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.5 min] device cuda:0/cuda:1
[  3.2 min] context tokens: {'A': 199}
[ 69.9 min] recorded low K
[ 71.9 min] 76 takes done
```
# low_fill · low top-up, full grief scene, lines with <2 passes (36)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 108 | 104 | 0 | 0/36 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | +12 | -1.0 | -0.6 | -0.2 | +1.5 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | speed 15-40% slower: 93, ≥2 dB quieter: 83, breathier ≥+3 dB: 70, gap ≤0.5 s: 23, no hiss >0.15 s: 23, no flat hold >0.5 s: 5 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.5 min] device cuda:0/cuda:1
[  3.2 min] context tokens: {'A': 199}
[ 73.7 min] recorded low K
[ 75.9 min] 108 takes done
```
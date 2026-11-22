# low_fill_3 · low top-up 3, grief scene + script text with sigh (20)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 80 | 79 | 0 | 0/20 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | +16 | +1.1 | +2.6 | +0.2 | +3.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | ≥2 dB quieter: 72, speed 15-40% slower: 67, breathier ≥+3 dB: 39, gap ≤0.5 s: 8, no hiss >0.15 s: 7, no flat hold >0.5 s: 3 |

Lost before measuring: words 1

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  3.0 min] context tokens: {'A': 199}
[ 46.5 min] recorded low K
[ 48.0 min] 80 takes done
```
# low_fill_2 · low top-up 2, grief scene, script text with its sigh (51)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | K | 153 | 149 | 3 | 2/51 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | K | +3 | -0.4 | +0.2 | -0.2 | +2.1 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | K | speed 15-40% slower: 115, ≥2 dB quieter: 113, breathier ≥+3 dB: 87, gap ≤0.5 s: 32, no hiss >0.15 s: 23, no flat hold >0.5 s: 5 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.5 min] device cuda:0/cuda:1
[  3.1 min] context tokens: {'A': 199}
[110.1 min] recorded low K
[114.0 min] 153 takes done
```
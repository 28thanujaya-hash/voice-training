# run24 · low scene context (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | A | 32 | 31 | 0 | 0/8 |
| low | S | 32 | 29 | 2 | 2/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | A | +6 | -2.2 | +0.1 | -0.2 | +1.9 | +nan | +nan | +nan | +nan |
| low | S | +0 | -2.1 | +0.1 | -0.5 | +5.1 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | A | speed 15-40% slower: 28, breathier ≥+3 dB: 23, gap ≤0.5 s: 18, ≥2 dB quieter: 13, no hiss >0.15 s: 7, no flat hold >0.5 s: 2 |
| low | S | speed 15-40% slower: 27, gap ≤0.5 s: 15, ≥2 dB quieter: 12, breathier ≥+3 dB: 9, no hiss >0.15 s: 7, no flat hold >0.5 s: 5 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.8 min] context tokens: {'A': 199, 'S': 660}
[  5.1 min] recorded low A
[  9.2 min] recorded low S
[ 10.0 min] 64 takes done
```
# run25 · human sad context (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | S | 32 | 29 | 0 | 0/8 |
| low | H1 | 32 | 29 | 0 | 0/8 |
| low | H3 | 32 | 25 | 1 | 1/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | S | -2 | -1.8 | +0.4 | -0.3 | +5.8 | +nan | +nan | +nan | +nan |
| low | H1 | -3 | +1.6 | -0.5 | -0.1 | +0.8 | +nan | +nan | +nan | +nan |
| low | H3 | -19 | +0.3 | -0.8 | -0.1 | +1.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | S | speed 15-40% slower: 25, ≥2 dB quieter: 15, gap ≤0.5 s: 12, no hiss >0.15 s: 7, breathier ≥+3 dB: 4, no flat hold >0.5 s: 3 |
| low | H1 | ≥2 dB quieter: 29, breathier ≥+3 dB: 21, speed 15-40% slower: 19, gap ≤0.5 s: 14, no flat hold >0.5 s: 10, no hiss >0.15 s: 9 |
| low | H3 | ≥2 dB quieter: 20, breathier ≥+3 dB: 19, speed 15-40% slower: 13, gap ≤0.5 s: 8, no flat hold >0.5 s: 7, no hiss >0.15 s: 5 |

Lost before measuring: words 13

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'S': 660, 'H1': 236, 'H3': 726}
[  5.6 min] recorded low S
[ 11.0 min] recorded low H1
[ 16.9 min] recorded low H3
[ 17.8 min] 96 takes done
```
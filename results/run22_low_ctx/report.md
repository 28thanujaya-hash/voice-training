# run22 · low context test (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | A | 32 | 29 | 0 | 0/8 |
| low | B | 32 | 28 | 0 | 0/8 |
| low | C | 32 | 30 | 0 | 0/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | A | +7 | -2.0 | -0.9 | -0.3 | +2.4 | +5 | -0.4 | -0.6 | -0.1 |
| low | B | +4 | -1.0 | -1.1 | -0.3 | +1.2 | +4 | +0.6 | -1.1 | -0.5 |
| low | C | +1 | -1.4 | +0.3 | +0.1 | +1.9 | +0 | +0.0 | +0.0 | +0.0 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | A | speed 15-40% slower: 27, breathier ≥+3 dB: 20, gap ≤0.5 s: 16, ≥2 dB quieter: 14, no hiss >0.15 s: 9, no flat hold >0.5 s: 5 |
| low | B | speed 15-40% slower: 24, ≥2 dB quieter: 23, breathier ≥+3 dB: 18, gap ≤0.5 s: 15, no hiss >0.15 s: 9, no flat hold >0.5 s: 6 |
| low | C | speed 15-40% slower: 26, breathier ≥+3 dB: 19, ≥2 dB quieter: 18, gap ≤0.5 s: 16, no hiss >0.15 s: 9, no flat hold >0.5 s: 5 |

Lost before measuring: words 9

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'A': 199, 'B': 527, 'C': 437}
[  5.1 min] recorded low A
[  8.9 min] recorded low B
[ 12.5 min] recorded low C
[ 13.4 min] 96 takes done
```
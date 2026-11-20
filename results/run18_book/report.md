# Full run · F low batch 4/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | A | 8 | 8 | 0 | 0/2 |
| bright | B | 8 | 8 | 0 | 0/2 |
| low | A | 24 | 19 | 1 | 1/6 |
| low | B | 24 | 18 | 0 | 0/6 |
| tense | A | 8 | 7 | 0 | 0/2 |
| tense | B | 8 | 5 | 0 | 0/2 |
| normal | A | 108 | 81 | 60 | 23/38 |
| normal | B | 44 | 25 | 10 | 4/38 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | A | +5 | +3.4 | +1.1 | +0.9 | -2.4 | +nan | +nan | +nan | +nan |
| bright | B | -3 | +2.3 | +0.5 | +1.7 | -3.8 | +nan | +nan | +nan | +nan |
| low | A | -9 | -2.0 | -0.8 | -0.4 | +2.4 | +nan | +nan | +nan | +nan |
| low | B | -14 | -1.7 | -0.5 | +0.0 | +1.5 | +nan | +nan | +nan | +nan |
| tense | A | +5 | +8.4 | +0.8 | +1.4 | -1.7 | +nan | +nan | +nan | +nan |
| tense | B | +28 | +8.7 | +2.0 | +1.1 | -2.2 | +nan | +nan | +nan | +nan |
| normal | A | +18 | +0.7 | -0.1 | +0.9 | -2.1 | +nan | +nan | +nan | +nan |
| normal | B | +18 | -0.2 | -0.7 | +0.4 | -2.1 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | A | pitch ≥+2.5 st: 7, movement ≥+0.8: 4, gap ≤0.5 s: 2, not breathy: 2, end not quieter: 1, no hiss >0.15 s: 1, no flat hold >0.5 s: 1, not slower: 1 |
| bright | B | pitch ≥+2.5 st: 7, not slower: 4, movement ≥+0.8: 2, end not quieter: 2, no flat hold >0.5 s: 1, gap ≤0.5 s: 1 |
| low | A | speed 15-40% slower: 14, breathier ≥+3 dB: 10, ≥2 dB quieter: 9, gap ≤0.5 s: 6, no flat hold >0.5 s: 5, no hiss >0.15 s: 4 |
| low | B | speed 15-40% slower: 13, ≥2 dB quieter: 12, breathier ≥+3 dB: 11, gap ≤0.5 s: 8, no hiss >0.15 s: 4, no flat hold >0.5 s: 3 |
| tense | A | end ≥3 dB quieter: 7, ≥10% faster: 5, falls through line: 5, pitch ≥+2 st: 5, gap ≤0.5 s: 1 |
| tense | B | end ≥3 dB quieter: 5, falls through line: 3, pitch ≥+2 st: 3, ≥10% faster: 1 |
| normal | A | no flat hold >0.5 s: 10, no hiss >0.15 s: 10, gap ≤0.5 s: 5 |
| normal | B | gap ≤0.5 s: 13, no hiss >0.15 s: 7, no flat hold >0.5 s: 4 |

Lost before measuring: words 61

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  3.6 min] context tokens: {'low': 199, 'tense': 92}
[  4.3 min] recorded bright A
[  5.3 min] recorded bright B
[  6.8 min] recorded low A
[  8.8 min] recorded low B
[  9.7 min] recorded tense A
[ 10.5 min] recorded tense B
[ 14.7 min] recorded normal A
[ 20.5 min] recorded normal B
[ 21.7 min] 232 takes done
```
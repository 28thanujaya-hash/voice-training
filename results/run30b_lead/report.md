# run30b_lead · line after a one-sentence mood lead-in (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | L | 32 | 26 | 0 | 0/8 |
| bright | L | 32 | 31 | 0 | 0/8 |
| tense | L | 32 | 32 | 4 | 3/8 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | L | +5 | -0.5 | -0.2 | -0.2 | +2.6 | +nan | +nan | +nan | +nan |
| bright | L | +6 | +3.8 | +2.1 | +1.0 | -0.3 | +nan | +nan | +nan | +nan |
| tense | L | +24 | +2.8 | +0.7 | +0.8 | +0.2 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | L | speed 15-40% slower: 25, ≥2 dB quieter: 20, gap ≤0.5 s: 16, breathier ≥+3 dB: 14, no flat hold >0.5 s: 5, no hiss >0.15 s: 5 |
| bright | L | pitch ≥+2.5 st: 18, end not quieter: 15, not breathy: 12, gap ≤0.5 s: 12, movement ≥+0.8: 10, not slower: 6, no hiss >0.15 s: 5, end fall gentle: 2, no flat hold >0.5 s: 1 |
| tense | L | pitch ≥+2 st: 21, ≥3 dB louder: 18, end ≥3 dB quieter: 15, ≥10% faster: 9, no hiss >0.15 s: 8, falls through line: 2 |

Lost before measuring: words 7

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.2 min] context tokens: {'A': 199}
[  8.1 min] recorded low L
[ 12.1 min] recorded bright L
[ 15.4 min] recorded tense L
[ 15.9 min] 96 takes done
```
# Run 12 · bright context + laugh, tense context + sigh

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | C | 24 | 24 | 1 | 1/12 |
| bright | X | 24 | 24 | 0 | 0/12 |
| bright | XL | 24 | 22 | 1 | 1/12 |
| tense | C | 24 | 21 | 0 | 0/12 |
| tense | X | 24 | 23 | 2 | 2/12 |
| tense | XS | 24 | 22 | 0 | 0/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | C | +11 | +3.5 | +2.9 | +1.2 | +2.3 | +0 | +0.0 | +0.0 | +0.0 |
| bright | X | +19 | +1.6 | +0.2 | +0.8 | -2.4 | +3 | -2.0 | -4.9 | -0.4 |
| bright | XL | +24 | +2.0 | +0.5 | +0.6 | -3.8 | +7 | -1.4 | -6.1 | -0.6 |
| tense | C | +3 | +1.8 | +0.3 | +0.8 | +0.5 | +0 | +0.0 | +0.0 | +0.0 |
| tense | X | +22 | +4.5 | -0.1 | +1.1 | -3.5 | +12 | +3.4 | -3.6 | +0.3 |
| tense | XS | +5 | +0.9 | -1.3 | +0.6 | -3.7 | -5 | -1.0 | -3.2 | -0.1 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | C | not breathy: 15, pitch ≥+2.5 st: 10, gap ≤0.5 s: 9, movement ≥+0.8: 8, end not quieter: 8, not slower: 4, no hiss >0.15 s: 3, end fall gentle: 1 |
| bright | X | pitch ≥+2.5 st: 19, movement ≥+0.8: 12, end not quieter: 10, gap ≤0.5 s: 9, not slower: 4, no hiss >0.15 s: 3, not breathy: 3, end fall gentle: 1, no flat hold >0.5 s: 1 |
| bright | XL | pitch ≥+2.5 st: 19, movement ≥+0.8: 13, end not quieter: 8, gap ≤0.5 s: 7, not slower: 4, no hiss >0.15 s: 1, not breathy: 1 |
| tense | C | ≥3 dB louder: 19, pitch ≥+2 st: 17, end ≥3 dB quieter: 17, ≥10% faster: 13, gap ≤0.5 s: 7, no hiss >0.15 s: 4, falls through line: 3, no flat hold >0.5 s: 2 |
| tense | X | pitch ≥+2 st: 15, end ≥3 dB quieter: 10, ≥3 dB louder: 9, ≥10% faster: 6, falls through line: 5, gap ≤0.5 s: 3, no hiss >0.15 s: 2 |
| tense | XS | pitch ≥+2 st: 20, end ≥3 dB quieter: 16, ≥3 dB louder: 16, ≥10% faster: 15, no hiss >0.15 s: 6, falls through line: 5, no flat hold >0.5 s: 2, gap ≤0.5 s: 2 |

Lost before measuring: words 8

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  4.3 min] context tokens: {'bright': 238, 'tense': 92}
[  5.5 min] recorded bright C
[  7.3 min] recorded bright X
[  9.3 min] recorded bright XL
[ 10.7 min] recorded tense C
[ 11.8 min] recorded tense X
[ 13.3 min] recorded tense XS
[ 13.8 min] 144 takes done
```
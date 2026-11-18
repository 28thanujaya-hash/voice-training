# Run 11 · bright and tense: own approved clip as context, with and without a tag

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | C | 24 | 24 | 1 | 1/12 |
| bright | X | 24 | 22 | 2 | 1/12 |
| bright | XG | 24 | 23 | 1 | 1/12 |
| bright | XC | 24 | 23 | 1 | 1/12 |
| tense | C | 24 | 23 | 0 | 0/12 |
| tense | X | 24 | 23 | 1 | 1/12 |
| tense | XR | 24 | 24 | 0 | 0/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | C | +16 | +3.7 | +2.7 | +1.5 | +1.6 | +0 | +0.0 | +0.0 | +0.0 |
| bright | X | +18 | +1.7 | +1.5 | +1.2 | -1.3 | +8 | -1.8 | -3.2 | -0.3 |
| bright | XG | +12 | +3.0 | +3.1 | +1.2 | +0.6 | -1 | -0.8 | -0.2 | -0.2 |
| bright | XC | +23 | +1.6 | +1.0 | +0.5 | -2.4 | +3 | -1.5 | -4.0 | -0.9 |
| tense | C | -1 | +1.4 | -0.1 | +0.8 | -1.3 | +0 | +0.0 | +0.0 | +0.0 |
| tense | X | +16 | +3.8 | +0.1 | +1.3 | -4.0 | +6 | +2.0 | -2.1 | +0.2 |
| tense | XR | -7 | +2.8 | -1.0 | +0.5 | -4.3 | -10 | +1.6 | -2.8 | -0.3 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | C | not breathy: 12, pitch ≥+2.5 st: 11, gap ≤0.5 s: 8, end not quieter: 8, movement ≥+0.8: 6, not slower: 5, end fall gentle: 3, no flat hold >0.5 s: 1 |
| bright | X | pitch ≥+2.5 st: 16, end not quieter: 8, movement ≥+0.8: 7, gap ≤0.5 s: 7, not slower: 5, not breathy: 5, no hiss >0.15 s: 3, end fall gentle: 2, no flat hold >0.5 s: 1 |
| bright | XG | not breathy: 10, pitch ≥+2.5 st: 9, end not quieter: 9, gap ≤0.5 s: 8, not slower: 5, movement ≥+0.8: 4, end fall gentle: 3, no hiss >0.15 s: 2 |
| bright | XC | pitch ≥+2.5 st: 14, movement ≥+0.8: 13, end not quieter: 7, gap ≤0.5 s: 5, not slower: 4, no hiss >0.15 s: 1 |
| tense | C | pitch ≥+2 st: 19, end ≥3 dB quieter: 19, ≥3 dB louder: 17, ≥10% faster: 13, gap ≤0.5 s: 8, falls through line: 3, no hiss >0.15 s: 2 |
| tense | X | pitch ≥+2 st: 20, end ≥3 dB quieter: 11, ≥10% faster: 9, ≥3 dB louder: 9, falls through line: 8, gap ≤0.5 s: 6, no hiss >0.15 s: 4 |
| tense | XR | pitch ≥+2 st: 22, ≥10% faster: 19, end ≥3 dB quieter: 16, ≥3 dB louder: 13, no hiss >0.15 s: 6, falls through line: 5, gap ≤0.5 s: 1 |

Lost before measuring: words 6

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  4.2 min] context tokens: {'bright': 238, 'tense': 92}
[  5.3 min] recorded bright C
[  7.1 min] recorded bright X
[  9.0 min] recorded bright XG
[ 11.1 min] recorded bright XC
[ 12.5 min] recorded tense C
[ 13.6 min] recorded tense X
[ 15.2 min] recorded tense XR
[ 15.6 min] 168 takes done
```
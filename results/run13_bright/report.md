# Run 13 · bright: normal punctuation vs bright vs bright + situational tag

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | C | 36 | 34 | 1 | 1/12 |
| bright | B | 36 | 35 | 0 | 0/12 |
| bright | T | 27 | 25 | 0 | 0/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | C | +17 | +0.8 | -0.3 | +0.9 | -0.0 | +0 | +0.0 | +0.0 | +0.0 |
| bright | B | +12 | +2.7 | +2.2 | +1.1 | +0.2 | -4 | +2.3 | +1.2 | +0.1 |
| bright | T | +10 | +4.1 | +2.1 | +0.5 | -0.5 | -3 | +4.3 | +0.2 | -0.3 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | C | pitch ≥+2.5 st: 27, gap ≤0.5 s: 18, movement ≥+0.8: 16, end not quieter: 12, not breathy: 11, no hiss >0.15 s: 6, not slower: 5, no flat hold >0.5 s: 1 |
| bright | B | pitch ≥+2.5 st: 20, gap ≤0.5 s: 16, not breathy: 15, end not quieter: 14, movement ≥+0.8: 13, not slower: 10, no hiss >0.15 s: 2, end fall gentle: 1 |
| bright | T | movement ≥+0.8: 15, pitch ≥+2.5 st: 13, not breathy: 11, not slower: 8, gap ≤0.5 s: 7, end not quieter: 6, end fall gentle: 4, no hiss >0.15 s: 2, no flat hold >0.5 s: 1 |

Lost before measuring: words 5

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  4.9 min] recorded bright C
[  7.1 min] recorded bright B
[  9.1 min] recorded bright T
[  9.5 min] 99 takes done
```
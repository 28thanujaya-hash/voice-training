# Run 14 · tense: context vs context + gasp vs context with a "!" ending

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | C | 36 | 33 | 0 | 0/12 |
| tense | X | 36 | 30 | 2 | 2/12 |
| tense | XG | 36 | 34 | 0 | 0/12 |
| tense | XE | 36 | 31 | 1 | 1/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | C | +19 | +1.0 | +0.2 | +0.8 | -0.7 | +0 | +0.0 | +0.0 | +0.0 |
| tense | X | +27 | +2.7 | +0.0 | +1.3 | -2.9 | +5 | +1.2 | -2.9 | +0.4 |
| tense | XG | +25 | +3.6 | +1.0 | +1.0 | -0.3 | +2 | +2.3 | -0.9 | +0.0 |
| tense | XE | +21 | +5.3 | +2.1 | +1.9 | -1.6 | +2 | +3.9 | -2.6 | +1.0 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | C | end ≥3 dB quieter: 29, pitch ≥+2 st: 27, ≥3 dB louder: 26, gap ≤0.5 s: 21, falls through line: 13, ≥10% faster: 11, no hiss >0.15 s: 1 |
| tense | X | end ≥3 dB quieter: 26, pitch ≥+2 st: 25, ≥3 dB louder: 16, falls through line: 13, gap ≤0.5 s: 9, ≥10% faster: 6, no hiss >0.15 s: 2 |
| tense | XG | end ≥3 dB quieter: 32, pitch ≥+2 st: 23, ≥3 dB louder: 15, falls through line: 12, ≥10% faster: 8, gap ≤0.5 s: 7 |
| tense | XE | end ≥3 dB quieter: 29, falls through line: 16, pitch ≥+2 st: 15, ≥10% faster: 9, ≥3 dB louder: 8, gap ≤0.5 s: 6, no hiss >0.15 s: 2 |

Lost before measuring: words 16

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.0 min] device cuda:0/cuda:0
[  4.1 min] context tokens: {'tense': 92}
[  5.9 min] recorded tense C
[  8.3 min] recorded tense X
[ 10.7 min] recorded tense XG
[ 12.8 min] recorded tense XE
[ 13.4 min] 144 takes done
```
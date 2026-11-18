# Run 15 · tense: context + gasp vs context + groan

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | C | 48 | 43 | 0 | 0/12 |
| tense | XG | 48 | 42 | 0 | 0/12 |
| tense | XR | 48 | 45 | 1 | 1/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | C | +20 | +0.8 | +0.5 | +0.9 | -0.3 | +0 | +0.0 | +0.0 | +0.0 |
| tense | XG | +19 | +4.5 | +0.8 | +1.4 | -0.6 | +3 | +3.7 | -0.4 | +0.5 |
| tense | XR | +17 | +1.7 | -1.0 | +0.6 | -3.0 | +2 | +1.1 | -3.0 | -0.6 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | C | end ≥3 dB quieter: 39, ≥3 dB louder: 38, pitch ≥+2 st: 33, gap ≤0.5 s: 32, falls through line: 20, ≥10% faster: 11, no hiss >0.15 s: 2, no flat hold >0.5 s: 1 |
| tense | XG | end ≥3 dB quieter: 40, pitch ≥+2 st: 25, ≥10% faster: 13, falls through line: 12, ≥3 dB louder: 9, gap ≤0.5 s: 8, no hiss >0.15 s: 4, no flat hold >0.5 s: 1 |
| tense | XR | end ≥3 dB quieter: 42, pitch ≥+2 st: 41, ≥3 dB louder: 29, falls through line: 21, ≥10% faster: 13, gap ≤0.5 s: 11, no hiss >0.15 s: 4, no flat hold >0.5 s: 2 |

Lost before measuring: words 14

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.1 min] context tokens: {'tense': 92}
[  4.8 min] recorded tense C
[  7.9 min] recorded tense XG
[ 10.8 min] recorded tense XR
[ 11.8 min] 144 takes done
```
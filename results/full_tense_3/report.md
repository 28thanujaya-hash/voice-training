# Full run · F tense batch 3/4: context only, 4 takes

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 164 | 156 | 3 | 2/41 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | -1 | +4.8 | +0.6 | +1.0 | -3.5 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | pitch ≥+2 st: 116, ≥10% faster: 109, end ≥3 dB quieter: 77, falls through line: 56, ≥3 dB louder: 42, no hiss >0.15 s: 18, gap ≤0.5 s: 14 |

Lost before measuring: words 8

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  4.8 min] context tokens: {'tense': 92}
[  8.4 min] recorded tense T
[ 10.9 min] 164 takes done
```
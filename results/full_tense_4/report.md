# Full run · F tense batch 4/4: context only, 4 takes

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 156 | 152 | 7 | 6/39 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | +3 | +5.0 | +0.8 | +1.1 | -4.4 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | pitch ≥+2 st: 102, ≥10% faster: 90, end ≥3 dB quieter: 62, ≥3 dB louder: 44, falls through line: 23, no hiss >0.15 s: 17, gap ≤0.5 s: 11 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  5.3 min] context tokens: {'tense': 92}
[  8.6 min] recorded tense T
[ 10.9 min] 156 takes done
```
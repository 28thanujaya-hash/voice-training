# Full run · F tense batch 2/4: context only, 4 takes

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 164 | 157 | 3 | 2/41 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | +20 | +3.5 | +0.0 | +1.3 | -3.9 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | pitch ≥+2 st: 129, end ≥3 dB quieter: 120, ≥3 dB louder: 71, ≥10% faster: 64, gap ≤0.5 s: 41, falls through line: 35, no hiss >0.15 s: 30, no flat hold >0.5 s: 4 |

Lost before measuring: words 7

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  3.7 min] context tokens: {'tense': 92}
[  9.8 min] recorded tense T
[ 12.7 min] 164 takes done
```
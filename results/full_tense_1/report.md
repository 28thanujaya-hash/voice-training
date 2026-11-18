# Full run · F tense batch 1/4: context only, 4 takes

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 164 | 161 | 1 | 1/41 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | +24 | +2.6 | -0.3 | +1.4 | -3.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | pitch ≥+2 st: 137, end ≥3 dB quieter: 121, ≥3 dB louder: 94, gap ≤0.5 s: 37, ≥10% faster: 37, falls through line: 35, no hiss >0.15 s: 25, no flat hold >0.5 s: 3 |

Lost before measuring: words 3

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  5.1 min] context tokens: {'tense': 92}
[ 11.5 min] recorded tense T
[ 14.7 min] 164 takes done
```
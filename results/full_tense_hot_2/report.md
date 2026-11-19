# Full run · F tense hot batch 2/2 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 84 | 71 | 1 | 1/21 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | +14 | +6.5 | +3.0 | +1.4 | +1.8 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | end ≥3 dB quieter: 51, falls through line: 34, ≥10% faster: 31, pitch ≥+2 st: 23, ≥3 dB louder: 9, gap ≤0.5 s: 4, no hiss >0.15 s: 4 |

Lost before measuring: words 12, align 1

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.7 min] device cuda:0/cuda:0
[  3.3 min] context tokens: {'tense': 92}
[  6.1 min] recorded tense T
[  7.6 min] 84 takes done
```
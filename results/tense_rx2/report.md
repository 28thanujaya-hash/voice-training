# tense_rx2 · tense top-up, context + one-CAPS rewrite, no tags (26)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | T | 104 | 95 | 5 | 3/26 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | T | +16 | +3.8 | +0.7 | +1.0 | -3.6 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | T | pitch ≥+2 st: 66, end ≥3 dB quieter: 47, ≥3 dB louder: 40, ≥10% faster: 37, falls through line: 19, no hiss >0.15 s: 15, gap ≤0.5 s: 6 |

Lost before measuring: words 9

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cuda:0/cuda:1
[  2.7 min] context tokens: {'tense': 92}
[  6.5 min] recorded tense T
[  8.0 min] 104 takes done
```
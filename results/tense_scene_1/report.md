# tense_scene_1 · tense top-up, full 'How dare you' scene, no tags, lines with

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | K | 54 | 53 | 3 | 2/18 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | K | +21 | +2.1 | +0.4 | +0.7 | -2.0 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | K | pitch ≥+2 st: 41, ≥3 dB louder: 33, end ≥3 dB quieter: 29, no hiss >0.15 s: 17, ≥10% faster: 16, falls through line: 12, gap ≤0.5 s: 10 |

Lost before measuring: words 1

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
[  2.8 min] context tokens: {'A': 199}
[ 25.1 min] recorded tense K
[ 26.2 min] 54 takes done
```
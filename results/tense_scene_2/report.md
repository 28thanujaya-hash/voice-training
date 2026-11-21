# tense_scene_2 · tense top-up, full 'How dare you' scene, no tags, lines with

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| tense | K | 51 | 47 | 4 | 4/17 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| tense | K | +21 | +2.4 | +0.8 | +0.6 | -1.8 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| tense | K | pitch ≥+2 st: 34, ≥3 dB louder: 26, end ≥3 dB quieter: 17, ≥10% faster: 15, falls through line: 7, gap ≤0.5 s: 6, no flat hold >0.5 s: 1 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cuda:0/cuda:1
[  2.8 min] context tokens: {'A': 199}
[ 24.2 min] recorded tense K
[ 25.0 min] 51 takes done
```
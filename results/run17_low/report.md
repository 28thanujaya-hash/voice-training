# Full run · F low batch 4/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | A | 40 | 38 | 0 | 0/10 |
| low | E | 20 | 20 | 1 | 1/10 |
| low | D | 20 | 20 | 1 | 1/10 |
| low | Q | 20 | 20 | 0 | 0/10 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | A | +3 | -0.0 | +1.0 | +0.2 | +3.1 | +nan | +nan | +nan | +nan |
| low | E | +4 | -2.2 | -0.2 | -0.4 | +3.6 | +nan | +nan | +nan | +nan |
| low | D | -0 | -1.6 | -0.2 | -0.0 | +2.2 | +nan | +nan | +nan | +nan |
| low | Q | +2 | -2.2 | +1.6 | -0.6 | +4.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | A | speed 15-40% slower: 35, ≥2 dB quieter: 28, breathier ≥+3 dB: 19, gap ≤0.5 s: 11, no hiss >0.15 s: 10, no flat hold >0.5 s: 4 |
| low | E | speed 15-40% slower: 18, gap ≤0.5 s: 15, ≥2 dB quieter: 9, breathier ≥+3 dB: 8, no hiss >0.15 s: 6, no flat hold >0.5 s: 4 |
| low | D | speed 15-40% slower: 15, ≥2 dB quieter: 13, breathier ≥+3 dB: 11, no hiss >0.15 s: 5, no flat hold >0.5 s: 1 |
| low | Q | speed 15-40% slower: 18, ≥2 dB quieter: 10, breathier ≥+3 dB: 7, no hiss >0.15 s: 4, no flat hold >0.5 s: 2 |

Lost before measuring: words 2

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.6 min] device cpu/cpu, 2 CPU threads
[  3.2 min] context tokens: {'low': 199}
[130.1 min] recorded low A
[244.3 min] recorded low E
[320.0 min] recorded low D
[380.6 min] recorded low Q
[389.6 min] 100 takes done
```
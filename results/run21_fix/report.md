# Full run · F low batch 4/4 (recipe in pilot.py)

Context = approved clip as an earlier turn. Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| bright | R1 | 48 | 47 | 0 | 0/12 |
| bright | R2 | 48 | 45 | 0 | 0/12 |
| tense | N | 48 | 47 | 5 | 3/12 |
| tense | R | 48 | 38 | 2 | 1/12 |
| tense | RX | 48 | 36 | 1 | 1/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| bright | R1 | +9 | +4.0 | +2.8 | +1.1 | +2.5 | +nan | +nan | +nan | +nan |
| bright | R2 | +8 | +4.3 | +4.0 | +1.6 | +4.8 | +nan | +nan | +nan | +nan |
| tense | N | +14 | +0.8 | +0.9 | +1.0 | -0.1 | +nan | +nan | +nan | +nan |
| tense | R | -8 | +2.3 | +1.0 | +1.0 | -1.5 | +nan | +nan | +nan | +nan |
| tense | RX | +2 | +5.8 | +0.6 | +1.2 | -4.7 | +nan | +nan | +nan | +nan |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| bright | R1 | not breathy: 29, pitch ≥+2.5 st: 23, gap ≤0.5 s: 19, movement ≥+0.8: 14, not slower: 14, end not quieter: 14, end fall gentle: 11, no hiss >0.15 s: 5, no flat hold >0.5 s: 4 |
| bright | R2 | not breathy: 35, gap ≤0.5 s: 22, end not quieter: 17, end fall gentle: 14, not slower: 14, movement ≥+0.8: 10, pitch ≥+2.5 st: 8, no hiss >0.15 s: 5, no flat hold >0.5 s: 2 |
| tense | N | ≥3 dB louder: 39, pitch ≥+2 st: 35, end ≥3 dB quieter: 26, no hiss >0.15 s: 19, ≥10% faster: 17, gap ≤0.5 s: 12, falls through line: 4, no flat hold >0.5 s: 3 |
| tense | R | end ≥3 dB quieter: 31, pitch ≥+2 st: 26, ≥10% faster: 26, ≥3 dB louder: 21, gap ≤0.5 s: 18, no hiss >0.15 s: 18, falls through line: 17, no flat hold >0.5 s: 2 |
| tense | RX | pitch ≥+2 st: 28, ≥10% faster: 24, end ≥3 dB quieter: 20, falls through line: 19, no hiss >0.15 s: 15, gap ≤0.5 s: 7, ≥3 dB louder: 6 |

Lost before measuring: words 27

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.1 min] device cpu/cpu, 2 CPU threads
[  2.6 min] context tokens: {'low': 199, 'tense': 92}
[106.7 min] recorded bright R1
[240.9 min] recorded bright R2
[319.1 min] recorded tense N
[466.0 min] recorded tense R
[575.7 min] recorded tense RX
[591.1 min] 240 takes done
```
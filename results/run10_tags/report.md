# Run 10 · Orpheus sound tags: low sniffle/sigh, bright chuckle/laugh/gasp, tense groan

Tag before the line; everything before the first word cut off. rel_* = against the same line's plain takes.

## Pass rate (agreed rules + quality checks; right words only)

| mood | arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | C | 24 | 20 | 0 | 0/12 |
| low | SN | 24 | 22 | 0 | 0/12 |
| low | S | 24 | 24 | 1 | 1/12 |
| bright | C | 24 | 23 | 0 | 0/12 |
| bright | CH | 24 | 23 | 0 | 0/12 |
| bright | LA | 24 | 22 | 0 | 0/12 |
| bright | GA | 24 | 23 | 0 | 0/12 |
| tense | C | 24 | 24 | 0 | 0/12 |
| tense | GR | 24 | 22 | 0 | 0/12 |

## Medians of right-word takes vs normal reference (and vs the same line's plain take)

| mood | arm | speed % | loudness dB | pitch st | movement | breathiness dB | rel speed % | rel loud | rel breath | rel move |
|---|---|---|---|---|---|---|---|---|---|---|
| low | C | +6 | +1.1 | +0.9 | +1.1 | +1.7 | +0 | +0.0 | +0.0 | +0.0 |
| low | SN | +6 | +1.8 | +0.2 | +0.1 | +2.0 | -1 | +0.3 | +2.1 | -1.1 |
| low | S | +3 | -0.8 | -0.1 | +0.0 | +3.0 | -2 | -1.6 | +2.0 | -1.0 |
| bright | C | +10 | +3.0 | +2.5 | +1.7 | +0.2 | +0 | +0.0 | +0.0 | +0.0 |
| bright | CH | +7 | +3.3 | +1.2 | +0.5 | -1.2 | +0 | +0.0 | -2.9 | -1.3 |
| bright | LA | +10 | +3.0 | +1.0 | +0.6 | -1.7 | -1 | -0.3 | -4.2 | -0.8 |
| bright | GA | +8 | +4.0 | +3.5 | +1.1 | +5.2 | -3 | -0.2 | +1.9 | -0.4 |
| tense | C | +5 | +0.9 | +0.3 | +0.9 | -0.6 | +0 | +0.0 | +0.0 | +0.0 |
| tense | GR | -11 | +1.6 | -0.5 | +0.2 | -2.3 | -12 | +0.8 | -1.1 | -0.7 |

## Which rules fail most

| mood | arm | rule: times failed |
|---|---|---|
| low | C | ≥2 dB quieter: 19, speed 15-40% slower: 17, breathier ≥+3 dB: 11, gap ≤0.5 s: 5, no hiss >0.15 s: 2, no flat hold >0.5 s: 2 |
| low | SN | ≥2 dB quieter: 20, speed 15-40% slower: 17, breathier ≥+3 dB: 15, gap ≤0.5 s: 4, no hiss >0.15 s: 3, no flat hold >0.5 s: 2 |
| low | S | ≥2 dB quieter: 22, speed 15-40% slower: 19, breathier ≥+3 dB: 11, no flat hold >0.5 s: 5, no hiss >0.15 s: 4, gap ≤0.5 s: 4 |
| bright | C | pitch ≥+2.5 st: 10, end not quieter: 10, not breathy: 9, gap ≤0.5 s: 7, movement ≥+0.8: 4, end fall gentle: 3, not slower: 3, no hiss >0.15 s: 2 |
| bright | CH | pitch ≥+2.5 st: 18, movement ≥+0.8: 14, not slower: 7, gap ≤0.5 s: 5, end not quieter: 5, not breathy: 5, no hiss >0.15 s: 2, no flat hold >0.5 s: 2, end fall gentle: 1 |
| bright | LA | pitch ≥+2.5 st: 14, movement ≥+0.8: 14, end not quieter: 9, not slower: 6, gap ≤0.5 s: 4, not breathy: 2, no flat hold >0.5 s: 2, no hiss >0.15 s: 1, end fall gentle: 1 |
| bright | GA | not breathy: 20, end not quieter: 9, gap ≤0.5 s: 8, not slower: 7, movement ≥+0.8: 7, pitch ≥+2.5 st: 7, end fall gentle: 4, no hiss >0.15 s: 1, no flat hold >0.5 s: 1 |
| tense | C | ≥3 dB louder: 19, end ≥3 dB quieter: 18, pitch ≥+2 st: 16, ≥10% faster: 14, gap ≤0.5 s: 8, falls through line: 4, no hiss >0.15 s: 3 |
| tense | GR | ≥10% faster: 18, pitch ≥+2 st: 18, end ≥3 dB quieter: 18, ≥3 dB louder: 14, falls through line: 8, no hiss >0.15 s: 5, gap ≤0.5 s: 5, no flat hold >0.5 s: 1 |

Lost before measuring: words 13

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  7.2 min] recorded low C
[  9.2 min] recorded low SN
[ 10.9 min] recorded low S
[ 12.3 min] recorded bright C
[ 14.2 min] recorded bright CH
[ 16.6 min] recorded bright LA
[ 18.4 min] recorded bright GA
[ 19.8 min] recorded tense C
[ 21.3 min] recorded tense GR
[ 21.7 min] 216 takes done
```
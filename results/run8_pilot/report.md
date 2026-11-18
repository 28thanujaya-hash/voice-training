# Run 8 · pilot: new lead-ins vs the agreed mood rules

Lead-ins: T1 = "Stop. Right now. That's enough!"; T2 = "No. Give it back. Now."; B1 = "Guess what? We won! We really won!"; B2 = "Yes! I passed! I can't believe it!"; L1 = "I'm tired. It was a long, sad day."; L2 = "She's gone. I miss her so much."

## Pass rate (all rules + quality checks; a take counts only if its words are right)

| mood | lead-in | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| low | L1 | 24 | 24 | 0 | 0/12 |
| low | L2 | 24 | 22 | 0 | 0/12 |
| low | both | 48 | | 0 | 0/12 |
| bright | B1 | 24 | 24 | 0 | 0/12 |
| bright | B2 | 24 | 23 | 2 | 2/12 |
| bright | both | 48 | | 2 | 2/12 |
| tense | T1 | 24 | 23 | 0 | 0/12 |
| tense | T2 | 24 | 24 | 1 | 1/12 |
| tense | both | 48 | | 1 | 1/12 |

## Which rules fail most (takes with right words that failed)

| mood | lead-in | rule: times failed |
|---|---|---|
| low | L1 | speed 15-40% slower: 19, ≥2 dB quieter: 18, breathier ≥+3 dB: 16, gap ≤0.5 s: 5, no flat hold >0.5 s: 3, no hiss >0.15 s: 3 |
| low | L2 | ≥2 dB quieter: 20, breathier ≥+3 dB: 18, speed 15-40% slower: 16, gap ≤0.5 s: 4, no hiss >0.15 s: 2 |
| bright | B1 | pitch ≥+2.5 st: 15, not breathy: 11, movement ≥+0.8: 11, gap ≤0.5 s: 10, end not quieter: 9, not slower: 5, no hiss >0.15 s: 2, end fall gentle: 1 |
| bright | B2 | pitch ≥+2.5 st: 12, end not quieter: 8, movement ≥+0.8: 6, not breathy: 6, gap ≤0.5 s: 5, end fall gentle: 2, not slower: 1, no flat hold >0.5 s: 1, no hiss >0.15 s: 1 |
| tense | T1 | pitch ≥+2 st: 19, ≥3 dB louder: 16, end ≥3 dB quieter: 13, ≥10% faster: 8, falls through line: 8, gap ≤0.5 s: 6, no hiss >0.15 s: 3 |
| tense | T2 | pitch ≥+2 st: 19, end ≥3 dB quieter: 15, ≥3 dB louder: 14, ≥10% faster: 10, falls through line: 6, no hiss >0.15 s: 4, gap ≤0.5 s: 4 |

## Medians of right-word takes (vs normal)

| mood | lead-in | speed % | loudness dB | pitch st | movement | breathiness dB | end loudness dB | gap s |
|---|---|---|---|---|---|---|---|---|
| low | L1 | +11 | -0.6 | +0.7 | -0.3 | +2.0 | -1.2 | 0.00 |
| low | L2 | +15 | +1.5 | +0.3 | +0.0 | +1.5 | -1.3 | 0.00 |
| bright | B1 | +22 | +3.6 | +2.0 | +1.0 | +0.1 | +0.3 | 0.48 |
| bright | B2 | +23 | +3.6 | +2.5 | +1.3 | -0.0 | +0.4 | 0.29 |
| tense | T1 | +14 | +1.8 | +0.3 | +0.8 | -2.5 | -1.6 | 0.16 |
| tense | T2 | +12 | +2.5 | -0.0 | +0.6 | -1.6 | -2.0 | 0.14 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.9 min] device cuda:0/cuda:0
[  6.0 min] recorded low L1
[  8.7 min] recorded low L2
[ 11.3 min] recorded bright B1
[ 13.8 min] recorded bright B2
[ 16.1 min] recorded tense T1
[ 18.4 min] recorded tense T2
[ 18.7 min] 144 takes done
```
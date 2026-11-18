# Run 9 · low: approved low clip as context, <sigh>, control

Arms: C = plain line; S = "<sigh>" before the line; A = approved low take "Oh… you're back." (run7_five low_01) given as an earlier turn; AS = A + S.
Everything before the line's first word is cut off in every arm.

## Pass rate (all low rules + quality checks; a take counts only if its words are right)

| arm | takes | words OK | PASS | lines with ≥1 PASS |
|---|---|---|---|---|
| C | 24 | 24 | 0 | 0/12 |
| S | 24 | 22 | 1 | 1/12 |
| A | 24 | 22 | 0 | 0/12 |
| AS | 24 | 24 | 0 | 0/12 |

## Which rules fail most (takes with right words that failed)

| arm | rule: times failed |
|---|---|
| C | ≥2 dB quieter: 22, speed 15-40% slower: 19, breathier ≥+3 dB: 17, gap ≤0.5 s: 6, no hiss >0.15 s: 3, no flat hold >0.5 s: 1 |
| S | speed 15-40% slower: 17, ≥2 dB quieter: 16, breathier ≥+3 dB: 13, gap ≤0.5 s: 5, no hiss >0.15 s: 3, no flat hold >0.5 s: 2 |
| A | speed 15-40% slower: 18, ≥2 dB quieter: 16, breathier ≥+3 dB: 14, gap ≤0.5 s: 5, no hiss >0.15 s: 4, no flat hold >0.5 s: 3 |
| AS | speed 15-40% slower: 21, ≥2 dB quieter: 17, breathier ≥+3 dB: 11, no hiss >0.15 s: 7, gap ≤0.5 s: 5, no flat hold >0.5 s: 4 |

## Medians of right-word takes (vs normal). Low needs speed −15 to −40 %, loudness ≤ −2 dB, breathiness ≥ +3 dB

| arm | speed % | loudness dB | pitch st | movement | breathiness dB | end loudness dB | gap s | slow+quiet+breathy (all 3) |
|---|---|---|---|---|---|---|---|---|
| C | +10 | +1.1 | +0.0 | +1.3 | +1.5 | -2.3 | 0.00 | 0/24 |
| S | -6 | -0.8 | +0.9 | -0.1 | +1.7 | -1.8 | 0.00 | 1/22 |
| A | +8 | -0.1 | +0.4 | +0.1 | +2.0 | -0.9 | 0.00 | 0/22 |
| AS | -5 | -1.2 | -0.1 | -0.3 | +4.2 | -1.6 | 0.00 | 1/24 |

Lost before measuring: words 4

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  0.8 min] device cuda:0/cuda:0
[  3.2 min] context: 199 tokens
[  4.2 min] recorded C
[  6.0 min] recorded S
[  7.5 min] recorded A
[  9.4 min] recorded AS
[  9.8 min] 96 takes done
```
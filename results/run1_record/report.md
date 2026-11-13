# Run 1 · stage 1: Orpheus recording + Gate 1 (smoke run)

- Lines: 20 · takes made: 21 · passed Gate 1 (words exact, no clipping): **15** · lines with a kept take: **14/20**
- Recording time: 5.8 min for 1.6 min of audio (0.27× real time on one T4)
- Pace (words per second, kept): Sam 3.04 · Maya 1.86
- GPU memory peak: 6.9 GB (GPU 0)

## Failed takes

- s01 take 1: words · heard: “No way! He's here. I have a little brother. His name is Tanuka.”
- s01 take 2: no audio · heard: “”
- s02 take 2: no audio · heard: “”
- s03 take 2: no audio · heard: “”
- s04 take 1: no audio · heard: “”
- s06 take 2: no audio · heard: “”
- s07 take 1: no audio · heard: “”
- s08 take 1: words · heard: “Hey, really sorry Maya, that's not fair.”
- s08 take 2: no audio · heard: “”
- s09 take 1: no audio · heard: “”
- s10 take 1: no audio · heard: “”
- m01 take 1: no audio · heard: “”
- m01 take 2: words · heard: “Basia gal face is so pretty tonight and the air is cool. You should see it.”
- m02 take 1: no audio · heard: “”
- m03 take 2: no audio · heard: “”
- m04 take 1: no audio · heard: “”
- m05 take 1: no audio · heard: “”
- m05 take 2: words · heard: “First Chennai, and then Notarai. I've been saving for a whole year.”
- m06 take 1: no audio · heard: “”
- m07 take 2: no audio · heard: “”
- m08 take 1: words · heard: “Poddy's in the hospital and I'm so far away. I just want to be there.”
- m08 take 2: no audio · heard: “”
- m09 take 1: no audio · heard: “”
- m10 take 1: no audio · heard: “”
- m10 take 2: words · heard: “When I think about it, Columbo taught me to be brave.”

## Kept

| id | who | row | s | words/s | text |
|---|---|---|---|---|---|
| s02 | sam | normal | 2.95 | 3.63 | So, how was your weekend? Did you do anything fun? |
| s03 | sam | bright | 4.04 | 2.86 | You cooked? Okay… but did you burn the rice? Like me? |
| s04 | sam | low | 3.21 | 3.99 | He cried all night… But then he smiled at me. Worth it. |
| s05 | sam | low | 4.47 | 2.81 | Bruno died last night. He was old. I'm okay. Just… quiet today. |
| s06 | sam | tense | 2.99 | 2.5 | I failed. The parking. Again. Don't laugh. |
| s07 | sam | bright | 3.19 | 2.34 | Wait. Seriously? He skipped the whole queue? |
| s09 | sam | normal | 3.27 | 2.93 | Um… I don't know. Maybe I'm not that clever. |
| s10 | sam | bright | 1.44 | 3.23 | I can't believe it! |
| m02 | maya | normal | 5.21 | 1.4 | Okay, tell me everything. What happened next? |
| m03 | maya | normal | 3.42 | 1.55 | Marvel again? That's so you. |
| m04 | maya | bright | 5.53 | 1.88 | So… I'm shift leader now. Me. Can you believe it? |
| m06 | maya | low | 5.32 | 3.12 | He shouted at me in front of everyone, so I went to the back and cried. |
| m07 | maya | tense | 6.58 | 1.88 | No. That was not okay. You don't speak to people like that. |
| m09 | maya | low | 6.24 | 1.33 | Oh, Sam… Bruno was family. Take your time. |

RESULT: PASS (stage 1 code works)

## Log
```
[  1.0 min] loading Orpheus (unsloth/orpheus-3b-0.1-ft, fp16) + SNAC
[  1.8 min] loaded; GPU memory 6.7 GB
[  1.8 min] loading Whisper large-v3-turbo
[  2.8 min] s01 sam/bright: 2 takes in 29 s → NONE passed
[  3.0 min] s02 sam/normal: 2 takes in 11 s → kept take 1
[  3.2 min] s03 sam/bright: 2 takes in 14 s → kept take 1
[  3.4 min] s04 sam/low: 2 takes in 12 s → kept take 2
[  3.7 min] s05 sam/low: 2 takes in 16 s → kept take 1
[  3.9 min] s06 sam/tense: 2 takes in 11 s → kept take 1
[  4.1 min] s07 sam/bright: 2 takes in 11 s → kept take 2
[  4.3 min] s08 sam/low: 2 takes in 11 s → NONE passed
[  4.5 min] s09 sam/normal: 2 takes in 12 s → kept take 2
[  4.6 min] s10 sam/bright: 2 takes in 5 s → kept take 2
[  5.0 min] m01 maya/normal: 2 takes in 25 s → NONE passed
[  5.4 min] m02 maya/normal: 2 takes in 20 s → kept take 2
[  5.6 min] m03 maya/normal: 2 takes in 12 s → kept take 1
[  5.9 min] m04 maya/bright: 2 takes in 21 s → kept take 2
[  6.3 min] m05 maya/bright: 2 takes in 23 s → NONE passed
[  6.7 min] m06 maya/low: 2 takes in 21 s → kept take 2
[  7.1 min] m07 maya/tense: 2 takes in 26 s → kept take 1
[  7.5 min] m08 maya/low: 2 takes in 25 s → NONE passed
[  7.9 min] m09 maya/low: 2 takes in 24 s → kept take 2
[  8.2 min] m10 maya/normal: 2 takes in 16 s → NONE passed
```

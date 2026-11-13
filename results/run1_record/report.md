# Run 1 · stage 1: Orpheus recording + Gate 1 (smoke run)

- Lines: 20 · takes made: 40 · passed Gate 1 (words exact, no clipping): **29** · lines with a kept take: **17/20**
- Recording time: 1.7 min for 2.8 min of audio (1.70× real time on one T4, 8 lines × 2 takes per batch)
- Pace (words per second, kept): Sam 3.19 · Maya 2.06
- GPU memory peak: 7.9 GB (GPU 0)

## Failed takes

- s01 take 1: words · heard: “No way. He's here. I have a little brother. His name is Thanoka.”
- s01 take 2: words · heard: “No way. He's here. I have a little brother. His name is Thanuka.”
- s05 take 1: words · heard: “Brillo died last night. He was old. I'm okay. Just quiet today.”
- s07 take 1: words · heard: “Wait, seriously? You skipped the whole queue?”
- m01 take 1: words · heard: “The scenic owl face is so pretty tonight, and the air is cool. You should see it.”
- m01 take 2: words · heard: “The sea at Galiface is so pretty tonight and the air is cool. You should see it.”
- m03 take 1: words · heard: “Marvel-a-den? That's so you.”
- m05 take 1: words · heard: “First Chennai, and then Matarai. I've been saving for a whole year.”
- m08 take 1: words · heard: “Patti's in the hospital. I'm so far away. I just want to be there.”
- m08 take 2: words · heard: “Potty's in hospital and I'm so far away. I just want to be there.”
- m10 take 1: words · heard: “When I think about it, Columbo taught me to be brave.”

## Names Whisper heard differently (not counted as failures)

- s01 take 1: thenuka · heard: “No way. He's here. I have a little brother. His name is Thanoka.”
- s01 take 2: thenuka · heard: “No way. He's here. I have a little brother. His name is Thanuka.”
- s05 take 1: bruno · heard: “Brillo died last night. He was old. I'm okay. Just quiet today.”
- m01 take 1: galle · heard: “The scenic owl face is so pretty tonight, and the air is cool. You should see it.”
- m01 take 2: galle · heard: “The sea at Galiface is so pretty tonight and the air is cool. You should see it.”
- m05 take 1: madurai · heard: “First Chennai, and then Matarai. I've been saving for a whole year.”
- m08 take 1: paati's · heard: “Patti's in the hospital. I'm so far away. I just want to be there.”
- m08 take 2: paati's · heard: “Potty's in hospital and I'm so far away. I just want to be there.”
- m10 take 1: colombo · heard: “When I think about it, Columbo taught me to be brave.”

## Kept

| id | who | row | s | words/s | text |
|---|---|---|---|---|---|
| s02 | sam | normal | 2.89 | 3.72 | So, how was your weekend? Did you do anything fun? |
| s03 | sam | bright | 3.74 | 3.11 | You cooked? Okay… but did you burn the rice? Like me? |
| s04 | sam | low | 3.12 | 4.11 | He cried all night… But then he smiled at me. Worth it. |
| s05 | sam | low | 4.89 | 2.56 | Bruno died last night. He was old. I'm okay. Just… quiet today. |
| s06 | sam | tense | 3.19 | 2.34 | I failed. The parking. Again. Don't laugh. |
| s07 | sam | bright | 3.04 | 2.47 | Wait. Seriously? He skipped the whole queue? |
| s08 | sam | low | 3.31 | 2.57 | Hey… I'm really sorry, Maya. That's not fair. |
| s09 | sam | normal | 3.1 | 3.1 | Um… I don't know. Maybe I'm not that clever. |
| s10 | sam | bright | 1.05 | 4.69 | I can't believe it! |
| m02 | maya | normal | 4.55 | 1.61 | Okay, tell me everything. What happened next? |
| m03 | maya | normal | 4.0 | 1.32 | Marvel again? That's so you. |
| m04 | maya | bright | 5.34 | 1.95 | So… I'm shift leader now. Me. Can you believe it? |
| m05 | maya | bright | 5.51 | 2.26 | First Chennai, and then Madurai. I've been saving for a whole year! |
| m06 | maya | low | 5.53 | 3.0 | He shouted at me in front of everyone, so I went to the back and cried. |
| m07 | maya | tense | 5.45 | 2.29 | No. That was not okay. You don't speak to people like that. |
| m09 | maya | low | 6.11 | 1.35 | Oh, Sam… Bruno was family. Take your time. |
| m10 | maya | normal | 4.3 | 2.69 | When I think about it, Colombo taught me to be brave. |

RESULT: PASS (stage 1 code works)

## Log
```
[  0.5 min] loading Orpheus (unsloth/orpheus-3b-0.1-ft, fp16) + SNAC
[  1.3 min] loaded; GPU memory 6.7 GB
[  1.3 min] loading Whisper large-v3-turbo
[  2.0 min] batch of 8 lines × 2 takes in 31 s
[  2.7 min] batch of 8 lines × 2 takes in 39 s
[  3.1 min] batch of 4 lines × 2 takes in 29 s
[  3.4 min] s01 sam/bright: NONE passed
[  3.4 min] s02 sam/normal: kept take 1
[  3.4 min] s03 sam/bright: kept take 2
[  3.5 min] s04 sam/low: kept take 1
[  3.5 min] s05 sam/low: kept take 2
[  3.5 min] s06 sam/tense: kept take 2
[  3.5 min] s07 sam/bright: kept take 2
[  3.5 min] s08 sam/low: kept take 1
[  3.5 min] s09 sam/normal: kept take 2
[  3.5 min] s10 sam/bright: kept take 2
[  3.5 min] m01 maya/normal: NONE passed
[  3.5 min] m02 maya/normal: kept take 2
[  3.5 min] m03 maya/normal: kept take 2
[  3.6 min] m04 maya/bright: kept take 2
[  3.6 min] m05 maya/bright: kept take 2
[  3.6 min] m06 maya/low: kept take 2
[  3.6 min] m07 maya/tense: kept take 2
[  3.6 min] m08 maya/low: NONE passed
[  3.6 min] m09 maya/low: kept take 1
[  3.6 min] m10 maya/normal: kept take 2
```

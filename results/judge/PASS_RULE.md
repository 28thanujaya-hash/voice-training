# The single judge and its pass rule (user, 20 Nov 2026)

**Judge:** Meta's superb/hubert-large-superb-er only (4 classes: neutral / happy / sad / angry). Our own judge and emotion2vec are no longer used. No ear involvement. If the judge is wrong, we accept it; we shape the sentences until it passes.

**Pass rule (user, 09:50; 0.8 at 09:47 was too strict):** a take passes when the judge gives its mood with **confidence above 0.5**:
| Mood | Must be judged | with p > 0.5 |
|---|---|---|
| normal | neutral; or happy / angry / sad only mildly | top answer neutral, or top answer happy with p_happy ≤ 0.5, or top answer angry with p_angry < 0.5, or top answer sad with p_sad < 0.5 (user, 09:56–09:57: mild happy, angry or sad is F's own voice; strong ones belong to bright, tense, low) |
| bright | happy | p_happy > 0.5 |
| low | sad | p_sad > 0.5 |
| tense | angry | p_angry > 0.5 |

Full F run, takes passing at 0.5: normal 25%, bright 69%, low 27%, tense 70%, hot tense 62% (top answer: 30 / 71 / 29 / 73 / 64%).
Scores: results/judge/superb_<run>.csv (tools/judge/superb.py, workflow judge_superb.yml).

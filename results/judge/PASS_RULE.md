# The single judge and its pass rule (user, 20 Nov 2026)

**Judge:** Meta's superb/hubert-large-superb-er only (4 classes: neutral / happy / sad / angry). Our own judge and emotion2vec are no longer used. No ear involvement. If the judge is wrong, we accept it; we shape the sentences until it passes.

**Pass rule (user, 09:47):** a take passes when the judge gives its mood with **confidence above 0.8**:
| Mood | Must be judged | with p > 0.8 |
|---|---|---|
| normal | neutral | p_neutral > 0.8 |
| bright | happy | p_happy > 0.8 |
| low | sad | p_sad > 0.8 |
| tense | angry | p_angry > 0.8 |

Full F run today (takes passing / lines with at least one passing take): normal 7% / 15%; bright 45% / 68%; low 9% / 23%; tense 47% / 68%; hot tense 33% / 54%.
Scores: results/judge/superb_<run>.csv (tools/judge/superb.py, workflow judge_superb.yml).

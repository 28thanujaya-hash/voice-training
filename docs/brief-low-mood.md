# Brief: making a TTS actor sound "low" (sad) to an emotion judge

Please answer as a single **.md file**.

## The project

We are building an offline English voice for a phone app. A character named F has four mood "rows": **normal, bright (happy), low (sad), tense (angry)**.

The pipeline:
1. **Actor:** Orpheus 3B, voice **tara**, records training lines. Orpheus reads text and supports a few sound tags (`<sigh>`, `<sniffle>`, `<gasp>`, `<groan>`, `<yawn>`, `<laugh>`, `<chuckle>`). It can also take an earlier "context turn" (text + its audio codes) as an example.
2. **Teacher:** Kokoro-82M, fine-tuned on the actor's passing takes, with one style row per mood.
3. **Student:** a small on-phone model that copies the teacher. **On the phone, tags do nothing.** At reading time the only levers are the mood row, punctuation, CAPS, and where the text is split.

## The judge

The only judge is **superb/hubert-large-superb-er** (HuBERT-large fine-tuned on IEMOCAP; 4 classes: neutral, happy, sad, angry). A low take passes only when the judge says **sad with probability > 0.5**. We accept the judge as it is, even when it's wrong. The task is to make the takes pass it.

## The problem: low fails

| Mood | Lines with at least one passing take |
|---|---|
| Tense | 147 / 161 |
| Bright | 114 / 132 |
| Normal | 78 / 127 |
| **Low** | **71 / 155** |

- Most failed low takes are judged **happy**. In the latest run, 63 of 98 takes were judged happy.
- Acoustic comparison of a passing vs a failing take of the same sentence (openSMILE eGeMAPS): passing takes have **longer pauses (0.17–0.32 s vs 0.12–0.14 s), are quieter, and say fewer syllables per second**. Failing takes run at about normal speed (median +2 to +4% vs her normal voice). Our target is 15–40% slower and at least 2 dB quieter.
- One long sentence passes on every take: *"After that, I walked home in the rain, and I didn't even notice I was wet."*

## What we tried

| Test | Low pass rate |
|---|---|
| No tag | 4/20 (20%) |
| `<sigh>` before the line | 5/24 (21%) |
| `<sniffle>` before the line | 5/22 (23%) |
| Context turn = an approved low clip ("Oh… you're back.") + `<sigh>` | Main recipe; full run 27% of takes |
| "…" at the natural pause (plain sad lines) | 7/20 (35%), vs 5/18 (28%) as written. No faster or slower than the original |
| Shocked lines ("He's not coming back?!"), as written | 0/20 |
| Shocked lines rewritten as `<sigh>` + "…" | 1/20 |
| Shocked lines rewritten as `<sigh>` + "…?" | 4/20 |

**What we see:** a tag makes one sound at the start, then she reads at normal speed. "…" adds a pause, but the words between pauses stay fast.

## Constraints (fixed)

- Keep Orpheus with the voice tara. No other TTS actor.
- **No audio processing to fake slowness** (no time-stretch or pitch-shift on training data). A fixed loudness gain is undecided.
- No spoken instructions or lead-in sentences (Orpheus reads them aloud, and lead-ins made her faster).
- Same words as the script. We may change punctuation, CAPS, splitting into pieces, and tags.
- Free GPU only (Kaggle T4 ~30 h/week, Colab T4 when available). Each test run is small: about 10–20 lines × a few versions × 4 takes.

## What we plan to test next

1. Split long lines into short pieces, each ending "…", recorded separately and joined with real silence.
2. A tag on every piece, not just the first.
3. Our slowest passing low take as the context example instead of "Oh… you're back."
4. `<groan>` / `<yawn>` on tired lines; `<sniffle>` + `<sigh>` on the saddest.

## Our questions

1. What writing changes (punctuation, splits, word order, CAPS) make a TTS model like Orpheus read **slower and quieter** without changing the words?
2. Which of our four planned tests would you run first, and what would you add?
3. Is there a way inside Orpheus's generation (sampling settings, temperature, repetition penalty, longer or multiple context turns, steering vectors, classifier-free-guidance-style tricks) to push the low reading slower, without processing the audio?
4. Since the phone model ignores tags, how do we make sure the low row learns "slow and quiet" from the recordings, so that it reads slowly even on plain text?
5. Anything about the judge (IEMOCAP "sad") that we should write toward, such as sentence length or ending shape?

Please be concrete: give example rewrites of these lines, and say what you'd expect each change to do.
- "I waited for an hour, but in the end, nobody came."
- "The house feels so empty without him."
- "I miss Paati's voice. She used to sing in the kitchen."
- "He's not coming back?!"

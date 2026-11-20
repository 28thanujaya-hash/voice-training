# Brief 2: writing rules so a TTS reads "low" and "normal" right

Please answer as a single **.md file**. This brief is **only about writing**.

## Setup (short)

- **Voice:** Orpheus 3B, voice tara, reads English lines for a character named F.
- **Judge:** an emotion classifier, superb/hubert-large-superb-er (IEMOCAP: neutral / happy / sad / angry). We accept its verdict even when it's wrong.
- **Pass rules:**
  - **Low** passes when the judge says sad with probability > 0.5.
  - **Normal** passes when it says neutral, or another mood only mildly (≤ 0.5).
- **The text is rewritten by an AI before the voice reads it.** On the phone, the final voice ignores tags, so the writing is the main lever.

**What the rewrite may change:** punctuation, CAPS, and where the line is split into separately spoken pieces (joined with silence).

**What it may not change:** the words or their order. Nothing may be added or removed.

## What the judge passes and fails today (4 takes per line)

### Low: lines that pass on every take

| Line | Median sad |
|---|---|
| I don't know — maybe I'm just tired. | 0.94 |
| I haven't listened to music for days… it just doesn't feel the same. | 0.89 |
| I almost called you — but I couldn't. | 0.87 |
| I'm so tired of being alone! | 0.84 |
| I know I made a mistake… and I feel terrible about it. | 0.83 |
| I'm just so tired of waiting. | 0.81 |
| They took her to the hospital at night, and nobody called me until morning… | 0.74 |
| I deleted all the photos by mistake… a whole year of photos. | 0.69 |
| After that, I walked home in the rain, and I didn't even notice I was wet. | 0.68 |
| Nobody even noticed I was gone. | 0.68 |

### Low: lines that never pass (median sad ≈ 0.00)

| Line |
|---|
| He called me last night… |
| He finally answered… |
| I saw him at the market… |
| It's done… |
| That sounds really lonely… |
| You forgot again?! |
| It's closing for good?! |
| He's not coming back?! |
| It's not fair! |
| I really thought he cared! |
| Nobody ASKED me. |
| Is it my fault? |

**Other failing low lines (best sad score < 0.3):**
- "Priya's gone home for the weekend, so the flat's empty."
- "I looked at the bus times to Jaffna three times today."
- "Nobody remembered my birthday this year… except Priya."
- "I watched an old film tonight… the one Paati liked."
- "Even the sea looks grey to me today…"
- "It's Monday again…"

### Normal: lines that never pass (every take heard as **happy**)

- That's okay. It's a hard sentence… let's try it again, slowly.
- That's alright… we can come back to this one later.
- Slowly… one word at a time.
- Hmm… no, not quite. But that's okay, let's look at it together.
- I work at the café in the evenings, so I study in the mornings.
- The bus was full again today, so I walked from Wellawatte.
- Priya made dosa this morning, and the whole flat smelled amazing.
- I call my family every Sunday, but this week Appa was busy.
- The café was quiet this afternoon, so I watched the people outside.

### Normal: lines that pass on every take (heard neutral)

- It's okay if you don't know the word. Just say what you can.
- Do you usually study at home, or do you go to the library?
- When I think about it, Colombo is busy, but it's never boring.
- Let's try a longer answer this time. Use "and" or "but".
- The train leaves at seven thirty, and the ticket is four hundred and fifty rupees.
- Really?

## What we notice (please confirm, correct or add)

**Low**
- Passing lines state a feeling in the first person ("I'm so tired", "I feel terrible", "I couldn't"). Failing ones only report an event ("He called me last night…").
- Short fragments ending "…" fail. Two-part lines joined by "…" or "—" pass.
- "?!", "!" on blame, and CAPS fail. Those sound angry or surprised.
- Speed isn't the answer. The always-passing "walked home in the rain" line is read 17–36% faster than her normal voice, and some very slow takes score ≈ 0.

**Normal**
- Gentle teacher reassurance ("That's okay… let's try again") and pleasant everyday stories are heard as happy.
- Questions, facts with numbers and plain instructions are heard neutral.

## Questions

1. **Low writing rules.** From the passing and failing lines, what writing patterns (within the rules above) make a line sound sad to this judge? Give a short numbered rule list, from most to least important.
2. **Low rewrites.** Rewrite each failing low line above (all 18) with those rules: same words, same order. Mark splits with " / ". After each, one line saying which rule you used. If you think a line can't become low by writing alone (for example "It's not fair!" or "You forgot again?!", which may really be tense), say so, and say which mood it belongs to.
3. **Normal writing rules.** What makes a line sound neutral rather than happy to this judge? Give a short rule list.
4. **Normal rewrites.** Rewrite each failing normal line above (9) the same way, with the rule used.
5. **Endings.** For low and for normal, which ending works best: ".", "…", "—", or a split at the last clause? Should the heaviest word come last?
6. **Short lines.** Very short lines ("It's done…", "Really?") give the judge little to hear. What can writing do for them, if anything?

Please keep it concrete: rules plus every rewrite, not general advice.

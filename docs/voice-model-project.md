# M & F Voice Model — Project Document

Nov 22, 2026 · @Thushara Jayawardane · Chat history: voice-chat-history.md (chats 1–5) and voice-chat-history-part2.md (chat 6 on) · Link style: link-style.md · Colab without a screen: colab-hands-free.md · Older judge work (chat 5): bright-judge.md · Script rewrites (draft 19 Nov): reading-rules-script-f.md

## Purpose and scope

The voice model is one small file (about 9 MB) on the phone that speaks as M and as F, offline, in four moods. It is its own project: the Spoken English app only calls it to read text aloud. Later it may also read books (an e-book reader), where the text is fixed and an AI prepares it for the voice (see Reading rules).

- **Delivers:** a voice that speaks everything in the app as M or F, at a clear learner pace, without internet.
- **Moods:** 4 rows per character (8 in total): normal, bright, low, tense.
- **Free only:** every model, tool and compute source is free and open (Orpheus, Kokoro, Paradee, Whisper, Kaggle, Colab).
- **Not in scope:** lessons, chat logic, Sinhala input, the app screens. Those belong to the Spoken English project.
- **Done means:** it passes every quality gate, ending with the student understanding every word and preferring it to the current voice.
- **Who decides:** the user alone (there is no separate mentor). Script wording, mood moves and approaches are his call.

## Saving work between chats (user, 20 Nov)

Each chat's workspace is private and is wiped when the chat ends. Only **the voice-training repo**, **the project docs** and **the user's Google Drive** survive.

1. **At the start of every chat, attach the voice-training repo with push access** and check that a push works. If it doesn't, tell the user before doing work that needs saving.
2. **Code and small results go into the repo as soon as they work**, not at the end of the chat.
3. **Bigger data** (measurements, embeddings, downloaded datasets): into the repo if under ~50 MB; otherwise into Google Drive → voice-training-results/, with a note in the repo saying where it is.
4. **Heavy work runs as a GitHub Actions job** (the repo is public: CPU machines are free), so the job itself lives in the repo and any chat can rerun it.
5. **Last resort**, if push and Drive both fail: put the code in a project doc.

## GPU rules (user, 21 Nov)

- **Order: 1. Colab, 2. Kaggle.** Use everything Colab gives. Break Colab work into **short jobs** (≈15 min) and save each job's results to GitHub as soon as it ends.
- **When Colab answers "Service Unavailable", move the job to Kaggle at once, and try Colab again only after 24 h.** (Colab locked 21 Nov ~18:30 → usable again 22 Nov 18:50.)
- **Kaggle allows only 2 GPU sessions at a time, queued ones included** ("Maximum batch GPU session count of 2"). **kaggle_queue.yml** pushes a list of jobs one by one as slots free, collects each finished job, and re-dispatches itself before the 6 h Actions limit.
- Kaggle jobs get only .py files: any clip a job needs (e.g. ctx_tense.mp3) must be downloaded by run.py (tense_rx failed without it).
- Full-scene jobs ran out of memory on Colab's single T4 for tense (run31_tense_1); they run fine on Kaggle (2 T4).
- The user said on 21 Nov evening: about 25 Kaggle GPU h left this week (reset Saturdays ~05:30 Colombo).

## The judge (user, 20 Nov): one outside judge, no ear

**The only judge is Meta's superb/hubert-large-superb-er** (HuBERT large fine-tuned on IEMOCAP; 4 answers: neutral / happy / sad / angry = our normal / bright / low / tense). The user is not involved in judging. **If the judge is wrong, we accept it: the work is to shape the recordings until the judge passes them.**

| Mood | A take passes when the judge's top answer is… |
| --- | --- |
| Bright | happy, confidence > 0.5 |
| Low | sad, confidence > 0.5 |
| Tense | angry, confidence > 0.5 |
| Normal | neutral; or happy / angry / sad only mildly (confidence ≤ 0.5) |

- **Length:** about 2 s of speech before it hears a mood; short lines mostly read neutral.
- **Its "sad" is big, acted sadness (IEMOCAP).**
- **Voice match** is checked alongside (tools/judge/voice_match.py, similarity to tara's own takes; usual recipe ≈ 0.70, low full scene ≈ 0.82).

Code: tools/judge/superb.py (judge_superb.yml), voice_match.py (voice_match.yml); results/judge/superb_<run>.csv, voice_<run>.csv. **Coverage** (lines with 0 / 1 / 2+ passing takes): tools/queue/coverage.py → results/judge/coverage.json. **Method comparison** (judge confidence by scene / context / tags / marks): tools/judge/compare_levers.py → results/judge/compare_levers.json.

## Recording recipes now in use (22 Nov)

| Mood | Recipe | Evidence |
| --- | --- | --- |
| **Low** | Line as the **last sentence of the full Anne grief scene** (ch. 37), one generation, only the line kept; **keep the script's `<sigh>`** | Scene + sigh: low_scene_2 56/70, low_fill_2 91/149, voice ~0.81. Scene **without** sigh: low_fill 3/104, voice 0.53 |
| **Tense** | **Context "Give it back!" + one-CAPS rewrite** (reading-rules-script-f.md), no tags | run21 RX 31/36. Full "How dare you" scene: only 13/100 |
| **Bright** | **Calm Anne scene** (ch. 15 "Isn't it good just to be alive…" + ch. 33 "I'm so glad my window looks east…") + the line, tags removed | run32 K 10/30 (heard angry far less than run31's excited picnic scene). Plain lines with no "!" went neutral (bright_calm_fill 17/76) → round 3 keeps "!" |
| **Normal** | Plain, no scene; no tags; "!" → ".", no CAPS | normal_fill_1/2 170/436 |

**What did not work for the mood (all judged):**
- **Reusing a recorded scene as a prefix** (run29): Orpheus emits end-of-speech at once (the scene is a finished utterance); blocking it for 1 s gives audio but no sadness (0–2/23).
- **Shorter scenes** (run30: last 2 sentences / last half): 2–3/~30, voice 0.70. Only the full ~55-word scene works.
- **One-sentence lead-ins** ("I am so sad / happy / angry.", run30b): 3–4/~30 per mood; bright heard angry, voice 0.49.
- Earlier: writing rewrites (run23), example clips as earlier turns (run22, run24, run25), IndexTTS2 (voice drifts).

**Judge confidence by method (same 8 hard lines):** low old recipe 0.12, context clips 0.14–0.23, lead-in 0.24, short scene 0.22, **full scene 0.75–0.81**; bright old 0.12, lead-in 0.22, excited scene 0.40, calm scene 0.46–0.52; tense old 0.11, lead-in 0.17. Levers vs plain on easier lines: bright chuckle +0.31, laugh +0.29; tense context +0.29, CAPS + context +0.50; low context + sigh +0.19, "…" at pauses +0.22.

## Characters, voices and moods

M speaks with the Orpheus voice **leo** and F with **tara**, chosen at the audition on 13 Nov. F is being built first, as the pilot.

| Character | Who | How they sound | Orpheus voice |
| --- | --- | --- | --- |
| F, 21 | From Jaffna, works at a café near Galle Face, studies English | Calm, witty, a little slower, full sentences, dry humour | tara |
| M, 20 | Peradeniya, IT diploma student, cricket and cooking | Warm, loud, fast, short sentences | leo |

Moods per character: **normal** (teaching, chat, dry humour), **bright** (excited, happy, teasing), **low** (sad, tired, sympathetic), **tense** (annoyed, firm, controlled anger). Full personas: sam-and-maya.md.

## Reading rules: how the AI prepares text for the voice

The text that reaches the voice is rewritten by an AI ("director"): same words, own punctuation, CAPS, splitting and voice row. **On the phone Paradee ignores tags**, so at reading time the only levers are voice row, punctuation, CAPS and splits. Tags only shape Orpheus when recording training data (for low the `<sigh>` before the line is essential with the scene method).

**Two steps, always in this order:** decide the mood from the meaning (precedence tense → low → bright → normal; unclear → normal), then rewrite into that mood's shape:
- **Low:** "." endings, no CAPS, "…" at pause points, shocked "?!" → "…?".
- **Bright:** "!" endings, no CAPS, no "…"/"—" breaks.
- **Tense:** one CAPS word on the contested word; units of ≤ ~5 words; "!" or "."; no tags.
- **Normal:** plain punctuation; no "!" and no CAPS.
- **Narration:** normal row; split at commas/breath points; silences 0.3 s comma, 0.4 s semicolon, 0.55 s sentence, 0.85 s paragraph.

## Pipeline

Actor (Orpheus) records → teacher (Kokoro) learns → student (Paradee) copies it for the phone. Gates G1–G4.

**Kokoro teacher plan (21 Nov):** per line and mood keep 1–2 takes that pass the judge, have the right words and voice match ≥ ~0.7; train on the line only; mostly single sentences (2–8 s) plus ~20% 2–3-sentence clips (≤ 15 s); keep loudness and pauses; one style row per mood (Kaggle T4); judge the teacher's rows on unseen lines; first teacher with ~150 clips per mood, then scale up, then Paradee.

## Current status and next steps (22 Nov 14:00)

**Coverage of F's script (lines with 2+ passing takes):** low 135/155, bright 114/134, tense 136/162, normal 107/171 (before round 3 and normal_fill_3 / tense_rx2).

**Running (Kaggle, kaggle_queue.yml):** normal_fill_3 (64 lines), tense_rx2 (26 lines), low_fill_3 (20 lines), bright_fill_3 (20 lines).

**Next steps:**
- ◐ Judge round 3; queue more top-ups for lines still under 2 passes (user: queue without asking).
- ☐ Pick per line the 1–2 best takes (judge pass + right words + voice match ≥ ~0.7); note: some recipes drift (bright ~0.5, normal ~0.55).
- ☐ First Kokoro teacher (~150 clips per mood), judge its rows.
- ☐ Scale up, retrain; then Paradee and phone tests. M's pilot after F passes.
- Waiting for the user: the 13 mood moves (reading-rules-script-f.md); a fixed loudness gain.

## History of runs and key results

| Date | Run | What happened | Result |
| --- | --- | --- | --- |
| 22 Nov | low_fill_2 | Grief scene + sigh back | 91/149, 33/51 lines, voice 0.80 |
| 22 Nov | bright_calm_fill | Calm scene, plain lines (no "!") | 17/76; mostly neutral |
| 22 Nov | tense_rx | Context + CAPS rewrite | Failed: context clip missing on Kaggle → tense_rx2 |
| 21–22 Nov | low_scene_1/2 | Grief scene + script text (sigh) | 45/68 and 56/70; voice 0.82 |
| 21–22 Nov | low_fill | Grief scene, **no sigh** | 3/104, voice 0.53 |
| 21–22 Nov | tense_scene_1/2 | Full "How dare you" scene, no tags | 13/100, voice 0.48 |
| 21–22 Nov | normal_fill_1/2 | Plain, no tags/marks | 170/436 |
| 21 Nov | run32 | Bright: calm scene vs no scene, plain line | K 10/30, C 8/32 |
| 21 Nov | run31 | Bright: excited picnic scene | 10/32, heard angry 18; tense crashed (Colab memory) |
| 21 Nov | run30b | One-sentence lead-ins | 3–4/~30 per mood |
| 21 Nov | run30 | Shorter scenes (2 sentences / half) | 3/31, 2/26 |
| 21 Nov | run29b/c | Scene reused as prefix | Instant end-of-speech; with end blocked 0–2/23 |
| 21 Nov | run28b | Low line at the end of the full scene | 56/57, voice 0.85 |
| 21 Nov | run22–27 | Context clips, scenes as earlier turns, IndexTTS2 | No real gain / voice drifts |
| 20 Nov | Single judge | Meta superb only | Tense 70%, bright 69%, low 27%, normal 39% |
| 19 Nov | Full run F | Old recipe, colab_chain.yml | ~6,000 takes |
| 16 Nov | run4 eval (G2) | Teacher v0.2 | Moods fail (rows alike) |
| 12–15 Nov | run0–run4 | Phones, audition, pilot | M = leo, F = tara |

## Infrastructure and working rules

All voice work lives in the **voice-training** repo ([github.com/28thanujaya-hash/voice-training](https://github.com/28thanujaya-hash/voice-training)).

| Item | Detail |
| --- | --- |
| Compute | Colab free (one T4, locks after ~3½ h); Kaggle ~30 GPU h/week, 2 sessions at once; CPU work on GitHub Actions |
| Kaggle | kaggle.yml (start / collect / sessions); kaggle_queue.yml (auto-queue + collect); kaggle_stop.yml (delete a notebook, only on request) |
| Colab | colab_chain.yml (jobs, gpu, alloc_tries); colab-hands-free.md |
| Top-up jobs | tools/queue/build_fill.py, build_fill2.py, build_fill3.py (build jobs for lines with < 2 passes); coverage.py |
| Judge | tools/judge/superb.py, voice_match.py, compare_levers.py |
| Secrets | KAGGLE_USERNAME, KAGGLE_API_TOKEN, COLAB_TOKEN |
| Models | Orpheus 3B (actor), Kokoro-82M (teacher), Paradee 1.3 (student), Whisper large-v3-turbo, SNAC; judge superb/hubert-large-superb-er; voice match SpeechBrain ECAPA |
| Licence duties | Trained voice name starts with "Llama"; app shows "Built with Llama" and ships the licence |

**Working rules:**
- Saving work between chats: see near the top. GPU rules: see above.
- One judge (Meta superb), no ear, plus voice match.
- The user decides wording, mood moves and approaches. For filling the script (top-ups), **queue without checking back** (user, 21 Nov).
- GPU tries: one round, then report; never re-push a queued Kaggle job.
- Argue pros and cons honestly; briefs for other AIs ask for a .md answer.
- No DSP slowing in training data. Emotion datasets only for judging unless the user OKs.
- Links: as in link-style.md.
- When a chat gets long, Claude writes the summary into the chat history, updates this doc, and continues in a new chat.

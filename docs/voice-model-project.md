# M & F Voice Model — Project Document

Nov 21, 2026 · @Thushara Jayawardane · Chat history: voice-chat-history.md (chats 1–5) and voice-chat-history-part2.md (chat 6 on) · Link style: link-style.md · Colab without a screen: colab-hands-free.md · Older judge work (chat 5): bright-judge.md · Script rewrites (draft 19 Nov): reading-rules-script-f.md

## Purpose and scope

The voice model is one small file (about 9 MB) on the phone that speaks as M and as F, offline, in four moods. It is its own project: the Spoken English app only calls it to read text aloud. Later it may also read books (an e-book reader), where the text is fixed and an AI prepares it for the voice (see Reading rules).

- **Delivers:** a voice that speaks everything in the app as M or F, at a clear learner pace, without internet.
- **Moods:** 4 rows per character (8 in total): normal, bright, low, tense.
- **Free only:** every model, tool and compute source is free and open (Orpheus, Kokoro, Paradee, Whisper, Kaggle, Colab).
- **Not in scope:** lessons, chat logic, Sinhala input, the app screens. Those belong to the Spoken English project.
- **Done means:** it passes every quality gate, ending with the student understanding every word and preferring it to the current voice.
- **Who decides:** the user alone (there is no separate mentor). Script wording, mood moves and approaches are his call.

## Saving work between chats (user, 20 Nov)

Each chat's workspace is private and is wiped when the chat ends. Only **the voice-training repo**, **the project docs** and **the user's Google Drive** survive. (Chat 5 could not push, so its judge data was lost and its code survived only in a project doc.)

1. **At the start of every chat, attach the voice-training repo with push access** and check that a push works. If it doesn't, tell the user before doing work that needs saving.
2. **Code and small results go into the repo as soon as they work**, not at the end of the chat.
3. **Bigger data** (measurements, embeddings, downloaded datasets): into the repo if under ~50 MB; otherwise into Google Drive → voice-training-results/, with a note in the repo saying where it is.
4. **Heavy work runs as a GitHub Actions job** (the repo is public: CPU machines are free), so the job itself lives in the repo and any chat can rerun it.
5. **Last resort**, if push and Drive both fail: put the code in a project doc.

## The judge (user, 20 Nov): one outside judge, no ear

**The only judge is Meta's superb/hubert-large-superb-er** (HuBERT large fine-tuned on IEMOCAP; 4 answers: neutral / happy / sad / angry = our normal / bright / low / tense). Our own judge and emotion2vec are no longer used. The user is not involved in judging. **If the judge is wrong, we accept it: the work is to shape the recordings until the judge passes them**, and to understand why the failures fail.

**Pass rule (confidence = the judge's probability for that answer):**

| Mood | A take passes when the judge's top answer is… |
| --- | --- |
| Bright | happy, confidence > 0.5 |
| Low | sad, confidence > 0.5 |
| Tense | angry, confidence > 0.5 |
| Normal | neutral; or happy / angry / sad only mildly (confidence ≤ 0.5). Mild happy is F's own voice; strong moods belong to the other rows |

**Full F run (actor takes, old recipe):** tense 70%, bright 69%, hot tense 62%, low 27%, normal 39%. Lines with at least one passing take: tense 147/161, bright 114/132, normal 78/127, low 71/155.

**What the judge needs (21 Nov):**
- **Length:** about 2 s of speech before it hears a mood. Under 1 s it mostly says neutral (low 0%, bright 15%, normal 97%). Low passes 8% on ≤4-word lines vs 82% on >14-word lines.
- **Its "sad" is big, acted sadness (IEMOCAP).** A real audiobook reader (Anne, LibriVox) passes bright 2/2, tense 2/2, normal 4/5, but low only 1/6.
- **Voice match** is checked alongside the judge from now on (tools/judge/voice_match.py: similarity to tara's own takes; Orpheus usual recipe ≈ 0.72, long-scene ≈ 0.85, actresses ≈ 0.1).

Code: tools/judge/superb.py (workflow judge_superb.yml), scores in results/judge/superb_<run>.csv; rule in results/judge/PASS_RULE.md; voice match results/judge/voice_<run>.csv.

## The long-scene method (21 Nov, user's idea) — the new recording recipe

**Orpheus picks up a mood from the sentences it has just spoken in the same utterance, not from earlier turns.** So each line is spoken as the **last sentence of a long scene in that mood**, and only the line is kept.

- **run28b (8 low lines that had never passed):** known scene first (Anne of Green Gables ch. 37, Anne grieving for Matthew) **30/30**; F's own homesick/lonely scene **26/27**. Voice match 0.84–0.86. Not slower (+11–14%) but clearly sad.
- Everything else tried for these lines stayed at 0–7%: writing rewrites (run23), one example clip as an earlier turn (run22), a 3-turn sad scene as earlier turns (run24), CREMA-D actress clips as context (run25), IndexTTS2 sliders/word descriptions (run26–27).
- **Scenes (public domain, Anne of Green Gables):** low = ch. 37 grief ("Half the time it seems to me that Matthew can't be dead…"); bright = ch. 13/2 picnic joy ("Oh, Marilla, there's going to be a Sunday-school picnic…"); tense = ch. 9 to Mrs. Lynde ("How dare you call me skinny and ugly?…"). **Normal: no scene (user).**
- **Cost:** speaking the whole scene each time is ~5× the GPU (~15 h for the script). **Cheaper version (user chose, run29):** record each mood's scene once, then give it as the start of the same utterance (scene text + line text, and the scene's own audio codes) so Orpheus generates only the line. If run29 matches run28b, the script is re-recorded this way (~2–3 GPU h).
- Full-scene jobs big_<mood>_1/2 exist in the repo but are **not to be run** (user, 21 Nov).

## Characters, voices and moods

M speaks with the Orpheus voice **leo** and F with **tara**, chosen at the audition on 13 Nov. F is being built first, as the pilot.

| Character | Who | How they sound | Orpheus voice | Audition notes |
| --- | --- | --- | --- | --- |
| F, 21 | From Jaffna, works at a café near Galle Face, studies English | Calm, witty, a little slower, full sentences, dry humour | tara | 10/10 lines exact, 2.2 words/s |
| M, 20 | Peradeniya, IT diploma student, cricket and cooking | Warm, loud, fast, short sentences | leo | 8/10 lines exact, 3.1 words/s (fast; slowed by the pace rules and the phone's speed setting) |

**The four moods (rows), per character:**

- **Normal:** teaching, chat, curious, dry humour.
- **Bright:** excited, happy, surprised, teasing.
- **Low:** sad, tired, sympathetic, worried.
- **Tense:** annoyed, firm, controlled anger.

Mood is chosen per sentence by switching the voice row; Gemini picks it in live replies. Full personas and life events: sam-and-maya.md.

## Reading rules: how the AI prepares text for the voice

The text that reaches the voice is always rewritten by an AI ("director"): same words, but its own punctuation, CAPS, splitting into units and choice of voice row. **On the phone Paradee ignores tags**, so at reading time the only levers are: voice row, punctuation, CAPS, and where the text is split. Tags (gasp, sigh…) only make Orpheus act when recording training data.

**Two steps, always in this order:** first decide the mood from the meaning (for a book: from the text before the line, never from any recording); then rewrite the line into that mood's shape.

**21 Nov:** for recording, writing turned out to be a weak lever (run23: GPT's rewrites had no effect; the long-scene method replaced it). The rules below still guide the phone text and the moods, but are no longer the main way to make a mood.

### Why takes fail the judge (20 Nov; same sentence, passed vs failed take, openSMILE eGeMAPS)

| Failure | What the passing take has that the failing one lacks | Lever |
| --- | --- | --- |
| Bright → heard sad | Vocal energy | "!" on short units, gasp; never chuckle / laugh; no "…" |
| Bright → heard angry | Flow and higher pitch; failures are overdone (louder, higher) | No CAPS, no "…" / "—" breaks; don't push harder |
| Bright → heard neutral | Melody | "?!" on surprise lines |
| Low → heard happy | Longer pauses, quieter (but slowness alone is not enough: 19% slower takes still heard happy) | Long-scene method |
| Tense → heard neutral | Punch | One CAPS word, short units, "!" (run21 RX 31/36) |
| Hot tense → heard happy | The gasp reads as excited surprise | No gasp in tense |

### Step 1 · Deciding the mood

Precedence when a sentence could be more than one: **tense** (blame, anger, a firm command) → **low** (hurt, loss, sympathy) → **bright** (plain good news, excitement) → **normal** (everything else). Mixed sentence: the feeling at the end decides. Unclear: normal.

| Mood | The sentence is this mood when… | Looks like it but isn't |
| --- | --- | --- |
| **Low** | The speaker's own hurt is stated: loss, regret, tiredness, loneliness, worry; sympathy | A list of mishaps; a complaint (→ tense); someone else's words; facts with the feeling only implied |
| **Bright** | Plain good news or excitement, said straight | Irony or punchline |
| **Tense** | Blame, a firm refusal or command, outrage, cold sarcasm | Disappointment or hurt → low; a playful complaint → normal |
| **Normal** | Teaching, chat, information, dry humour, book narration, anything unclear | |

### Step 2 · Rewriting into the mood's shape (same words)

- **Low:** "." endings (never "!", "?!"); `<sigh>` for the actor; no CAPS; shocked "?!" → "…?".
- **Bright:** gasp or no tag (never chuckle / laugh); short exclamations; no CAPS; "?!" for surprise.
- **Tense:** one CAPS word on the contested word; units of ≤ ~5 words; "!" or "." ending; no tags.
- **Normal:** keep the words; plain punctuation.
- **Narration (book reading):** always the normal row; split long sentences at commas and breath points; fixed silences: 0.3 s comma, 0.4 s semicolon, 0.55 s between sentences, 0.85 s between paragraphs.

## Pipeline

A big actor model records the acting, a mid-size teacher learns it, and a small student copies the teacher so it can run on the phone. Each step has its own check (gates G1–G4).

**Kokoro teacher plan (21 Nov):**
1. Per line and mood, keep 1–2 takes that pass the judge, have the right words and voice match ≥ ~0.7. Train on the line only (no scene, no tags).
2. Mostly single sentences (2–8 s) plus ~20% 2–3-sentence clips (≤ 15 s); no paragraphs.
3. Keep loudness and pauses (no normalisation): teacher v0.2 failed with all rows alike.
4. One style row per mood, fine-tuned on a Kaggle T4.
5. Judge the teacher's rows the same way (judge + voice match) on unseen lines.
6. First teacher with ~150 clips per mood as a check that rows differ; then scale up (3 takes per line + Set B), then Paradee.

## How the moods were made in the full run (19 Nov, old recipe)

| Mood | Context | Tag | Text |
| --- | --- | --- | --- |
| Normal | None | Chuckle on 5 dry jokes | As written |
| Low | "Oh… you're back." | `<sigh>` (not on caring questions, pleading, shocked "?!") | As written |
| Tense, cold | "Give it back!" | None | As written |
| Tense, hot (42) | "Give it back!" | `<gasp>` (heard as happy) | As written |
| Bright | None | Gasp / chuckle / laugh | Every line ends "!" or "?!" |

Replaced by the long-scene method (above) for the next recording.

**Pages (claude.ai, private to the user):** [Original vs actor: Anne, 10 lines](https://claude.ai/artifact/UW9TFxWN9tRjbTVBPVJffz), [Narration: original vs actor, 5 paragraphs](https://claude.ai/artifact/NP6C3fLKAVWZ915rz6uMQY), [F auto-sort check 1](https://claude.ai/artifact/Vjg64uiTzYoKz9oq4PqPZU), [F auto-sort check 2](https://claude.ai/artifact/FJUw1nHhi4d7FK4EnrC51i), [F bright: 10 removed takes](https://claude.ai/artifact/X65CSV15qviDXupcL3HxSa), [F bright check 4](https://claude.ai/artifact/RkX13EG4kZPe6i42NyRGg4).

## Current status and next steps (21 Nov 13:50)

F has 625 lines (normal 171, bright 134, low 156, tense 162). Full run recorded except part of normal batch 4. Total takes so far: about 6,000.

**Running:** run29a (bright + tense, Kaggle) and run29b (low, Colab): the cheap long-scene method (scene recorded once, reused as the start of each utterance).

**Next steps:**
- ◐ Collect and judge run29a/b (judge + voice match). Compare low with run28b (56/57).
- ☐ If it holds: re-record the script with the long-scene method (bright, low, tense; normal plain), 2 takes per line, pick by judge + voice match.
- ☐ First Kokoro teacher (~150 clips per mood), judge its rows.
- ☐ Scale up (more takes, Set B), retrain; then Paradee and phone tests.
- ☐ M's pilot, only after F passes.
- Waiting for the user: the 13 mood moves (reading-rules-script-f.md); a fixed loudness gain.
- Not used (yet): IndexTTS2 (works only by copying a real emotion clip, and the voice drifts to the clip's speaker); Groq's Orpheus v1 (has [directions], but no tara); Orpheus fine-tune on passing takes.

## History of runs and key results

| Date | Run | What happened | Result |
| --- | --- | --- | --- |
| 21 Nov | run29a/b | Long-scene method, scene recorded once and reused | Running |
| 21 Nov | **run28b** | **Low line as the last sentence of a long sad scene, one generation** | **Known scene 30/30, F's scene 26/27, voice 0.85** |
| 21 Nov | run26–27 | IndexTTS2 in tara's voice, 4 moods | Only copying a real emotion clip works (bright 20/24, tense 22/24, low 10/24, normal 11/24); voice drifts (0.17–0.49) |
| 21 Nov | run22–25 | Low: example clips, 3-turn scene, actress clips as earlier turns | 0–6 of ~29; no real gain |
| 21 Nov | run23 | GPT's writing rewrites, low + normal | No effect |
| 21 Nov | Book human | Karen Savage through the judge | Low 1/6; bright, tense pass |
| 20 Nov | Clip length | Full-run re-analysis | Judge needs ~2 s; short lines can't pass low/bright |
| 20 Nov | run21 | Tense / bright rewrites (CPU) | Tense RX 31/36; bright rewrites worse |
| 20 Nov | Single judge | Meta superb only, pass > 0.5 | Tense 70%, bright 69%, low 27%, normal 39% |
| 20 Nov | run18_book | Anne: dialogue + narration, director from text only | Pages sent |
| 19 Nov | Book study | Anne of Green Gables aligned with the text | Human moods are small shifts |
| 19 Nov | Full run F | Batches through colab_chain.yml | Tense, hot, low, bright done |
| 18 Nov | run9–15 | Low / context / tags; bright / tense recipes | Tags only nudge |
| 17–18 Nov | run5–8 | Lead-ins, IndexTTS, measures | Lead-ins and IndexTTS dropped |
| 16 Nov | run4 eval (G2) | Teacher v0.2 | **Moods fail** (4 rows sound alike) |
| 12–15 Nov | run0–run4 | Phones, smoke test, audition, pilot | M = leo, F = tara |

## Infrastructure and working rules

All voice work lives in the **voice-training** repo ([github.com/28thanujaya-hash/voice-training](https://github.com/28thanujaya-hash/voice-training)). Kaggle and Colab jobs are started by Claude through GitHub Actions.

| Item | Detail |
| --- | --- |
| Compute | Kaggle ~30 GPU h/week (reset Saturdays ~05:30 Colombo; 2 GPU jobs at once). Colab free: one T4, locks after ~3½ h for up to ~24 h. CPU work runs as GitHub Actions jobs. Paid options if ever needed: Modal, RunPod (see history part 2) |
| Kaggle | kaggle.yml (start / collect, gpu T4 / none); kaggle_stop.yml stops a running job by deleting its notebook (only when the user asks) |
| Colab | colab_chain.yml (jobs, gpu, alloc_tries); single T4: long generations need small batches. How it runs without a screen: colab-hands-free.md |
| Recording jobs | kaggle/jobs/full_<mood>_<n> (old recipe); run28b_longscene (full scene); run29a/b_prefix (scene reused); big_<mood>_<n> (full scene, do not run) |
| Judge | tools/judge/superb.py + judge_superb.yml; tools/judge/voice_match.py + voice_match.yml; tools/judge/pick_sad_ctx.py + pick_sad_ctx.yml (CREMA-D clips the judge is surest about) |
| Book study | tools/book/; results/book_anne/; results/book_human/ (human clips as judge input) |
| Secrets | KAGGLE_USERNAME, KAGGLE_API_TOKEN, COLAB_TOKEN; MODAL_TOKEN_ID / MODAL_TOKEN_SECRET (secret is wrong: missing "as-") |
| Models | Orpheus 3B (actor, Llama 3.2 licence), Kokoro-82M (teacher), Paradee 1.3 (student), Whisper large-v3-turbo, SNAC; judge superb/hubert-large-superb-er; voice match SpeechBrain ECAPA; IndexTTS2 (tested only) |
| Licence duties | The trained voice's name must start with "Llama"; the app shows "Built with Llama" and ships the licence |
| Phones | X9C and A34 |

**Working rules:**

- **Saving work between chats:** see the section near the top.
- **One judge (Meta superb), no ear,** plus voice match.
- The user decides wording, mood moves and approaches (no separate mentor).
- **GPU tries:** one round, then report; no hours of retrying. Don't start a run the user hasn't approved.
- Argue pros and cons honestly; don't just agree.
- Briefs for other AIs ask for the answer as a .md file.
- No slowing the audio by processing (DSP) in training data. A fixed loudness gain is still undecided.
- Emotion datasets (CREMA-D, RAVDESS, ESD) are for judging; using them as context or emotion examples bends this rule and needs the user's OK.
- Never re-push a queued Kaggle job.
- Links: as in link-style.md (direct links to the exact page, short named links).
- When a chat gets long, Claude writes the summary into the chat history, updates this doc, and continues in a new chat.

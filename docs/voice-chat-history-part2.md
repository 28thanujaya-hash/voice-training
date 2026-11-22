# Voice training — chat history summary, part 2 (chat 6 onwards)

Part 1 (chats 1–5) is voice-chat-history.md and stays as it is. Start a new chat with: "Continue from voice-chat-history.md, voice-chat-history-part2.md and voice-model-project.md".

---

## Chat 6 · 20–21 Nov 2026

**Judge:** Meta superb only, pass at confidence > 0.5 (normal = neutral, or another mood only mildly). User is not involved in judging.

**Compute tried (20 Nov):**
- Lightning AI (free credits, 4 h sessions, repriced Sept 2026) and Google TRC (TPUs, not GPUs): not used.
- Saturn Cloud: free accounts now get 0 hours ("Max of 0 hours of resource usage"). Dead end.
- Modal: account made, $1 free credit only; token secret pasted without its "as-" start, user gave up. Workflow modal_check.yml exists.
- Venice: an AI service, not GPU rental.
- Groq hosts a newer Orpheus (orpheus-v1-english) with written directions like [cheerful] / [whisper], free tier 100 requests/day, but voices autumn/diana/hannah/austin/daniel/troy, **no tara**. User: "not yet".
- Pay-as-you-go if ever needed: Modal (T4 ~$0.59/h, $30/month free with a card), RunPod Community (4090 ~$0.34/h), Vast.ai (cheapest, least stable).
- Kaggle GPU reset 21 Nov ~05:30; Kaggle runs 2 GPU jobs at once. Colab unlocked 21 Nov ~10:45.
- Doc written: claude/colab-hands-free.md (how Colab runs with no screen).

**Results (20 Nov):**
- run21 (Kaggle CPU): tense RX (rewrite: one CAPS word, short units, "!" + context "Give it back!") 31/36 = best tense recipe; plain "." ending flattens her (12/47). Bright rewrites (gasp, short exclamations) worse than the full run (failures heard angry).
- run17 (low "…"/"?!" rewrites): small effects; shocked lines as sigh + "…?" 4/20.
- **Clip length (full-run re-analysis, user: "we missed something"):** the judge needs ~2 s of speech to hear a mood. Under 1 s: low 0%, bright 15%, normal 97% (defaults to neutral). Low passes 8% on ≤4-word lines vs 82% on >14-word lines. Within the same line, longer (slower) takes pass more (low 62% vs 35%). Bright fails by overdoing it (failures louder and higher, heard angry).
- Human reader check: Karen Savage's Anne audiobook through the judge: bright 2/2, tense 2/2, normal narration 4/5, **low 1/6**. The judge's "sad" (IEMOCAP, acted) is bigger than book sadness.

**Results (21 Nov, Kaggle GPU):**
- run23 (GPT's writing rewrites, low + normal): no effect, almost all heard happy.
- run22 (low, one example clip: current / slowest passing / saddest): 1–3 of ~29.
- run24 (3-turn tara sad scene as earlier turns): 6/29 (1/29 in run25: noise).
- run25 (CREMA-D actress sad clips as context): no gain; voice drifts away from tara.
- run26/run27 (IndexTTS2 in tara's voice): only "copy a real emotion clip" works (bright 20/24, tense 22/24, low 10/24, normal 11/24 on never-passing lines); sliders and word descriptions fail. But the voice becomes the actress (voice match 0.17–0.49 vs Orpheus 0.72).
- **run28b (user's idea): the low line spoken as the LAST sentence of a long sad scene, one generation, only the line kept. Known scene (Anne grieving for Matthew, ch. 37) 30/30, F's own homesick/lonely scene 26/27, on 8 lines that never passed. Voice match 0.84–0.86 (more tara than the usual recipe). Not slower (+11–14%), but clearly sad.**

**Decisions (user, 21 Nov):**
- Use the long-scene method for all categories; **normal needs no scene**.
- Too expensive as full scenes (~5× GPU: ~15 h for the script). **Option 1 chosen:** record each mood's scene once, then give it as the start of the same utterance (scene text + line text, the scene's own audio codes) so Orpheus speaks only the line. Test: run29a (bright + tense, Kaggle) and run29b (low, Colab), started 21 Nov 13:33.
- Big full-scene jobs (big_<mood>_1/2) are built but **not to be run**; big_low_1 slipped out and was stopped after ~9 min (notebook deleted with kaggle_stop.yml).
- Kokoro plan: train on single sentences (2–8 s) plus ~20% 2–3-sentence clips (≤15 s), no paragraphs; keep loudness and pauses (no normalisation); one style row per mood; first teacher with ~150 clips per mood as a check that rows differ, then scale up (3 takes per line + Set B).
- Links: see claude/link-style.md.

**Tools added (repo):** tools/judge/voice_match.py + voice_match.yml (speaker similarity to tara, ECAPA); tools/judge/pick_sad_ctx.py + pick_sad_ctx.yml (CREMA-D clips the judge is surest about, any emotion); kaggle_stop.yml (stop a running Kaggle job by deleting its notebook, only on request); results/book_human (human clips as judge input); docs/brief-low-mood.md, docs/brief-writing-low-normal.md (GPT briefs).

**Open:**
- Collect and judge run29a/run29b (results in results/run29a_prefix, results/run29b_prefix; move mp3s into takes/, judge_superb.yml, voice_match.yml). If the prefix method matches run28b, re-record the script that way (2–3 GPU h), then the first Kokoro teacher.
- Pending user calls: the 13 mood moves (reading-rules-script-f.md); a fixed loudness gain.
- Claude's weekly usage was at ~94% on 21 Nov 13:45.

---

## Chat 7 · 21–22 Nov 2026

**Start:** repo attached with push access; push check OK.

**run29 (scene reused as prefix) failed:** run29b lost all 32 low takes. Cause (run29c, Colab): after the recorded scene Orpheus emits end-of-speech at once on every line (the scene is a finished utterance). With end-of-speech blocked for ~1 s the takes have audio but are not sad: 0/23 (whole scene), 2/22 (scene silence cut). run29a (same code, queued on Kaggle) was deleted on the user's request.

**Cheaper variants of the scene, all judged, all failed:**
- run30 shorter scenes: last 2 sentences 3/31, last half 2/26, voice ~0.70.
- run30b one-sentence lead-ins (user's idea) "I am so sad / happy / angry.": low 3/26, bright 4/31 (heard angry), tense 3/32; voice 0.49–0.69.
- → Only the full ~55-word scene, spoken in the same generation, works.

**Bright / tense with full scenes:** run31 bright (Anne picnic joy) 10/32, heard angry 18, voice 0.55; tense crashed on Colab (memory). run32 calm happy scene (Anne ch. 15 + ch. 33, user: "calmer scene from the book", marks and tags removed): K 10/30, fewer heard angry; no-scene control 8/32.

**Method comparison** (user asked to see judge confidence by scene / marks / tags): tools/judge/compare_levers.py. Same 8 hard low lines: old recipe 0.12, context clips ≤0.23, lead-in 0.24, short scene 0.22, full scene 0.75–0.81.

**Rules set by the user:**
- GPU order **1. Colab, 2. Kaggle**; use everything Colab gives; short Colab jobs; save each job's results to GitHub at once.
- **"Service Unavailable" on Colab → move the job to Kaggle at once; try Colab again only after 24 h** (next: 22 Nov 18:50).
- **Queue the script top-ups without checking back** ("continue full run"); remove all tags, marks as needed.

**Kaggle:** only 2 GPU sessions at once, queued included ("Maximum batch GPU session count of 2"). New **kaggle_queue.yml** pushes jobs as slots free, collects them, re-dispatches itself. Kaggle jobs get only .py files: tense_rx failed because ctx_tense.mp3 wasn't there (tense_rx2 downloads it).

**Top-ups (lines with < 2 passing takes):**
- low_scene_1/2 (grief scene + script text with sigh): 45/68, 56/70, voice 0.82.
- low_fill (scene, **no sigh**): 3/104, voice 0.53 → **the sigh is essential**; low_fill_2 (sigh back): 91/149, voice 0.80.
- tense_scene_1/2 (full "How dare you" scene, no tags): 13/100 → tense goes back to context + one-CAPS rewrite (tense_rx2).
- normal_fill_1/2 (plain, no tags, "!" → "."): 170/436.
- bright_calm_fill (calm scene, plain line without "!"): 17/76, mostly neutral → bright_fill_3 keeps "!".

**Coverage 22 Nov 14:00 (lines with 2+ passing takes):** low 135/155, bright 114/134, tense 136/162, normal 107/171.

**Running:** normal_fill_3, tense_rx2, low_fill_3, bright_fill_3 (kaggle_queue). Tools: tools/queue/ (build_fill*.py, coverage.py, tense_rewrites.json), tools/diag/run29_diag.py.

**Open:** judge round 3, more top-ups until every line has 2 passing takes; pick takes (judge + words + voice ≥ ~0.7); first Kokoro teacher. Pending user calls: 13 mood moves; loudness gain.

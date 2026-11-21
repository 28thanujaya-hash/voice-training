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

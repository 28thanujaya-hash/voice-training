# Run 7 · grey-zone cut + IndexTTS vs Orpheus lessons (17 Nov, CPU only, local)

## Grey-zone cut (mentor's map, 14:54/15:04): normal = big circle, moods only outside it
Pairwise classifiers normal-vs-mood on the run5 measures (sentence-held-out). Normal circle edge = 90th percentile of normal clips toward each mood.
Mood clip kept only if beyond that edge; normal clip kept only if inside all three edges. Everything else = grey zone, dropped.

| mood | clips kept | lines with ≥1 clip |
|---|---|---|
| normal | 284/365 | 139/152 |
| bright | 265/337 | 116/128 |
| low | 181/590 | 69/130 |
| tense | 346/369 | 136/143 |

Kept low vs kept normal (medians): breathier (H1-H2 10.7 vs 7.1 dB, CPP 17.7 vs 19.8), articulation 7% slower, only 0.45 dB quieter, 0.45 st lower.
(Looser edge, 80th pct: low 95/130 lines, normal 120/152.) Per-clip keep flags: keep_q90.csv.

## IndexTTS (40 clips) vs Orpheus (1,661 clips): mood minus normal, same measure code
| | Orpheus low | IndexTTS low | Orpheus tense | IndexTTS tense | Orpheus bright | IndexTTS bright |
|---|---|---|---|---|---|---|
| articulation rate | −3% | −15% | 0% | +12% | 0% | −19% |
| loudness | −0.5 dB | −3.9 dB | +3.8 dB | +4.8 dB | +2.6 dB | +3.2 dB |
| pitch | −0.6 st | 0 st | +0.3 st | +5.5 st | +1.7 st | +6.9 st |
| pitch movement (SD) | −0.1 | −0.7 | +0.6 | +0.8 | +1.0 | +1.6 |
| CPP (voice clarity) | −1.1 | −4.1 | −0.7 | −3.4 | −1.0 | −1.4 |
| H1-H2 (breathiness) | +1.2 dB | +5.2 dB | −2.0 dB | +5.3 dB | +0.1 dB | +2.4 dB |
| phrase slope | −0.6 | +0.4 | −0.9 | −3.1 | −0.2 | −0.4 |

IndexTTS low = slower words, much quieter, much breathier, flatter; not lower in pitch. Orpheus low has only a little breathiness.
IndexTTS tense = higher, faster, no hesitation, falls through the whole phrase. Orpheus tense = louder with a final fall, but not higher or faster.
Caveat: IndexTTS 10 clips per mood on 12 sentences; Orpheus many different lines. Directions are reliable, exact sizes are not.

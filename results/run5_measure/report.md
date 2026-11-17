# Run 5 · measure: all clips against the new mood measures (GPT review, 17 Nov)

Clips measured: 1661 (normal 365, bright 337, low 590, tense 369), lines: 553

## 1. Per-mood profile (median, with middle half in brackets)

| measure | normal | bright | low | tense |
|---|---|---|---|---|
| syllables/s | 3.48 (2.88…4.17) | 3.42 (2.89…3.97) | 3.33 (2.77…4.02) | 3.41 (2.95…4.00) |
| articulation rate (syl/s without pauses) | 4.16 (3.45…4.76) | 4.17 (3.61…4.69) | 4.04 (3.35…4.72) | 4.15 (3.50…4.69) |
| pauses ≥150 ms | 1.00 (0.00…1.00) | 1.00 (0.00…1.00) | 0.00 (0.00…1.00) | 1.00 (0.00…1.00) |
| pause share of time | 0.13 (0.00…0.25) | 0.19 (0.00…0.25) | 0.00 (0.00…0.28) | 0.17 (0.00…0.25) |
| pitch (st re 100 Hz) | 11.16 (10.21…12.53) | 12.91 (11.70…14.38) | 10.60 (9.74…11.83) | 11.47 (10.60…12.95) |
| pitch spread (SD st) | 2.16 (1.62…2.69) | 3.17 (2.74…3.73) | 2.09 (1.51…2.62) | 2.76 (2.34…3.38) |
| pitch range 90-10 (st) | 5.46 (4.06…6.76) | 8.32 (6.84…9.80) | 5.21 (3.81…6.80) | 7.06 (5.70…8.71) |
| phrase slope (st/s) | -0.76 (-1.95…-0.08) | -1.00 (-2.56…0.10) | -1.32 (-3.35…-0.26) | -1.61 (-4.36…-0.51) |
| final 400 ms slope (st/s) | -2.24 (-7.26…1.92) | -6.30 (-16.28…4.12) | -2.13 (-5.85…1.23) | -7.69 (-16.24…1.03) |
| end pitch vs body (st) | -1.44 (-2.57…-0.34) | -2.65 (-4.88…0.13) | -1.61 (-2.64…-0.58) | -2.75 (-4.06…-1.54) |
| loudness (LUFS) | -27.20 (-28.48…-25.61) | -24.63 (-25.93…-23.21) | -27.66 (-29.00…-26.25) | -23.39 (-24.95…-21.45) |
| loudness spread (dB SD) | 6.95 (6.52…7.47) | 7.03 (6.57…7.58) | 6.90 (6.21…7.54) | 7.54 (7.10…8.05) |
| end loudness vs body (dB) | -3.57 (-6.28…-1.71) | -3.94 (-6.69…-1.85) | -3.80 (-5.99…-1.50) | -5.63 (-8.58…-3.18) |
| CPP (higher = clearer, firmer voice) | 19.61 (18.54…20.40) | 18.64 (17.80…19.46) | 18.53 (17.70…19.41) | 18.88 (18.11…19.68) |
| HNR (dB, lower = breathier/rougher) | 18.19 (15.93…20.59) | 15.49 (13.98…17.76) | 18.01 (15.75…20.13) | 14.83 (12.76…16.62) |
| H1-H2 (dB, higher = breathier) | 7.24 (5.32…9.52) | 7.30 (5.14…9.95) | 8.42 (6.20…11.28) | 5.28 (3.54…8.18) |
| tilt (>1 kHz vs <1 kHz, dB) | -11.77 (-13.86…-9.75) | -10.51 (-12.30…-8.55) | -11.95 (-14.33…-9.65) | -9.05 (-11.60…-6.87) |
| first pause at (share of line) | 0.31 (0.21…0.40) | 0.32 (0.23…0.42) | 0.34 (0.26…0.43) | 0.35 (0.27…0.44) |

## 2. How well each measure alone separates two moods
AUC 0.50 = no help, 1.00 = perfect. Arrow = which way the second mood goes.

| measure | low→normal | normal→tense | normal→bright | tense→bright | low→tense |
|---|---|---|---|---|---|
| syllables/s | 0.54 ↑ | 0.52 ↓ | 0.53 ↓ | 0.51 ↓ | 0.52 ↑ |
| articulation rate (syl/s without pauses) | 0.53 ↑ | 0.51 ↓ | 0.50 ↑ | 0.51 ↑ | 0.52 ↑ |
| pauses ≥150 ms | 0.57 ↑ | 0.51 ↓ | 0.53 ↑ | 0.55 ↑ | 0.57 ↑ |
| pause share of time | 0.51 ↑ | 0.53 ↑ | 0.57 ↑ | 0.54 ↑ | 0.53 ↑ |
| pitch (st re 100 Hz) | 0.60 ↑ | 0.56 ↑ | 0.74 ↑ | 0.69 ↑ | 0.66 ↑ |
| pitch spread (SD st) | 0.53 ↑ | 0.73 ↑ | 0.83 ↑ | 0.64 ↑ | 0.74 ↑ |
| pitch range 90-10 (st) | 0.52 ↑ | 0.72 ↑ | 0.83 ↑ | 0.64 ↑ | 0.73 ↑ |
| phrase slope (st/s) | 0.57 ↑ | 0.63 ↓ | 0.53 ↓ | 0.60 ↑ | 0.56 ↓ |
| final 400 ms slope (st/s) | 0.52 ↓ | 0.63 ↓ | 0.59 ↓ | 0.52 ↑ | 0.65 ↓ |
| end pitch vs body (st) | 0.52 ↑ | 0.68 ↓ | 0.60 ↓ | 0.52 ↑ | 0.66 ↓ |
| loudness (LUFS) | 0.57 ↑ | 0.89 ↑ | 0.80 ↑ | 0.66 ↓ | 0.91 ↑ |
| loudness spread (dB SD) | 0.53 ↑ | 0.72 ↑ | 0.52 ↑ | 0.70 ↓ | 0.72 ↑ |
| end loudness vs body (dB) | 0.51 ↓ | 0.64 ↓ | 0.52 ↓ | 0.62 ↑ | 0.65 ↓ |
| CPP (higher = clearer, firmer voice) | 0.70 ↑ | 0.64 ↓ | 0.68 ↓ | 0.55 ↓ | 0.57 ↑ |
| HNR (dB, lower = breathier/rougher) | 0.53 ↑ | 0.78 ↓ | 0.71 ↓ | 0.58 ↑ | 0.76 ↓ |
| H1-H2 (dB, higher = breathier) | 0.59 ↓ | 0.65 ↓ | 0.50 ↑ | 0.64 ↑ | 0.72 ↓ |
| tilt (>1 kHz vs <1 kHz, dB) | 0.51 ↑ | 0.72 ↑ | 0.62 ↑ | 0.61 ↓ | 0.72 ↑ |
| old_pitch | 0.61 ↑ | 0.60 ↑ | 0.76 ↑ | 0.67 ↑ | 0.70 ↑ |
| old_range | 0.55 ↑ | 0.67 ↑ | 0.80 ↑ | 0.64 ↑ | 0.70 ↑ |
| old_move | 0.55 ↑ | 0.61 ↓ | 0.56 ↓ | 0.52 ↑ | 0.56 ↓ |
| old_pace | 0.67 ↑ | 0.57 ↑ | 0.52 ↓ | 0.60 ↓ | 0.76 ↑ |
| old_lufs | 0.60 ↑ | 0.90 ↑ | 0.81 ↑ | 0.66 ↓ | 0.94 ↑ |
| old_tilt | 0.50 ↑ | 0.73 ↑ | 0.62 ↑ | 0.63 ↓ | 0.72 ↑ |

## 3. Mood classifier — old 6 measures: 59% of clips land on their intended mood (chance 25%)

| intended ↓ / measured as → | normal | bright | low | tense |
|---|---|---|---|---|
| normal | 23% | 6% | 65% | 6% |
| bright | 8% | 44% | 25% | 23% |
| low | 10% | 3% | 87% | 0% |
| tense | 0% | 15% | 22% | 63% |

## 3. Mood classifier — new measures: 64% of clips land on their intended mood (chance 25%)

| intended ↓ / measured as → | normal | bright | low | tense |
|---|---|---|---|---|
| normal | 45% | 7% | 44% | 4% |
| bright | 8% | 51% | 14% | 27% |
| low | 13% | 5% | 79% | 3% |
| tense | 4% | 18% | 5% | 73% |

## 3. Mood classifier — new without pitch/loudness level: 56% of clips land on their intended mood (chance 25%)

| intended ↓ / measured as → | normal | bright | low | tense |
|---|---|---|---|---|
| normal | 37% | 10% | 43% | 9% |
| bright | 11% | 42% | 21% | 25% |
| low | 11% | 8% | 74% | 7% |
| tense | 9% | 17% | 17% | 57% |

## 4. GPT mood bundles, checked inside each sentence group (11 groups with all four moods)

| check | groups passing |
|---|---|
| low slower than normal (syl/s) | 8/11 |
| low more pause time than normal | 2/11 |
| low lower pitch than normal | 5/11 |
| low quieter than normal | 9/11 |
| low end weakens more than normal (loudness) | 4/11 |
| low breathier than normal (H1-H2) | 8/11 |
| low less clear voice than normal (CPP) | 9/11 |
| bright higher than normal | 11/11 |
| bright more pitch movement than normal (SD) | 11/11 |
| bright more pitch movement than tense (SD) | 10/11 |
| bright higher than tense | 10/11 |
| tense firmer voice than normal (CPP) | 5/11 |
| tense less breathy than low (H1-H2) | 9/11 |
| tense falls more at the end than bright | 2/11 |
| tense more loudness contrast than normal | 9/11 |
| tense louder than normal | 10/11 |
| normal faster than low, slower than bright | 0/11 |

## 5. Best clip per line by the new measures (provisional, before the 12-sentence diagnostic sets the targets)

| mood | lines | best clip measured as its own mood | median fit |
|---|---|---|---|
| normal | 152 | 100 | 0.55 |
| bright | 128 | 99 | 0.63 |
| low | 130 | 120 | 0.81 |
| tense | 143 | 118 | 0.79 |

## Log
```
[  0.0 min] $ pip install -q praat-parselmouth pyloudnorm soundfile librosa cmudict num2words scikit-learn
[  1.4 min] 1661 distinct clips for 553 lines
[  1.8 min] measured 0/1661
[  2.6 min] measured 300/1661
[  3.1 min] measured 600/1661
[  4.0 min] measured 900/1661
[  4.5 min] measured 1200/1661
[  5.2 min] measured 1500/1661
[  5.4 min] measured 1661 clips
[  5.5 min] done
```
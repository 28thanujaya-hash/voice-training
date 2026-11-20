# 4-way mood judge (HuBERT base + logistic regression), women only

Counts: crema 2312, ravdess 336, esd 7000

## Cross-dataset: share right on the left-out set (chance 25%)

| trained on | tested on | right | neutral | happy | sad | angry |
|---|---|---|---|---|---|---|
| ravdess + esd | crema | **61%** | 43% | 42% | 88% | 68% |
| ravdess | crema | **41%** | 3% | 3% | 99% | 55% |
| crema + esd | ravdess | **69%** | 85% | 49% | 58% | 93% |
| crema | ravdess | **62%** | 50% | 28% | 69% | 96% |
| crema + ravdess | esd | **57%** | 27% | 40% | 92% | 70% |
| crema + ravdess | esd | **57%** | 27% | 40% | 92% | 70% |

## tara, judge's top choice (judge trained on crema + ravdess + esd)

| set | takes | neutral | happy | sad | angry | right mood |
|---|---|---|---|---|---|---|
| full_bright | 493 | 10% | 38% | 41% | 12% | 38% |
| full_low | 581 | 4% | 5% | 90% | 1% | 90% |
| full_normal | 476 | 33% | 16% | 47% | 4% | 33% |
| full_tense | 626 | 46% | 15% | 6% | 33% | 33% |
| full_tense_hot | 146 | 15% | 30% | 11% | 44% | 44% |
| run13_bright | 94 | 24% | 18% | 50% | 7% | 18% |
| run14_tense | 128 | 39% | 22% | 23% | 16% | 16% |
| run15_tense | 130 | 35% | 14% | 36% | 15% | 15% |
| run9_low | 92 | 11% | 16% | 70% | 3% | 70% |

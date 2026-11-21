# run29c_fix · why run29b lost every take, and a fix

## A: first tokens of run29b's exact prompt (128258 = end of speech)

| line | first tokens | ends at once |
|---|---|---|
| m3l50 | 128258 | yes |
| m3l10 | 128258 | yes |
| m3l22 | 128258 | yes |
| m3l23 | 128258 | yes |
| m3l49 | 128258 | yes |
| m3l56 | 128258 | yes |
| m3l66 | 128258 | yes |
| m3l32 | 128258 | yes |

## B (end blocked ~1 s) and C (B + scene silence cut): Meta superb, low passes at sad > 0.5

| arm | takes | decoded | right words | PASS | lines with ≥1 PASS |
|---|---|---|---|---|---|
| B | 32 | 32 | 23 | 0 | 0/8 |
| C | 32 | 32 | 22 | 2 | 2/8 |

## Log
```
[  4.3 min] models loaded
[  4.8 min] scene: full 185 frames, trimmed 182 frames
[  6.7 min] m3l50 done
[  8.8 min] m3l10 done
[ 10.7 min] m3l22 done
[ 12.5 min] m3l23 done
[ 14.5 min] m3l49 done
[ 16.5 min] m3l56 done
[ 18.6 min] m3l66 done
[ 20.8 min] m3l32 done
```

"""Compare the director's mood calls with how the human read each line, per character.
Usage: python3 tools/book/compare.py results/book_anne ch09 ch37 ..."""
import csv, sys, statistics as S, collections
base, chs = sys.argv[1], sys.argv[2:]
G = collections.defaultdict(list)
for ch in chs:
    r = {x['sent']: x for x in csv.DictReader(open(f'{base}/{ch}.csv'))}
    for l in open(f'{base}/director/{ch}.txt'):
        if not l[0].isdigit(): continue
        i, m, spk = l.split()[:3]
        x = r.get(i)
        if x and x['start'] and x.get('pitch_rel') not in (None, '', 'nan'): G[(spk, m)].append(x)
f = lambda L, k: S.median(float(x[k]) for x in L if x[k] not in ('', 'nan'))
M = {'n': 'normal', 'b': 'bright', 'l': 'low', 't': 'tense'}
print(f"{'character':9} {'mood':7} {'lines':>5} {'speed%':>7} {'loud dB':>8} {'pitch st':>9} {'move st':>8} {'end fall':>9}")
for spk in sorted({k[0] for k in G}, key=lambda s: -sum(len(v) for k, v in G.items() if k[0] == s)):
    for m in 'nblt':
        L = G.get((spk, m), [])
        if len(L) >= 3:
            print(f"{spk:9} {M[m]:7} {len(L):5} {f(L,'rate_rel'):+7.1f} {f(L,'loud_rel'):+8.2f} {f(L,'pitch_rel'):+9.2f} {f(L,'move_rel'):+8.2f} {f(L,'end_fall'):+9.2f}")

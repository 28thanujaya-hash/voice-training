"""Per-line regrouping by the judge (chat 8). A line passes its mood with >=1 passing take.
A failed line moves to the mood the judge heard confidently (top answer, p>0.5) in most of its takes;
if no take is confidently another mood it moves to normal. Writes results/judge/regroup.csv."""
import csv, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../queue')
from coverage import FULL, TOP, K, R, pil, ok
INV = {v: k for k, v in K.items()}
rows = []
for m in K:
    ids, txt = [], {}
    for j in FULL[m]:
        ns = pil(j); [ids.append(i) for i in ns['LINES'][m] if i not in ids]; txt.update(ns.get('TXT', {}))
    takes = collections.defaultdict(list)
    for run in FULL[m] + TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f):
            for r in csv.DictReader(open(f)): takes[r['id']].append(r)
    for i in ids:
        T = takes[i]; n_pass = sum(ok(r, m) for r in T)
        conf = collections.Counter(); best = collections.defaultdict(float)
        for r in T:
            p = float(r['p_' + r['judged']])
            if p > .5 and INV[r['judged']] != m: conf[INV[r['judged']]] += 1; best[INV[r['judged']]] = max(best[INV[r['judged']]], p)
        if n_pass: new = m
        elif conf: new = max(conf, key=lambda k: (conf[k], best[k]))
        else: new = 'normal'
        t = re.sub(r'<[^>]+>\s*', '', txt.get(i, '')).strip()
        rows.append(dict(id=i, mood=m, takes=len(T), passes=n_pass, new=new, conf_other=dict(conf), text=t))
with open(f"{R}/results/judge/regroup.csv", 'w', newline='') as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
for m in K:
    s = [r for r in rows if r['mood'] == m]; f = [r for r in s if not r['passes']]
    print(m, 'tried', len(s), 'passed', len(s) - len(f), 'failed', len(f), 'moved', dict(collections.Counter(r['new'] for r in f)), 'no takes', sum(r['takes'] == 0 for r in s))
print('final', dict(collections.Counter(r['new'] for r in rows)))
print('final x orig', dict(collections.Counter((r['mood'], r['new']) for r in rows)))

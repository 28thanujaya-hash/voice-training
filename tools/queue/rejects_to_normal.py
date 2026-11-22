"""User 22 Nov: takes rejected by their own mood (bright / low / tense) go to the NORMAL row when the judge is not confident in any mood
(judged neutral, or happy / sad / angry all <= 0.5) - the normal pass rule. Only right-word takes (the judge CSVs hold only those).
Writes results/judge/normal_from_rejects.csv (run, take, id, from_mood, judged, p_*) and prints counts."""
import csv, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C
R = C.R; out = []; seen = set()
for m in ('bright', 'low', 'tense'):
    for run in C.FULL[m] + C.TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if not os.path.exists(f): continue
        for r in csv.DictReader(open(f)):
            if r.get('mood', m) != m or C.ok(r, m) or (run, r['take']) in seen: continue
            if C.ok(r, 'normal'):
                seen.add((run, r['take'])); out.append(dict(run=run, take=r['take'], id=r['id'], from_mood=m, judged=r['judged'], **{k: r['p_' + k] for k in ('neutral', 'happy', 'sad', 'angry')}))
with open(f"{R}/results/judge/normal_from_rejects.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0])); w.writeheader(); w.writerows(out)
n = collections.Counter(o['from_mood'] for o in out); L = collections.Counter(o['from_mood'] for o in {(o['id'], o['from_mood']): o for o in out}.values())
print('takes moved to normal:', dict(n), 'total', len(out)); print('distinct lines:', dict(L), 'total', sum(L.values()))

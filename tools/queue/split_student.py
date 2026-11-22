"""User 22 Nov: keep some recordings for the student (Paradee). Whole lines are held out (never seen by the Kokoro teacher), 20% per mood,
fixed seed so every chat gets the same split. Normal includes the rejects moved to normal (normal_from_rejects.csv).
Writes results/judge/split.csv (id, mood, set = teacher | student) and prints passing-take counts per set."""
import csv, os, random, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C
R = C.R; takes = collections.defaultdict(list)   # (mood, id) -> passing takes
for m in C.K:
    for run in C.FULL[m] + C.TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f):
            for r in csv.DictReader(open(f)):
                if r.get('mood', m) == m and C.ok(r, m): takes[(m, r['id'])].append((run, r['take']))
for r in csv.DictReader(open(f"{R}/results/judge/normal_from_rejects.csv")): takes[('normal', r['id'])].append((r['run'], r['take']))
rows, cnt = [], collections.Counter()
for m in C.K:
    ids = sorted({i for (mm, i) in takes if mm == m}); random.Random(f"split-{m}").shuffle(ids); cut = round(len(ids) * 0.2)
    for k, i in enumerate(ids):
        s = 'student' if k < cut else 'teacher'; rows.append(dict(id=i, mood=m, set=s)); cnt[(m, s, 'lines')] += 1; cnt[(m, s, 'takes')] += len(takes[(m, i)])
with open(f"{R}/results/judge/split.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ['id', 'mood', 'set']); w.writeheader(); w.writerows(rows)
for m in C.K: print(f"{m:7s} teacher {cnt[(m,'teacher','lines')]} lines / {cnt[(m,'teacher','takes')]} takes | student {cnt[(m,'student','lines')]} lines / {cnt[(m,'student','takes')]} takes")

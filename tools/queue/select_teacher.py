"""Teacher v0.3 clip choice (22 Nov). Per (mood, line): the best 2 takes that pass the judge (own mood, or normal via the rejects rule),
have the right words (the judge CSVs hold only right-word takes) and voice match >= 0.70; ranked by judge confidence for the mood.
Student lines (split.csv) are left out. ~8% of teacher lines (fixed seed) are validation. Text = the take's own spoken text (tags removed).
Writes results/teacher_v03/train.csv: file,row,text_b,text,split,id,url (url = raw GitHub mp3)."""
import csv, os, re, sys, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C
R = C.R; RAW = "https://raw.githubusercontent.com/28thanujaya-hash/voice-training/main/results"; MINV = 0.70
split = {(r['mood'], r['id']): r['set'] for r in csv.DictReader(open(f"{R}/results/judge/split.csv"))}
def texts(run):
    f = f"{R}/results/{run}/takes.csv"; d = {}
    if os.path.exists(f):
        for r in csv.DictReader(open(f)): d[f"{r['id']}_{r['var']}_{r['take']}"] = re.sub(r"<[^>]+>\s*", "", r['text']).strip()
    return d
def voice(run):
    f = f"{R}/results/judge/voice_{run}_mix.csv"   # mixed reference (all 4 moods)
    return {r['file'][:-4]: float(r['cos']) for r in csv.DictReader(open(f))} if os.path.exists(f) else {}
cand = collections.defaultdict(list)   # (row, id) -> (score, run, take, text, voice)
def add(run, rows, row_of):
    T, V = texts(run), voice(run)
    for r in rows:
        row = row_of(r); k = C.K[row]; v = V.get(r['take'])
        if v is None or v < MINV or r['take'] not in T: continue
        score = float(r['p_' + k]) if row != 'normal' else float(r['p_neutral'])
        cand[(row, r['id'])].append((score, run, r['take'], T[r['take']], round(v, 3)))
for m in C.K:
    for run in C.FULL[m] + C.TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f): add(run, [r for r in csv.DictReader(open(f)) if r.get('mood', m) == m and C.ok(r, m)], lambda r, m=m: m)
rej = collections.defaultdict(set)
for r in csv.DictReader(open(f"{R}/results/judge/normal_from_rejects.csv")): rej[r['run']].add(r['take'])
for run, ts in rej.items(): add(run, [r for r in csv.DictReader(open(f"{R}/results/judge/superb_{run}.csv")) if r['take'] in ts], lambda r: 'normal')
out = []; rnd = random.Random("teacher-v03-val")
for (row, i), L in sorted(cand.items()):
    if split.get((row, i)) != 'teacher': continue
    s = 'val' if rnd.random() < 0.08 else 'train'
    for score, run, take, text, v in sorted(L, reverse=True)[:2]:
        out.append(dict(file=f"final/{row}_{take}_{run}.wav", row=row, text_b=text, text=text, split=s, id=i, url=f"{RAW}/{run}/takes/{take}.mp3", voice=v, conf=round(score, 3)))
os.makedirs(f"{R}/results/teacher_v03", exist_ok=True)
with open(f"{R}/results/teacher_v03/train.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0])); w.writeheader(); w.writerows(out)
c = collections.Counter((o['row'], o['split']) for o in out); L = collections.Counter(o['row'] for o in {(o['row'], o['id']): o for o in out}.values())
for m in C.K: print(f"{m:7s} lines {L[m]:3d} | train clips {c[(m,'train')]:3d} | val clips {c[(m,'val')]:2d}")

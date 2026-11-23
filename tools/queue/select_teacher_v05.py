"""Teacher v0.5 clip choice (23 Nov, chat 8): as v0.4, but bright and tense keep up to 4 passing takes per sentence
(confidence >= 0.6) instead of the best 2, because v0.4's bright and tense rows were weak (eval 43 and 56 of 148).
v0.4 text: Teacher v0.4 clip choice (22 Nov, chat 8). As v0.3, with two changes from the user's regroup (22 Nov 16:53):
(1) a sentence that failed its own mood joins the mood the judge heard (> 0.5; otherwise normal) — results/judge/regroup.csv — unless its words do not fit (fit = no);
(2) the old per-take rejects-to-normal rule is dropped (it put sad / angry words into the normal row).
v0.3 text: Per (mood, line): the best 2 takes that pass the judge (own mood, or normal via the rejects rule),
have the right words (the judge CSVs hold only right-word takes) and voice match not in the run's worst 20% (and >= 0.35); ranked by judge confidence for the mood.
Student lines (split.csv) are left out. ~8% of teacher lines (fixed seed) are validation. Text = the take's own spoken text (tags removed).
Writes results/teacher_v05/train.csv: file,row,text_b,text,split,id,url (url = raw GitHub mp3)."""
import csv, os, re, sys, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C
R = C.R; RAW = "https://raw.githubusercontent.com/28thanujaya-hash/voice-training/main/results"; MINV = 0.35   # 22 Nov: absolute 0.70 was unfair (batches 3-4 score ~0.45 with the same recipe)
split = {(r['mood'], r['id']): r['set'] for r in csv.DictReader(open(f"{R}/results/judge/split.csv"))}
SPLIT_ID = {i: v for (m, i), v in split.items()}
def texts(run):
    f = f"{R}/results/{run}/takes.csv"; d = {}
    if os.path.exists(f):
        for r in csv.DictReader(open(f)): d[f"{r['id']}_{r['var']}_{r['take']}"] = re.sub(r"<[^>]+>\s*", "", r['text']).strip()
    return d
def voice(run):
    f = f"{R}/results/judge/voice_{run}_mix.csv"   # mixed reference (all 4 moods)
    if not os.path.exists(f): return {}
    d = {r['file'][:-4]: float(r['cos']) for r in csv.DictReader(open(f))}
    v = sorted(d.values()); cut = max(MINV, v[int(len(v) * 0.2)])   # relative: drop each run's worst 20% (the score also depends on the sentences)
    return {k: x for k, x in d.items() if x >= cut}
cand = collections.defaultdict(list)   # (row, id) -> (score, run, take, text, voice)
def add(run, rows, row_of):
    T, V = texts(run), voice(run)
    for r in rows:
        row = row_of(r); k = C.K[row]; v = V.get(r['take'])
        if v is None or r['take'] not in T: continue
        score = float(r['p_' + k]) if row != 'normal' else float(r['p_neutral'])
        cand[(row, r['id'])].append((score, run, r['take'], T[r['take']], round(v, 3)))
for m in C.K:
    for run in C.FULL[m] + C.TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f): add(run, [r for r in csv.DictReader(open(f)) if r.get('mood', m) == m and C.ok(r, m)], lambda r, m=m: m)
RG = {(r['mood'], r['id']): r for r in csv.DictReader(open(f"{R}/results/judge/regroup.csv"))}
INV = {v: k for k, v in C.K.items()}
for (m, i), g in RG.items():   # moved sentences: their takes the judge heard as the new mood
    new = g['new']
    if new == m or g['fit'] == 'no': continue
    def heard(r, new=new):
        p = {k: float(r['p_' + k]) for k in ('neutral', 'happy', 'sad', 'angry')}
        return max(p['happy'], p['sad'], p['angry']) <= .5 or r['judged'] == 'neutral' if new == 'normal' else (r['judged'] == C.K[new] and p[C.K[new]] > .5)
    for run in C.FULL[m] + C.TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f): add(run, [r for r in csv.DictReader(open(f)) if r['id'] == i and heard(r)], lambda r, new=new: new)
out = []; rnd = random.Random("teacher-v04-val")
for (row, i), L in sorted(cand.items()):
    if split.get((row, i), SPLIT_ID.get(i)) != 'teacher': continue   # moved sentences: use their own mood's split
    s = 'val' if rnd.random() < 0.08 else 'train'
    keep = [x for x in sorted(L, reverse=True) if x[0] >= .6][:4] if row in ('bright', 'tense') else []
    for score, run, take, text, v in (keep if len(keep) > 2 else sorted(L, reverse=True)[:2]):
        out.append(dict(file=f"final/{row}_{take}_{run}.wav", row=row, text_b=text, text=text, split=s, id=i, url=f"{RAW}/{run}/takes/{take}.mp3", voice=v, conf=round(score, 3)))
os.makedirs(f"{R}/results/teacher_v05", exist_ok=True)
with open(f"{R}/results/teacher_v05/train.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0])); w.writeheader(); w.writerows(out)
c = collections.Counter((o['row'], o['split']) for o in out); L = collections.Counter(o['row'] for o in {(o['row'], o['id']): o for o in out}.values())
for m in C.K: print(f"{m:7s} lines {L[m]:3d} | train clips {c[(m,'train')]:3d} | val clips {c[(m,'val')]:2d}")

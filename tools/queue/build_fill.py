"""Builds (no tags; marks per reading rules) Kaggle top-up jobs so every script line gets >=2 judge-passing takes (21 Nov, user: queue, continue the full run).
low_fill: low lines with <2 passes (not in low_scene_1), full Anne grief scene. tense_scene_1/2: tense lines with <2 passes, full Anne "How dare you" scene, tags removed.
normal_fill_1/2: normal lines with <2 passes (incl. never recorded), plain as in the full run. Meta superb pass rule as in results/judge/PASS_RULE.md."""
import csv, collections, os, re, shutil, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); KJ = f"{R}/kaggle/jobs"
sys.path.insert(0, f"{KJ}/full_low_1"); import lines5
BASE = {r[0]: r[3] for r in lines5.build()}
def pil(j): ns = {}; exec(open(f"{KJ}/{j}/pilot.py").read(), ns); return ns
K = {'low': 'sad', 'bright': 'happy', 'tense': 'angry', 'normal': 'neutral'}
JOBS = {'low': [f'full_low_{i}' for i in range(1, 5)], 'tense': [f'full_tense_{i}' for i in range(1, 5)] + ['full_tense_hot_1', 'full_tense_hot_2'], 'normal': [f'full_normal_{i}' for i in range(1, 5)]}
EXTRA = {'low': ['low_scene_1', 'low_scene_2', 'run28b_longscene'], 'tense': [], 'normal': []}
def passes(m):
    c = collections.Counter()
    for run in JOBS[m] + EXTRA[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if not os.path.exists(f): continue
        for r in csv.DictReader(open(f)):
            p = {k: float(r['p_' + k]) for k in ('neutral', 'happy', 'sad', 'angry')}
            ok = (r['judged'] == 'neutral' or max(p['happy'], p['sad'], p['angry']) <= .5) if m == 'normal' else (r['judged'] == K[m] and p[K[m]] > .5)
            c[r['id']] += ok
    return c
def ids_text(m):
    ids, txt = [], {}
    for j in JOBS[m]:
        ns = pil(j); ids += [i for i in ns['LINES'][m] if i not in ids]; txt.update({k: v for k, v in ns.get('TXT', {}).items() if isinstance(k, str)})
    return ids, {i: txt.get(i, BASE[i]) for i in ids}
def make(J, tmpl, mood, ids, txt, arms, takes, head):
    shutil.rmtree(f"{KJ}/{J}", ignore_errors=True); shutil.copytree(f"{KJ}/{tmpl}", f"{KJ}/{J}")
    s = open(f"{KJ}/{J}/run.py").read().replace(tmpl, J).split('\n', 1); s[0] = f"# {J}: {head}"
    s = '\n'.join(s); s = re.sub(r'report = \["# [^"]*"', f'report = ["# {J} · {head[:60]}"', s, count=1); open(f"{KJ}/{J}/run.py", "w").write(s)
    out = []
    for l in open(f"{KJ}/{J}/pilot.py").read().split('\n'):
        if l.startswith('LINES ='): l = 'LINES = ' + repr({mood: ids})
        elif l.startswith('ARMS ='): l = 'ARMS = ' + arms
        elif l.startswith('TXT ='): l = 'TXT = ' + repr(txt)
        elif l.startswith('TAKES ='): l = f'TAKES = {takes}'
        out.append(l)
    if not any(l.startswith('TXT =') for l in out): out.append('TXT = ' + repr(txt))
    open(f"{KJ}/{J}/pilot.py", "w").write(f"# {J} (21 Nov): {head}\n" + '\n'.join(out)); print(J, len(ids))
def halves(x): h = (len(x) + 1) // 2; return [x[:h], x[h:]]
untag = lambda t: re.sub(r"<[^>]+>\s*", "", t).strip()
def clean(t, mood):   # user 21 Nov: remove all tags; marks only as the reading rules need
    t = untag(t)
    if mood == 'low': t = t.replace('?!', '…?').replace('!', '.').replace(' — ', '… ').replace('—', '… '); t = re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).lower(), t)
    if mood == 'tense': t = t.replace('?!', '!').replace('…', '.').replace(' — ', '. ').replace('—', '. ')
    if mood == 'normal': t = t.replace('?!', '?').replace('!', '.').replace('…', ',').replace(' — ', ', ').replace('—', ', '); t = re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).lower(), t)
    return re.sub(r"\s+", " ", t).strip()
# low
c = passes('low'); ids, T = ids_text('low'); ls1 = set(pil('low_scene_1')['LINES']['low'])
SC = pil('run28b_longscene')['TXT'][('m3l50', 'K')].split(' || ')[0]
low = [i for i in ids if c[i] < 2 and i not in ls1]
make('low_fill', 'run28b_longscene', 'low', low, {(i, 'K'): SC + ' || ' + clean(T[i], 'low') for i in low}, "{'low': {'K': (False, None, False)}}", 3, f"low top-up, full grief scene, lines with <2 passes ({len(low)})")
# tense
c = passes('tense'); ids, T = ids_text('tense'); TS = pil('run29a_prefix')['SCENE']['tense']
ten = [i for i in ids if c[i] < 2]
for k, part in enumerate(halves(ten), 1):
    make(f'tense_scene_{k}', 'run28b_longscene', 'tense', part, {(i, 'K'): TS + ' || ' + clean(T[i], 'tense') for i in part}, "{'tense': {'K': (False, None, False)}}", 3, f"tense top-up, full 'How dare you' scene, no tags, lines with <2 passes ({len(part)})")
# normal
c = passes('normal'); ids, T = ids_text('normal')
nor = [i for i in ids if c[i] < 2]
for k, part in enumerate(halves(nor), 1):
    make(f'normal_fill_{k}', 'full_normal_1', 'normal', part, {i: clean(T[i], 'normal') for i in part}, "{'normal': {'T': (False, None, False)}}", 4, f"normal top-up, plain as in the full run, lines with <2 passes ({len(part)})")

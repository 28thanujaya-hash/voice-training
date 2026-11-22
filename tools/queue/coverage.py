"""Lines with 0 / 1 / 2+ judge-passing takes per mood, across the full run and every top-up run. Prints, and writes results/judge/coverage.json."""
import csv, json, os, collections, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def pil(j): ns = {}; exec(open(f"{R}/kaggle/jobs/{j}/pilot.py").read(), ns); return ns
K = {'low': 'sad', 'bright': 'happy', 'tense': 'angry', 'normal': 'neutral'}
FULL = {'low': [f'full_low_{i}' for i in range(1, 5)], 'bright': [f'full_bright_{i}' for i in range(1, 5)],
        'tense': [f'full_tense_{i}' for i in range(1, 5)] + ['full_tense_hot_1', 'full_tense_hot_2'], 'normal': [f'full_normal_{i}' for i in range(1, 5)]}
TOP = {'low': ['low_scene_1', 'low_scene_2', 'run28b_longscene', 'low_fill', 'low_fill_2', 'low_fill_3'],
       'bright': ['run31_bright_1', 'run31_bright_2', 'run32_bright_calm', 'run32_bright_calm_2', 'bright_calm_fill', 'bright_fill_3', 'bright_fill_4'],
       'tense': ['tense_scene_1', 'tense_scene_2', 'tense_rx2', 'tense_fill_3'], 'normal': ['normal_fill_1', 'normal_fill_2', 'normal_fill_3', 'normal_fill_4']}
def ok(r, m):
    p = {k: float(r['p_' + k]) for k in ('neutral', 'happy', 'sad', 'angry')}
    return (r['judged'] == 'neutral' or max(p['happy'], p['sad'], p['angry']) <= .5) if m == 'normal' else (r['judged'] == K[m] and p[K[m]] > .5)
def counts(m):
    ids = []; [ids.extend(i for i in pil(j)['LINES'][m] if i not in ids) for j in FULL[m]]
    c = collections.Counter()
    for run in FULL[m] + TOP[m]:
        f = f"{R}/results/judge/superb_{run}.csv"
        if os.path.exists(f):
            for r in csv.DictReader(open(f)): c[r['id']] += ok(r, m)
    return ids, c
if __name__ == "__main__":
    out = {}
    for m in K:
        ids, c = counts(m); out[m] = {'lines': len(ids), '0': sum(c[i] == 0 for i in ids), '1': sum(c[i] == 1 for i in ids), '2+': sum(c[i] >= 2 for i in ids)}
        print(m, out[m])
    json.dump(out, open(f"{R}/results/judge/coverage.json", "w"), indent=1)

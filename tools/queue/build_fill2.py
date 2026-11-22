"""Round 2 top-ups (22 Nov), chosen from round 1 results:
low_fill_2: full grief scene WITH the script's own <sigh> (round 1 without it: 3/104; low_scene with it: ~75%).
tense_rx: context "Give it back!" + one-CAPS rewrite (reading-rules-script-f.md; run21 RX 31/36), no tags. Full scene for tense was weak (13/100).
bright_calm_fill: calm Anne scene + plain line (run32 K 10/30, fewer heard angry). normal_fill_3: plain, no tags/marks."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_fill as B   # re-running round 1 builds is harmless (same folders, same content)
R = B.R; rx = json.load(open(f"{R}/tools/queue/tense_rewrites.json"))
def need(m, extra):
    B.EXTRA[m] = extra; c = B.passes(m); ids, T = B.ids_text(m); return [i for i in ids if c[i] < 2], T
# low
B.JOBS['low'] = B.JOBS['low']; low, T = need('low', ['low_scene_1', 'low_scene_2', 'run28b_longscene', 'low_fill'])
SC = B.pil('run28b_longscene')['TXT'][('m3l50', 'K')].split(' || ')[0]
B.make('low_fill_2', 'run28b_longscene', 'low', low, {(i, 'K'): SC + ' || ' + T[i] for i in low}, "{'low': {'K': (False, None, False)}}", 3, f"low top-up 2, grief scene, script text with its sigh ({len(low)})")
# tense
ten, T = need('tense', ['tense_scene_1', 'tense_scene_2'])
B.make('tense_rx', 'full_tense_1', 'tense', ten, {i: rx.get(i, B.clean(T[i], 'tense')) for i in ten}, "{'tense': {'T': (True, None, False)}}", 4, f"tense top-up, context + one-CAPS rewrite, no tags ({len(ten)})")
# bright
B.JOBS['bright'] = [f'full_bright_{i}' for i in range(1, 5)]
bri, T = need('bright', ['run31_bright_1', 'run31_bright_2', 'run32_bright_calm', 'run32_bright_calm_2'])
CS = B.pil('run32_bright_calm')['TXT']; CS = next(v for k, v in CS.items() if k[1] == 'K').split(' || ')[0]
def plain(t):
    t = B.untag(t); t = re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).lower(), t)
    return re.sub(r"\s+", " ", t.replace('?!', '.').replace('!', '.').replace(' — ', ', ').replace('—', ', ').replace('…', ',')).strip()
B.make('bright_calm_fill', 'run32_bright_calm', 'bright', bri, {(i, 'K'): CS + ' || ' + plain(T[i]) for i in bri}, "{'bright': {'K': (False, None, False)}}", 3, f"bright top-up, calm scene + plain line ({len(bri)})")
# normal
nor, T = need('normal', ['normal_fill_1', 'normal_fill_2'])
B.make('normal_fill_3', 'full_normal_1', 'normal', nor, {i: B.clean(T[i], 'normal') for i in nor}, "{'normal': {'T': (False, None, False)}}", 4, f"normal top-up 3, plain ({len(nor)})")

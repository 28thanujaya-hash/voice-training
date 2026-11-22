"""Round 3 (22 Nov): low_fill_3 = grief scene + script text with its sigh (round 2: 91/149); bright_fill_3 = calm scene + the script line
with tags removed but its "!" kept (round 2 plain lines went neutral: 41/76)."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C, build_fill as B
def need(m):
    ids, c = C.counts(m); return [i for i in ids if c[i] < 2]
T = B.ids_text('low')[1]; low = need('low'); SC = B.pil('run28b_longscene')['TXT'][('m3l50', 'K')].split(' || ')[0]
B.make('low_fill_3', 'run28b_longscene', 'low', low, {(i, 'K'): SC + ' || ' + T[i] for i in low}, "{'low': {'K': (False, None, False)}}", 4, f"low top-up 3, grief scene + script text with sigh ({len(low)})")
B.JOBS['bright'] = C.FULL['bright']; T = B.ids_text('bright')[1]; bri = need('bright')
CS = next(v for k, v in B.pil('run32_bright_calm')['TXT'].items() if k[1] == 'K').split(' || ')[0]
B.make('bright_fill_3', 'run32_bright_calm', 'bright', bri, {(i, 'K'): CS + ' || ' + B.untag(T[i]) for i in bri}, "{'bright': {'K': (False, None, False)}}", 4, f"bright top-up 3, calm scene + script line, tags removed, '!' kept ({len(bri)})")

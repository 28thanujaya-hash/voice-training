"""Round 4 (22 Nov, chat 8): bright_fill_4 = the 8 bright sentences with no passing take (mostly short "?!" surprise lines that read neutral).
Two arms, both the scene + the line in one generation: K = excited picnic scene (run31), L = calm scene (run32) + <laugh> before the line. '!' kept."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as C, build_fill as B
B.JOBS['bright'] = C.FULL['bright']; T = B.ids_text('bright')[1]
ids, c = C.counts('bright'); bri = [i for i in ids if c[i] == 0]
EX = B.pil('run31_bright_1')['TXT'][('m3b31', 'K')].split(' || ')[0]
CS = next(v for k, v in B.pil('run32_bright_calm')['TXT'].items() if k[1] == 'K').split(' || ')[0]
txt = {}
for i in bri:
    txt[(i, 'K')] = EX + ' || ' + B.untag(T[i]); txt[(i, 'L')] = CS + ' || <laugh> ' + B.untag(T[i])
B.make('bright_fill_4', 'run32_bright_calm', 'bright', bri, txt, "{'bright': {'K': (False, None, False), 'L': (False, None, False)}}", 4, f"bright top-up 4, excited scene / calm scene + laugh ({len(bri)})")
print(bri)

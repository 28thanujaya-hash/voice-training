# Maya line list for run 5 = run-4 lines + the fixes approved 16 Nov (fixes.py). Rows: (id, row, group, text, split).
from data import LINES as L4
import fixes as F
def build():
    out = []
    for lid, row, grp, text, split, _src in L4:
        if lid in F.DROP: continue
        key = f"{grp}:{row}" if grp else None
        text = F.CHANGE.get(lid, F.CHANGE.get(key, text) if key else text)
        if lid in F.MOVE: row = F.MOVE[lid]
        out.append((lid, row, grp, text, split))
    out += [(lid, row, grp, text, split) for lid, row, text, grp, split in F.ADD]   # fixes.ADD is (id, row, text, group, split)
    return out
LEAD = {"normal": "Hi, how was your day? Mine was fine.",
        "bright": "Oh wow, this is the best news ever!",
        "low": "I'm so tired… nothing went right today.",
        "tense": "I am really angry about this. Listen to me."}

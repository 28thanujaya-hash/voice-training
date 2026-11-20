"""4-way mood judge (neutral / happy / sad / angry = normal / bright / low / tense), trained on women's acted speech only.

Usage: python tools/judge/judge.py   (reads results/judge/emb/*.npz, writes results/judge/report.md and tara_judged.csv)
1. Cross-dataset test: train on all human sets but one, test on the one left out (speakers never seen) — with and without ESD.
2. Final judge on all human sets (with ESD), applied to every tara take.
"""
import glob, os, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "results/judge")
E, M = [], []
for f in sorted(glob.glob(f"{D}/emb/*.npz")):
    z = np.load(f, allow_pickle=False)
    if len(z["E"]) == 0: continue
    E.append(z["E"].astype(np.float32)); M.append(pd.DataFrame({k: z[k] for k in z.files if k != "E"}))
E = np.concatenate(E); M = pd.concat(M, ignore_index=True)
MOODS = ["neutral", "happy", "sad", "angry"]
mk = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=4000))
H = M.set.isin(["crema", "ravdess", "esd"]) & M.mood.isin(MOODS)
lines = ["# 4-way mood judge (HuBERT base + logistic regression), women only\n",
         "Counts: " + ", ".join(f"{s} {int((H & (M.set == s)).sum())}" for s in ("crema", "ravdess", "esd")) + "\n",
         "## Cross-dataset: share right on the left-out set (chance 25%)\n", "| trained on | tested on | right | neutral | happy | sad | angry |", "|---|---|---|---|---|---|---|"]
for test in ("crema", "ravdess", "esd"):
    for train in ([s for s in ("crema", "ravdess", "esd") if s != test], [s for s in ("crema", "ravdess") if s != test]):
        if not train or (H & (M.set == test)).sum() == 0: continue
        a = H & M.set.isin(train); b = H & (M.set == test)
        if a.sum() == 0: continue
        c = mk().fit(E[a], M.mood[a]); p = c.predict(E[b]); y = M.mood[b].values
        per = [f"{(p[y == m] == m).mean():.0%}" if (y == m).any() else "—" for m in MOODS]
        lines.append(f"| {' + '.join(train)} | {test} | **{(p == y).mean():.0%}** | " + " | ".join(per) + " |")
c = mk().fit(E[H], M.mood[H])
T = (M.set == "tara").values
if T.any():
    P = c.predict_proba(E[T]); cls = list(c.classes_)
    out = M[T][["spk", "mood", "level", "item"]].rename(columns={"spk": "run", "level": "var", "item": "take"}).copy()
    for i, k in enumerate(cls): out["p_" + k] = P[:, i].round(3)
    out["judged"] = [cls[i] for i in P.argmax(1)]
    out.to_csv(f"{D}/tara_judged.csv", index=False)
    want = {"normal": "neutral", "bright": "happy", "low": "sad", "tense": "angry"}
    lines += ["\n## tara, judge's top choice (judge trained on crema + ravdess + esd)\n", "| set | takes | neutral | happy | sad | angry | right mood |", "|---|---|---|---|---|---|---|"]
    out["group"] = out.run.str.replace(r"_\d+$", "", regex=True) + " " + out["var"]
    for g, x in out.groupby(out.run.str.replace(r"_\d+$", "", regex=True)):
        sh = x.judged.value_counts(normalize=True)
        mood = x.mood.mode().iat[0] if x.mood.notna().any() and len(x.mood.mode()) else ""
        right = f"{(x.judged == want.get(mood, '')).mean():.0%}" if mood in want else "—"
        lines.append(f"| {g} | {len(x)} | " + " | ".join(f"{sh.get(m, 0):.0%}" for m in MOODS) + f" | {right} |")
open(f"{D}/report.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))

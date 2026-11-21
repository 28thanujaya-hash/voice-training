"""Judge confidence by method (scene, context, tags, marks, writing). Meta superb only.
Confidence = the judge's probability for the target mood (low→sad, bright→happy, tense→angry, normal→neutral), mean over right-word takes.
Part 1: same 8 never-passing lines per mood, many methods (fair comparison).
Part 2: lever vs plain inside the same run (same lines, same day): change in mean confidence.
Writes results/judge/compare_levers.json and prints both tables."""
import csv, glob, json, os, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); J = f"{ROOT}/results/judge"
KEY = {"low": "sad", "bright": "happy", "tense": "angry", "normal": "neutral"}
def rows(run):
    f = f"{J}/superb_{run}.csv"
    return list(csv.DictReader(open(f))) if os.path.exists(f) else []
def stat(R, mood):
    k = KEY[mood]; p = [float(r["p_" + k]) for r in R]
    if not p: return None
    ok = [r for r in R if r["judged"] == k and float(r["p_" + k]) > 0.5]
    return dict(n=len(p), mean=round(st.mean(p), 3), median=round(st.median(p), 3), pass_pct=round(100 * len(ok) / len(p)))
def pick(run, mood, var=None, ids=None):
    return [r for r in rows(run) if r.get("mood") == mood and (var is None or r["var"] == var) and (ids is None or r["id"] in ids)]
low8 = sorted({r["id"] for r in rows("run28b_longscene")})
bt8 = {m: sorted({r["id"] for r in rows("run30b_lead") if r["mood"] == m}) for m in ("bright", "tense")}
full = lambda m: sum((rows(f"full_{m}_{n}") for n in range(1, 5)), [])
P1 = {"low": [("Old recipe (context + sigh), full run", [r for r in full("low") if r["id"] in low8]),
              ("Context: slowest passing take (run22 B)", pick("run22_low_ctx", "low", "B")),
              ("Context: saddest take (run22 C)", pick("run22_low_ctx", "low", "C")),
              ("Context: 3-turn sad scene as earlier turns (run24)", pick("run24_low_scene", "low", "S")),
              ("Context: actress sad clips (run25 H3)", pick("run25_low_human", "low", "H3")),
              ("Lead-in \"I am so sad.\" (run30b)", pick("run30b_lead", "low", "L")),
              ("Scene, last 2 sentences (run30 S1)", pick("run30_short", "low", "S1")),
              ("Scene, last half (run30 S2)", pick("run30_short", "low", "S2")),
              ("Full scene: Anne grief (run28b K)", pick("run28b_longscene", "low", "K")),
              ("Full scene: F's own (run28b F)", pick("run28b_longscene", "low", "F"))]}
for m in ("bright", "tense"):
    r31 = sum((pick(f"run31_{m}_{n}", m) for n in (1, 2)), [])
    P1[m] = [(("Old recipe (tag, \"!\"), full run" if m == "bright" else "Old recipe (context \"Give it back!\"), full run"), [r for r in full(m) + (rows("full_tense_hot_1") + rows("full_tense_hot_2") if m == "tense" else []) if r["id"] in bt8[m]]),
             (f"Lead-in \"I am so {'happy' if m == 'bright' else 'angry'}.\" (run30b)", pick("run30b_lead", m, "L")),
             ("Full scene: Anne " + ("picnic joy" if m == "bright" else "\"How dare you\"") + " (run31)", r31)]
P2 = [("low", "Tag: sigh", "run9_low", "C", "S"), ("low", "Context \"Oh… you're back.\"", "run9_low", "C", "A"), ("low", "Context + sigh", "run9_low", "C", "AS"),
      ("low", "Tag: sniffle", "run10_tags", "C", "SN"), ("low", "Marks: \"…\" at pauses", "run17_low", "A", "E"), ("low", "Writing: GPT rewrite", "run23_writing", "O", "R"),
      ("bright", "Tag: chuckle", "run10_tags", "C", "CH"), ("bright", "Tag: laugh", "run10_tags", "C", "LA"), ("bright", "Tag: gasp", "run10_tags", "C", "GA"),
      ("bright", "Context (bright clip)", "run11_ctx", "C", "X"), ("bright", "Marks: \"!\" instead of \".\"", "run13_bright", "C", "B"), ("bright", "Marks \"!\" + tag", "run13_bright", "C", "T"),
      ("tense", "Tag: groan", "run10_tags", "C", "GR"), ("tense", "Context \"Give it back!\"", "run14_tense", "C", "X"), ("tense", "Context + gasp", "run14_tense", "C", "XG"),
      ("tense", "Context + \"!\" ending", "run14_tense", "C", "XE"), ("tense", "Marks: one CAPS word, short units", "run21_fix", "N", "R"), ("tense", "CAPS rewrite + context", "run21_fix", "N", "RX"),
      ("normal", "Writing: GPT rewrite", "run23_writing", "O", "R")]
out = {"part1": {}, "part2": []}
for m, L in P1.items():
    print(f"\n== {m} (same 8 lines: {', '.join(low8 if m == 'low' else bt8[m])})")
    out["part1"][m] = []
    for name, R in L:
        s = stat(R, m)
        if s: out["part1"][m].append(dict(method=name, **s)); print(f"  {s['mean']:.2f} mean  {s['pass_pct']:3d}% pass  n={s['n']:3d}  {name}")
print("\n== lever vs plain, same run")
for m, name, run, base, arm in P2:
    a, b = stat(pick(run, m, base), m), stat(pick(run, m, arm), m)
    if a and b:
        d = dict(mood=m, lever=name, run=run, plain=a["mean"], with_lever=b["mean"], change=round(b["mean"] - a["mean"], 3), n=b["n"])
        out["part2"].append(d); print(f"  {m:6s} {d['change']:+.2f}  ({a['mean']:.2f} → {b['mean']:.2f})  {name} [{run}]")
json.dump(out, open(f"{J}/compare_levers.json", "w"), indent=1)

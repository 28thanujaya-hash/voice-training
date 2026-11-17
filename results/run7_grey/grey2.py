import pandas as pd, numpy as np
d=pd.read_csv("/home/claude/grey_065.csv")
M=["low","tense","bright"]
for Q in (0.80,0.90):
    edge={m:d[d.row=="normal"]["p_"+m].quantile(Q) for m in M}
    def keep(r):
        if r.row=="normal": return all(r["p_"+m]<edge[m] for m in M)
        return r["p_"+r.row]>=edge[r.row]
    d["keep"]=d.apply(keep,axis=1)
    print(f"\n== normal circle edge = its {int(Q*100)}th percentile toward each mood: "+", ".join(f"{m} p={edge[m]:.2f}" for m in M))
    for m in ["normal","bright","low","tense"]:
        s=d[d.row==m]; L=s.groupby("id").keep.any()
        tr=s[s.split=="train"]; va=s[s.split!="train"]
        print(f"{m:7s} clips kept {s.keep.sum():4d}/{len(s):4d}  lines {L.sum():3d}/{len(L):3d}  (train {tr.groupby('id').keep.any().sum()}/{tr.id.nunique()}, other {va.groupby('id').keep.any().sum()}/{va.id.nunique()})")
    d.to_csv(f"/home/claude/grey_q{int(Q*100)}.csv",index=False)
# what do kept low clips look like vs normal kept, and vs dropped low
d=pd.read_csv("/home/claude/grey_q90.csv")
K=["syl_s","artic","pause_share","f0_med","f0_sd","lufs","cpp","h1h2","final_drop"]
print("\nmedians (q90 edge)")
t=pd.concat({"normal kept":d[(d.row=="normal")&d.keep][K].median(),"low kept":d[(d.row=="low")&d.keep][K].median(),"low dropped":d[(d.row=="low")&~d.keep][K].median()},axis=1)
print(t.round(2).to_string())

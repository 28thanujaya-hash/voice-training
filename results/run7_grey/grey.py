import pandas as pd, numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_predict
d=pd.read_csv("spoken-english/results/run5_measure/measures.csv")
K=["syl_s","artic","pauses","pause_share","f0_med","f0_sd","f0_rng","slope","final_slope","final_drop","lufs","int_sd","int_drop","cpp","hnr","h1h2","tilt"]
d["g"]=d.group.fillna(d.id)
P={}
for m in ["low","tense","bright"]:
    s=d[d.row.isin(["normal",m])]
    X=s[K].replace([np.inf,-np.inf],np.nan).values
    p=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=3000,C=0.5))
    pr=cross_val_predict(p,X,s.row==m,groups=s.g,cv=GroupKFold(5),method="predict_proba")[:,1]
    P[m]=pd.Series(pr,index=s.index)
    # fit on all to see which cues matter
    p.fit(np.nan_to_num(X,nan=np.nanmedian(X)),s.row==m)
    c=pd.Series(p[-1].coef_[0],index=K).sort_values(key=abs,ascending=False)
    print(m,"top cues:",", ".join(f"{k}{v:+.2f}" for k,v in c.head(6).items()))
for m in P: d["p_"+m]=P[m]
import sys
for HI in (0.65,0.70):
    LO=1-HI
    keep=[]
    for i,r in d.iterrows():
        if r.row=="normal": k=all((pd.isna(r["p_"+m]) or r["p_"+m]<=LO) for m in P)
        else: k=r["p_"+r.row]>=HI
        keep.append(k)
    d["keep"]=keep
    print(f"\n== grey zone = {LO:.2f}..{HI:.2f}")
    for m in ["normal","bright","low","tense"]:
        s=d[d.row==m]; L=s.groupby("id").keep.any()
        print(f"{m:7s} clips kept {s.keep.sum():4d}/{len(s):4d}   lines with >=1 clip {L.sum():3d}/{len(L):3d}   by split: "+
              ", ".join(f"{sp} {s[s.split==sp].groupby('id').keep.any().sum()}/{s[s.split==sp].id.nunique()}" for sp in sorted(s.split.dropna().unique())))
    if HI==0.65: d.to_csv("/home/claude/grey_065.csv",index=False)

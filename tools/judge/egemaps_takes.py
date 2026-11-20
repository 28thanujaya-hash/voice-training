import csv,os,sys,opensmile,librosa,numpy as np,pandas as pd
from concurrent.futures import ProcessPoolExecutor
J=pd.read_csv('results/judge/tara_judged.csv')
J=J[J.run.str.match(r'full_(bright|tense)')]
def go(row):
    run,take=row
    f=f'results/{run}/takes/{take}.mp3'
    if not os.path.exists(f): return None
    sm=opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02,feature_level=opensmile.FeatureLevel.Functionals)
    y,sr=librosa.load(f,sr=16000); y=librosa.effects.trim(y,top_db=35)[0]
    d=sm.process_signal(y,sr).iloc[0].to_dict(); d['take']=take; d['dur']=len(y)/sr; return d
with ProcessPoolExecutor(os.cpu_count()) as ex: out=[o for o in ex.map(go,zip(J['run'],J['take']),chunksize=8) if o]
pd.DataFrame(out).to_csv('/tmp/egemaps_bt.csv',index=False); print(len(out))

# Jejak kertas M166 V1 (Titik Pusing Momentum) — HANYA rekod isyarat; tiada belian, tiada kesan pada Papertrade C.
# Jalan: python3 WFO/kaedah_baru/jejak_M166.py [--stor folder] [--hingga YYYYMMDD]
# Sumber: stor harga repo BacktestShariah2/data/harga/stor (harga_A.csv = 431 saham, harga_idx.csv). Jangan commit stor.
# Output: BacktestShariah2/uji_kertas/jejak_M166.csv (tambah baris; tarikh sama diganti). Tempoh jejak hingga 15 Jan 2027.
import sys, os, argparse
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import numpy as np, pandas as pd
import _rangka_r as R
from stor import muat, frames_dict
ap=argparse.ArgumentParser(); ap.add_argument('--stor',default=os.path.join(REPO,'BacktestShariah2','data','harga','stor'))
ap.add_argument('--hingga',default=None); ap.add_argument('--keluar',default=os.path.join(REPO,'BacktestShariah2','uji_kertas','jejak_M166.csv'))
a=ap.parse_args()
fr_all,idx=frames_dict(muat(a.stor))
A=muat(a.stor)['harga_A.csv']; fr={t:g for t,g in fr_all.items() if t in set(A.ticker)}
if a.hingga:
    h=pd.Timestamp(a.hingga); fr={t:g[g.index<=h] for t,g in fr.items()}; idx={t:g[g.index<=h] for t,g in idx.items()}
fr={t:g for t,g in fr.items() if len(g)}
spy=idx['SPY'].close

def keadaan(c):
    S=c/c.shift(252)-1; F=c/c.shift(21)-1; k=pd.Series(np.nan,c.index,dtype=object); ok=S.notna()&F.notna()
    k[ok&(S>0)&(F>0)]='Bull'; k[ok&(S>0)&(F<=0)]='Correction'; k[ok&(S<=0)&(F<=0)]='Bear'; k[ok&(S<=0)&(F>0)]='Rebound'
    return k
kd=keadaan(spy)
RS12={t:R.rs12(g,idx) for t,g in fr.items()}
RS1={}
for t,g in fr.items():
    rsl=g.close/R.spy_pada(g,idx); RS1[t]=rsl/rsl.shift(21)-1
P12=R.pct(RS12); P1=R.pct(RS1)
rb=(kd.reindex(P12.index,method='ffill')=='Rebound').values[:,None]
PK=pd.DataFrame(np.where(rb,P1.values,P12.values),index=P12.index,columns=P12.columns)
K={};sah={}
for t,g in fr.items():
    k=kd.reindex(g.index,method='ffill'); reb=(k=='Rebound')
    K[t]=RS12[t].reindex(g.index).where(~reb,RS1[t].reindex(g.index)); sah[t]=k.notna()&(k!='Bear')
R.pasang(fr,idx,K,0.90,False,PK,sah)   # Rangka R tanpa SMA200, kolam 10% ikut keadaan (tandai_keluar dilangkau dalam penggunaan ini: hanya sig)
tarikh=max(g.index[-1] for g in fr.values()); k=kd.reindex([tarikh],method='ffill').iloc[0]
rows=[dict(tarikh=tarikh.date(),keadaan=k,saham=t,kunci='RS1' if k=='Rebound' else 'RS12',nilai_kunci=round(float(g['rank'].iloc[-1]),4),
           tutup=round(float(g.close.iloc[-1]),4),henti_0_88=round(float(g.close.iloc[-1])*0.88,4)) for t,g in fr.items() if g.index[-1]==tarikh and bool(g.sig.iloc[-1])]
D=pd.DataFrame(rows,columns=['tarikh','keadaan','saham','kunci','nilai_kunci','tutup','henti_0_88']).sort_values('nilai_kunci',ascending=False)
D['kedudukan']=range(1,len(D)+1)
old=pd.read_csv(a.keluar) if os.path.exists(a.keluar) else pd.DataFrame(columns=D.columns)
old=old[old.tarikh.astype(str)!=str(tarikh.date())]
pd.concat([old,D]).to_csv(a.keluar,index=False)
print('tarikh',tarikh.date(),'keadaan',k,'isyarat',len(D),'saham',len(fr)); print(D.head(8).to_string(index=False))

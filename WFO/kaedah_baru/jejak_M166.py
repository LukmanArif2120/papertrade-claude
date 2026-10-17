# Jejak kertas M166 V1 (Titik Pusing Momentum) — HANYA rekod isyarat; tiada belian, tiada kesan pada Papertrade C.
# Jalan: python3 WFO/kaedah_baru/jejak_M166.py   Output: BacktestShariah2/uji_kertas/jejak_M166.csv (tambah baris; tarikh sama diganti).
# Sumber data: data_mentah/ (sama seperti backtest). Tempoh jejak: hingga 15 Jan 2027.
import sys, os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.argv=[sys.argv[0],os.devnull]
sys.path[:0]=[os.path.join(REPO,'WFO','kaedah_baru')]
import step2_M166 as M
from step2_M166 import *
ctx=M.sediakan(M.fr); M.pasang_kunci(M.fr,ctx['SPY'],'V1')
kead=M.keadaan(M.spy); tarikh=max(g.index[-1] for g in M.fr.values()); k=kead.reindex([tarikh],method='ffill').iloc[0]
rows=[]
for t,g in M.fr.items():
    if g.index[-1]==tarikh and bool(g.sig.iloc[-1]):
        rows.append(dict(tarikh=tarikh.date(),keadaan=k,saham=t,kunci='RS1' if k=='Rebound' else 'RS12',nilai_kunci=round(float(g['rank'].iloc[-1]),4),tutup=round(float(g.close.iloc[-1]),4),henti_0_88=round(float(g.close.iloc[-1])*0.88,4)))
D=pd.DataFrame(rows,columns=['tarikh','keadaan','saham','kunci','nilai_kunci','tutup','henti_0_88']).sort_values('nilai_kunci',ascending=False)
D['kedudukan']=range(1,len(D)+1)
f=os.path.join(REPO,'BacktestShariah2','uji_kertas','jejak_M166.csv')
old=pd.read_csv(f) if os.path.exists(f) else pd.DataFrame(columns=D.columns)
old=old[old.tarikh.astype(str)!=str(tarikh.date())]
pd.concat([old,D]).to_csv(f,index=False)
print('tarikh',tarikh.date(),'keadaan',k,'isyarat',len(D)); print(D.head(8).to_string(index=False))

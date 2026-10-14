# TAMBAHAN SHARIAH v1.0 — lapisan atas enjin v1.2; TIDAK mengubah trades/portfolio/metrik/gate/skor
from enjin import *
SETS=['S1','S2','S3','S4']; HARI=[5,10,15,20,30,40,60]
def muat():
    fr={}; asal={}
    for s in SETS:
        d=pd.read_csv(cari(f'dataset_{s}.csv')); d['date']=pd.to_datetime(d.date.astype(str))
        for t,g in d.groupby('ticker'): fr[t]=g.sort_values('date').set_index('date').copy(); asal[t]=s
    ix=pd.read_csv(cari('index_benchmark.csv')); ix['date']=pd.to_datetime(ix.date.astype(str))
    idx={t:g.sort_values('date').set_index('date').copy() for t,g in ix.groupby('ticker')}
    return fr, idx, asal
def subset(fr,asal,s): return fr if s=='431' else {t:g for t,g in fr.items() if asal[t]==s}
def tambah(T,cv,fr,B):
    T=T[T.ent>=pd.Timestamp(START)]; bl=cv.resample('ME').last().pct_change().dropna()
    x={'ew_cagr':round(B['Sama rata 100']['cagr'],4),'bulan_untung':round((bl>0).mean(),4),'bulan10':round((bl>=0.10).mean(),4)}
    R={k:[] for k in HARI}
    for r in T.itertuples():
        g=fr[r.ticker]; i=g.index.get_loc(r.ent); e=g.open.values[i]; c=g.close.values
        for k in HARI:
            if i+k-1<len(c): R[k].append(c[i+k-1]/e-1)
    x['pegang']='|'.join(f'{k}:{np.mean(v)*100:.1f}' for k,v in R.items() if v)
    return x
LAJUR2=['set']+LAJUR+['ew_cagr','menang_ew','bulan_untung','bulan10','pegang']
def baris2(set_,id_,kaedah,varian,T,cv,frs,idx,ada_henti,catatan=''):
    B=penanda(idx,frs); m=metrik(T,cv,B,ada_henti=ada_henti); r=baris(id_,kaedah,varian,m,B,catatan)
    r.update(tambah(T,cv,frs,B)); r['set']=set_; r['menang_ew']=bool(m['cagr']>B['Sama rata 100']['cagr']); return r

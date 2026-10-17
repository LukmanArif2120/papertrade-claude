# L02B — ujian semula L02 V2 (rank = p, tanpa penapis) dengan kriteria pra-daftar (WFO/laporan/L02B_V2_rank.md).
# Jalan: python3 WFO/kaedah_baru/step2_L02B.py [folder_keluar]. Perlu WFO/data/hasil/L02_isyarat.csv.gz (p_V2 larian L02).
import sys, os, time
sys.argv=[sys.argv[0]]+sys.argv[1:]
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import step2_L02 as L
from step2_L02 import *
t0=time.time()
BAHARU=['M74','M05','M80','M12','M46','M40']; ASAL=list(L.KAEDAH)
tarikh=L.C.index; suku=pd.date_range(L.OOS,tarikh[-1],freq='QS')

def jalan(frk, pas, semula, tm, wm, pmap, sets):
    """pmap: dict (tarikh,ticker)->p atau None (asas). Pulangkan {set: (cagr, mdd, n)} luar sampel."""
    pas()
    for t,g in frk.items():
        s=g.sig.fillna(False).astype(bool)&(g.index>=L.OOS); g['sig']=s
        if pmap is not None:
            g['rank']=[pmap.get((d,t),-1e9) if v else -1e9 for d,v in zip(g.index,s.values)]
    semula(); out={}
    for st in sets:
        f=subset(frk,asal,st); T=trades(f,tmax=tm,warm=wm); cv=portfolio(T,f); c=cv[cv.index>=L.OOS]; T=T[T.ent>=L.OOS]
        out[st]=(enjin._cagr(c),enjin._mdd(c),len(T))
    return out

rows=[]
# ---------- Ujian A: 6 kaedah baharu, model baharu
L.KAEDAH=BAHARU
DATA={}
for k in BAHARU:
    frk={t:g[['open','high','low','close','volume','turnover']].copy() for t,g in L.fr.items()}
    nm,tm,wm,pas,semula=L.sediakan(k,frk); pas()
    T=trades(frk,tmax=tm,warm=wm); T['y']=L.label_tiga(frk,T); T['X']=list(L.ciri(T.sig.values,T.ticker.values,k))
    S=pd.DataFrame([(d,t) for t,g in frk.items() for d in g.index[g.sig.fillna(False).astype(bool).values&(g.index>=L.OOS)]],columns=['tarikh','ticker'])
    S['X']=list(L.ciri(S.tarikh.values,S.ticker.values,k)) if len(S) else []
    DATA[k]=dict(nm=nm,tm=tm,wm=wm,pas=pas,semula=semula,frk=frk,T=T,S=S,p=np.full(len(S),np.nan))
    print(k,nm,'dagangan',len(T),'y',round(T.y.mean(),3),'isyarat OOS',len(S),round(time.time()-t0),'s',flush=True)
TA=pd.concat([d['T'] for d in DATA.values()],ignore_index=True)
for qi,qs in enumerate(suku):
    qe=suku[qi+1] if qi+1<len(suku) else tarikh[-1]+pd.Timedelta(days=1)
    had=tarikh[max(0,tarikh.searchsorted(qs)-25)]; tr=TA[TA.ent<had]
    X=np.vstack(tr.X.values).astype(float); mu=np.nanmean(X,0); sd=np.nanstd(X,0); sd[sd==0]=1
    f=L.logit(np.nan_to_num((X-mu)/sd),tr.y.values)
    for k,d in DATA.items():
        S=d['S']
        if not len(S): continue
        m=((S.tarikh>=qs)&(S.tarikh<qe)).values
        if m.any(): d['p'][m]=f(np.nan_to_num((np.vstack(S.X.values[m]).astype(float)-mu)/sd))
for k,d in DATA.items():
    pm={(a,b):p for a,b,p in zip(d['S'].tarikh,d['S'].ticker,d['p'])}
    a=jalan(d['frk'],d['pas'],d['semula'],d['tm'],d['wm'],None,['431'])['431']
    v=jalan(d['frk'],d['pas'],d['semula'],d['tm'],d['wm'],pm,['431'])['431']
    rows.append(dict(ujian='A',kaedah=k,varian=d['nm'],set='431',cagr_asas=a[0],cagr_v2=v[0],mdd_asas=a[1],mdd_v2=v[1],n_asas=a[2],n_v2=v[2]))
    print('A',k,[round(x,4) for x in a],[round(x,4) for x in v],flush=True)
# ---------- Ujian B: 6 kaedah asal, subset S1–S4, p daripada L02
L.KAEDAH=ASAL
I=pd.read_csv(os.path.join(L.REPO,'WFO','data','hasil','L02_isyarat.csv.gz'),parse_dates=['tarikh'])
for k in ASAL:
    frk={t:g[['open','high','low','close','volume','turnover']].copy() for t,g in L.fr.items()}
    nm,tm,wm,pas,semula=L.sediakan(k,frk); x=I[I.kaedah==k]
    pm={(a,b):p for a,b,p in zip(x.tarikh,x.ticker,x.p_V2)}
    a=jalan(frk,pas,semula,tm,wm,None,SETS); v=jalan(frk,pas,semula,tm,wm,pm,SETS)
    for s in SETS:
        rows.append(dict(ujian='B',kaedah=k,varian=nm,set=s,cagr_asas=a[s][0],cagr_v2=v[s][0],mdd_asas=a[s][1],mdd_v2=v[s][1],n_asas=a[s][2],n_v2=v[s][2]))
    print('B',k,{s:(round(a[s][0],3),round(v[s][0],3)) for s in SETS},round(time.time()-t0),'s',flush=True)
R=pd.DataFrame(rows); R.to_csv(os.path.join(KELUAR,'L02B_ringkasan.csv'),index=False)
A_=R[R.ujian=='A']; okA=int((A_.cagr_v2>=A_.cagr_asas).sum()); medA=float((A_.cagr_v2-A_.cagr_asas).median())
B_=R[R.ujian=='B']; okB=int((B_.assign(l=B_.cagr_v2>=B_.cagr_asas).groupby('kaedah').l.sum()>=3).sum())
print('A',okA,'/6 median',round(medA*100,2),'| B',okB,'/6 | LULUS' if okA>=4 and medA>0 and okB>=4 else '| DITOLAK')
print('siap',round(time.time()-t0),'s')

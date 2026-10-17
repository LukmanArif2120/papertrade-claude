# STEP-2 L02 — Meta-label (López de Prado) atas 6 kaedah; enjin v1.2 beku. Jalan: python3 WFO/kaedah_baru/step2_L02.py [folder_keluar]
# Spec: SPEC_SEMUA_KAEDAH.md (`FAIL ASAL: spec/L02`). Output: L02_ringkasan.csv, L02_isyarat.csv.gz (folder_keluar; salin ke WFO/data/hasil/).
# Luar sampel 1 Jan 2023 – hujung data (16 suku); latih semula awal setiap suku guna isyarat masuk < awal suku − 25 hari dagangan.
import sys, os, importlib, time, math, pickle
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)
import _rangka_r as R
import enjin
from statistics import NormalDist
fr,idx,asal=muat(); t0=time.time()
OOS=pd.Timestamp('2023-01-01')
KAEDAH=['M96','M30','M79','M111','M114','M81']
spy=idx['SPY'].close

# ---------------- ciri (tutup hari i; tiada pandang ke hadapan)
def panel(f): return pd.DataFrame({t:f(g) for t,g in fr.items()}).sort_index()
C=panel(lambda g:g.close)
RS12={t:R.rs12(g,idx) for t,g in fr.items()}
def _rs1(g):
    rsl=g.close/R.spy_pada(g,idx); return rsl/rsl.shift(21)-1
CIRI={'pct_rs12':R.pct(RS12),'pct_rs1':R.pct({t:_rs1(g) for t,g in fr.items()}),
      'atr_c':panel(lambda g:enjin.atr(g)/g.close),'c_sma50':panel(lambda g:g.close/g.close.rolling(50).mean()-1),
      'c_sma200':panel(lambda g:g.close/g.close.rolling(200).mean()-1),'c_maks252':panel(lambda g:g.close/g.close.rolling(252).max()-1),
      'vol20_252':panel(lambda g:g.volume.rolling(20).mean()/g.volume.rolling(252).mean())}
sp=spy.reindex(C.index,method='ffill')
PASAR={'spy_ret252':sp/sp.shift(252)-1,'spy_sma200':sp/sp.rolling(200).mean()-1,'spy_vol21':sp.pct_change().rolling(21).std()*np.sqrt(252)}
# PCT_ind(IR6) seperti M165 (0.5 jika industri < 3 ahli sah)
PI=pd.read_csv(os.path.join(REPO,'BacktestShariah2/papertrade/peta_industri.csv')).set_index('ticker').industri
RET6=(C/C.shift(126)-1); IR={}
for k,ahli in PI[PI.index.isin(list(fr))].groupby(PI).groups.items():
    a=RET6[list(ahli)]; IR[k]=a.mean(axis=1).where(a.notna().sum(axis=1)>=3)
PIND=pd.DataFrame(IR).rank(axis=1,pct=True)
CIRI['pct_ind']=pd.DataFrame({t:(PIND[PI[t]] if t in PI.index and PI[t] in PIND else pd.Series(np.nan,C.index)) for t in C.columns}).fillna(0.5)
NAMA_CIRI=list(CIRI)+list(PASAR)+[f'id_{k}' for k in KAEDAH]
print('ciri siap',round(time.time()-t0),'s',flush=True)

def ciri(tarikh, tick, kaedah):
    """tarikh, tick: array sama panjang -> matriks ciri."""
    ri=C.index.get_indexer(pd.DatetimeIndex(tarikh)); ci=C.columns.get_indexer(tick)
    X=[CIRI[k].values[ri,ci] for k in CIRI]+[PASAR[k].values[ri] for k in PASAR]+[np.full(len(ri),1.0 if kaedah==k else 0.0) for k in KAEDAH]
    return np.column_stack(X)

# ---------------- isyarat kaedah
def sediakan(k, frk):
    if k=='M114':
        F={t:R.rs12(g,idx) for t,g in frk.items()}; P=R.pct(F)
        def pas(): R.pasang(frk,idx,F,0.90,True,P)
        def semula():
            for g in frk.values(): R.tandai_keluar(g)
        return 'V4 Kolam 10%',None,200,pas,semula
    m=importlib.import_module(f'kaedah.{k}')
    def pas(): m.sedia(frk,idx)
    def semula():
        if k=='M81':
            for g in frk.values(): g['exitc']=m._exit_ekor(g,g.sig.astype(bool).values,m._rma_atr(g,20).values,m.WARM)
    return m.VARIAN,m.TMAX,m.WARM,pas,semula

def label_tiga(frk, T):
    """y=1 jika high >= buka_masuk x1.10 dalam <=20 hari dagangan dari masuk SEBELUM low <= henti kaedah (henti pada hari isyarat);
       kedua-dua pada hari sama -> 0."""
    y=np.zeros(len(T),int)
    for n,r in enumerate(T.itertuples()):
        g=frk[r.ticker]; i=g.index.get_loc(r.sig); e=g.open.values[i+1]; sp=float(g['stop'].values[i])
        if np.isnan(sp): sp=-np.inf
        hi=g.high.values[i+1:i+21]; lo=g.low.values[i+1:i+21]
        for a,b in zip(hi,lo):
            if b<=sp: break
            if a>=e*1.10: y[n]=1; break
    return y

# ---------------- model
def logit(X,y,lam=1.0,it=50):
    w=np.zeros(X.shape[1]); b=0.0
    for _ in range(it):                       # Newton (IRLS); L2 pada w sahaja
        z=X@w+b; p=1/(1+np.exp(-np.clip(z,-30,30))); W=p*(1-p)
        gw=X.T@(p-y)+lam*w; gb=(p-y).sum()
        H=X.T@(X*W[:,None])+lam*np.eye(X.shape[1]); hb=W.sum(); hwb=X.T@W
        M=np.block([[H,hwb[:,None]],[hwb[None,:],np.array([[hb]])]]); d=np.linalg.solve(M,np.r_[gw,gb])
        w-=d[:-1]; b-=d[-1]
        if np.abs(d).max()<1e-8: break
    return lambda Z:1/(1+np.exp(-np.clip(Z@w+b,-30,30)))
def hgb(X,y):
    from sklearn.ensemble import HistGradientBoostingClassifier
    m=HistGradientBoostingClassifier(random_state=0).fit(X,y); return lambda Z:m.predict_proba(Z)[:,1]

if __name__=='__main__':
    tarikh=C.index; td=lambda d:tarikh[tarikh.searchsorted(d)]
    suku=pd.date_range(OOS,tarikh[-1],freq='QS')
    # 1. semua isyarat (trades sebelum had slot) setiap kaedah + label + ciri
    DATA={}; SIG={}
    for k in KAEDAH:
        frk={t:g[['open','high','low','close','volume','turnover']].copy() for t,g in fr.items()}
        nm,tm,wm,pas,semula=sediakan(k,frk); pas()
        T=trades(frk,tmax=tm,warm=wm); T['y']=label_tiga(frk,T); T['y4']=(T.ret>=0.10).astype(int)
        T['X']=list(ciri(T.sig.values,T.ticker.values,k)); T['kaedah']=k
        # semua hari isyarat luar sampel (untuk penapis sig sebenar)
        rows=[(d,t) for t,g in frk.items() for d in g.index[g.sig.fillna(False).astype(bool).values & (g.index>=OOS)]]
        S=pd.DataFrame(rows,columns=['tarikh','ticker']); S['X']=list(ciri(S.tarikh.values,S.ticker.values,k)) if len(S) else []
        DATA[k]=(nm,tm,wm,T); SIG[k]=(S,frk,pas,semula)
        print(k,nm,'dagangan',len(T),'y',round(T.y.mean(),3),'isyarat OOS',len(S),round(time.time()-t0),'s',flush=True)
    TA=pd.concat([d[3] for d in DATA.values()],ignore_index=True)
    # 2. latih berjalan ke hadapan: p bagi setiap hari isyarat OOS
    MODEL={'V1':('y',logit),'V2':('y',logit),'V3':('y',hgb),'V4':('y4',logit)}
    P={v:{k:np.full(len(SIG[k][0]),np.nan) for k in KAEDAH} for v in MODEL}; AMB={v:{} for v in MODEL}
    for qi,qs in enumerate(suku):
        qe=suku[qi+1] if qi+1<len(suku) else tarikh[-1]+pd.Timedelta(days=1)
        had=tarikh[max(0,tarikh.searchsorted(qs)-25)]
        tr=TA[TA.ent<had]; X=np.vstack(tr.X.values).astype(float)
        mu=np.nanmean(X,0); sd=np.nanstd(X,0); sd[sd==0]=1; Xs=np.nan_to_num((X-mu)/sd)
        for v,(lab,fn) in MODEL.items():
            if v=='V2': continue
            f=fn(Xs,tr[lab].values); pt=f(Xs); thr=float(np.median(pt)); AMB[v][str(qs.date())]=(thr,len(tr),float(tr[lab].mean()))
            for k in KAEDAH:
                S=SIG[k][0]
                if not len(S): continue
                m=((S.tarikh>=qs)&(S.tarikh<qe)).values
                if m.any():
                    Z=np.nan_to_num((np.vstack(S.X.values[m]).astype(float)-mu)/sd); P[v][k][m]=f(Z)
                    if v=='V1': P['V2'][k][m]=P[v][k][m]
        for k in KAEDAH: pass
        print('suku',qs.date(),'latih',len(tr),'ambang V1',round(AMB['V1'][str(qs.date())][0],3),flush=True)
    # 3. portfolio luar sampel: asas lawan V1–V4
    def jalan(k,v):
        S,frk,pas,semula=SIG[k]; nm,tm,wm,_=DATA[k]; pas()
        key={(d,t):i for i,(d,t) in enumerate(zip(S.tarikh,S.ticker))}
        for t,g in frk.items():
            s=g.sig.fillna(False).astype(bool)&(g.index>=OOS); g['sig']=s
            if v is None: continue
            pp=np.array([P[v][k][key[(d,t)]] if (d,t) in key else np.nan for d in g.index]) if s.any() else np.full(len(g),np.nan)
            if v=='V2': g['rank']=np.where(np.isnan(pp),-1e9,pp)
            else:
                thr=np.array([AMB[v][str(suku[max(0,suku.searchsorted(d,side='right')-1)].date())][0] if d>=OOS else np.nan for d in g.index]) if s.any() else np.full(len(g),np.nan)
                g['sig']=s&(pp>=thr)
        semula()
        T=trades(frk,tmax=tm,warm=wm); cv=portfolio(T,frk); T=T[T.ent>=OOS]; c=cv[cv.index>=OOS]
        r=c.pct_change().dropna()
        return dict(kaedah=k,varian='asas' if v is None else v,n=len(T),hit10=float((T.mfe>=0.10).mean()) if len(T) else np.nan,
                    win=float((T.ret>0).mean()) if len(T) else np.nan,avg=float(T.ret.mean()) if len(T) else np.nan,
                    cagr=enjin._cagr(c),mdd=enjin._mdd(c),sr=float(r.mean()/r.std()) if r.std()>0 else np.nan,
                    sk=float(r.skew()),ku=float(r.kurt()+3),nhari=len(r)),c
    rows=[]; KV={}
    for k in KAEDAH:
        for v in [None,'V1','V2','V3','V4']:
            d,c=jalan(k,v); rows.append(d); KV[(k,d['varian'])]=c
            print(k,d['varian'],d['n'],round(d['hit10'],3),round(d['cagr'],4),round(d['mdd'],4),flush=True)
    Rg=pd.DataFrame(rows)
    # DSR (cara W01) atas 24 percubaan berpenapis
    N=NormalDist(); tr=Rg[Rg.varian!='asas']; srs=tr.sr.dropna().values; nk=len(srs); g_=0.5772156649
    sr0=math.sqrt(np.var(srs))*((1-g_)*N.inv_cdf(1-1/nk)+g_*N.inv_cdf(1-1/(nk*math.e)))
    Rg['dsr']=[N.cdf((r.sr-sr0)*math.sqrt(r.nhari-1)/math.sqrt(max(1e-12,1-r.sk*r.sr+(r.ku-1)/4*r.sr**2))) if r.varian!='asas' and not np.isnan(r.sr) else np.nan for r in Rg.itertuples()]
    Rg['sr0_tahunan']=sr0*math.sqrt(252)
    # ketepatan label pada isyarat yang menjadi dagangan (asas OOS)
    Rg.to_csv(os.path.join(KELUAR,'L02_ringkasan.csv'),index=False)
    pickle.dump(dict(AMB=AMB,KV=KV,P={v:{k:list(P[v][k]) for k in KAEDAH} for v in P}),open(os.path.join(KELUAR,'l02.pkl'),'wb'))
    # isyarat OOS + p
    out=[]
    for k in KAEDAH:
        S=SIG[k][0][['tarikh','ticker']].copy(); S['kaedah']=k
        for v in MODEL: S['p_'+v]=P[v][k]
        out.append(S)
    pd.concat(out).to_csv(os.path.join(KELUAR,'L02_isyarat.csv.gz'),index=False,float_format='%.4f')
    # latihan: kadar label
    TA[['kaedah','ticker','sig','ent','ret','mfe','y','y4']].to_csv(os.path.join(KELUAR,'L02_label.csv.gz'),index=False,float_format='%.4f')
    print('siap',round(time.time()-t0),'s')

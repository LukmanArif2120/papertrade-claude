# ENJIN BACKTEST STANDARD v1.2 — jangan ubah logik teras
import pandas as pd, numpy as np, glob
COST=0.001; START='2019-11-01'; H1_END='2022-12-31'; ENJIN='v1.2'

def cari(nama):
    for pat in [f'/root/.claude/uploads/**/*{nama}', f'/mnt/user-data/uploads/**/*{nama}', f'/mnt/project/{nama}', f'/home/claude/**/{nama}']:
        f=glob.glob(pat,recursive=True)
        if f: return sorted(f)[-1]
    raise FileNotFoundError(nama+' tiada — minta pengguna muat naik ke Project Files')

def rsi(c,n=14):
    dl=c.diff(); au=dl.clip(lower=0).ewm(alpha=1/n,adjust=False).mean()
    ad=(-dl.clip(upper=0)).ewm(alpha=1/n,adjust=False).mean(); return 100-100/(1+au/ad)
def atr(g,n=14):
    c=g.close; tr=pd.concat([g.high-g.low,(g.high-c.shift()).abs(),(g.low-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def siap(g):
    for k,v in [('sig',False),('stop',np.nan),('tgt',np.nan),('exitc',False),('rank',0.0)]:
        if k not in g: g[k]=v
    return g

def trades(fr, tmax=None, warm=200):
    out=[]
    for t,g in fr.items():
        g=siap(g); o,h,l,c=g.open.values,g.high.values,g.low.values,g.close.values
        sig=g.sig.fillna(False).astype(bool).values; st=g.stop.astype(float).values; tg=g.tgt.astype(float).values
        ex=g.exitc.fillna(False).astype(bool).values; rk=g['rank'].astype(float).values; ix=g.index; n=len(g); i=warm
        while i<n-1:
            if not sig[i]: i+=1; continue
            e=o[i+1]; sp=st[i] if not np.isnan(st[i]) else -np.inf
            j=i+1; x=None; why='hujung'
            while j<n:
                tgt=tg[j-1] if j>i+1 else np.nan
                if j>i+1 and o[j]<=sp: x,why=o[j],'henti'; break
                if l[j]<=sp: x,why=sp,'henti'; break
                if not np.isnan(tgt):
                    if j>i+1 and o[j]>=tgt: x,why=o[j],'sasaran'; break
                    if h[j]>=tgt: x,why=tgt,'sasaran'; break
                if ex[j] and j+1<n: j+=1; x,why=o[j],'isyarat keluar'; break
                if tmax and (j-i)>=tmax: x,why=c[j],'masa'; break
                j+=1
            if x is None: j=n-1; x=c[j]
            out.append(dict(ticker=t,sig=ix[i],ent=ix[i+1],ex=ix[j],ret=x/e*(1-COST)/(1+COST)-1,days=j-i,
                            why=why,rank=rk[i],mfe=h[i+1:j+1].max()/e-1))
            i=j+1
    return pd.DataFrame(out)

def portfolio(T, fr, slots=8, w=0.125):
    dates=sorted(set().union(*[g.index for g in fr.values()])); dates=[x for x in dates if x>=pd.Timestamp(START)]
    T=T[T.ent>=pd.Timestamp(START)].sort_values(['ent','rank'],ascending=[True,False])
    byent={k:v for k,v in T.groupby('ent')}; cl={t:g.close for t,g in fr.items()}
    eq=cash=1.0; pos=[]; curve=[]
    for dt in dates:
        keep=[]
        for p in pos:
            if p['ex']==dt: cash+=p['a']*(1+p['ret'])
            else: keep.append(p)
        pos=keep
        if dt in byent:
            for _,r in byent[dt].iterrows():
                if len(pos)>=slots: break
                if any(p['t']==r.ticker for p in pos): continue
                a=min(cash,eq*w)
                if a<=0: break
                cash-=a; pos.append(dict(t=r.ticker,ex=r.ex,ret=r.ret,a=a,ent=dt))
        keep=[]
        for p in pos:                      # v1.2: tutup posisi yang keluar pada hari masuk
            if p['ex']==dt and p['ent']==dt: cash+=p['a']*(1+p['ret'])
            else: keep.append(p)
        pos=keep
        mv=sum(p['a']*cl[p['t']].asof(dt)/cl[p['t']].asof(p['ent']) if p['ent']!=dt else p['a'] for p in pos)
        eq=cash+mv; curve.append((dt,eq))
    return pd.Series(dict(curve))

def _cagr(s):
    y=(s.index[-1]-s.index[0]).days/365.25; return (s.iloc[-1]/s.iloc[0])**(1/y)-1
def _mdd(s): return (s/s.cummax()-1).min()

def penanda(idx, fr):
    out={}
    ew=pd.concat([g.close[g.index>=START]/g.close[g.index>=START].iloc[0] for g in fr.values()],axis=1).ffill().mean(axis=1)
    for k,s in [('QQQ',idx['QQQ'].close),('SPY',idx['SPY'].close),('Sama rata 100',ew)]:
        s=s[s.index>=START]
        out[k]=dict(cagr=_cagr(s),mdd=_mdd(s),h1=_cagr(s[:H1_END]),h2=_cagr(s[H1_END:]),
                    tahunan=s.resample('YE').last().pct_change().dropna())
    return out

def metrik(T, cv, B, ada_henti, long_only=True, mekanikal=True):
    T=T[T.ent>=pd.Timestamp(START)]; w=T.ret>0
    yrs=(cv.index[-1]-cv.index[0]).days/365.25
    th=cv.resample('YE').last().pct_change().dropna(); sp=B['SPY']['tahunan']
    th=th[th.index.isin(sp.index)][:-1]  # tahun kalendar penuh sahaja
    m=dict(n=len(T),dagangan_setahun=len(T)/yrs,win=w.mean(),avg=T.ret.mean(),avgwin=T.ret[w].mean(),
           avgloss=T.ret[~w].mean(),pf=T.ret[w].sum()/-T.ret[~w].sum(),days=T.days.mean(),
           hit10=(T.mfe>=0.10).mean(),ret10=(T.ret>=0.10).mean(),
           cagr=_cagr(cv),mdd=_mdd(cv),h1=_cagr(cv[:H1_END]),h2=_cagr(cv[H1_END:]),
           thn_kalah_spy=(th>sp.reindex(th.index)).mean(),terburuk=T.ret.min(),
           ada_henti=ada_henti,long_only=long_only,mekanikal=mekanikal)
    m['mar']=m['cagr']/abs(m['mdd']) if m['mdd']<0 else np.nan
    return m

def gate(m,B):
    return {'G1':m['ada_henti'] and m['avgloss']>=-0.12,'G2':m['n']>=100,'G3':m['cagr']>B['SPY']['cagr'],
            'G4':m['mdd']>=-0.45,'G5':m['h1']>0 and m['h2']>0,'G6':m['long_only'] and m['mekanikal']}

def skor(m,B):
    c=lambda x:max(0.0,min(1.0,x)); spy,qqq=B['SPY']['cagr'],B['QQQ']['cagr']
    s={'S1':25*c((m['cagr']-spy)/((qqq+0.10)-spy)),'S2':20*c(m['mar']/1.5),'S3':15*c(m['thn_kalah_spy']),
       'S4':10*c(min(m['h1'],m['h2'])/max(m['h1'],m['h2'])) if max(m['h1'],m['h2'])>0 else 0.0,
       'S5':15*c(m['ret10']/0.40),'S6':(5 if 20<=m['dagangan_setahun']<=150 else 0)+(5 if 5<=m['days']<=60 else 0),
       'S7':5*c(m['avg']/0.05)}
    s['JUMLAH']=sum(s.values()); return s

def keputusan(m,B):
    g=gate(m,B)
    if not all(g.values()): return 'DITOLAK', g, None
    s=skor(m,B); q=B['QQQ']
    if s['JUMLAH']>=75 and m['h1']>q['h1'] and m['h2']>q['h2']: k='GUNA'
    elif s['JUMLAH']>=60: k='UJI KERTAS'
    else: k='SIMPAN'
    return k, g, s

LAJUR=['id','kaedah','varian','enjin','tarikh','keputusan','skor','cagr','mdd','mar','h1','h2','thn_kalah_spy',
       'n','dagangan_setahun','win','avg','avgwin','avgloss','pf','days','hit10','ret10','terburuk',
       'ada_henti','gate_gagal','catatan']
def baris(id_,kaedah,varian,m,B,catatan=''):
    k,g,s=keputusan(m,B)
    r={'id':id_,'kaedah':kaedah,'varian':varian,'enjin':ENJIN,'tarikh':pd.Timestamp.today().strftime('%Y-%m-%d'),
       'keputusan':k,'skor':round(s['JUMLAH'],1) if s else '','gate_gagal':' '.join(x for x,v in g.items() if not v),'catatan':catatan}
    for x in LAJUR:
        if x not in r: r[x]=round(m[x],4) if isinstance(m[x],float) else m[x]
    return r

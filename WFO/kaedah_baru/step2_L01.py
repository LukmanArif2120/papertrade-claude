# STEP-2 L01 — Penapis Rejim Crash (lapisan atas sig; enjin v1.2 beku). Jalan: python3 WFO/kaedah_baru/step2_L01.py [folder_keluar]
# Output: L01.csv (lajur LAJUR2) dan l01.pkl dalam folder_keluar. Disalin ke BacktestShariah2/data/lapisan/L01.csv (TIDAK masuk registry_M_gabung.csv).
import sys, os, importlib, time, pickle
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)
import _rangka_r as R
import enjin
fr,idx,asal=muat(); t0=time.time()
spy=idx['SPY'].close
# bendera (tutup hari i, tiada pandang ke hadapan)
vol63=spy.pct_change().rolling(63).std()*np.sqrt(252)
A=(spy/spy.shift(252)-1<0)&spy.shift(252).notna()
B=(spy/spy.shift(504)-1<0)&spy.shift(504).notna()
C=A&(vol63>vol63.expanding(min_periods=252).quantile(0.8))&vol63.notna()
BEND={'A':A,'B':B,'C':C}
print('hari bendera (dalam sampel):',{k:int(v[v.index>=START].sum()) for k,v in BEND.items()})

def tapis(fr_,bendera):
    if bendera is None: return
    for g in fr_.values():
        f=bendera.reindex(g.index,method='ffill').fillna(False).astype(bool)
        g['sig']=(g.sig.astype(bool)&~f)

KAEDAH=['M96','M30','M79','M111','M114','M166']
def sediakan(k,fr_):
    """Pulangkan (varian, tmax, warm, ada_henti, pasang(bendera))."""
    if k in ('M114','M166'):
        if k=='M114':
            F={t:R.rs12(g,idx) for t,g in fr_.items()}; P=R.pct(F); nm='V4 Kolam 10%'
            def pas(b):
                R.pasang(fr_,idx,F,0.90,True,P)
                if b is not None: tapis(fr_,b); [R.tandai_keluar(g) for g in fr_.values()]
        else:
            import step2_M166 as M6
            ctx=M6.sediakan(fr_); nm='V1 Dikunci (keadaan SPY, Bear dilarang)'
            def pas(b):
                M6.pasang_kunci(fr_,ctx['SPY'],'V1')
                if b is not None: tapis(fr_,b); [R.tandai_keluar(g) for g in fr_.values()]
        return nm,None,200,True,pas
    m=importlib.import_module(f'kaedah.{k}')
    def pas(b):
        m.sedia(fr_,idx)
        if b is not None: tapis(fr_,b)   # exitc modul tidak bergantung pada sig
    return m.VARIAN,m.TMAX,m.WARM,m.ADA_HENTI,pas

if __name__=='__main__':
    # step2_M166 dimuat melalui import: ia menjalankan muat() sendiri; elak dengan membekalkan fr/idx sudah ada
    rows=[]; ring={}
    for k in KAEDAH:
        frk={t:g[['open','high','low','close','volume','turnover']].copy() for t,g in fr.items()}
        nm,tm,wm,henti,pas=sediakan(k,frk)
        for b in [None,'A','B','C']:
            pas(None if b is None else BEND[b])
            vn=nm if b is None else f'{nm} + L01-{b}'
            for s in ['431']+SETS:
                f=subset(frk,asal,s); T=trades(f,tmax=tm,warm=wm); cv=portfolio(T,f)
                r=baris2(s,k,'Lapisan L01',vn,T,cv,f,idx,henti,f'Bendera {b}' if b else 'Asas (tanpa lapisan)'); rows.append(r)
                ring[(k,b,s)]=(r['cagr'],r['mdd'],r['n'],r['keputusan'])
            print(k,b,'431:',ring[(k,b,'431')],[ring[(k,b,s)][:2] for s in SETS],round(time.time()-t0),'s',flush=True)
    pd.DataFrame(rows,columns=LAJUR2).to_csv(os.path.join(KELUAR,'L01.csv'),index=False)
    pickle.dump(ring,open(os.path.join(KELUAR,'l01.pkl'),'wb')); print('siap')

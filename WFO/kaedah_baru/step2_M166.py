# STEP-2 M166 — Titik Pusing Momentum (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M166.py [folder_keluar]
# Output: M166.csv (lajur LAJUR2) dan m166.pkl dalam folder_keluar (lalai: folder semasa). Registry: BacktestShariah2/kod/registry/M166.csv.
import sys, os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)   # lokasi data repo; enjin tidak diubah
import _rangka_r as R
fr,idx,asal=muat()
import time, pickle; t0=time.time()
spy=idx['SPY'].close

def keadaan(c, lambat=252, laju=21):
    """Bull/Correction/Bear/Rebound daripada siri tutup c; NaN jika S atau F tiada."""
    S=c/c.shift(lambat)-1; F=c/c.shift(laju)-1
    k=pd.Series(np.nan,c.index,dtype=object)
    ok=S.notna()&F.notna()
    k[ok&(S>0)&(F>0)]='Bull'; k[ok&(S>0)&(F<=0)]='Correction'
    k[ok&(S<=0)&(F<=0)]='Bear'; k[ok&(S<=0)&(F>0)]='Rebound'
    return k

def rs_n(g,n):
    rsl=g.close/R.spy_pada(g,idx); return rsl/rsl.shift(n)-1

def ew_indeks(fr_):
    r=pd.DataFrame({t:g.close.pct_change() for t,g in fr_.items()}).sort_index()
    return (1+r.mean(axis=1).fillna(0)).cumprod()

def bina(fr_, kead, laju_rs=21):
    """Pulangkan konteks: RS12, RS_laju (dict), persentil, keadaan."""
    RS12={t:R.rs12(g,idx) for t,g in fr_.items()}
    RSF={t:rs_n(g,laju_rs) for t,g in fr_.items()}
    return dict(RS12=RS12,RSF=RSF,P12=R.pct(RS12),PF=R.pct(RSF),kead=kead)

def pasang_kunci(fr_, C, mod):
    """mod: 'V1' (Bear dilarang, Rebound->RSF), 'V2' (tiada sekatan Bear), 'V5' (Correction & Bear dilarang)."""
    K={}; PK={}; sah={}
    kd=C['kead']
    for t,g in fr_.items():
        k=kd.reindex(g.index,method='ffill')
        reb=(k=='Rebound')
        K[t]=C['RS12'][t].reindex(g.index).where(~reb,C['RSF'][t].reindex(g.index))
        if mod=='V1': ok=k.notna()&(k!='Bear')
        elif mod=='V2': ok=k.notna()
        else: ok=k.isin(['Bull','Rebound'])
        sah[t]=ok
    idxs=C['P12'].index; kk=kd.reindex(idxs,method='ffill'); rb=(kk=='Rebound').values[:,None]
    PK=pd.DataFrame(np.where(rb,C['PF'].values,C['P12'].values),index=idxs,columns=C['P12'].columns)
    R.pasang(fr_,idx,K,0.90,False,PK,sah)

def pasang_v0(fr_, C):
    B=0.5*C['P12']+0.5*C['PF']; PB=B.rank(axis=1,pct=True)
    K={t:B[t].reindex(g.index) for t,g in fr_.items()}
    R.pasang(fr_,idx,K,0.90,False,PB)

def konteks(fr_):
    c={}
    c['SPY']=bina(fr_,keadaan(spy))
    return c

NAMA='Titik Pusing Momentum (Goulding, Harvey & Mazzoleni)'
RR='Rangka R: kolam PCT(K)>=0.90 (431), vol20>=100K, henti buka_masuk x0.88, keluar tutup<maks tutup sejak masuk-3xATR22 atau tutup<henti; tiada penapis SMA200 SPY'
KD='Keadaan SPY: S=pulangan 252 hari, F=pulangan 21 hari; Bull S>0,F>0; Correction S>0,F<=0; Bear S<=0,F<=0; Rebound S<=0,F>0. K=RS12 (Bull/Correction), RS1 (Rebound). Andaian saya: keadaan dikira pada tutup i, RS12=R.rs12 (M114), RS1=(C/SPY)_i/(C/SPY)_(i-21)-1'

def varian(ctx):
    return [('V0 Laju pertengahan statik 50/50',lambda f:pasang_v0(f,ctx['SPY']),True,
             'K=0.5 PCT(RS12)+0.5 PCT(RS1); kolam PCT(K)>=0.90; tiada penapis keadaan. Andaian saya: Rangka R dipakai (henti 12%, chandelier), tiada SMA200; PCT(K) ialah persentil bagi campuran'),
            ('V1 Dikunci (keadaan SPY, Bear dilarang)',lambda f:pasang_kunci(f,ctx['SPY'],'V1'),True,KD+'. '+RR),
            ('V2 V1 tanpa sekatan Bear',lambda f:pasang_kunci(f,ctx['SPY'],'V2'),True,'V1 tetapi Bear dibenarkan (kunci RS12 dalam Bear): hanya pertukaran kunci'),
            ('V3 V1 keadaan daripada indeks sama rata 431',lambda f:pasang_kunci(f,ctx['EW'],'V1'),True,'V1 tetapi S/F daripada indeks sama rata 431 (pulangan harian purata, kumulatif). RS1/RS12 kekal lawan SPY. Andaian saya'),
            ('V4 V1 isyarat pantas 63 hari',lambda f:pasang_kunci(f,ctx['S63'],'V1'),True,'V1 tetapi F=pulangan SPY 63 hari dan RS3=(C/SPY)_i/(C/SPY)_(i-63)-1 untuk Rebound'),
            ('V5 V1 tanpa Correction',lambda f:pasang_kunci(f,ctx['SPY'],'V5'),True,'V1 tetapi isyarat hanya dalam Bull dan Rebound')]

def sediakan(fr_):
    ctx={}
    ctx['SPY']=bina(fr_,keadaan(spy))
    ctx['EW']=dict(ctx['SPY']); ctx['EW']['kead']=keadaan(ew_indeks(fr_))
    c63=bina(fr_,keadaan(spy,252,63),63)
    ctx['S63']=c63
    return ctx

def cagr_dis25(cv): return tambahan.__dict__['_cagr'](cv[:'2025-12-31']) if '_cagr' in tambahan.__dict__ else None

if __name__=='__main__':
    import enjin
    ctx=sediakan(fr); print('konteks siap',round(time.time()-t0),'s')
    VAR=varian(ctx); rows=[]; simpan={}
    for nm,fn,henti,cat in VAR:
        fn(fr); T=trades(fr); cv=portfolio(T,fr)
        r=baris2('431','M166',NAMA,nm,T,cv,fr,idx,henti,cat); rows.append(r)
        simpan[nm]=(T,cv); print(nm,r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['n'],r['gate_gagal'],round(time.time()-t0),'s',flush=True)
    R4=pd.DataFrame(rows)
    lulus=R4[R4.gate_gagal.fillna('')=='']
    pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
    print('Ke subset:',pilih)
    for nm,fn,henti,cat in VAR:
        if nm not in pilih: continue
        fn(fr)
        for s in SETS:
            f=subset(fr,asal,s); T=trades(f); cv=portfolio(T,f)
            r=baris2(s,'M166',NAMA,nm,T,cv,f,idx,henti,cat); rows.append(r); simpan[(s,nm)]=(T,cv)
            print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
    out=pd.DataFrame(rows,columns=LAJUR2); out.to_csv(os.path.join(KELUAR,'M166.csv'),index=False)
    # tanpa 8 saham bermasalah (persentil dikira semula atas 423)
    f423={t:g for t,g in fr.items() if t not in R.LAPAN}; c423=sediakan(f423); ex={}
    for nm,fn,henti,cat in varian(c423):
        if nm[:2] not in ('V1','V2','V5') and nm not in pilih: continue
        fn(f423); T=trades(f423); cv=portfolio(T,f423); B=penanda(idx,f423); m=metrik(T,cv,B,ada_henti=henti)
        ex[nm]=(baris(nm,'M166',nm,m,B)['keputusan'],round(m['cagr'],4),round(m['mdd'],4),round(enjin._cagr(cv[:'2025-12-31']),4)); print('423',nm,ex[nm])
    pickle.dump(dict(simpan=simpan,pilih=pilih,ex423=ex),open(os.path.join(KELUAR,'m166.pkl'),'wb'))
    print('siap',round(time.time()-t0),'s')

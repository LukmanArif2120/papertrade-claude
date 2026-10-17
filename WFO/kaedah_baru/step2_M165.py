# STEP-2 M165 — Momentum Industri (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M165.py [folder_keluar]
# Output: M165.csv (lajur LAJUR2) dan m165.pkl dalam folder_keluar (lalai: folder semasa). Registry: BacktestShariah2/kod/registry/M165.csv.
import sys, os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)   # lokasi data repo; enjin tidak diubah
import _rangka_r as R
import enjin
fr,idx,asal=muat()
import time, pickle; t0=time.time()
PI=pd.read_csv(os.path.join(REPO,'BacktestShariah2/papertrade/peta_industri.csv')).set_index('ticker').industri

def ir_industri(fr_, n, min_ahli):
    """IR_n per industri (purata sama berat pulangan n hari ahli ada data; min_ahli ahli sah) dan persentil merentas industri layak."""
    RET=pd.DataFrame({t:g.close/g.close.shift(n)-1 for t,g in fr_.items()}).sort_index()
    IR={}; 
    for k,ahli in PI[PI.index.isin(list(fr_))].groupby(PI).groups.items():
        a=RET[list(ahli)]; c=a.notna().sum(axis=1)
        IR[k]=a.mean(axis=1).where(c>=min_ahli)
    IR=pd.DataFrame(IR); return IR, IR.rank(axis=1,pct=True)

def konteks(fr_, n_ir=126, min_ahli=3):
    c={}
    c['RS12']={t:R.rs12(g,idx) for t,g in fr_.items()}; c['PRS']=R.pct(c['RS12'])
    c['IR'],c['PI']=ir_industri(fr_,n_ir,min_ahli)
    return c

def sah_industri(fr_, C, ambang=0.80):
    s={}
    for t,g in fr_.items():
        if t in PI.index and PI[t] in C['PI'].columns: s[t]=(C['PI'][PI[t]]>=ambang).reindex(g.index).fillna(False)
        else: s[t]=pd.Series(False,g.index)
    return s

def pasang_v0(fr_, C):
    tarikh=pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr_.values()])))
    hb=set(pd.Series(tarikh,tarikh).groupby(tarikh.to_period('M')).max())
    if (tarikh[-1]+pd.offsets.BDay(1)).month==tarikh[-1].month: hb.discard(tarikh[-1])
    S=sah_industri(fr_,C)
    for t,g in fr_.items():
        h=pd.Series(g.index.isin(list(hb)),g.index)
        ir=C['IR'][PI[t]].reindex(g.index) if t in PI.index and PI[t] in C['IR'].columns else pd.Series(np.nan,g.index)
        ret=(g.close/g.close.shift(126)-1).fillna(0)
        g['sig']=(h&S[t]).fillna(False).astype(bool); g['stop']=np.nan; g['tgt']=np.nan; g['exitc']=False
        g['rank']=(ir+1e-6*ret).astype(float)

NAMA='Momentum Industri (Moskowitz & Grinblatt)'
RR='Rangka R: henti buka_masuk x0.88; keluar tutup<maks tutup sejak masuk-3xATR22 atau tutup<henti; SPY>SMA200; vol20>=100K'
UM='Industri: peta_industri.csv (snapshot Okt 2026). IR6=purata sama berat pulangan 126 hari ahli ada data (min 3 ahli sah); PCT_ind merentas industri layak. Andaian saya: industri <3 ahli sah pada hari itu tiada isyarat'
def varian(fr_):
    C=konteks(fr_); C1=konteks(fr_,21); C5=konteks(fr_,126,5)
    F=C['RS12']
    return [('V0 Sumber bulanan (industri sahaja)',lambda f:pasang_v0(f,C),False,'Hujung bulan: sig PCT_ind(IR6)>=0.80; rank IR6 (+1e-6 x pulangan 126 hari saham sebagai pemutus seri; Andaian saya); tmax 126; tiada henti; tiada exitc. '+UM,126),
            ('V1 Dikunci (industri 20% + RS12 20%)',lambda f:R.pasang(f,idx,F,0.80,True,C['PRS'],sah_industri(f,C)),True,'sig PCT_ind>=0.80 + PCT(RS12)>=0.80 (431) ; rank RS12. '+RR+'. '+UM,None),
            ('V2 V1 IR1 (21 hari)',lambda f:R.pasang(f,idx,F,0.80,True,C['PRS'],sah_industri(f,C1)),True,'V1 dengan IR1 = purata sama berat pulangan 21 hari ahli industri',None),
            ('V3 V1 tanpa syarat RS saham',lambda f:R.pasang(f,idx,F,0.0,True,C['PRS'],sah_industri(f,C)),True,'Industri sahaja (PCT_ind>=0.80); rank RS12; RS12 mesti sah',None),
            ('V4 V1 industri >=5 ahli',lambda f:R.pasang(f,idx,F,0.80,True,C['PRS'],sah_industri(f,C5)),True,'V1 hanya industri >=5 ahli sah (persentil industri dikira atas industri layak itu)',None),
            ('V5 V1 tanpa penapis SPY',lambda f:R.pasang(f,idx,F,0.80,False,C['PRS'],sah_industri(f,C)),True,'V1 tanpa SPY>SMA200',None)]

if __name__=='__main__':
    VAR=varian(fr); print('konteks siap',round(time.time()-t0),'s')
    nl=(PI.index.isin(list(fr))); print('saham dipeta',nl.sum(),'industri',PI[PI.index.isin(list(fr))].nunique())
    rows=[]; simpan={}
    for nm,fn,henti,cat,tm in VAR:
        fn(fr); T=trades(fr,tmax=tm); cv=portfolio(T,fr)
        r=baris2('431','M165',NAMA,nm,T,cv,fr,idx,henti,cat); rows.append(r); simpan[nm]=(T,cv)
        print(nm,r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['n'],r['gate_gagal'],'dis25',round(enjin._cagr(cv[:'2025-12-31']),4),round(time.time()-t0),'s',flush=True)
    R4=pd.DataFrame(rows); lulus=R4[R4.gate_gagal.fillna('')=='']
    pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
    print('Ke subset:',pilih)
    for nm,fn,henti,cat,tm in VAR:
        if nm not in pilih: continue
        fn(fr)
        for s in SETS:
            f=subset(fr,asal,s); T=trades(f,tmax=tm); cv=portfolio(T,f)
            r=baris2(s,'M165',NAMA,nm,T,cv,f,idx,henti,cat); rows.append(r); simpan[(s,nm)]=(T,cv)
            print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
    pd.DataFrame(rows,columns=LAJUR2).to_csv(os.path.join(KELUAR,'M165.csv'),index=False)
    f423={t:g for t,g in fr.items() if t not in R.LAPAN}; ex={}
    for nm,fn,henti,cat,tm in varian(f423):
        fn(f423); T=trades(f423,tmax=tm); cv=portfolio(T,f423); B=penanda(idx,f423); m=metrik(T,cv,B,ada_henti=henti)
        ex[nm]=(baris(nm,'M165',nm,m,B)['keputusan'],round(m['cagr'],4),round(m['mdd'],4),round(enjin._cagr(cv[:'2025-12-31']),4)); print('423',nm,ex[nm],flush=True)
    pickle.dump(dict(simpan=simpan,pilih=pilih,ex423=ex),open(os.path.join(KELUAR,'m165.pkl'),'wb'))
    print('siap',round(time.time()-t0),'s')

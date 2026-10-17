# STEP-2 M164 — Pulangan Hari Pengumuman Pendapatan (EAR) (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M164.py [folder_keluar]
# Data tarikh: BacktestShariah2/data/pemangkin/tarikh_pendapatan.csv (aliran kerja tarikh_pendapatan.yml; Nasdaq + Yahoo).
# Output: M164.csv (lajur LAJUR2), m164.pkl, M164_liputan.csv dalam folder_keluar. Registry: BacktestShariah2/kod/registry/M164.csv.
import sys, os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)
import _rangka_r as R
import enjin
fr,idx,asal=muat()
import time, pickle; t0=time.time()
spy=idx['SPY'].close
TP=os.path.join(REPO,'BacktestShariah2','data','pemangkin','tarikh_pendapatan.csv')

def pengumuman():
    """Tapis tarikh: dua sumber beza > 1 hari -> buang; d0 bukan hari dagangan dataset -> buang;
       pendua (saham sama, <= 7 hari kalendar) -> simpan yang pertama. Pulangkan DataFrame ticker, d0, i (= d0+1), ear, catatan bilangan."""
    d=pd.read_csv(TP,dtype={'beza_hari':'float'}); d['d0']=pd.to_datetime(d.d0); n0=len(d); cat={'mentah':n0}
    d=d[d.ticker.isin(list(fr))]; cat['dalam_431']=len(d)
    b=d.sumber.eq('kedua')&(d.beza_hari.abs()>1); cat['buang_bercanggah']=int(b.sum()); d=d[~b]
    d=d.sort_values(['ticker','d0']); d=d[~(d.groupby('ticker').d0.diff().dt.days<=7)]; cat['selepas_pendua']=len(d)
    rows=[]; bukan=0
    sx=spy
    for r in d.itertuples():
        g=fr[r.ticker]; ix=g.index
        if r.d0 not in ix: bukan+=1; continue
        k=ix.get_loc(r.d0)
        if k<2 or k+1>=len(ix): continue
        c=g.close.values; a,b_=ix[k-2],ix[k+1]
        s0,s1=sx.asof(a),sx.asof(b_)
        rows.append((r.ticker,r.d0,b_,c[k+1]/c[k-2]-s1/s0,r.sumber))
    cat['buang_bukan_hari_dagangan']=bukan
    A=pd.DataFrame(rows,columns=['ticker','d0','i','ear','sumber']); cat['sah']=len(A)
    return A,cat

def titik_putus(A, q, tarikh, n=63, mn=100):
    """BP_i: persentil q EAR bagi semua pengumuman dengan hari isyarat dalam [i-n, i-1] (hari dagangan); min mn pengumuman."""
    pos=tarikh.get_indexer(A.i); A=A.assign(pos=pos).sort_values('pos'); P=A.pos.values; E=A.ear.values
    bp=np.full(len(tarikh),np.nan)
    for j in range(len(tarikh)):
        lo,hi=np.searchsorted(P,j-n),np.searchsorted(P,j)
        if hi-lo>=mn: bp[j]=np.quantile(E[lo:hi],q)
    return pd.Series(bp,tarikh)

def pasang(A, bp, sumber=False, spy_f=False, rs=False, tmax=63, P12=None):
    E={t:pd.Series(np.nan,g.index) for t,g in fr.items()}
    for r in A.itertuples(): E[r.ticker].loc[r.i]=r.ear
    for t,g in fr.items():
        e=E[t]; b=bp.reindex(g.index)
        s=e.notna()&b.notna()&(e>=b)&(g.volume.rolling(20).mean()>=1e5)
        if spy_f: s&=R.spy_atas_sma200(g,idx)
        if rs: s&=(P12[t].reindex(g.index)>=0.80)
        g['sig']=s.fillna(False).astype(bool); g['tgt']=np.nan; g['rank']=e.astype(float)
        if sumber:
            g['stop']=np.nan; g['exitc']=False
        else:
            g['stop']=g.open.shift(-1)*0.88; R.tandai_keluar(g,tmax=tmax)

NAMA='Pulangan Hari Pengumuman Pendapatan (EAR)'
RR='Rangka R: henti buka_masuk x0.88; keluar tutup<maks tutup sejak masuk-3xATR22 atau tutup<henti'
UM='EAR=C(d0+1)/C(d0-2)-SPY(d0+1)/SPY(d0-2); sig pada d0+1 jika EAR>=BP90 (persentil EAR semua pengumuman dengan hari isyarat dalam 63 hari dagangan lepas, min 100); vol20>=100K; rank EAR. Tarikh: Nasdaq + Yahoo (beza >1 hari dibuang)'
if __name__=='__main__':
    A,cat=pengumuman(); print('pengumuman',cat,flush=True)
    tarikh=pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    BP90=titik_putus(A,0.90,tarikh); BP80=titik_putus(A,0.80,tarikh)
    P12=R.pct({t:R.rs12(g,idx) for t,g in fr.items()})
    VAR=[('V0 Sumber (pegang 63 hari, tiada henti)',lambda:pasang(A,BP90,sumber=True),False,63,'Pegang tepat 63 hari (tmax); tiada henti, tiada exitc. '+UM),
         ('V1 Dikunci (EAR>=BP90, Rangka R, tmax 63)',lambda:pasang(A,BP90),True,63,RR+'; tmax 63. '+UM),
         ('V2 V1 BP80',lambda:pasang(A,BP80),True,63,'V1 dengan persentil ke-80'),
         ('V3 V1 + SPY>SMA200',lambda:pasang(A,BP90,spy_f=True),True,63,'V1 + tutup SPY>SMA200'),
         ('V4 V1 + PCT(RS12)>=0.80',lambda:pasang(A,BP90,rs=True,P12=P12),True,63,'V1 + PCT RS12>=0.80 (431)'),
         ('V5 V1 tanpa tmax',lambda:pasang(A,BP90,tmax=None),True,None,'V1 tanpa had masa')]
    rows=[]; simpan={}
    for nm,fn,henti,tm,c in VAR:
        fn(); T=trades(fr,tmax=tm); cv=portfolio(T,fr)
        r=baris2('431','M164',NAMA,nm,T,cv,fr,idx,henti,c); rows.append(r); simpan[nm]=(T,cv)
        print(nm,r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['n'],r['gate_gagal'],'dis25',round(enjin._cagr(cv[:'2025-12-31']),4),round(time.time()-t0),'s',flush=True)
    R4=pd.DataFrame(rows); lulus=R4[R4.gate_gagal.fillna('')=='']
    pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
    print('Ke subset:',pilih)
    for nm,fn,henti,tm,c in VAR:
        if nm not in pilih: continue
        fn()
        for s in SETS:
            f=subset(fr,asal,s); T=trades(f,tmax=tm); cv=portfolio(T,f)
            r=baris2(s,'M164',NAMA,nm,T,cv,f,idx,henti,c); rows.append(r); simpan[(s,nm)]=(T,cv)
            print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
    pd.DataFrame(rows,columns=LAJUR2).to_csv(os.path.join(KELUAR,'M164.csv'),index=False)
    L=A.groupby('ticker').agg(n=('d0','size'),pertama=('d0','min'),akhir=('d0','max'),jurang_maks_hari=('d0',lambda x:x.diff().dt.days.max()))
    L.reindex(sorted(fr)).to_csv(os.path.join(KELUAR,'M164_liputan.csv'))
    pickle.dump(dict(simpan=simpan,pilih=pilih,cat=cat,A=A,BP90=BP90),open(os.path.join(KELUAR,'m164.pkl'),'wb'))
    print('siap',round(time.time()-t0),'s')

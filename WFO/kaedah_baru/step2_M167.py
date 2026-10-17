# STEP-2 M167 — Momentum Semalaman (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M167.py [folder_keluar]
# Output: M167.csv (lajur LAJUR2) dan m167.pkl dalam folder_keluar (lalai: folder semasa). Registry: BacktestShariah2/kod/registry/M167.csv.
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

def ovn(g,n):
    on=np.log(g.open/g.close.shift())
    return on.rolling(n,min_periods=n).sum()

def konteks(fr_):
    c={}
    for n in (21,63,252): c[n]={t:ovn(g,n) for t,g in fr_.items()}
    c['P21']=R.pct(c[21]); c['P63']=R.pct(c[63]); c['P252']=R.pct(c[252])
    c['RS12']={t:R.rs12(g,idx) for t,g in fr_.items()}; c['PRS']=R.pct(c['RS12'])
    return c

def pasang_v0(fr_,C):
    tarikh=pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr_.values()])))
    hb=set(pd.Series(tarikh,tarikh).groupby(tarikh.to_period('M')).max())
    if (tarikh[-1]+pd.offsets.BDay(1)).month==tarikh[-1].month: hb.discard(tarikh[-1])
    for t,g in fr_.items():
        p=C['P21'][t].reindex(g.index); h=pd.Series(g.index.isin(list(hb)),g.index); ok=(p>=0.90)&C[21][t].reindex(g.index).notna()
        g['sig']=(h&ok).fillna(False).astype(bool); g['stop']=np.nan; g['tgt']=np.nan
        g['exitc']=(h&~(p>=0.90)).fillna(False).astype(bool); g['rank']=C[21][t].reindex(g.index).astype(float)

NAMA='Momentum Semalaman (Lou, Polk & Skouras)'
RR='Rangka R: kolam PCT>=0.90 (431), SPY>SMA200, vol20>=100K, henti buka_masuk x0.88, keluar tutup<maks tutup sejak masuk-3xATR22 atau tutup<henti'
UM='ON=ln(buka_t/tutup_(t-1)) harga terlaras; OVN21=jumlah ON 21 hari (min 21 sah). Andaian saya: buka harian proksi VWAP 9:30-10:00; hari buka=tutup semalam dikekalkan (ON=0)'
def varian(C):
    return [('V0 Sumber bulanan (tiada henti)',lambda f:pasang_v0(f,C),False,'Hujung bulan: sig PCT(OVN21)>=0.90; keluar hujung bulan jika PCT<0.90; tiada henti, tiada penapis SPY; vol20 tidak dikenakan. '+UM),
            ('V1 Dikunci (OVN21, Rangka R)',lambda f:R.pasang(f,idx,C[21],0.90,True,C['P21']),True,'rank OVN21. '+RR+'. '+UM),
            ('V2 V1 kunci OVN252',lambda f:R.pasang(f,idx,C[252],0.90,True,C['P252']),True,'V1 dengan OVN252 (jumlah ON 252 hari)'),
            ('V3 V1 kolam PCT(RS12), rank OVN21',lambda f:R.pasang(f,idx,C[21],0.90,True,C['PRS']),True,'Kolam PCT(RS12)>=0.90 (M114 V4); rank OVN21 (OVN21 mesti sah)'),
            ('V4 V1 tanpa penapis SPY',lambda f:R.pasang(f,idx,C[21],0.90,False,C['P21']),True,'V1 tanpa SPY>SMA200'),
            ('V5 V1 kunci OVN63',lambda f:R.pasang(f,idx,C[63],0.90,True,C['P63']),True,'V1 dengan OVN63')]

if __name__=='__main__':
    C=konteks(fr); print('OVN siap',round(time.time()-t0),'s')
    stale=np.mean(np.concatenate([(g.open==g.close.shift()).values[1:] for g in fr.values()])); print('buka=tutup semalam',round(stale,4))
    VAR=varian(C); rows=[]; simpan={}
    for nm,fn,henti,cat in VAR:
        fn(fr); T=trades(fr); cv=portfolio(T,fr)
        r=baris2('431','M167',NAMA,nm,T,cv,fr,idx,henti,cat); rows.append(r); simpan[nm]=(T,cv)
        print(nm,r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['n'],r['gate_gagal'],'dis25',round(enjin._cagr(cv[:'2025-12-31']),4),round(time.time()-t0),'s',flush=True)
    R4=pd.DataFrame(rows); lulus=R4[R4.gate_gagal.fillna('')=='']
    pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
    print('Ke subset:',pilih)
    for nm,fn,henti,cat in VAR:
        if nm not in pilih: continue
        fn(fr)
        for s in SETS:
            f=subset(fr,asal,s); T=trades(f); cv=portfolio(T,f)
            r=baris2(s,'M167',NAMA,nm,T,cv,f,idx,henti,cat); rows.append(r); simpan[(s,nm)]=(T,cv)
            print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
    pd.DataFrame(rows,columns=LAJUR2).to_csv(os.path.join(KELUAR,'M167.csv'),index=False)
    f423={t:g for t,g in fr.items() if t not in R.LAPAN}; ex={}
    for nm,fn,henti,cat in varian(konteks(f423)):
        if nm[:2] not in ('V1','V2','V3','V4','V5'): continue
        fn(f423); T=trades(f423); cv=portfolio(T,f423); B=penanda(idx,f423); m=metrik(T,cv,B,ada_henti=henti)
        ex[nm]=(baris(nm,'M167',nm,m,B)['keputusan'],round(m['cagr'],4),round(m['mdd'],4),round(enjin._cagr(cv[:'2025-12-31']),4)); print('423',nm,ex[nm],flush=True)
    pickle.dump(dict(simpan=simpan,pilih=pilih,ex423=ex),open(os.path.join(KELUAR,'m167.pkl'),'wb'))
    print('siap',round(time.time()-t0),'s')

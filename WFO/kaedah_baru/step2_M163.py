# STEP-2 M163 — Kekuatan Mutlak (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M163.py [folder_keluar]
# Output: M163.csv (lajur LAJUR2) dan m163.pkl dalam folder_keluar (lalai: folder semasa). Registry: BacktestShariah2/kod/registry/M163.csv.
import sys, os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
KELUAR=sys.argv[1] if len(sys.argv)>1 else '.'
sys.path[:0]=[os.path.join(REPO,'BacktestShariah2','kod'), os.path.join(REPO,'WFO','kaedah_baru')]
import tambahan
from tambahan import *
tambahan.cari=lambda nama: os.path.join(REPO,'data_mentah',nama)   # lokasi data repo; enjin tidak diubah
import _rangka_r as R
from _resid import resid
fr,idx,asal=muat()
import time, pickle; t0=time.time()

def kekuatan(g): return g.close.shift(21)/g.close.shift(252)-1            # AS_i = C(i-21)/C(i-252) - 1

def titik_putus(A, q=0.90, tetingkap=None, min_hari=126):
    """BP_m: persentil q semua nilai AS (semua saham, semua hari <= hari dagangan terakhir bulan m-1).
       Terkumpul sejak AS pertama sah, atau tetingkap bergolek `tetingkap` hari dagangan. Pulangkan Series per tarikh."""
    ada=A.notna().any(axis=1); hari0=ada.values.argmax()
    bulan=A.index.to_period('M'); bp=pd.Series(np.nan,A.index); V=A.values
    for m in bulan.unique():
        k=np.searchsorted(A.index.values, A.index[bulan==m][0].to_datetime64())   # baris pertama bulan m; cutoff = k-1
        if k-hari0<min_hari: continue
        a=V[hari0:k] if tetingkap is None else V[max(hari0,k-tetingkap):k]
        x=a[~np.isnan(a)]
        if len(x): bp[bulan==m]=np.percentile(x,q*100)
    return bp

def bina(fr_):
    A=pd.DataFrame({t:kekuatan(g) for t,g in fr_.items()}).sort_index()
    return A, {'BP90':titik_putus(A,0.90),'BP80':titik_putus(A,0.80),'BP90_504':titik_putus(A,0.90,504)}

spy=idx['SPY'].close
F_RES={t:resid(g,spy)[0] for t,g in fr.items()}
A,BP=bina(fr)
print('AS & BP siap', round(time.time()-t0),'s')

def pasang(fr_, A, bp, rank='AS', penapis_spy=False):
    for t,g in fr_.items():
        a=A[t].reindex(g.index); b=bp.reindex(g.index)
        s=(a>=b)&a.notna()&b.notna()&(g.volume.rolling(20).mean()>=1e5)
        if penapis_spy: s&=R.spy_atas_sma200(g,idx)
        g['sig']=s.fillna(False).astype(bool); g['stop']=g.open.shift(-1)*0.88; g['tgt']=np.nan
        g['rank']=(a if rank=='AS' else F_RES[t].reindex(g.index)).astype(float)
        R.tandai_keluar(g)

tarikh=A.index
hb=set(pd.Series(tarikh,tarikh).groupby(tarikh.to_period('M')).max())
if (tarikh[-1]+pd.offsets.BDay(1)).month==tarikh[-1].month: hb.discard(tarikh[-1])
def sedia_v0(fr_, A, bp):
    for t,g in fr_.items():
        a=A[t].reindex(g.index); b=bp.reindex(g.index); h=pd.Series(g.index.isin(list(hb)),g.index)
        ok=(a>=b)&a.notna()&b.notna()
        g['sig']=(h&ok).fillna(False).astype(bool); g['stop']=np.nan; g['tgt']=np.nan
        g['exitc']=(h&~ok).fillna(False).astype(bool); g['rank']=a.astype(float)

NAMA='Kekuatan Mutlak (Gulen & Petkova)'
UMUM='AS=C(i-21)/C(i-252)-1; BP = persentil semua AS (semua saham, semua hari hingga hujung bulan lepas), kemas kini bulanan, min 126 hari pengumpulan. Andaian saya: persentil interpolasi linear; 126 hari dikira dari hari pertama mana-mana AS sah'
RR='Rangka R: henti buka_masuk x0.88; keluar tutup<maks tutup sejak masuk-3xATR22 atau tutup<henti; vol20>=100K'
VAR=[('V0 Sumber bulanan (tiada henti)',lambda f,A,B:sedia_v0(f,A,B['BP90']),False,
      'Hujung bulan (kalendar M96): sig AS>=BP90; keluar hujung bulan jika AS<BP90; tiada henti, tiada penapis volum/SPY; rank AS. '+UMUM),
     ('V1 Dikunci (AS>=BP90, Rangka R)',lambda f,A,B:pasang(f,A,B['BP90']),True,'Harian: AS>=BP90 tanpa penapis SPY; rank AS. '+RR+'. '+UMUM),
     ('V2 V1 + SPY>SMA200',lambda f,A,B:pasang(f,A,B['BP90'],penapis_spy=True),True,'V1 + tutup SPY>SMA200'),
     ('V3 V1 BP80',lambda f,A,B:pasang(f,A,B['BP80']),True,'V1 dengan persentil ke-80'),
     ('V4 V1 rank RESID (M162)',lambda f,A,B:pasang(f,A,B['BP90'],rank='RESID'),True,
      'V1 tetapi rank = RESID M162 (beta SPY). Andaian saya: RESID NaN diletak paling bawah'),
     ('V5 V1 tetingkap bergolek 504 hari',lambda f,A,B:pasang(f,A,B['BP90_504']),True,
      'V1 tetapi BP90 daripada 504 hari dagangan terakhir (bukan terkumpul); kemas kini bulanan')]
if __name__=='__main__':
    rows=[]; simpan={}
    for nm,fn,henti,cat in VAR:
        fn(fr,A,BP); T=trades(fr); cv=portfolio(T,fr)
        r=baris2('431','M163',NAMA,nm,T,cv,fr,idx,henti,cat); rows.append(r)
        simpan[nm]=(T,cv); print(nm, r['keputusan'], r['skor'], r['cagr'], r['mdd'], r['n'], r['gate_gagal'], round(time.time()-t0),'s')
    R4=pd.DataFrame(rows)
    lulus=R4[R4.gate_gagal.fillna('')=='']
    pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
    print('Ke subset:',pilih)
    for nm,fn,henti,cat in VAR:
        if nm not in pilih: continue
        fn(fr,A,BP)          # isyarat atas 431 (BP daripada taburan 431); subset hanya menapis saham
        for s in SETS:
            f=subset(fr,asal,s); T=trades(f); cv=portfolio(T,f)
            r=baris2(s,'M163',NAMA,nm,T,cv,f,idx,henti,cat); rows.append(r); simpan[(s,nm)]=(T,cv)
            print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
    out=pd.DataFrame(rows,columns=LAJUR2); out.to_csv(os.path.join(KELUAR,'M163.csv'),index=False)
    pickle.dump(dict(simpan=simpan,pilih=pilih,BP=BP),open(os.path.join(KELUAR,'m163.pkl'),'wb'))
    print('siap',round(time.time()-t0),'s')

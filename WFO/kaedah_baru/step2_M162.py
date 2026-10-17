# STEP-2 M162 — Momentum Residual (enjin v1.2 beku; Rangka R). Jalan: python3 WFO/kaedah_baru/step2_M162.py [folder_keluar]
# Output: M162.csv (lajur LAJUR2) dan m162.pkl dalam folder_keluar (lalai: folder semasa). Registry: BacktestShariah2/kod/registry/M162.csv.
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
from _resid import resid
spy=idx['SPY'].close
# industri: pulangan sama berat ahli lain (industri >= 3 saham dalam 431)
pi=pd.read_csv(os.path.join(REPO,'BacktestShariah2/papertrade/peta_industri.csv')).set_index('ticker').industri
RET=pd.DataFrame({t:g.close.pct_change() for t,g in fr.items()})
IND={}
for k,ahli in pi[pi.index.isin(list(fr))].groupby(pi).groups.items():
    ahli=list(ahli)
    if len(ahli)<3: continue
    S=RET[ahli].sum(axis=1,min_count=1); C=RET[ahli].notna().sum(axis=1)
    for t in ahli:
        lain=C-RET[t].notna().astype(int); x=(S-RET[t].fillna(0))/lain
        IND[t]=x.where(lain>=2)
F1={}; F2={}
for t,g in fr.items():
    F1[t]=resid(g,spy)[0]
    F2[t]=resid(g,spy,IND[t])[0] if t in IND else F1[t]
print('RESID siap', round(time.time()-t0),'s; saham 2 faktor:',len(IND))
P1=R.pct(F1); P2=R.pct(F2)
tarikh=pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
hb=set(pd.Series(tarikh,tarikh).groupby(tarikh.to_period('M')).max())
if (tarikh[-1]+pd.offsets.BDay(1)).month==tarikh[-1].month: hb.discard(tarikh[-1])
def sedia_v0():
    for t,g in fr.items():
        p=P1[t].reindex(g.index); h=pd.Series(g.index.isin(list(hb)),g.index)
        g['sig']=(h&(p>=0.90)&(g.volume.rolling(20).mean()>=1e5)&F1[t].reindex(g.index).notna()).fillna(False)
        g['stop']=np.nan; g['tgt']=np.nan; g['exitc']=(h&~(p>=0.90)).fillna(False); g['rank']=F1[t].reindex(g.index)
VAR=[('V0 Sumber bulanan (proksi pasaran, tiada henti)',lambda:sedia_v0(),False,
      'Hujung bulan (kalendar M96): PCT RESID>=0.90 + vol20>=100K; keluar hujung bulan jika PCT<0.90; tiada henti; tiada penapis SPY. Andaian saya: FF3 diganti model pasaran SPY'),
     ('V1 Dikunci (Rangka R, RESID beta SPY)',lambda:R.pasang(fr,idx,F1,0.90,True,P1),True,
      'Rangka R: PCT RESID>=0.90 (431) + SPY>SMA200 + vol20>=100K; henti buka_masuk x0.88; keluar tutup<maks tutup sejak masuk-3xATR22. RESID = jumlah e(t-251..t-21)/(SD e x akar N), e=r-beta.m, beta 252 hari (min 200), N>=180'),
     ('V2 V1 tanpa penapis SPY',lambda:R.pasang(fr,idx,F1,0.90,False,P1),True,'V1 tanpa penapis SPY>SMA200'),
     ('V3 V1 keluar tutup<SMA50',lambda:R.pasang(fr,idx,F1,0.90,True,P1,exit_sma50=True),True,'V1 tetapi keluar tutup<SMA50 (atau tutup<henti)'),
     ('V4 V1 residual 2 faktor (SPY + industri)',lambda:R.pasang(fr,idx,F2,0.90,True,P2),True,
      'V1 tetapi e=r-b1.m-b2.ind; ind = pulangan sama berat ahli lain industri (peta_industri, industri>=3 saham, >=2 ahli lain sah); industri <3 saham guna model pasaran'),
     ('V5 V1 kolam 20%',lambda:R.pasang(fr,idx,F1,0.80,True,P1),True,'V1 tetapi kolam PCT>=0.80')]
rows=[]; simpan={}
for nm,fn,henti,cat in VAR:
    fn(); T=trades(fr); cv=portfolio(T,fr)
    r=baris2('431','M162','Momentum Residual (Blitz, Huij & Martens)',nm,T,cv,fr,idx,henti,cat); rows.append(r)
    simpan[nm]=(T,cv); print(nm, r['keputusan'], r['skor'], r['cagr'], r['mdd'], r['n'], r['gate_gagal'], round(time.time()-t0),'s')
R4=pd.DataFrame(rows)
lulus=R4[R4.gate_gagal.fillna('')=='']
pilih=lulus.sort_values('skor',ascending=False).varian.tolist() if len(lulus) else [R4.sort_values('cagr',ascending=False).varian.iloc[0]]
if len(lulus)==0: pilih=pilih[:1]
print('Ke subset:',pilih)
for nm,fn,henti,cat in VAR:
    if nm not in pilih: continue
    fn()
    for s in SETS:
        f=subset(fr,asal,s); T=trades(f); cv=portfolio(T,f)
        r=baris2(s,'M162','Momentum Residual (Blitz, Huij & Martens)',nm,T,cv,f,idx,henti,cat); rows.append(r)
        print(' ',s,nm[:2],r['keputusan'],r['skor'],r['cagr'],r['mdd'],r['ew_cagr'],r['gate_gagal'])
out=pd.DataFrame(rows,columns=LAJUR2); out.to_csv(os.path.join(KELUAR,'M162.csv'),index=False)
pickle.dump(dict(simpan=simpan,F1=F1,F2=F2,pilih=pilih),open(os.path.join(KELUAR,'m162.pkl'),'wb'))
print('siap',round(time.time()-t0),'s')

import pandas as pd,json
o=pd.concat([pd.read_csv('ohlc_okt.csv')[['ticker','date','low']],pd.read_csv('ohlc_extra.csv')[['ticker','date','low']]])
s=pd.read_csv('snap12.csv');s['date']=20261012
o=pd.concat([o,s[['ticker','date','low']]]).drop_duplicates(['ticker','date'],keep='last')
L={t:g.set_index('date')['low'] for t,g in o.groupby('ticker')}
out={};miss=0;dup=0
for ak,f in [('M','db/papertrade/moomoo.json'),('C','db/papertrade/claude.json')]:
  for r in json.load(open(f))['rows']:
    k=f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"
    b=int(r['tarikh_beli'].replace('-',''));lo=L.get(r['saham'])
    if lo is None: miss+=1;continue
    if r.get('keluar') and r.get('tarikh_keluar'):
      e=int(r['tarikh_keluar'].replace('-',''));w=lo[(lo.index>=b)&(lo.index<e)].tolist()
      if r.get('harga_keluar') is not None:w.append(r['harga_keluar'])
    else: w=lo[lo.index>=b].tolist()
    if not w: miss+=1;continue
    v=round(min(0,(min(w)/r['harga_beli']-1)*100),2)
    if k in out: dup+=1;v=min(v,out[k])
    out[k]=v
print(len(out),miss,dup)
json.dump({'rows':out,'dibina':'2026-10-13 04:00 MYT','harga_hingga':'2026-10-12 intraday (Moomoo snapshot ~15:48 NY)','definisi':'Penurunan maksimum % = (harga rendah terendah sejak hari beli hingga hari ini, atau sehingga keluar) ÷ harga beli − 1, maksimum 0. Bagi posisi keluar: rendah hari sebelum hari keluar dan harga keluar. Kunci: akaun|saham|kaedah|tarikh_beli (akaun M=Moomoo, C=Claude).'},open('mae.json','w'),separators=(',',':'))
import os;print(os.path.getsize('mae.json'))

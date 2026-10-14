import pandas as pd, numpy as np, sys
d=pd.concat([pd.read_csv(f'data/dataset_S{i}.csv') for i in range(1,5)]).sort_values(['ticker','date'])
pc=d.groupby('ticker').close.shift(); tr=pd.concat([d.high-d.low,(d.high-pc).abs(),(d.low-pc).abs()],axis=1).max(axis=1)
d['atr_pct']=tr.groupby(d.ticker).transform(lambda x:x.rolling(22).mean())/d.close
A=d[['ticker','date','atr_pct']]
rows=[]
for v in sys.argv[1:]:
    k=pd.read_csv(f'hasil/P02/kejadian_{v}.csv',low_memory=False); k=k[(k.ufuk_penuh==True)&(k.gap!=True)]
    k=k.merge(A,left_on=['ticker','hari'],right_on=['ticker','date'],how='left')
    q=k[k.status=='C0'].atr_pct.quantile([.2,.4,.6,.8]).to_numpy(); k['aq']=np.digitize(k.atr_pct,q)+1
    def adj(g,ref):
        w=ref.aq.value_counts(normalize=True)
        return ((g.groupby('aq').kelas.apply(lambda x:(x=='Berjaya').mean())*w).sum(), (g.groupby('aq').K3_untung.mean()*w).sum(),
                (g.groupby('aq').kelas.apply(lambda x:(x=='Gagal teruk').mean())*w).sum())
    for nm,f in [('semua',lambda x:x),('penemuan',lambda x:x[x.tempoh=='penemuan']),('pengesahan',lambda x:x[x.tempoh=='pengesahan']),('tanpa2020',lambda x:x[x.tahun!=2020])]:
        kk=f(k); C0=kk[kk.status=='C0']
        r=dict(varian=v,potongan=nm,C0_bj=(C0.kelas=='Berjaya').mean(),C0_K3=C0.K3_untung.mean(),C0_gt=(C0.kelas=='Gagal teruk').mean())
        for s in ['B1','B3','C1']:
            g=kk[kk.status==s]; b,k3,gt=adj(g,C0); r[f'{s}_n']=len(g); r[f'{s}_bj_sel']=b; r[f'{s}_K3_sel']=k3; r[f'{s}_gt_sel']=gt
        sub=0
        for s in ['S1','S2','S3','S4']:
            kq=kk[kk.subset==s]; c0=kq[kq.status=='C0']; b,k3,_=adj(kq[kq.status=='B1'],c0)
            sub+= int(k3>c0.K3_untung.mean())
        r['subset_B1_K3_lebih']=sub
        rows.append(r)
o=pd.DataFrame(rows); pd.set_option('display.width',300)
print(o.round(3).to_string()); o.to_csv('hasil/P02/selaras_atr.csv',index=False)

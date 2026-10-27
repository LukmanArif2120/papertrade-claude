"""STEP 2b — kohort "naik dan naik" (masih_naik = ya), dijejak hingga 252 hari dagangan.

Menjawab: kalau masih naik pada hari ke-63, berapa jauh lagi ia pergi?
Guna: python3 REVERSE/step2b_kohort.py 2025
Output: REVERSE/kohort_masih_naik_<TAHUN>.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, ind as I, keluar as K  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402

UFUK = 252


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a = ap.parse_args()
    th = a.tahun
    t0 = time.time()
    runs = pd.read_csv(AKAR / 'REVERSE' / f'runs_{th}.csv')
    runs['tarikh_sah'] = pd.to_datetime(runs['tarikh_sah'], errors='coerce')
    koh = runs[(runs.masih_naik == 'ya') & (runs.entry_sah == 'ya') & (runs.sebab_kecuali.isna()
               | (runs.sebab_kecuali == ''))].copy()
    lain = runs[(runs.masih_naik == 'tidak') & (runs.entry_sah == 'ya')].copy()
    tick = sorted(set(koh.ticker))
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy = ix['SPY']['close']
    spy_naik = ((spy > spy.rolling(50, min_periods=50).mean())
                & (spy > spy.rolling(200, min_periods=200).mean())).to_numpy()
    univ = D.universe()
    peta = D.peta_sektor(list(fr))
    si = D.indeks_sektor(fr, peta, univ, spy.index)
    print(f'[{time.time()-t0:.0f}s] kohort masih_naik {len(koh)} | rujukan reda {len(lain)}')

    rows = []
    for tk, grp in koh.groupby('ticker'):
        g = fr.get(tk)
        if g is None:
            continue
        sek = peta.loc[tk, 'sektor']
        ind = I.kira(g, spy=spy, sektor_idx=si[sek] if sek in si.columns else None)
        arr = K.sedia(g, ind)
        pn = pd.Series(spy_naik, index=spy.index).reindex(g.index).fillna(False).to_numpy()
        c = arr['c']
        to = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy('float64')
        for _, r in grp.iterrows():
            if pd.isna(r['tarikh_sah']) or r['tarikh_sah'] not in g.index:
                continue
            i = int(g.index.get_loc(r['tarikh_sah']))
            if i + 1 >= c.size:
                continue
            ks = kos_sisi(to[i])
            masuk = c[i + 1 - 1] if False else arr['o'][i + 1]
            masuk_kos = masuk * (1.0 + ks)
            b = min(i + UFUK, c.size - 1)
            seg = c[i + 1:b + 1]
            if not np.isfinite(seg).any():
                continue
            i_pk = int(np.nanargmax(seg)) + i + 1
            naik_penuh = (c[i_pk] - r['rendah_mula']) / r['rendah_mula'] * 100.0
            # exit mana menyala dahulu
            pertama, hari_pertama = '', 10 ** 9
            for nm in K.EXIT13:
                d = K.jalan(arr, i, UFUK, nm)
                if d is None:
                    continue
                if not d['terbuka'] and d['hari_pegang'] < hari_pertama:
                    hari_pertama, pertama = d['hari_pegang'], nm
            ch = K.jalan(arr, i, UFUK, 'chandelier_4atr')
            rows.append(dict(
                ticker=tk, sektor=sek, tarikh_sah=r['tarikh_sah'].date(),
                kumpulan_63=r['kumpulan'], jenis_kenaikan=r['jenis_kenaikan'],
                pct_naik_rendah_63=r['pct_naik_rendah'], hari_ke_puncak_63=r['hari_ke_puncak'],
                tarikh_puncak_penuh=g.index[i_pk].date(),
                harga_puncak_penuh=round(float(c[i_pk]), 4),
                pct_naik_penuh=round(float(naik_penuh), 2),
                hari_ke_puncak_penuh=int(i_pk - int(g.index.get_loc(
                    pd.Timestamp(r['tarikh_mula']))) if pd.notna(r['tarikh_mula']) else i_pk - i),
                mfe252=round(float(np.nanmax(seg) / masuk_kos - 1.0) * 100, 2),
                mae252=round(float(np.nanmin(seg) / masuk_kos - 1.0) * 100, 2),
                exit_pertama=pertama, hari_exit_pertama=(hari_pertama if pertama else ''),
                chandelier_hari=ch['hari_pegang'] if ch else '',
                chandelier_pul=round((ch['keluar_kasar'] * (1 - ks) / masuk_kos - 1) * 100, 2)
                if ch else '',
                terpotong_data='ya' if b < i + UFUK else 'tidak'))
    out = pd.DataFrame(rows)
    out.to_csv(AKAR / 'REVERSE' / f'kohort_masih_naik_{th}.csv', index=False)
    if len(out):
        print(f'n kohort dijejak {len(out)}')
        print(f'  % akhirnya melebihi 100%: {(out.pct_naik_penuh >= 100).mean()*100:.1f}%')
        print(f'  median %_naik_penuh: {out.pct_naik_penuh.median():.1f}%'
              f' (lawan median 63 hari {out.pct_naik_rendah_63.median():.1f}%)')
        print(f'  median hari pegang Chandelier: '
              f'{pd.to_numeric(out.chandelier_hari, errors="coerce").median():.0f}')
        print(f'  median pulangan Chandelier selepas kos: '
              f'{pd.to_numeric(out.chandelier_pul, errors="coerce").median():.1f}%')
        print('  exit pertama paling kerap:')
        print(out.exit_pertama.value_counts().head(5).to_string())
        print(f'  terpotong hujung data: {(out.terpotong_data=="ya").mean()*100:.1f}%')
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()

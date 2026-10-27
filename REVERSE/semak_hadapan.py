"""Imbasan pandang ke hadapan bagi REVERSE/teras/ind.py (SPEC §3.5; cara AUTOTUNE/kaedah/semak_hadapan.py).

Bagi setiap tarikh potong c: kira() atas data dipotong pada c (termasuk) lawan kira() atas data
penuh. SEMUA lajur indikator mesti sama bagi semua tarikh <= c. Indikator entry dibaca pada hari
isyarat itu sendiri, jadi tiada kelonggaran "buka esok" seperti enjin kaedah.

Indeks sektor juga diuji terpotong: ia hasil darab kumulatif median pulangan, jadi kausal.

Guna: python3 REVERSE/semak_hadapan.py <TAHUN> [--ticker N] [--potong N]
Output: REVERSE/PANDANG_HADAPAN_<TAHUN>.md
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, ind as I  # noqa: E402

TOL = 1e-6
AKHIR_DATA = pd.Timestamp('2026-10-16')


def tarikh_potong(th):
    """12 hujung bulan tahun kajian + 2 titik selepasnya (>= 12 tarikh potong, SPEC §3.5)."""
    bulan = pd.date_range(f'{th}-01-01', f'{th}-12-31', freq='ME')
    lanjut = [t for t in pd.date_range(f'{th + 1}-03-31', f'{th + 1}-12-31', freq='2QE')
              if t <= AKHIR_DATA][:2]
    return [t.strftime('%Y-%m-%d') for t in list(bulan) + lanjut]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    ap.add_argument('--ticker', type=int, default=40)
    ap.add_argument('--potong', type=int, default=0)
    a = ap.parse_args()
    semua = tarikh_potong(a.tahun)
    potong = semua[:a.potong] if a.potong else semua

    univ = D.universe()
    tick = D.tickers_tahun(a.tahun, univ)
    rng = np.random.default_rng(42)
    pilih = sorted(rng.choice(tick, size=min(a.ticker, len(tick)), replace=False).tolist())
    fr = D.muat_harga(pilih, f'{a.tahun - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{a.tahun - 2}-06-01', '2026-10-16')
    spy = ix['SPY']['close']
    peta = D.peta_sektor(list(fr))
    si_penuh = D.indeks_sektor(fr, peta, univ, spy.index)

    gagal = []
    n_banding = 0
    for c in potong:
        cc = pd.Timestamp(c)
        frp = {t: g[g.index <= cc] for t, g in fr.items()}
        sip = D.indeks_sektor(frp, peta, univ, spy.index[spy.index <= cc])
        for t, g in fr.items():
            sek = peta.loc[t, 'sektor']
            penuh = I.kira(g, spy=spy, sektor_idx=si_penuh[sek] if sek in si_penuh else None)
            pot = I.kira(frp[t], spy=spy[spy.index <= cc],
                         sektor_idx=sip[sek] if sek in sip else None)
            if pot.empty:
                continue
            a2 = penuh.loc[penuh.index <= cc]
            b2 = pot.loc[pot.index <= cc]
            sama = a2.index.intersection(b2.index)
            for kol in penuh.columns:
                x = a2.loc[sama, kol].to_numpy('float64')
                y = b2.loc[sama, kol].to_numpy('float64')
                n_banding += 1
                kedua_nan = np.isnan(x) & np.isnan(y)
                beza = ~kedua_nan & ~(np.abs(x - y) <= TOL * np.maximum(1.0, np.abs(x)))
                if beza.any():
                    i = int(np.flatnonzero(beza)[0])
                    gagal.append(dict(potong=c, ticker=t, lajur=kol, n_beza=int(beza.sum()),
                                      tarikh=str(sama[i].date()), penuh=float(x[i]),
                                      terpotong=float(y[i])))
    md = [f'# Imbasan pandang ke hadapan {a.tahun} — REVERSE/teras/ind.py', '',
          f'- Tarikh potong: {len(potong)} ({potong[0]} … {potong[-1]})',
          f'- Ticker diuji: {len(fr)} (benih 42)',
          f'- Perbandingan lajur×potong×ticker: {n_banding}',
          f'- Toleransi relatif: {TOL}', '']
    if gagal:
        md += ['## GAGAL', '', '| potong | ticker | lajur | n_beza | tarikh | penuh | terpotong |',
               '|---|---|---|---|---|---|---|']
        for r in gagal[:60]:
            md.append(f"| {r['potong']} | {r['ticker']} | {r['lajur']} | {r['n_beza']} | "
                      f"{r['tarikh']} | {r['penuh']:.6g} | {r['terpotong']:.6g} |")
        md += ['', f'Jumlah kegagalan: {len(gagal)}']
    else:
        md += ['## LULUS', '',
               'Tiada lajur indikator berubah apabila data dipotong. Semua lajur hari t hanya '
               'bergantung pada bar <= t.']
    (AKAR / 'REVERSE' / f'PANDANG_HADAPAN_{a.tahun}.md').write_text('\n'.join(md) + '\n')
    print(f'potong {len(potong)} | ticker {len(fr)} | banding {n_banding} | gagal {len(gagal)}')
    for r in gagal[:10]:
        print(' GAGAL', r)
    return 1 if gagal else 0


if __name__ == '__main__':
    sys.exit(main())

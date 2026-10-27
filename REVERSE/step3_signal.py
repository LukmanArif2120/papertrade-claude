"""STEP 3 — populasi kuintil dibekukan, dedup Spearman, kawalan rawak, matriks signal.

Guna: python3 REVERSE/step3_signal.py 2025
Output: .cache/kuintil_<TAHUN>.json, .cache/rawak_<TAHUN>.parquet,
        REVERSE/taburan_indikator_<TAHUN>.csv, baris dedup dalam log_ujian.csv
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import signal as S  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a = ap.parse_args()
    th = a.tahun
    t0 = time.time()
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sah = (sig.jenis_peristiwa != '') & (sig.dalam_univ == 1)
    ev = sig[sah]
    pop = ev[ev.kumpulan_data == 'A']
    print(f'peristiwa sah {len(ev)} | POPULASI KUINTIL (kumpulan A) {len(pop)}')

    simpan, buang = S.dedup(pop)
    kuin = S.kuintil(pop, simpan)
    (CACHE / f'kuintil_{th}.json').write_text(json.dumps(
        dict(populasi='peristiwa sah kumpulan A', n=int(len(pop)), simpan=simpan,
             dibuang=[dict(buang=b, kerana=s, rho=round(r, 3)) for b, s, r in buang],
             sempadan=kuin), indent=1))
    print(f'dedup: simpan {len(simpan)} | dibuang {len(buang)}')
    for b, s_, r in buang:
        print(f'  buang {b} (rho {r:+.2f} dengan {s_})')

    # log_ujian
    log = KELUAR / 'log_ujian.csv'
    baris = []
    for b, s_, r in buang:
        baris.append(dict(tarikh='2026-10-27', fasa='STEP3', subset='-', signal=b, jenis='dedup',
                          n=len(pop), keterangan=f'Spearman {r:+.3f} dengan {s_}',
                          keputusan='dedup_spearman'))
    if baris:
        pd.DataFrame(baris).to_csv(log, mode='a', header=False, index=False)

    # kawalan rawak: 10,000 titik, 833/bulan, benih 42
    rng = np.random.default_rng(42)
    layak = sig[sig.dalam_univ == 1].reset_index(drop=True)
    layak['bulan'] = layak.tarikh.dt.strftime('%Y-%m')
    pilih = []
    per_bulan = 10000 // 12
    for i, (b, grp) in enumerate(layak.groupby('bulan')):
        n = per_bulan + (10000 - per_bulan * 12 if i == 11 else 0)
        n = min(n, len(grp))
        pilih.append(grp.sample(n=n, random_state=int(rng.integers(0, 2**31))))
    rawak = pd.concat(pilih, ignore_index=True)
    rawak.to_parquet(CACHE / f'rawak_{th}.parquet', index=False)
    print(f'kawalan rawak {len(rawak)} titik ({rawak.bulan.nunique()} bulan)')

    # taburan indikator berterusan mengikut hasil
    rows = []
    for k in simpan:
        for h in ('SUPER PADU', 'PADU', 'BIASA', 'GAGAL'):
            x = ev.loc[ev.hasil == h, k].to_numpy('float64')
            x = x[np.isfinite(x)]
            if x.size == 0:
                continue
            rows.append(dict(indikator=k, hasil=h, n=int(x.size),
                             median=round(float(np.median(x)), 4),
                             p25=round(float(np.quantile(x, .25)), 4),
                             p75=round(float(np.quantile(x, .75)), 4)))
        x = rawak[k].to_numpy('float64')
        x = x[np.isfinite(x)]
        if x.size:
            rows.append(dict(indikator=k, hasil='RAWAK', n=int(x.size),
                             median=round(float(np.median(x)), 4),
                             p25=round(float(np.quantile(x, .25)), 4),
                             p75=round(float(np.quantile(x, .75)), 4)))
    pd.DataFrame(rows).to_csv(KELUAR / f'taburan_indikator_{th}.csv', index=False)

    sg = S.bina(ev, kuin)
    print(f'signal dibina: {len(sg)} '
          f'(binari {sum(1 for k in sg if k.startswith("b:"))}, '
          f'kuintil {sum(1 for k in sg if k.startswith(("q1:", "q5:")))}, '
          f'pemicu x konteks {sum(1 for k in sg if "&" in k)})')
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()

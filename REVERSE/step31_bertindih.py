"""Berapa banyak daripada 78 topeng MASUK yang DIUJI sebenarnya memberi maklumat BERBEZA?

Soalan pengguna: "apa kata kalau kita test kesemuanya?" Sebelum membayar 78x kos operasi,
ukur dahulu berapa ujian BEBAS yang 78 kohort itu sebenarnya mewakili. Topeng seperti
`N16` (rsi2<10), `N75` (rsi14<40), `N17` (rsi14 silang 30) dan `N19` (bb<0 DAN rsi14<30)
mencetus pada bar terlebih jual yang bertindih, jadi mereka bukan ujian bebas.

Ukuran: Jaccard berpasangan pada bar cair, kemudian pengelompokan pautan-lengkap pada
jarak 1-Jaccard. Satu wakil setiap kelompok = bilangan kohort yang memberi maklumat berbeza.

Ini DIAGNOSTIK operasi, bukan gate kajian. Tiada dakwaan prestasi dibuat.

Guna: python3 REVERSE/step31_bertindih.py [--amb 0.5]
"""
import argparse
import csv
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step18_nxx as S18    # noqa: E402

KELUAR = AKAR / 'REVERSE'
CAIR = 100_000.0


def diuji():
    """Topeng MASUK berstatus DIUJI dalam registry, dengan keluarganya."""
    out = {}
    with (AKAR / 'BacktestShariah2' / 'data' / 'registry_N.csv').open() as fh:
        for r in csv.DictReader(fh):
            i = r['id']
            if i.startswith('N') and i[1:].isdigit() and r['status'].startswith('DIUJI'):
                out[i] = r['keluarga']
    return out


def kelompokkan(J, nama, amb):
    """Pautan lengkap: dua topeng dalam kelompok sama hanya jika SETIAP pasangan >= amb."""
    kump = []
    for i, n in enumerate(nama):
        for k in kump:
            if all(J[i, j] >= amb for j in k):
                k.append(i)
                break
        else:
            kump.append([i])
    return [[nama[i] for i in k] for k in kump]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--amb', type=float, default=0.5, help='ambang Jaccard untuk "pendua"')
    a = ap.parse_args(argv)

    t0 = time.time()
    KEL = diuji()
    rsf = S18.rs_persentil()
    bk = S18.kelompok_ticker()[0]          # satu kelompok cukup untuk struktur bertindih
    P = S18._sedia(bk, S18.PUL, rsf)
    T = S18.topeng(P)
    cair = P.nilai20.to_numpy() >= CAIR
    ada = [k for k in KEL if k in T]
    print(f'{len(ada)} topeng DIUJI daripada {len(KEL)} dalam registry · '
          f'{int(cair.sum()):,} bar cair  [{time.time() - t0:.0f}s]')

    M = {}
    for k in ada:
        m = np.asarray(T[k], bool) & cair
        if m.sum() >= 200:                 # MIN_N kajian
            M[k] = m
    nama = sorted(M, key=lambda x: int(x[1:]))
    A = np.vstack([M[k] for k in nama])
    n = len(nama)
    print(f'{n} topeng dengan >= 200 isyarat dalam kelompok ini')

    inter = (A.astype('int32') @ A.T.astype('int32')).astype('float64')
    tot = np.diag(inter)
    union = tot[:, None] + tot[None, :] - inter
    J = np.divide(inter, union, out=np.zeros_like(inter), where=union > 0)

    kump = kelompokkan(J, nama, a.amb)
    print()
    print('=' * 78)
    print(f'KELOMPOK PENDUA pada Jaccard >= {a.amb} (pautan lengkap)')
    print('=' * 78)
    byk = [k for k in kump if len(k) > 1]
    for k in sorted(kump, key=lambda x: -len(x)):
        if len(k) == 1:
            continue
        fam = sorted({KEL[x] for x in k})
        print(f'  {len(k):>2} topeng [{"/".join(fam)}]: {" ".join(k)}')
    print(f'\n  {len(kump)} kelompok · {len(byk)} mengandungi pendua · '
          f'{n - len(kump)} topeng ialah pendua yang boleh dibuang')
    print(f'  -> bilangan kohort yang memberi MAKLUMAT BERBEZA: {len(kump)} daripada {n}')

    print()
    print('Pasangan paling bertindih:')
    iu = np.triu_indices(n, 1)
    o = np.argsort(-J[iu])[:15]
    for q in o:
        i, j = iu[0][q], iu[1][q]
        print(f'  {nama[i]:<6} {nama[j]:<6} Jaccard {J[i, j]:.3f}   '
              f'({KEL[nama[i]]}/{KEL[nama[j]]})')

    print()
    print('Bertindih median DALAM keluarga lawan ANTARA keluarga:')
    dalam, antara = [], []
    for q in range(len(iu[0])):
        i, j = iu[0][q], iu[1][q]
        (dalam if KEL[nama[i]] == KEL[nama[j]] else antara).append(J[i, j])
    print(f'  dalam keluarga  n={len(dalam):>5}  median {np.median(dalam):.3f}  '
          f'p90 {np.percentile(dalam, 90):.3f}')
    print(f'  antara keluarga n={len(antara):>5}  median {np.median(antara):.3f}  '
          f'p90 {np.percentile(antara, 90):.3f}')

    pd.DataFrame(J, index=nama, columns=nama).to_csv(KELUAR / 'bertindih_nxx.csv',
                                                     float_format='%.4f')
    with (KELUAR / 'bertindih_kelompok.csv').open('w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['kelompok', 'wakil', 'keluarga', 'n_topeng', 'topeng'])
        for q, k in enumerate(kump, 1):
            w.writerow([q, k[0], KEL[k[0]], len(k), ' '.join(k)])
    print(f'\n-> bertindih_nxx.csv · bertindih_kelompok.csv  [{time.time() - t0:.0f}s]')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

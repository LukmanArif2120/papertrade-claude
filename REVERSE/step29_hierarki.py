"""E6 — GABUNGAN `GB07`: hierarki merentas paksi. Pradaftar `REVERSE/SPEC_HIERARKI.md`.

Signal A mentakrif ALAM (saringan BERDIRI, bukan pintu harian), signal B mentakrif URUTAN.
Eksperimen TERAKHIR dalam baris gilir `STRATEGI.md`.

Enjin `step27.simulasi` (putaran berpangkat X32) + `had_ind` E5 diguna semula tanpa
perubahan; saringan A dikenakan dengan memotong peta calon pada setiap sauh.

Guna: python3 REVERSE/step29_hierarki.py [--benih 20] [--laporan-sahaja]
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.pembinaan as PB  # noqa: E402
import REVERSE.step18_nxx as S18  # noqa: E402
import REVERSE.step22_portfolio_n as S22  # noqa: E402
import REVERSE.step27_keluar_portfolio as S27  # noqa: E402
import REVERSE.step28_korelasi as S28  # noqa: E402

KELUAR = AKAR / 'REVERSE'

UJI0 = '2020-01-01'
LATIH0, LATIH1 = '2012-01-01', '2019-12-31'
N_BENIH = 20
T1_CAGR, T1_MDD = 17.95, -26.82
T3_CAGR, T3_MDD = 15.0, -15.0
AMBANG_NISBAH = 0.669

# spec §3 — grid tetap
ALAM_N = 500
SARING = ['A0', 'A1', 'A2', 'A3', 'A4']
URUT = ['U02', 'U14', 'U01']
SLOT = [8, 20]
HAD = [None, 2]
IMBANG = 63


def saring(LY, P, MA200, RSP, ATRP, nama):
    """Saringan BERDIRI dikenakan pada setiap sauh. Semua ambang dinilai PADA sauh."""
    if nama == 'A0':
        return LY
    out = {}
    for a, v in LY.items():
        if nama == 'A1':
            m = P.C[v, a] > MA200[v, a]
        elif nama == 'A2':
            m = np.nan_to_num(RSP[v, a], nan=-1.0) >= 50.0
        elif nama == 'A3':
            m = np.nan_to_num(RSP[v, a], nan=-1.0) >= 80.0
        else:                                  # A4: bawah median ATR% keratan rentas
            x = ATRP[v, a]
            med = np.nanmedian(x)
            m = np.isfinite(x) & (x <= med) if np.isfinite(med) else np.zeros(v.size, bool)
        w = v[np.nan_to_num(m, nan=False).astype(bool)]
        if w.size:
            out[a] = w
    return out


def ringkas(R):
    g = (R.groupby(['saring', 'urutan', 'slot', 'had'], dropna=False)
          .agg(cagr=('cagr', 'median'), mdd=('mdd', 'median'),
               cagr_p5=('cagr', lambda x: float(np.percentile(x, 5))),
               cagr_p95=('cagr', lambda x: float(np.percentile(x, 95))),
               cagr_latih=('cagr_latih', 'median'), dedah=('dedah', 'median'),
               n_dag=('n_dagangan', 'median'), kos_tahun=('kos_tahun', 'median'),
               buka=('buka_purata', 'median'), n_alam=('n_alam', 'median'),
               nb=('benih', 'size')).reset_index())
    g['nisbah'] = g.cagr / g.mdd.abs()
    ctl = {(r.saring, r.slot, r.had): r.cagr_p95
           for r in g[g.urutan == 'U01'].itertuples()}
    g['ctl_p95'] = [ctl.get((r.saring, r.slot, r.had), np.nan) for r in g.itertuples()]
    g['P1'] = g.cagr > T1_CAGR
    g['P2'] = g.mdd >= T1_MDD
    g['P3'] = np.where(g.urutan == 'U01', False, g.cagr > g.ctl_p95)
    g['P4'] = g.nisbah > AMBANG_NISBAH
    g['T1'] = g.P1 & g.P2
    g['T3'] = (g.cagr >= T3_CAGR) & (g.mdd >= T3_MDD)
    return g.sort_values('cagr', ascending=False)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'hierarki.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))

    t0 = time.time()
    print('1/3 panel + matriks saringan...', flush=True)
    P = PB.Panel()
    S18.rs_persentil()
    RSP = S22._matriks(P, S22.RSPF, 'rs_pst')
    MA200 = S22._matriks(P, S18.PANEL, 'ma200')
    ATRP = P.A / np.where(P.C > 0, P.C, np.nan)
    IND, n_ind, _ = S28.peta_industri(P)
    print(f'  siap, {n_ind} industri  [{time.time() - t0:.0f}s]', flush=True)

    print('2/3 alam titik-masa + saringan berdiri...', flush=True)
    LY = S28.alam_pit(S22.peta_layak(P), P, ALAM_N)
    ALAM = {}
    for nm in SARING:
        sv = saring(LY, P, MA200, RSP, ATRP, nm)
        n = float(np.mean([v.size for v in sv.values()])) if sv else 0.0
        ALAM[nm] = (sv, n)
        print(f'  {nm}: {n:.0f} nama/sesi (daripada {ALAM_N})', flush=True)

    hari = pd.DatetimeIndex(P.tarikh)
    m0 = int(np.searchsorted(P.tarikh, np.datetime64(UJI0)))
    l0 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH0)))
    l1 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH1)))
    tahun = (hari[-1] - hari[m0]).days / 365.25

    print('3/3 simulasi...', flush=True)
    baris = []
    for nm in SARING:
        sv, n_alam = ALAM[nm]
        for cara in URUT:
            for slot in SLOT:
                for had in HAD:
                    for bn in (range(1, a.benih + 1) if cara == 'U01' else [0]):
                        ek, nd, dg = S27.simulasi(P, RSP, sv, sv, slot, IMBANG, cara, bn,
                                                  m0, ind=IND, had_ind=had)
                        pe = float(np.nanmean(ek[m0:]))
                        baris.append(dict(
                            saring=nm, urutan=cara, slot=slot,
                            had='tiada' if had is None else str(had), benih=bn,
                            n_alam=n_alam,
                            cagr=PB.cagr(ek[m0:], hari[m0:]), mdd=PB.mdd(ek[m0:]),
                            cagr_latih=PB.cagr(ek[l0:l1], hari[l0:l1]),
                            mdd_latih=PB.mdd(ek[l0:l1]), n_dagangan=nd,
                            kos_tahun=dg['kos_wang'] / max(pe, 1e-9) * 100 / tahun,
                            **{k: v for k, v in dg.items() if k != 'kos_wang'}))
            print(f'  {nm} · {cara}: siap [{time.time() - t0:.0f}s]', flush=True)
    R = pd.DataFrame(baris)
    R.to_csv(f, index=False, float_format='%.4f')
    return laporan(R)


def laporan(R):
    g = ringkas(R)
    g.to_csv(KELUAR / 'hierarki_ringkas.csv', index=False, float_format='%.4f')
    base = {(r.urutan, r.slot, r.had): (r.cagr, r.mdd)
            for r in g[g.saring == 'A0'].itertuples()}
    sub = g[g.saring != 'A0'].copy()
    sub['d_cagr'] = [r.cagr - base[(r.urutan, r.slot, r.had)][0] for r in sub.itertuples()]
    sub['d_mdd'] = [r.mdd - base[(r.urutan, r.slot, r.had)][1] for r in sub.itertuples()]
    e6a = sub[(sub.d_cagr > 0) & (sub.d_mdd > 0)]

    print()
    print(f'SPUS 2020-2025: CAGR {T1_CAGR:.2f}%  MDD {T1_MDD:.2f}%')
    print(f'{len(g)} konfigurasi · T1 {int(g.T1.sum())} · T3 {int(g.T3.sum())} · '
          f'P1 {int(g.P1.sum())} · P2 {int(g.P2.sum())} · P3 {int(g.P3.sum())} · '
          f'P4 {int(g.P4.sum())}')
    print(f'E6a saringan mengalahkan A0 pada KEDUA-DUA paksi: {len(e6a)}/{len(sub)} sel '
          f'-> {"LULUS" if len(e6a) else "GAGAL"}')
    if len(e6a):
        print(e6a[['saring', 'urutan', 'slot', 'had', 'cagr', 'mdd', 'nisbah',
                   'd_cagr', 'd_mdd']].to_string(index=False,
                                                 float_format=lambda v: f'{v:+.2f}'))
    print()
    print('Kesan purata setiap saringan (lawan A0 pada sel sepadan):')
    print(sub.groupby('saring')[['d_cagr', 'd_mdd']].median().to_string(
        float_format=lambda v: f'{v:+.2f}'))
    print()
    print('Saiz alam selepas saringan:')
    print(g.groupby('saring').n_alam.median().to_string(float_format=lambda v: f'{v:.0f}'))
    print()
    kol = ['saring', 'urutan', 'slot', 'had', 'nb', 'cagr', 'cagr_p5', 'cagr_p95', 'mdd',
           'nisbah', 'dedah', 'buka', 'n_dag', 'kos_tahun', 'T1', 'T3', 'P3', 'P4']
    print(g.head(14)[kol].to_string(index=False, float_format=lambda v: f'{v:.2f}'))
    print()
    print('MDD paling cetek:')
    print(g.nlargest(8, 'mdd')[kol].to_string(index=False,
                                              float_format=lambda v: f'{v:.2f}'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

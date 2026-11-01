"""E5 — KORELASI `KR03`: had bilangan pegangan setiap industri. Pradaftar
`REVERSE/SPEC_KORELASI.md`.

Enjin E4 (`step27.simulasi`, putaran berpangkat `X32`) diguna semula dengan SATU tambahan:
`had_ind`. Lalai `None` memberi tingkah laku identik dengan E4 — kawalan regresi disahkan.

Alam: `AL04` TITIK-MASA (N teratas ikut nilai dagangan 20 hari pada sauh itu sendiri),
pembetulan yang dipaksa oleh E4 — keahlian SPUS hari ini menyanjung MDD 30.9 mata, dan E5
mengukur kesan pada paksi MDD.

Guna: python3 REVERSE/step28_korelasi.py [--benih 20] [--laporan-sahaja]
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
import REVERSE.pembinaan as PB  # noqa: E402
import REVERSE.step18_nxx as S18  # noqa: E402
import REVERSE.step22_portfolio_n as S22  # noqa: E402
import REVERSE.step27_keluar_portfolio as S27  # noqa: E402

KELUAR = AKAR / 'REVERSE'
TV = AKAR / 'BacktestShariah2' / 'data' / 'skrin' / 'tv_us.csv'

UJI0 = '2020-01-01'
LATIH0, LATIH1 = '2012-01-01', '2019-12-31'
N_BENIH = 20
T1_CAGR, T1_MDD = 17.95, -26.82
T3_CAGR, T3_MDD = 15.0, -15.0
AMBANG_NISBAH = 0.669
AMBANG_MDD = 0.50        # spec §6 E5a-MDD

# spec §5 — grid tetap
ALAM_N = [214, 500]
MASUK = ['RAWAK', 'GB02_atau3']
URUT = ['U02', 'U01']
SLOT = [8, 20, 40]
HAD = [None, 1, 2, 3]
IMBANG = 63              # dikunci (spec §5)


def peta_industri(P):
    """Array kumpulan industri bagi setiap indeks ticker panel.

    Ticker tanpa industri dikumpulkan sebagai SATU kumpulan `TIDAK_DIKETAHUI` yang tertakluk
    kepada had yang sama (spec §3) — melayan setiap yang tidak diketahui sebagai kumpulannya
    sendiri akan membuka lubang kepekatan tanpa had.
    """
    tv = {r['ticker']: r['industry']
          for r in csv.DictReader(open(TV, encoding='utf-8'))}
    nama, idn = {}, np.zeros(len(P.tick), dtype='int32')
    for i, t in enumerate(P.tick):
        g = tv.get(t) or 'TIDAK_DIKETAHUI'
        if g not in nama:
            nama[g] = len(nama)
        idn[i] = nama[g]
    tiada = sum(1 for t in P.tick if not tv.get(t))
    return idn, len(nama), tiada


def alam_pit(LAY, P, n):
    """`AL04` TITIK-MASA: N teratas ikut nilai dagangan 20 hari pada sauh ITU SENDIRI."""
    out = {}
    for a, v in LAY.items():
        if v.size <= n:
            out[a] = v
            continue
        nv = np.nan_to_num(P.N[v, a], nan=-1.0)
        out[a] = v[np.argsort(-nv, kind='stable')[:n]]
    return out


def ringkas(R):
    g = (R.groupby(['alam_n', 'masuk', 'urutan', 'slot', 'had'], dropna=False)
          .agg(cagr=('cagr', 'median'), mdd=('mdd', 'median'),
               cagr_p5=('cagr', lambda x: float(np.percentile(x, 5))),
               cagr_p95=('cagr', lambda x: float(np.percentile(x, 95))),
               cagr_latih=('cagr_latih', 'median'), dedah=('dedah', 'median'),
               n_dag=('n_dagangan', 'median'), kos_tahun=('kos_tahun', 'median'),
               buka=('buka_purata', 'median'), nb=('benih', 'size')).reset_index())
    g['nisbah'] = g.cagr / g.mdd.abs()
    ctl = {(r.alam_n, r.masuk, r.slot, r.had): r.cagr_p95
           for r in g[g.urutan == 'U01'].itertuples()}
    g['ctl_p95'] = [ctl.get((r.alam_n, r.masuk, r.slot, r.had), np.nan)
                    for r in g.itertuples()]
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
    f = KELUAR / 'korelasi.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))

    t0 = time.time()
    print('1/3 panel + peta industri...', flush=True)
    S = S22.bina_isyarat()
    P = PB.Panel()
    S18.rs_persentil()
    RSP = S22._matriks(P, S22.RSPF, 'rs_pst')
    IND, n_ind, n_tiada = peta_industri(P)
    print(f'  {n_ind} kumpulan industri; {n_tiada:,}/{len(P.tick):,} ticker tanpa industri'
          f'  [{time.time() - t0:.0f}s]', flush=True)

    print('2/3 alam titik-masa + calon...', flush=True)
    LAY = S22.peta_layak(P)
    it = {t: i for i, t in enumerate(P.tick)}
    idt = {d: i for i, d in enumerate(P.tarikh)}
    S = S[S.ticker.isin(it)]
    ii = S.ticker.map(it).to_numpy()
    jj = np.array([idt.get(d, -1) for d in S.date.to_numpy()])
    ok = jj >= 0
    ii, jj = ii[ok], jj[ok]
    msk = S.a3.to_numpy()[ok]
    sig = {}
    o = np.argsort(jj[msk], kind='stable')
    js, iss = jj[msk][o], ii[msk][o]
    b = np.flatnonzero(np.concatenate([[True], js[1:] != js[:-1], [True]]))
    for s_, e_ in zip(b[:-1], b[1:]):
        sig[int(js[s_])] = iss[s_:e_].astype('int64')
    ALAM = {}
    for n in ALAM_N:
        LY = alam_pit(LAY, P, n)
        cal = {}
        for aa, v in LY.items():
            w = sig.get(aa)
            if w is None:
                continue
            x = np.intersect1d(w, v, assume_unique=False)
            if x.size:
                cal[aa] = x.astype('int64')
        ALAM[n] = (LY, {'RAWAK': LY, 'GB02_atau3': cal})
        print(f'  AL04 {n}: {np.mean([v.size for v in LY.values()]):.0f} calon/sesi; '
              f'berisyarat {np.mean([cal[k].size for k in cal]) if cal else 0:.1f}/sesi',
              flush=True)

    hari = pd.DatetimeIndex(P.tarikh)
    m0 = int(np.searchsorted(P.tarikh, np.datetime64(UJI0)))
    l0 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH0)))
    l1 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH1)))
    tahun = (hari[-1] - hari[m0]).days / 365.25

    print('3/3 simulasi...', flush=True)
    baris = []
    for n in ALAM_N:
        LY, CAL = ALAM[n]
        for mk in MASUK:
            for cara in URUT:
                for slot in SLOT:
                    for had in HAD:
                        for bn in (range(1, a.benih + 1) if cara == 'U01' else [0]):
                            ek, nd, dg = S27.simulasi(P, RSP, CAL[mk], LY, slot, IMBANG,
                                                      cara, bn, m0, ind=IND, had_ind=had)
                            pe = float(np.nanmean(ek[m0:]))
                            baris.append(dict(
                                alam_n=n, masuk=mk, urutan=cara, slot=slot,
                                had='tiada' if had is None else str(had), benih=bn,
                                cagr=PB.cagr(ek[m0:], hari[m0:]), mdd=PB.mdd(ek[m0:]),
                                cagr_latih=PB.cagr(ek[l0:l1], hari[l0:l1]),
                                mdd_latih=PB.mdd(ek[l0:l1]),
                                n_dagangan=nd,
                                kos_tahun=dg['kos_wang'] / max(pe, 1e-9) * 100 / tahun,
                                **{k: v for k, v in dg.items() if k != 'kos_wang'}))
                print(f'  AL04 {n} · {mk} · {cara}: siap [{time.time() - t0:.0f}s]',
                      flush=True)
    R = pd.DataFrame(baris)
    R.to_csv(f, index=False, float_format='%.4f')
    return laporan(R)


def laporan(R):
    g = ringkas(R)
    g.to_csv(KELUAR / 'korelasi_ringkas.csv', index=False, float_format='%.4f')
    k = ['alam_n', 'masuk', 'urutan', 'slot']
    base = {(r.alam_n, r.masuk, r.urutan, r.slot): (r.mdd, r.nisbah, r.cagr)
            for r in g[g.had == 'tiada'].itertuples()}
    sub = g[g.had != 'tiada'].copy()
    sub['d_mdd'] = [r.mdd - base[(r.alam_n, r.masuk, r.urutan, r.slot)][0]
                    for r in sub.itertuples()]
    sub['d_nis'] = [r.nisbah - base[(r.alam_n, r.masuk, r.urutan, r.slot)][1]
                    for r in sub.itertuples()]
    sub['d_cagr'] = [r.cagr - base[(r.alam_n, r.masuk, r.urutan, r.slot)][2]
                     for r in sub.itertuples()]
    kadar_mdd = float((sub.d_mdd > 0).mean())
    a_mdd = kadar_mdd >= AMBANG_MDD
    a_nis = bool((sub.d_nis > 0).any())

    print()
    print(f'SPUS 2020-2025: CAGR {T1_CAGR:.2f}%  MDD {T1_MDD:.2f}%')
    print(f'{len(g)} konfigurasi · T1 {int(g.T1.sum())} · T3 {int(g.T3.sum())} · '
          f'P1 {int(g.P1.sum())} · P2 {int(g.P2.sum())} · P3 {int(g.P3.sum())} · '
          f'P4 {int(g.P4.sum())}')
    print(f'E5a-MDD   had mencetekkan MDD pada {int((sub.d_mdd > 0).sum())}/{len(sub)} = '
          f'{kadar_mdd:.1%} sel (ambang {AMBANG_MDD:.0%}) -> '
          f'{"LULUS" if a_mdd else "GAGAL"}')
    print(f'E5a-NISBAH ada had menaikkan nisbah: '
          f'{int((sub.d_nis > 0).sum())}/{len(sub)} sel -> '
          f'{"LULUS" if a_nis else "GAGAL"}')
    print()
    print('Kesan purata setiap had (lawan "tiada" pada sel sepadan):')
    print(sub.groupby('had')[['d_cagr', 'd_mdd', 'd_nis']].median().to_string(
        float_format=lambda v: f'{v:+.2f}'))
    print()
    print('Replikasi dapatan E4 pada alam kausal (masuk bersignal lawan tiada isyarat):')
    print(g.groupby(['alam_n', 'masuk'])[['cagr', 'mdd', 'nisbah']].max().to_string(
        float_format=lambda v: f'{v:+.2f}'))
    print()
    kol = ['alam_n', 'masuk', 'urutan', 'slot', 'had', 'nb', 'cagr', 'cagr_p5',
           'cagr_p95', 'mdd', 'nisbah', 'dedah', 'buka', 'n_dag', 'kos_tahun',
           'T1', 'T3', 'P3', 'P4']
    print(g.head(15)[kol].to_string(index=False, float_format=lambda v: f'{v:.2f}'))
    print()
    print('MDD paling cetek:')
    print(g.nlargest(8, 'mdd')[kol].to_string(index=False,
                                              float_format=lambda v: f'{v:.2f}'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

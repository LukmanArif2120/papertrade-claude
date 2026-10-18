# Semakan deskriptif post-hoc (BUKAN pemilihan pra-daftar): M82, M121, M38 dengan PARAM asal (tanpa penalaan),
# sistem A02 (8 slot × 12.5%, kos/slippage/gap/topeng universe A02) bagi lorong had60 dan asal:
#   P1 = 2013-01-01 – 2018-12-31 (kumpulan A, B; mesti sama dengan hasil_a02/saringan.csv)
#   P2 = 2019-01-01 – hujung data (kumpulan A, B, A+B)
# serta M82 sahaja dalam sistem utama A03 (F + M, 5 slot × 20%, had rugi 8%) bagi tempoh yang sama.
# Statistik daripada dagangan yang DIPEGANG portfolio. Memakai semula Penilai02 (tala_a02) dan Penilai03 (tala_a03).
#   python3 AUTOTUNE/sahkan/uji_asal.py [--cache AUTOTUNE/.cache_a02] [--fund AUTOTUNE/.cache_fund_a03] [--proses 2]
#   → AUTOTUNE/hasil_a03/uji_asal_m82.csv
import argparse, os, sys, time, warnings
from multiprocessing import get_context
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import tala as T1           # noqa: E402
import tala_a02 as T2       # noqa: E402
import tala_a03 as T3       # noqa: E402
from tala import E, O       # noqa: E402

KAEDAH = ['M82', 'M121', 'M38']
A03_KAEDAH = ['M82']
CSV = os.path.join(AT, 'hasil_a03', 'uji_asal_m82.csv')
SARINGAN = os.path.join(AT, 'hasil_a02', 'saringan.csv')
P1 = ('2013-01-01', '2018-12-31')
P2_MULA = '2019-01-01'
_G = {}


def statistik(T):
    r = pd.Series(T.ret if len(T) else [], dtype=float)
    n = len(r); u, k = r[r > 0], r[r <= 0]
    return dict(n=n, menang=len(u) / n if n else np.nan, kalah=len(k) / n if n else np.nan,
                purata_untung=u.mean() if len(u) else np.nan, purata_rugi=k.mean() if len(k) else np.nan,
                jangkaan=r.mean() if n else np.nan,
                pf=(u.sum() / -k.sum()) if len(k) and k.sum() < 0 else np.nan,
                hari=float(T.days.mean()) if n else np.nan)


def jalan(kerja):
    """kerja = (kaedah, sistem, tempoh) → senarai baris (lorong × kumpulan)."""
    warnings.filterwarnings('ignore')
    mid, sistem, tempoh = kerja
    t0 = time.time(); sumber = T1.Sumber(_G['dir'])
    m = T1.muat_kaedah(mid)
    panas = pd.Timedelta(days=O.panas_a02(m))
    if tempoh == 'P1': B0, B1, kum = pd.Timestamp(P1[0]), pd.Timestamp(P1[1]), ['A', 'B']
    else: B0, B1, kum = pd.Timestamp(P2_MULA), sumber.akhir_data(), ['A', 'B', 'AB']
    fr, idx, univ = sumber.muat(B0 - panas, B1, 'AB')
    if sistem == 'A02':
        pn = T2.Penilai02(m, fr, idx, univ, sumber, B0, B1, kum)
        hs = {(lo, g): v for (lo, g), v in pn.jalan02({}, kum, T2.LORONG, harian=False).items()}
    else:
        eps = T3.muat_eps(_G['fund'])
        pn = T3.Penilai03(m, fr, idx, univ, sumber, B0, B1, kum, eps=eps, varian=T3.UTAMA)
        hs = {(lo, g): v for (lo, g, _), v in pn.jalan03({}, kum, T2.LORONG, (T3.UTAMA,), harian=False).items()}
    spy_th = O.tahunan(pn.spy_cv)
    out = []
    for (lo, g), (mt, _, Tp) in hs.items():
        r = dict(kaedah=mid, sistem=sistem, lorong=lo, tempoh=tempoh, kumpulan=g, mula=str(B0.date()), akhir=str(B1.date()))
        r.update(statistik(Tp))
        r.update(cagr=mt['cagr'], mdd=mt['mdd'], spy_cagr=mt['spy_cagr'], spy_mdd=mt['spy_mdd'], lebihan=mt['lebihan'],
                 win_rekod=mt['win'], hari_rekod=mt['days'])
        for y, v in mt['tahunan'].items(): r[f't{y}'] = v
        for y, v in spy_th.items(): r[f'spy{y}'] = v
        out.append(r)
    print(mid, sistem, tempoh, f'{time.time() - t0:.0f}s', flush=True)
    return out


def semak(D):
    """Banding P1 sistem A02 dengan hasil_a02/saringan.csv; pulang senarai beza (lajur, rekod, kini)."""
    S = pd.read_csv(SARINGAN).set_index(['kaedah', 'lorong'])
    beza = []
    for _, r in D[(D.sistem == 'A02') & (D.tempoh == 'P1')].iterrows():
        s = S.loc[(r.kaedah, r.lorong)]; g = r.kumpulan
        for a, b in (('cagr', 'cagr'), ('mdd', 'mdd'), ('n', 'n'), ('win_rekod', 'menang'), ('hari_rekod', 'hari'),
                     ('lebihan', 'lebihan'), ('spy_cagr', 'spy'), ('spy_mdd', 'spy_mdd')):
            x, y = float(r[a]), float(s[f'{b}_{g}'])
            if not np.isclose(x, y, rtol=2e-5, atol=2e-6): beza.append((r.kaedah, r.lorong, g, b, y, x))
    return beza


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--cache', default=T2.CACHE); a.add_argument('--fund', default=T3.CACHE_F)
    a.add_argument('--proses', type=int, default=2); a.add_argument('--keluar', default=CSV)
    x = a.parse_args(argv)
    _G['dir'] = str(T2.ambil_data(x.cache)); _G['fund'] = T3.ambil_fundamental(x.fund)
    kerja = [(m, 'A02', t) for t in ('P2', 'P1') for m in KAEDAH] + [(m, 'A03', t) for t in ('P2', 'P1') for m in A03_KAEDAH]
    R = []
    with get_context('fork').Pool(x.proses, maxtasksperchild=1) as p:
        for out in p.imap_unordered(jalan, kerja): R += out
    D = pd.DataFrame(R)
    th = sorted([c for c in D if c.startswith('t2')]); sp = sorted([c for c in D if c.startswith('spy2')])
    tetap = [c for c in D if c not in th and c not in sp]
    D['_k'] = D.kaedah.map({k: i for i, k in enumerate(KAEDAH)})
    D = D.sort_values(['_k', 'sistem', 'tempoh', 'lorong', 'kumpulan']).drop(columns='_k')[tetap + th + sp]
    D.to_csv(x.keluar, index=False, float_format='%.6g')
    b = semak(D)
    print(f'{len(D)} baris → {x.keluar}; beza dengan saringan.csv: {len(b)}')
    for z in b[:20]: print('  BEZA', z)


if __name__ == '__main__':
    main()

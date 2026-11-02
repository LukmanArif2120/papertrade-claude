"""Portfolio 94 — larian B: tiga kecacatan dibetulkan + jalur benih. Pradaftar
`REVERSE/SPEC_PORTFOLIO_94B.md`.

Larian A (`PORTFOLIO_94.md`) menetapkan P2 0/8, P4 0/8, T1 0 — itu kekal. Yang dibetulkan:

(a) `U02` ialah PENDUA `U14` dalam larian A (matriks momentum sama, baris bit-identik).
    Kini momentum 6-1 sebenar, dengan semakan korelasi WAJIB sebelum larian.
(b) `RAWAK` menguji SUSUNAN bukan ISYARAT. Lengan `RAWAKALAM`: masuk rawak daripada alam
    cair dengan kolam, kiraan/hari, taburan keluar DAN pemeringkat dipadankan — jadi
    satu-satunya perbezaan ialah isyarat masuk.
(c) `PENUH` bukan berat sama rata (saiz berayun 2.7x). Kini pecahan TETAP 1/200.

Guna: python3 REVERSE/step34_portfolio_94b.py [--benih 20] [--semak-sahaja]
Output: REVERSE/PORTFOLIO_94B.md, REVERSE/portfolio_94b.csv
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
import REVERSE.step33_portfolio_94 as S33  # noqa: E402
from REVERSE.teras import kos as K  # noqa: E402

KELUAR = AKAR / 'REVERSE'
N_TETAP = 200            # spec §2(c) — pecahan tetap bagi lengan PENUH
N_BENIH = 20
SPUS_CAGR, SPUS_MDD = 17.95, -26.82
AMBANG_NISBAH = 0.669
URUT = ['U14', 'U02', 'U08', 'U01']


# ---------------------------------------------------------------- matriks urutan
def mom(C, belakang):
    """Momentum (t-21) / (t-belakang) - 1. NaN -> -9e9. U14 = 252, U02 = 147."""
    n, m = C.shape
    U = np.full((n, m), -9e9, 'float32')
    for t in range(belakang + 1, m):
        with np.errstate(invalid='ignore', divide='ignore'):
            v = C[:, t - 21] / C[:, t - belakang] - 1.0
        U[:, t] = np.where(np.isfinite(v), v, -9e9)
    return U


def semak_u02(U14, U02, rng):
    """Spec §2(a): korelasi Spearman U14 lawan U02 mesti < 0.99, jika tidak ia pendua."""
    n, m = U14.shape
    ti = rng.integers(0, n, 4000)
    da = rng.integers(300, m, 4000)
    a, b = U14[ti, da], U02[ti, da]
    ok = (a > -9e8) & (b > -9e8)
    a, b = a[ok], b[ok]
    if a.size < 500:
        return np.nan, a.size
    ra = pd.Series(a).rank().to_numpy()
    rb = pd.Series(b).rank().to_numpy()
    return float(np.corrcoef(ra, rb)[0, 1]), int(a.size)


# ---------------------------------------------------------------- kawalan alam
def rawak_alam(M, C94, benih):
    """Spec §2(b): masuk RAWAK daripada alam cair, dipadankan dengan C94 pada
    (bilangan calon setiap hari) dan (taburan kod keluar). Kolam, kiraan, keluar dan
    pemeringkat dipadankan — satu-satunya perbezaan ialah isyarat masuk."""
    rng = np.random.default_rng(10_000 + benih)
    out = {}
    n = M['C'].shape[0]
    for a, (ti_a, kc_a) in C94.items():
        d = a + 1
        if d >= M['C'].shape[1]:
            continue
        layak = np.flatnonzero(np.isfinite(M['C'][:, a]) & np.isfinite(M['N'][:, a]) &
                               (M['N'][:, a] >= PB.CAIR) &
                               np.isfinite(M['O'][:, d]) & (M['O'][:, d] > 0))
        if layak.size == 0:
            continue
        k = min(ti_a.size, layak.size)
        pilih = rng.choice(layak, size=k, replace=False)
        # taburan keluar dipadankan: ambil sampel kc_a hari itu
        kod = rng.choice(kc_a, size=k, replace=True) if kc_a.size else np.zeros(k, 'int32')
        out[a] = (pilih.astype('int32'), kod.astype('int32'))
    del n
    return out


# ---------------------------------------------------------------- simulasi
def simulasi(M, UM, CAL, slot, urut, benih, pecahan_tetap=None):
    """Sama seperti step33 tetapi (1) matriks urutan dipilih betul, (2) lengan PENUH
    memakai pecahan TETAP bukan ekuiti/bilangan-calon-hari-itu."""
    rng = np.random.default_rng(benih)
    m = M['C'].shape[1]
    cache = {}
    tunai, prev, n_dag = 1.0, 1.0, 0
    buka = []
    ek = np.full(m, np.nan)
    dz = np.full(m, np.nan)
    had = pecahan_tetap is None
    for d in range(1, m):
        if buka:
            for p in [x for x in buka if x[3] == d]:
                tunai += p[2] * p[4] * (1 - K.kos_sisi(M['N'][p[0], d]))
                buka.remove(p)
        a = d - 1
        c = CAL.get(a)
        if c is not None and c[0].size and (not had or len(buka) < slot):
            ti_a, kc_a = c
            ok = (np.isfinite(M['O'][ti_a, d]) & (M['O'][ti_a, d] > 0) &
                  np.isfinite(M['N'][ti_a, a]) & (M['N'][ti_a, a] >= PB.CAIR))
            ti_a, kc_a = ti_a[ok], kc_a[ok]
            if ti_a.size:
                if urut == 'U01':
                    o = rng.permutation(ti_a.size)
                elif urut == 'U08':
                    o = np.argsort(np.nan_to_num(
                        M['A'][ti_a, a] / np.maximum(M['C'][ti_a, a], 1e-9), nan=9e9),
                        kind='stable')
                else:
                    o = np.argsort(-UM[urut][ti_a, a], kind='stable')
                ti_a, kc_a = ti_a[o], kc_a[o]
                ada = {(x[0], x[1]) for x in buka}
                for ti, kc in zip(ti_a.tolist(), kc_a.tolist()):
                    if had and len(buka) >= slot:
                        break
                    if (ti, kc) in ada:
                        continue
                    belanja = min(prev / (slot if had else pecahan_tetap), tunai)
                    if belanja <= 1e-12:
                        break
                    kx, pj = S33.hari_keluar(M, ti, d, kc, cache)
                    if kx <= d:
                        continue
                    unit = belanja * (1 - K.kos_sisi(M['N'][ti, a])) / float(M['O'][ti, d])
                    tunai -= belanja
                    buka.append((ti, kc, unit, kx, pj))
                    ada.add((ti, kc))
                    n_dag += 1
        nilai = tunai
        for ti, _, unit, _, _ in buka:
            cc = M['C'][ti, d]
            if np.isfinite(cc):
                nilai += unit * float(cc)
        ek[d] = prev = nilai
        dz[d] = 1.0 - (tunai / nilai if nilai > 0 else 1.0)
    return ek, dz, n_dag


# ---------------------------------------------------------------- larian
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--semak-sahaja', action='store_true')
    a = ap.parse_args(argv)

    p94, _ = S33.kohort()
    M = S33.matriks()
    C94 = S33.calon(p94)
    print(f'kohort {len(p94)} kombinasi, {len(C94)} hari calon', flush=True)

    UM = {'U14': mom(M['C'], 252), 'U02': mom(M['C'], 147)}
    rho, nn = semak_u02(UM['U14'], UM['U02'], np.random.default_rng(3))
    print(f'SEMAKAN §2(a): Spearman U14 lawan U02 = {rho:.4f} pada n={nn}', flush=True)
    if not (np.isfinite(rho) and rho < 0.99):
        raise SystemExit(f'U02 masih pendua U14 (rho={rho}); lengan dibuang seperti spec §2(a)')
    print('  -> U02 BUKAN pendua; lengan sah', flush=True)
    if a.semak_sahaja:
        return 0

    R, t0 = [], time.time()

    def lari(nama, CAL, slot, urut, benih, tetap=None):
        ek, dz, nd = simulasi(M, UM, CAL, slot, urut, benih, pecahan_tetap=tetap)
        r = S33.tingkap(M, ek, dz)
        r.update(lengan=nama, slot=('penuh' if tetap else slot), urut=urut, benih=benih,
                 n_dag=nd)
        R.append(r)
        print(f"  [{time.time() - t0:.0f}s] {nama:9s} slot={str(r['slot']):>5} {urut} "
              f"b{benih:<3} CAGR {r['cagr']:+7.2f}%  MDD {r['mdd']:+7.2f}%  "
              f"nisbah {r['nisbah']:.2f}  dedah {r['dedah']:.0f}%  n {nd}", flush=True)

    for slot in (8, 40):
        for urut in URUT:
            for b in range(a.benih):
                lari('P94', C94, slot, urut, b)
    CR = {}
    for b in range(a.benih):
        CR[b] = rawak_alam(M, C94, b)
        lari('RAWAKALAM', CR[b], 8, 'U14', b)
    for b in range(a.benih):
        lari('RAWAKALAM', CR[b], 40, 'U14', b)
    lari('PENUH', C94, None, 'U14', 0, tetap=N_TETAP)

    d = pd.DataFrame(R)
    d.to_csv(KELUAR / 'portfolio_94b.csv', index=False)
    laporan(d, rho)
    return 0


def laporan(d, rho):
    L = ['# Portfolio 94 — larian B (tiga kecacatan dibetulkan, jalur benih)', '',
         'Pradaftar `REVERSE/SPEC_PORTFOLIO_94B.md` — dikomit sebelum keputusan dilihat.',
         f'Penanda aras SPUS: CAGR {SPUS_CAGR:+.2f}%  MDD {SPUS_MDD:+.2f}%  '
         f'nisbah {SPUS_CAGR / abs(SPUS_MDD):.3f}',
         f'Semakan §2(a): Spearman `U14` lawan `U02` = **{rho:.4f}** (< 0.99, jadi `U02` '
         'bukan pendua seperti dalam larian A).', '']

    def band(g):
        return (np.nanpercentile(g.cagr, 5), np.nanmedian(g.cagr), np.nanpercentile(g.cagr, 95),
                np.nanpercentile(g.mdd, 5), np.nanmedian(g.mdd), np.nanmedian(g.nisbah),
                np.nanmedian(g.dedah))
    L += ['## Jalur benih setiap lengan (20 benih)', '',
          '| Lengan | Slot | Urutan | CAGR p5 | CAGR median | CAGR p95 | MDD median | '
          'Nisbah median | Dedah |', '|---|---|---|--:|--:|--:|--:|--:|--:|']
    kunci = ['lengan', 'slot', 'urut']
    ring = {}
    for (ln, sl, ur), g in d.groupby(kunci, dropna=False):
        p5, md, p95, _, mdd_m, nis, ded = band(g)
        ring[(ln, sl, ur)] = (md, mdd_m, nis, p95)
        L.append(f'| {ln} | {sl} | {ur} | {p5:+.2f}% | **{md:+.2f}%** | {p95:+.2f}% | '
                 f'{mdd_m:+.2f}% | {nis:.2f} | {ded:.0f}% |')
    L += ['', '## Gate (median lengan; P3 = median P94 > p95 RAWAKALAM slot sama)', '',
          '| Lengan | Slot | Urutan | P1 | P2 | P3 | P4 | T1 |', '|---|---|---|:-:|:-:|:-:|:-:|:-:|']
    y = lambda b: '✓' if b else '✗'  # noqa: E731
    for (ln, sl, ur), (md, mdd_m, nis, _) in sorted(ring.items(), key=lambda x: str(x[0])):
        if ln == 'RAWAKALAM':
            continue
        p95r = ring.get(('RAWAKALAM', sl, 'U14'), (np.nan,) * 4)[3]
        p1, p2 = md > SPUS_CAGR, mdd_m >= SPUS_MDD
        p3 = np.isfinite(p95r) and md > p95r
        p4 = nis > AMBANG_NISBAH
        L.append(f'| {ln} | {sl} | {ur} | {y(p1)} | {y(p2)} | {y(p3)} | {y(p4)} | '
                 f'{y(p1 and p2)} |')
    (KELUAR / 'PORTFOLIO_94B.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L))


if __name__ == '__main__':
    raise SystemExit(main())

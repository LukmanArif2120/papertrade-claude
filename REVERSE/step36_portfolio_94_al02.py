"""Portfolio 94 pada alam `AL02` (SPUS) — syarat yang `SPEC_PORTFOLIO_94B.md` §8 wajibkan.

Spec 94B §8: *"Jika `P3` lulus: ia mesti diulang pada alam `AL02` sebelum sebarang dakwaan,
kerana E4 mengukur `AL02` menyanjung MDD sebanyak 30.9 mata berbanding `AL04` titik-masa."*

`P3` LULUS pada 8 slot dalam larian B (`U14` +11.65%, `U08` +12.17%, `U02` +19.80% lawan
jalur `RAWAKALAM` p95 +10.64%). Jadi syarat itu kini dicetus dan larian ini melaksanakannya.
Tiada spec baharu: gate kekal `SPEC_PORTFOLIO_94B.md` §5 tanpa perubahan.

AL02 dikenakan seperti E2 (`step25_alam.py`): memotong peta calon kepada indeks ticker SPUS
sahaja — enjin, keluar, pemeringkat dan kos tidak berubah, jadi satu-satunya perbezaan
daripada larian B ialah ALAM.

AMARAN DATA YANG MENGIKAT SETIAP NOMBOR DI SINI: keahlian SPUS ialah petikan **semasa**
ditolak ke belakang. E4 mengukur ia menyanjung MDD sebanyak 30.9 mata (−37.94% menjadi
−68.80% pada alam titik-masa `AL04` yang kausal). Jadi MDD di sini ialah **had bawah
optimistik**, bukan anggaran tak berbias.

Guna: python3 REVERSE/step36_portfolio_94_al02.py [--benih 20]
Output: REVERSE/PORTFOLIO_94_AL02.md, REVERSE/portfolio_94_al02.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step25_alam as S25  # noqa: E402
import REVERSE.step33_portfolio_94 as S33  # noqa: E402
import REVERSE.step34_portfolio_94b as S34  # noqa: E402

KELUAR = AKAR / 'REVERSE'
SPUS_CAGR, SPUS_MDD = 17.95, -26.82
AMBANG_NISBAH = 0.669
URUT = ['U14', 'U02', 'U08', 'U01']


def idx_spus(M):
    """Indeks ticker dalam matriks step33 yang ahli SPUS. Senarai daripada step25, bukan tangan."""
    sp = set(S25.alam_spus())
    it = {t: i for i, t in enumerate(M['tick'])}
    idx = sorted(it[t] for t in sp if t in it)
    return np.asarray(idx, 'int32'), len(sp)


def potong(CAL, ahli):
    """Potong peta calon kepada ahli alam sahaja — cara E2 mengenakan AL02."""
    s = set(ahli.tolist())
    out = {}
    for a, (ti, kc) in CAL.items():
        keep = np.fromiter((int(x) in s for x in ti), bool, ti.size)
        if keep.any():
            out[a] = (ti[keep], kc[keep])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=20)
    a = ap.parse_args(argv)

    p94, _ = S33.kohort()
    M = S33.matriks()
    C94 = S33.calon(p94)
    ahli, n_sp = idx_spus(M)
    print(f'AL02: {n_sp} ticker SPUS, {ahli.size} dalam panel', flush=True)

    C = potong(C94, ahli)
    n_a = [z[0].size for z in C94.values()]
    n_b = [z[0].size for z in C.values()]
    print(f'kolam/hari: AL01 median {int(np.median(n_a))} -> AL02 median {int(np.median(n_b))} '
          f'({len(C)} hari)', flush=True)
    print(f'  nisbah kolam:slot pada 8 slot: AL01 {np.median(n_a) / 8:.0f}x -> '
          f'AL02 {np.median(n_b) / 8:.0f}x', flush=True)

    UM = {'U14': S34.mom(M['C'], 252), 'U02': S34.mom(M['C'], 147)}
    R, t0 = [], time.time()

    def lari(nama, CAL, slot, urut, benih):
        ek, dz, nd = S34.simulasi(M, UM, CAL, slot, urut, benih)
        r = S33.tingkap(M, ek, dz)
        r.update(lengan=nama, slot=slot, urut=urut, benih=benih, n_dag=nd)
        R.append(r)
        print(f"  [{time.time() - t0:.0f}s] {nama:9s} slot={slot:>3} {urut} b{benih:<3} "
              f"CAGR {r['cagr']:+7.2f}%  MDD {r['mdd']:+7.2f}%  nisbah {r['nisbah']:.2f}  "
              f"dedah {r['dedah']:.0f}%  n {nd}", flush=True)

    for slot in (8, 40):
        for urut in URUT:
            for b in range(a.benih):
                lari('P94', C, slot, urut, b)
    for b in range(a.benih):
        CR = potong(S34.rawak_alam(M, C94, b), ahli)
        lari('RAWAKALAM', CR, 8, 'U14', b)
        lari('RAWAKALAM', CR, 40, 'U14', b)

    d = pd.DataFrame(R)
    d.to_csv(KELUAR / 'portfolio_94_al02.csv', index=False)
    laporan(d, n_sp, ahli.size, int(np.median(n_a)), int(np.median(n_b)))
    return 0


def laporan(d, n_sp, n_panel, kolam_a, kolam_b):
    L = ['# Portfolio 94 pada alam AL02 (SPUS) — syarat SPEC_PORTFOLIO_94B §8', '',
         'Dicetus kerana `P3` LULUS pada 8 slot dalam larian B. Gate kekal spec 94B §5.',
         f'AL02: {n_sp} ticker SPUS, {n_panel} dalam panel.',
         f'Kolam calon/hari: AL01 median **{kolam_a}** -> AL02 median **{kolam_b}** '
         f'(nisbah kolam:slot pada 8 slot {kolam_a // 8}x -> {kolam_b // 8}x).',
         '',
         '**AMARAN DATA:** keahlian SPUS ialah petikan SEMASA ditolak ke belakang. E4 mengukur '
         'ia menyanjung MDD sebanyak **30.9 mata** berbanding alam titik-masa `AL04`. MDD di '
         'bawah ialah had bawah OPTIMISTIK, bukan anggaran tak berbias.', '',
         '| Lengan | Slot | Urutan | CAGR p5 | CAGR median | CAGR p95 | MDD median | '
         'Nisbah median | Dedah |', '|---|---|---|--:|--:|--:|--:|--:|--:|']
    ring = {}
    for (ln, sl, ur), g in d.groupby(['lengan', 'slot', 'urut'], dropna=False):
        p5 = np.nanpercentile(g.cagr, 5)
        md = np.nanmedian(g.cagr)
        p95 = np.nanpercentile(g.cagr, 95)
        mdd = np.nanmedian(g.mdd)
        nis = np.nanmedian(g.nisbah)
        ring[(ln, sl, ur)] = (md, mdd, nis, p95)
        L.append(f'| {ln} | {sl} | {ur} | {p5:+.2f}% | **{md:+.2f}%** | {p95:+.2f}% | '
                 f'{mdd:+.2f}% | {nis:.2f} | {np.nanmedian(g.dedah):.0f}% |')
    L += ['', '## Gate (median lengan; P3 = median P94 > p95 RAWAKALAM slot sama)', '',
          '| Lengan | Slot | Urutan | P1 | P2 | P3 | P4 | T1 |', '|---|---|---|:-:|:-:|:-:|:-:|:-:|']
    y = lambda b: '✓' if b else '✗'  # noqa: E731
    for (ln, sl, ur), (md, mdd, nis, _) in sorted(ring.items(), key=lambda x: str(x[0])):
        if ln == 'RAWAKALAM':
            continue
        p95r = ring.get(('RAWAKALAM', sl, 'U14'), (np.nan,) * 4)[3]
        p1, p2 = md > SPUS_CAGR, mdd >= SPUS_MDD
        p3 = bool(np.isfinite(p95r) and md > p95r)
        p4 = nis > AMBANG_NISBAH
        L.append(f'| {ln} | {sl} | {ur} | {y(p1)} | {y(p2)} | {y(p3)} | {y(p4)} | '
                 f'{y(p1 and p2)} |')
    (KELUAR / 'PORTFOLIO_94_AL02.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L))


if __name__ == '__main__':
    raise SystemExit(main())

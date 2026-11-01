"""Pengesahan BEBAS bagi `REVERSE/SEMAKAN_LATIH.md`.

Mengira semula kesan Dakwaan A (had industri, E5) dan Dakwaan B (saringan berdiri, E6)
pada tingkap TAHAN dan LATIH **tanpa pandas** — hanya `csv` + `statistics` daripada
pustaka standard. Tujuannya ialah laluan kod yang berasingan sepenuhnya daripada
`groupby` yang menghasilkan nombor laporan asal, supaya persetujuan antara kedua-duanya
bukan persetujuan sesuatu dengan dirinya sendiri.

Juga melaporkan **sebaran** setiap sel (min, bilangan, pecahan negatif), kerana median
sahaja tidak boleh membezakan kesan sebenar daripada beberapa sel terpencil.

Guna: python3 REVERSE/semak_latih.py [--semak]
`--semak` keluar 1 jika mana-mana nombor dalam SEMAKAN_LATIH.md tidak dihasilkan semula.
"""
import argparse
import csv
import statistics as st
from math import comb
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parents[1]
KELUAR = AKAR / 'REVERSE'

# Nombor yang SEMAKAN_LATIH.md dakwa. Toleransi 0.01 mata (laporan 2 desimal).
DAKWA_A = {           # had -> (tahan d_cagr, tahan d_mdd, latih d_cagr, latih d_mdd, % sel)
    '1': (+1.65, +1.60, -0.19, +1.12, 83.3),
    '2': (+0.76, +0.02, +0.04, +0.00, 45.8),
    '3': (+0.47, +0.00, +0.12, +0.00, 33.3),
}
DAKWA_B = {           # saring -> sama
    'A1': (+1.67, +1.47, +0.63, +1.11, 66.7),
    'A2': (+4.26, +0.94, +0.64, +0.64, 66.7),
    'A3': (+6.29, +0.23,  0.00,  0.00, 33.3),
    'A4': (-17.47, +22.09, +0.16, +18.62, 100.0),
}
METRIK = ('cagr', 'mdd', 'cagr_latih', 'mdd_latih')
TOL = 0.011
TOL_PCT = 0.06


def baca(nama):
    with (KELUAR / nama).open() as fh:
        return list(csv.DictReader(fh))


def med_sel(baris, kunci_sel, lajur):
    """Median merentas BENIH bagi setiap sel. Mengganti `groupby(...).median()`."""
    kump = {}
    for r in baris:
        k = tuple(r[c] for c in kunci_sel)
        kump.setdefault(k, []).append(float(r[lajur]))
    return {k: st.median(v) for k, v in kump.items()}, {k: len(v) for k, v in kump.items()}


def kesan(baris, kunci_asas, lajur_var, nilai_asas, lajur_metrik):
    """Δ metrik setiap sel sepadan, lawan `nilai_asas` bagi lajur yang berubah.

    Memulangkan {nilai_var: [senarai Δ setiap sel]}.
    """
    kunci_penuh = list(kunci_asas) + [lajur_var]
    med, nb = med_sel(baris, kunci_penuh, lajur_metrik)
    asas = {k[:-1]: v for k, v in med.items() if k[-1] == nilai_asas}
    out = {}
    for k, v in med.items():
        if k[-1] == nilai_asas:
            continue
        b = asas.get(k[:-1])
        if b is None:
            continue
        out.setdefault(k[-1], []).append(v - b)
    return out, nb


def sebaran(d):
    n = len(d)
    neg = sum(1 for v in d if v < 0)
    return dict(n=n, median=st.median(d), min_=sum(d) / n,
                p_neg=100.0 * neg / n, terkecil=min(d), terbesar=max(d))


def tanda(d):
    """Ujian tanda binomial dua-hujung berpasangan, H0: median Δ = 0. Seri diabaikan."""
    pos = sum(1 for x in d if x > 0)
    neg = sum(1 for x in d if x < 0)
    n = pos + neg
    if n == 0:
        return 0, 0, 1.0
    k = min(pos, neg)
    return pos, n, min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def bh(uji, q=0.05):
    """Benjamini-Hochberg. `uji` = senarai tuple yang elemen terakhirnya p."""
    m = len(uji)
    u = sorted(uji, key=lambda r: r[-1])
    amb = [q * (i + 1) / m for i in range(m)]
    kmax = max([i for i in range(m) if u[i][-1] <= amb[i]], default=-1)
    return u, amb, kmax


def ujian_tanda_semua(K, H):
    """Bahagian 2 — ujian tanda setiap kesan, kemudian BH-FDR merentas KESEMUANYA."""
    uji = []
    for metrik in METRIK:
        med, _ = med_sel(K, ['alam_n', 'masuk', 'urutan', 'slot', 'had'], metrik)
        for hd in ('1', '2', '3'):
            d = [v - med[(a, m, u, s, 'tiada')]
                 for (a, m, u, s, h), v in med.items() if h == hd]
            uji.append((f'A had{hd}', metrik, st.median(d)) + tanda(d))
        med, _ = med_sel(H, ['saring', 'urutan', 'slot', 'had'], metrik)
        for sr in ('A1', 'A2', 'A3', 'A4'):
            d = [v - med[('A0', u, s, h)]
                 for (sg, u, s, h), v in med.items() if sg == sr]
            uji.append((f'B {sr}', metrik, st.median(d)) + tanda(d))
    u, amb, kmax = bh(uji)
    print()
    print('=' * 78)
    print(f'UJIAN TANDA BERPASANGAN + BH-FDR q<=0.05 merentas {len(u)} ujian')
    print('=' * 78)
    print(f'{"":<7}{"lever":<9} {"metrik":<12} {"median":>8} {"+/n":>8} {"p":>9} '
          f'{"amb BH":>8}')
    for i, (lv, mt, md, pos, n, p) in enumerate(u):
        print(f'{"LULUS  " if i <= kmax else "       "}{lv:<9} {mt:<12} {md:>+8.2f} '
              f'{pos:>4}/{n:<3} {p:>9.4f} {amb[i]:>8.4f}')
    lulus = u[:kmax + 1]
    lat = [r for r in lulus if r[1].endswith('latih')]
    nc = sum(1 for r in lat if r[1].startswith('cagr'))
    nm = sum(1 for r in lat if r[1].startswith('mdd'))
    print()
    print(f'{len(lulus)}/{len(u)} melepasi FDR · {len(lat)} ialah LUAR SAMPEL (latih)')
    print(f'  kesan CAGR luar sampel melepasi FDR: {nc}')
    print(f'  kesan MDD  luar sampel melepasi FDR: {nm}')
    for r in lat:
        print(f'    {r[0]:<9} {r[1]:<12} median {r[2]:+.2f}  p={r[5]:.4f}')
    return nc, nm


def degenerat(H):
    """Bahagian 3 — sel `A2`/`A3` x `U02` adalah degenerat ikut binaan (spec §4.1).

    Menyaring ikut `rs_pst` lalu memeringkat ikut `rs_pst` ialah tiada-op, jadi 4
    daripada 12 sel memberi Δ = 0.00 TEPAT dan mencairkan median ke arah sifar.
    """
    print()
    print('=' * 78)
    print('KESAN PENCAIRAN SEL DEGENERAT (A2/A3 x U02 = tiada-op ikut binaan)')
    print('=' * 78)
    print(f'{"sar":<5} {"metrik":<12} {"semua 12":>9} {"tanpa U02":>10} {"beza":>8}')
    for metrik in METRIK:
        med, _ = med_sel(H, ['saring', 'urutan', 'slot', 'had'], metrik)
        for sr in ('A1', 'A2', 'A3', 'A4'):
            d = [(u, v - med[('A0', u, s, h)])
                 for (sg, u, s, h), v in med.items() if sg == sr]
            a = st.median([x for _, x in d])
            b = st.median([x for u, x in d if u != 'U02'])
            tag = '  <<< degenerat' if sr in ('A2', 'A3') else ''
            print(f'{sr:<5} {metrik:<12} {a:>+9.2f} {b:>+10.2f} {b - a:>+8.2f}{tag}')


def lapor(tajuk, baris, kunci_asas, lajur_var, nilai_asas, dakwa, urut):
    print()
    print('=' * 78)
    print(tajuk)
    print('=' * 78)
    gagal = []
    for metrik, lbl in zip(METRIK, ('TAHAN CAGR', 'TAHAN MDD',
                                     'LATIH CAGR', 'LATIH MDD')):
        d, nb = kesan(baris, kunci_asas, lajur_var, nilai_asas, metrik)
        idx = {'cagr': 0, 'mdd': 1, 'cagr_latih': 2, 'mdd_latih': 3}[metrik]
        print()
        print(f'{lbl}  (Δ lawan {nilai_asas})')
        print(f'  {lajur_var:<6} {"n sel":>6} {"median":>9} {"dakwa":>9} {"min":>9} '
              f'{"%<0":>7} {"terkecil":>9} {"terbesar":>9}')
        for v in urut:
            if v not in d:
                continue
            s = sebaran(d[v])
            dk = dakwa[v][idx]
            ok = abs(s['median'] - dk) <= TOL
            if not ok:
                gagal.append(f'{lbl} {v}: kira {s["median"]:+.4f} dakwa {dk:+.2f}')
            print(f'  {v:<6} {s["n"]:>6} {s["median"]:>+9.2f} {dk:>+9.2f} '
                  f'{s["min_"]:>+9.2f} {s["p_neg"]:>6.1f}% {s["terkecil"]:>+9.2f} '
                  f'{s["terbesar"]:>+9.2f}  {"OK" if ok else "<<< BEZA"}')
    # % sel MDD latih mencetek
    d, _ = kesan(baris, kunci_asas, lajur_var, nilai_asas, 'mdd_latih')
    print()
    print('% sel dengan MDD LATIH lebih cetek:')
    for v in urut:
        if v not in d:
            continue
        pct = 100.0 * sum(1 for x in d[v] if x > 0) / len(d[v])
        dk = dakwa[v][4]
        ok = abs(pct - dk) <= TOL_PCT
        if not ok:
            gagal.append(f'% sel {v}: kira {pct:.2f} dakwa {dk:.1f}')
        print(f'  {v:<6} {pct:>6.1f}%  (dakwa {dk:.1f}%)  {"OK" if ok else "<<< BEZA"}')
    semua = [x for v in urut if v in d for x in d[v]]
    print(f'  SEMUA  {100.0 * sum(1 for x in semua if x > 0) / len(semua):>6.1f}%'
          f'  (R2 ambang 50%)')
    return gagal


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--semak', action='store_true')
    a = ap.parse_args(argv)

    K = baca('korelasi.csv')
    H = baca('hierarki.csv')
    print(f'korelasi.csv {len(K)} larian · hierarki.csv {len(H)} larian')
    print('laluan: csv + statistics (pustaka standard), tiada pandas, tiada groupby')

    gagal = []
    gagal += lapor('DAKWAAN A — had industri `KR03` (E5)', K,
                   ['alam_n', 'masuk', 'urutan', 'slot'], 'had', 'tiada',
                   DAKWA_A, ['1', '2', '3'])
    gagal += lapor('DAKWAAN B — saringan berdiri `GB07` (E6)', H,
                   ['urutan', 'slot', 'had'], 'saring', 'A0',
                   DAKWA_B, ['A1', 'A2', 'A3', 'A4'])

    nc, nm = ujian_tanda_semua(K, H)
    degenerat(H)
    if nc:
        gagal.append(f'{nc} kesan CAGR luar sampel melepasi FDR (dijangka 0)')

    print()
    print('=' * 78)
    if gagal:
        print(f'TIDAK DIHASILKAN SEMULA — {len(gagal)} beza:')
        for g in gagal:
            print('  ' + g)
    else:
        print('SEMUA nombor SEMAKAN_LATIH.md dihasilkan semula melalui laluan bebas.')
    print('=' * 78)
    return 1 if (gagal and a.semak) else 0


if __name__ == '__main__':
    sys.exit(main())

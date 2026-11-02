"""Paksi CARA pada KESEMUA enam keluar kohort 94 — pradaftar `REVERSE/SPEC_CARA_94.md`.

`cara_94.csv` mengukur 6 cara pada keluar `X13` sahaja, dan `X13` memegang **6 daripada 94**
slot produksi. Laporan itu menyatakan bakinya ialah ANGGAPAN. Skrip ini menukar anggapan itu
menjadi ukuran: enam keluar yang `jejak_semua.csv` sebenarnya pakai, setiap satu dengan masuk
yang BERPASANGAN dengannya dalam produksi.

Enjin: `step23_cara.py` yang SAMA, dengan `KELUAR_ID` ditukar. Tiada enjin kedua. Peraturan
keluar diterjemahkan daripada `step33_portfolio_94.hari_keluar()`, dan lalai `X13` disemak
bit-identik (md5 `cara.csv`) sebelum larian ini ditafsir.

BH-FDR: `m = 30` (5 cara x 6 keluar) dikira SEKALI merentas kesemua 30 p-value yang
dikumpul, bukan enam kali secara berasingan. Spec §3 menetapkannya sebelum keputusan dilihat.

`cara.csv` dan `CARA.md` yang dikomit TIDAK ditulis ganti: ia disimpan dan dipulihkan sekitar
setiap larian, kerana `REVERSE/strategi.py --semak` membacanya dan akan gagal dalam CI jika
ia hanyut.

Guna: python3 REVERSE/step38_cara_94.py [--keluar X36,X16] [--laporan-sahaja]
Output: REVERSE/CARA_KELUAR_94.md, REVERSE/cara_keluar_94.csv
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
import REVERSE.step18_nxx as S18  # noqa: E402
import REVERSE.step23_cara as S23  # noqa: E402

RV = AKAR / 'REVERSE'
JEJAK = RV / 'jejak_semua.csv'
KELUAR_SEMUA = ['X36', 'X16', 'X17', 'X14', 'X13', 'X15']   # urutan bilangan slot
M_PRADAFTAR = 30                      # spec §3: 5 cara x 6 keluar
ALT = [k for k in S23.KOD if k != 'C01']
SIMPAN = ('cara.csv', 'CARA.md')


def kolam_keluar():
    """{keluar: [masuk, ...]} daripada fail keputusan produksi, bukan tangan."""
    J = list(csv.DictReader(open(JEJAK, encoding='utf-8')))
    assert J, 'jejak_semua.csv kosong'
    out = {}
    for x in J:
        out.setdefault(x['keluar'], set()).add(x['masuk'])
    return {k: sorted(v) for k, v in out.items()}


def lari_satu(kid, masuk):
    """Jalankan enjin CARA sekali bagi satu keluar; pulangkan baris mentah."""
    asal = {n: (RV / n).read_bytes() for n in SIMPAN if (RV / n).exists()}
    S23.KELUAR_ID = kid
    S23.KOLAM3 = masuk
    try:
        (RV / 'cara.csv').unlink(missing_ok=True)
        rc = S23.main([])
        if rc:
            raise SystemExit(f'{kid}: enjin CARA pulang {rc}')
        R = list(csv.DictReader(open(RV / 'cara.csv', encoding='utf-8')))
    finally:
        for n, b in asal.items():
            (RV / n).write_bytes(b)
        for n in SIMPAN:                       # fail yang tiada asal -> jangan tinggalkan
            if n not in asal:
                (RV / n).unlink(missing_ok=True)
    for r in R:
        r['keluar'] = kid
        r['n_masuk'] = len(masuk)
        for g in ('CARA1', 'CARA2', 'CARA3'):  # dikira m=6 per-keluar; dibuang, dikira semula
            r.pop(g, None)
    return R


def gate(R):
    """Gate spec §3 dengan BH-FDR dikira SEKALI merentas kesemua 30 p-value."""
    T = {(r['keluar'], r['cara']): r for r in R if r['tingkap'] == 'tahan'}
    L = {(r['keluar'], r['cara']): r for r in R if r['tingkap'] == 'latih'}
    kunci = [(k, c) for k in sorted({x['keluar'] for x in R}) for c in ALT if (k, c) in T]
    p = np.array([float(T[q]['p']) for q in kunci], dtype='float64')
    lulus2, amb = S18.bh_m(p, M_PRADAFTAR)
    G = {}
    for i, q in enumerate(kunci):
        g1 = float(T[q]['beza']) > 0 and q in L and float(L[q]['beza']) > 0
        G[q] = (bool(g1), bool(lulus2[i]), float(T[q]['jangkaan_sig']) > 0)
    for r in R:
        q = (r['keluar'], r['cara'])
        g = G.get(q, (False, False, False))
        r['CARA1'], r['CARA2'], r['CARA3'] = (str(g[0]), str(g[1]), str(g[2]))
        r['MENANG'] = str(all(g))
    return G, amb, len(kunci)


def laporan(R, G, amb, nk):
    D = pd.DataFrame(R)
    for c in D.columns:
        if c not in ('cara', 'tingkap', 'keluar', 'CARA1', 'CARA2', 'CARA3', 'MENANG'):
            D[c] = pd.to_numeric(D[c], errors='coerce')
    D.to_csv(RV / 'cara_keluar_94.csv', index=False, float_format='%.6f')

    slot = {k: v for k, v in
            pd.read_csv(JEJAK).groupby('keluar').size().items()}
    menang = sorted(q for q, g in G.items() if all(g))
    L = ['# Paksi CARA pada KESEMUA enam keluar kohort 94', '',
         'Pradaftar `REVERSE/SPEC_CARA_94.md` — dikomit sebelum keputusan dilihat.',
         f'BH-FDR dikira SEKALI merentas {nk} perbandingan (m dipradaftar = '
         f'{M_PRADAFTAR}); ambang BH p = {amb}.',
         '', '## Gate — ringkasan setiap keluar', '',
         '| Keluar | Slot produksi | Masuk | CARA1 | CARA2 | CARA3 | MENANG |',
         '|---|--:|--:|--:|--:|--:|--:|']
    for k in KELUAR_SEMUA:
        q = [(k, c) for c in ALT if (k, c) in G]
        if not q:
            continue
        nm = int(D[(D.keluar == k) & (D.tingkap == 'tahan')].n_masuk.iloc[0])
        L.append(f'| `{k}` | {slot.get(k, 0)} | {nm} | '
                 f'{sum(G[x][0] for x in q)}/5 | {sum(G[x][1] for x in q)}/5 | '
                 f'{sum(G[x][2] for x in q)}/5 | '
                 f'{sum(all(G[x]) for x in q)}/5 |')
    L += ['', f'**LULUS KETIGA-TIGA GATE: {len(menang)} daripada {nk}** — '
          + (', '.join(f'`{a}x{b}`' for a, b in menang) if menang else 'tiada.'), '']

    L += ['## Jangkaan setiap ISYARAT, tingkap TAHAN (bar tidak terisi = 0)', '',
          '| Keluar | ' + ' | '.join(f'`{c}`' for c in S23.KOD) + ' | sebaran |',
          '|---|' + '--:|' * (len(S23.KOD) + 1)]
    for k in KELUAR_SEMUA:
        g = D[(D.keluar == k) & (D.tingkap == 'tahan')].set_index('cara')
        if g.empty:
            continue
        v = [float(g.loc[c, 'jangkaan_sig']) if c in g.index else np.nan for c in S23.KOD]
        bk = S23.KOD[int(np.nanargmax(v))]
        L.append(f'| `{k}` | ' + ' | '.join(
            ('**' + f'{x:+.3f}%' + '**' if S23.KOD[i] == bk else f'{x:+.3f}%')
            for i, x in enumerate(v))
            + f' | {np.nanmax(v) - np.nanmin(v):.3f} mata |')
    L += ['', 'Tebal = cara terbaik setiap keluar pada ukuran setiap ISYARAT.', '']

    L += ['## Jangkaan setiap ISIAN, tingkap TAHAN (hanya bar yang terisi)', '',
          '| Keluar | ' + ' | '.join(f'`{c}`' for c in S23.KOD) + ' |',
          '|---|' + '--:|' * len(S23.KOD)]
    for k in KELUAR_SEMUA:
        g = D[(D.keluar == k) & (D.tingkap == 'tahan')].set_index('cara')
        if g.empty:
            continue
        L.append(f'| `{k}` | ' + ' | '.join(
            f'{float(g.loc[c, "jangkaan_isi"]):+.3f}%' if c in g.index else '-'
            for c in S23.KOD) + ' |')
    L += ['', '**Kadar isian setiap keluar** (bar isyarat yang benar-benar menjadi posisi):',
          '', '| Keluar | ' + ' | '.join(f'`{c}`' for c in S23.KOD) + ' |',
          '|---|' + '--:|' * len(S23.KOD)]
    for k in KELUAR_SEMUA:
        g = D[(D.keluar == k) & (D.tingkap == 'tahan')].set_index('cara')
        if g.empty:
            continue
        L.append(f'| `{k}` | ' + ' | '.join(
            f'{float(g.loc[c, "kadar_isi"]):.1f}%' if c in g.index else '-'
            for c in S23.KOD) + ' |')
    L += ['', 'Jurang antara dua jadual di atas ialah sebab `jangkaan_isi` tidak boleh '
          'dibaca sendirian: `C03`/`C04` hanya terisi apabila harga JATUH, jadi jangkaan '
          'setiap isian yang tinggi boleh datang daripada pemilihan bar, bukan kelebihan.',
          '']
    (RV / 'CARA_KELUAR_94.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', default=','.join(KELUAR_SEMUA))
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = RV / 'cara_keluar_94.csv'
    if a.laporan_sahaja and f.exists():
        R = list(csv.DictReader(open(f, encoding='utf-8')))
        G, amb, nk = gate(R)
        return laporan(R, G, amb, nk)

    KK = kolam_keluar()
    pilih = [k for k in a.keluar.split(',') if k]
    hilang = [k for k in pilih if k not in KK]
    if hilang:
        raise SystemExit(f'keluar tiada dalam jejak_semua.csv: {hilang}')
    R, t0 = [], time.time()
    for i, k in enumerate(pilih):
        print(f'\n===== {i + 1}/{len(pilih)} keluar {k} '
              f'({len(KK[k])} masuk) [{time.time() - t0:.0f}s]', flush=True)
        R += lari_satu(k, KK[k])
    G, amb, nk = gate(R)
    return laporan(R, G, amb, nk)


if __name__ == '__main__':
    raise SystemExit(main())

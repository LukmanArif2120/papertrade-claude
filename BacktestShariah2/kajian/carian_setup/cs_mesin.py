"""Carian setup — MESIN berkala (SPEC pindaan 14 Nov 2026 (n), bahagian (c)): "mesin sentiasa mencari dan menala".

Setiap larian menarik kelompok varian BAHARU (benih = nombor larian): satu varian rawak julat penuh bagi setiap kaedah M dan
12 set parameter rawak (termasuk di luar grid) bagi setiap keluarga K; menskor pada kumpulan A dengan peraturan pindaan (n)(a)
(sasaran `terus`, enjin prasyarat x penapis); menilai yang terbaik pada kumpulan B; dan MENAMBAH ke papan terkumpul
`hasil/MESIN/papan.csv` (tambah-sahaja) serta menjana `hasil/MESIN/LAPORAN.md`. Papan disusun ikut skor A; lajur B ialah
semakan, bukan kunci susunan. Mesin TIDAK mendaftar setup ke papertrade dan tidak menyentuh Lejar, kad skor atau kohort F.
Guna: python3 cs_mesin.py <kerja> [n_m]     (n_m = had bilangan kaedah M setiap larian; lalai semua)
      python3 cs_mesin.py lapor             (jana semula laporan daripada papan)"""
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_param as kp  # noqa: E402
import cs_tala7 as t7  # noqa: E402

N_K, N_NILAI_B, V_ASAS = 12, 15, 1000            # dikunci pindaan (n): 12 varian setiap keluarga K; 15 terbaik dinilai pada B
D_MESIN = os.path.join(SINI, 'hasil', 'MESIN')
PAPAN = os.path.join(D_MESIN, 'papan.csv')
LAJUR = ['larian', 'tarikh', 'nama', 'induk', 'pencetus', 'param', 'prasyarat', 'penapis', 'skor_A', 'n_E1', 'n_E2',
         'n_B', 'terus_B', 'asas_B', 'kl_K1', 'kl_K2', 'kl_K3']
KUNCI = ('K1', 'K2', 'K3')


def baca_papan():
    return pd.read_csv(PAPAN) if os.path.exists(PAPAN) else pd.DataFrame(columns=LAJUR)


def kelompok(n, n_m=None):
    """(grid K, tugas M) larian ke-n. Benih tetap: larian yang sama sentiasa menarik varian yang sama."""
    rng = np.random.default_rng([atom.BENIH, 77, n])
    G = [(f'{fam}.r{n}_{i}', fam, kp.rawak(fam, rng)) for fam in kp.KELUARGA for i in range(1, N_K + 1)]
    pj = pd.read_csv(os.path.join(cari.AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    mid = sorted({t[1] for t in cari.senarai_benih() if t[1].startswith('M')})
    if n_m:
        mid = sorted(rng.choice(mid, min(n_m, len(mid)), replace=False).tolist())
    tugas = [(f'{m}.{V_ASAS + n}', m, cari.param_varian(pj, m, V_ASAS + n)) for m in mid]
    return G, [t for t in tugas if t[2]]


def _ev_m(kerja, set_, fail):
    pan = cari.panel(kerja, set_)
    bn = pickle.load(open(os.path.join(kerja, fail), 'rb'))
    N = len(pan['c'])
    return {n: np.flatnonzero(atom.mula_isyarat(np.unpackbits(b)[:N].astype(bool), pan['mula']) & pan['sah'])
            for n, b in bn['sig'].items()}


def larian(kerja, n_m=None):
    os.makedirs(kerja, exist_ok=True)
    os.makedirs(D_MESIN, exist_ok=True)
    papan = baca_papan()
    n = int(papan.larian.max()) + 1 if len(papan) else 1
    for s in ('A', 'B'):
        cari.panel(kerja, s)
    if not os.path.exists(os.path.join(kerja, 'lapis_A.pkl')):
        lapis.bina(kerja)
    G, tugas = kelompok(n, n_m)
    cari.log(f'mesin larian {n}: {len(G)} varian K, {len(tugas)} varian M')
    ev = t7.keluarga_grid(kerja, 'A', G)
    cari.benih(kerja, 'A', tugas=tugas, fail=f'benih_A_mesin{n}.pkl')
    ev.update(_ev_m(kerja, 'A', f'benih_A_mesin{n}.pkl'))
    S = t7.skor_ev(kerja, ev)
    teks = {nama: kp.teks(fam, p) for nama, fam, p in G}
    param = {nama: p for nama, _, p in G}
    param.update({nama: P for nama, _, P in tugas})
    baris = []
    for nama, r in S.items():
        if not r.get('cukup') or not len(r['atas'][0]) or not np.isfinite(r['atas'][1][0]):
            continue
        q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(r['atas'][0][:1]))
        baris.append(dict(larian=n, tarikh=pd.Timestamp.now('UTC').strftime('%Y-%m-%d'), nama=nama, induk=t7.induk(nama),
                          pencetus=teks.get(nama, f'kaedah {t7.induk(nama)} (varian rawak)'),
                          param=json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in param[nama].items()},
                                           sort_keys=True),
                          prasyarat=c5.tk_pra(q1, q2, kod=True), penapis=c5.tk_pen(f1, f2), skor_A=round(float(r['atas'][1][0]), 5),
                          n_E1=r['n_ev'][0], n_E2=r['n_ev'][1], _q=(q1, q2, f1, f2)))
    T = pd.DataFrame(baris).sort_values(['skor_A', 'nama'], ascending=[False, True], kind='stable').reset_index(drop=True)
    atas = T[T.skor_A > 0].head(N_NILAI_B)
    if len(atas):
        panB = cari.panel(kerja, 'B')
        L = lapis.muat(kerja, 'B')
        Lr, V = (L['L1'], L['L2']), t7.label_terus(panB)
        evB = {}
        gk = [g for g in G if g[0] in set(atas.nama)]
        if gk:
            evB.update(t7.keluarga_grid(kerja, 'B', gk))
        tm = [t for t in tugas if t[0] in set(atas.nama)]
        if tm:
            cari.benih(kerja, 'B', tugas=tm, fail=f'benih_B_mesin{n}.pkl')
            evB.update(_ev_m(kerja, 'B', f'benih_B_mesin{n}.pkl'))
        for i, r in atas.iterrows():
            e = evB[r.nama]
            k = t7.kadar7(panB, V, e[c5.topeng(panB, Lr, e, *r._q)])
            T.loc[i, ['n_B', 'terus_B', 'asas_B']] = [k[-1][0], round(k[-1][1], 5), round(k[-1][2], 5)]
            for j, t in enumerate(KUNCI):
                T.loc[i, f'kl_{t}'] = round(k[j][1] - k[j][2], 5) if k[j][0] else np.nan
    T = T.drop(columns='_q').reindex(columns=LAJUR)
    pd.concat([papan, T], ignore_index=True).to_csv(PAPAN, index=False)
    cari.log(f"mesin larian {n}: {len(T)} varian berskor ditambah; skor A terbaik {T.skor_A.max() * 100:+.2f} mata ({T.nama.iloc[0]})")
    lapor()


def lapor():
    P = baca_papan()
    if not len(P):
        return
    p = lambda x, t=True: '–' if x != x else (f'{x * 100:+.1f}' if t else f'{x * 100:.1f}')
    try:
        sys.path.insert(0, os.path.join(cari.AKAR, 'BacktestShariah2', 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    S = P.sort_values(['skor_A', 'nama'], ascending=[False, True], kind='stable')
    S = S[S.groupby('induk').cumcount() < 2].head(30)
    dinilai = P[P.n_B.notna()]
    tahan = dinilai[(dinilai[['kl_K1', 'kl_K2', 'kl_K3']] > 0).all(axis=1) & (dinilai.n_B >= 300)]
    A = ['# Mesin carian setup — papan terkumpul (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_mesin.py` (workflow `mesin_carian.yml`). Peraturan dikunci dalam '
         '`kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(c). **Jangan sunting secara manual; `papan.csv` tambah-sahaja.**', '',
         f"- Larian setakat ini: **{int(P.larian.max())}** (terakhir {P.tarikh.max()}); varian berskor terkumpul: **{len(P):,}** "
         f"({int((P.induk.str[0] == 'M').sum()):,} kaedah M, {int((P.induk.str[0] == 'K').sum()):,} keluarga indikator).",
         f"- Skor A > 0: {int((P.skor_A > 0).sum()):,}. Dinilai pada saham tidak dilihat (15 terbaik setiap larian): {len(dinilai)}; "
         f"mengatasi rawak dalam K1, K2 DAN K3 dengan belian ≥ 300: **{len(tahan)}**.",
         '- Skor A = min dua era carian bagi [kelebihan kadar "naik lagi" atas saham rawak hari sama − 2 ralat piawai]. Semakin '
         'banyak varian dicuba, semakin melambung skor A terbaik; lajur B yang dibaca.', '',
         '## 30 teratas ikut skor A (maks 2 setiap induk)', '',
         '| # | Larian | Pencetus | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 |',
         '|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(S.itertuples(), 1):
        b = ('–', '–', '–') if r.n_B != r.n_B else (f'{int(r.n_B):,}', f'{p(r.terus_B, False)} ({p(r.asas_B, False)})',
                                                    f'{p(r.kl_K1)} / {p(r.kl_K2)} / {p(r.kl_K3)}')
        A.append(f"| {i} | {r.larian} | `{r.nama}` {r.pencetus} | {r.prasyarat if isinstance(r.prasyarat, str) else '–'} | "
                 f"{r.penapis if isinstance(r.penapis, str) else '–'} | {p(r.skor_A)} | {b[0]} | {b[1]} | {b[2]} |")
    A += ['', '## Setiap larian', '', '| Larian | Tarikh | Varian berskor | Skor A > 0 | Skor A terbaik | Dinilai pada B | Bertahan K1–K3 |',
          '|---|---|---|---|---|---|---|']
    for n, g in P.groupby('larian'):
        d = g[g.n_B.notna()]
        A.append(f"| {n} | {g.tarikh.iloc[0]} | {len(g)} | {int((g.skor_A > 0).sum())} | {p(g.skor_A.max())} | {len(d)} | "
                 f"{int(((d[['kl_K1', 'kl_K2', 'kl_K3']] > 0).all(axis=1) & (d.n_B >= 300)).sum())} |")
    A += ['', 'Kaveat: kumpulan B sudah dilihat berkali-kali (bukan tahanan bersih); tiada saham delist; setup di sini BUKAN '
          'calon papertrade tanpa keputusan pengguna berasingan.', '']
    open(os.path.join(D_MESIN, 'LAPORAN.md'), 'w', encoding='utf-8').write('\n'.join(A))


if __name__ == '__main__':
    if sys.argv[1] == 'lapor':
        lapor()
    else:
        larian(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)

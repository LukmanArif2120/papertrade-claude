"""Carian setup — analisis PENGESAHAN "higher high baru entry" (SPEC pindaan 14 Nov 2026 (ac), asalnya (r) di cawangan lama
`claude/dreamy-lovelace-38z7wm`; diminta pengguna). Dibawa ke `main` 16 Nov 2026; hasil 14 Nov 2026 TIDAK dijana semula.

(2) Pencetus sedia ada ikut gaya masuk (beli semasa lemah / pengesahan pembalikan / undur dalam uptrend / pengesahan kekuatan
    atau higher high): kelebihan kadar tangkap pencetus SAHAJA pada kumpulan B bagi `terus` (swing) dan `besar` (trend).
(3) Lapisan pengesahan atas setup F sedia ada: V0 beli buka esok; S1 tutup sahkan (tutup > tinggi hari isyarat dalam 3 sesi,
    beli buka berikutnya); S2 pecah tinggi (buy-stop pada tinggi hari isyarat dalam 3 sesi). Diukur dari harga beli sebenar.
Guna: python3 cs_sahkan.py <kerja>. Keluaran: hasil/PENGESAHAN.md, PENGESAHAN.csv, PENGESAHAN_keluarga.csv."""
import os
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_cs07 as c7  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_param as kp  # noqa: E402
import cs_pegang as pg  # noqa: E402
import cs_portfolio6 as p6  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402
import cs_trend8 as t8  # noqa: E402

N_SAH, JARAK = 3, 24                    # tetingkap pengesahan (sesi) dan jarak minimum antara isyarat satu saham (dikunci (ac))
GAYA = {'beli semasa lemah (tiada pengesahan)': ('K01', 'K03', 'K06', 'K18'),
        'pengesahan pembalikan (lemah lalu berpatah naik)': ('K02', 'K04', 'K13', 'K24'),
        'undur dalam uptrend': ('K17', 'K22'),
        'pengesahan kekuatan / higher high (pecah tinggi, silang naik, gap)': (
            'K05', 'K07', 'K08', 'K09', 'K10', 'K11', 'K12', 'K14', 'K15', 'K16', 'K19', 'K20', 'K23', 'K25'),
        'lain (julat sempit)': ('K21',)}


def sahkan(pan, ev):
    """Bagi isyarat bar t: (d1, b2, p2). d1 = bar pertama dalam t+1..t+3 dengan tutup > tinggi[t] (-1 jika tiada);
    b2 = bar pertama dengan tinggi > tinggi[t]; p2 = harga beli buy-stop = max(buka[b2], tinggi[t])."""
    h, c, o = pan['h'], pan['c'], pan['o']
    d1 = np.full(len(ev), -1, np.int64)
    b2 = np.full(len(ev), -1, np.int64)
    p2 = np.zeros(len(ev))
    for j in range(1, N_SAH + 1):
        bar = ev + j
        m = (d1 < 0) & (c[bar] > h[ev])
        d1[m] = bar[m]
        m = (b2 < 0) & (h[bar] > h[ev])
        b2[m] = bar[m]
        p2[m] = np.maximum(o[bar[m]], h[ev[m]])
    return d1, b2, p2


def _ukur(St, s, kol):
    R = k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, s, kol)[0]
    lab = St[7]
    if not len(R):
        return dict(n=0, m5=np.nan, terus=np.nan, tp=np.nan, menang=np.nan, rugi8=np.nan, purata=np.nan), R, lab
    return dict(n=len(R), m5=float((lab[:, 0] > 0).mean()), terus=float((lab[:, 1] > 0).mean()),
                tp=float(((lab[:, 0] > 0) & (R >= 0.10)).mean()), menang=float((R > 0).mean()),
                rugi8=float((R <= -0.08).mean()), purata=float(R.mean())), R, lab


def setup_f(kerja, pan, Lr):
    """(id, dipercayai, isyarat masuk kumpulan B, henti, lajur keluar) bagi setiap setup kedudukan akhir."""
    EV = cari.pencetus(pan, __import__('pickle').load(open(os.path.join(kerja, 'benih_B.pkl'), 'rb')))
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    ked = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv'))
    out = []
    for q in ked.itertuples():
        r = reg.loc[q.id]
        if r.pusingan == 'CS07':
            d = c7.dari_takrif7(r.takrif)
            ev = t7.ev_satu(kerja, 'B', d['pencetus'])
        else:
            d = p6.dari_takrif5(r.takrif)
            ev = EV[d['pencetus']]
            d['s'], d['kol'] = pg.lama_ke_baharu(d['lajur'])
        out.append((q.id, bool(q.dipercayai), int(q.kedudukan), ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])],
                    d['s'], d['kol']))
    return out


def lapisan(kerja):
    import cs_lapis as lapis
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr, XA = (L['L1'], L['L2']), k7.siri_set(kerja, 'B')
    akhir = pan['mula'][pan['tid'] + 1]
    baris = []
    for fid, dp, ked, e0, s, kol in setup_f(kerja, pan, Lr):
        e0 = e0[e0 + N_SAH + k7.TMAX + 1 < akhir[e0]]
        e0 = e0[teras.satu_posisi(e0, np.full(len(e0), JARAK - 1), pan['tid'])]
        if len(e0) < 30:
            continue
        d1, b2, p2 = sahkan(pan, e0)
        m1, m2 = d1 >= 0, b2 >= 0
        v0, R0, lab0 = _ukur(k7.sedia_pan(pan, XA, e0), s, kol)
        s1, _, _ = _ukur(k7.sedia_pan(pan, XA, d1[m1]), s, kol)
        s2, _, _ = _ukur(k7.sedia_pan(pan, XA, b2[m2] - 1, px=p2[m2]), s, kol)
        b = {'id': fid, 'kedudukan': ked, 'dipercayai': dp, 'isyarat': len(e0), 'sah1': float(m1.mean()), 'sah2': float(m2.mean()),
             'premium1': float((pan['o'][d1[m1] + 1] / pan['o'][e0[m1] + 1] - 1).mean()) if m1.any() else np.nan,
             'premium2': float((p2[m2] / pan['o'][e0[m2] + 1] - 1).mean()) if m2.any() else np.nan,
             # isyarat yang sama dibeli cara V0: yang kemudian disahkan (S2) lawan yang tidak
             'v0_terus_sah': float((lab0[m2, 1] > 0).mean()) if m2.any() else np.nan,
             'v0_terus_tak': float((lab0[~m2, 1] > 0).mean()) if (~m2).any() else np.nan,
             'v0_purata_sah': float(R0[m2].mean()) if m2.any() else np.nan,
             'v0_purata_tak': float(R0[~m2].mean()) if (~m2).any() else np.nan}
        for nama, v in (('v0', v0), ('s1', s1), ('s2', s2)):
            b.update({f'{k_}_{nama}': x for k_, x in v.items()})
        baris.append(b)
    return pd.DataFrame(baris)


def gaya(kerja):
    """Kelebihan pencetus SAHAJA (tanpa prasyarat/penapis) setiap varian keluarga K pada kumpulan B, dua label."""
    pan = cari.panel(kerja, 'B')
    V = t7.label_terus(pan)
    S8, V8, _, _ = t8.label_v(pan)
    ev = t7.keluarga(kerja, 'B')['ev']
    peta = {f: g for g, fs in GAYA.items() for f in fs}
    baris = []
    for nama, fam, p in kp.grid():
        e = ev[nama]
        k = t7.kadar7(pan, V, e)[-1]
        e8 = e[S8[e]]
        e8 = e8[teras.satu_posisi(e8, np.full(len(e8), t8.H_MAX - 1), pan['tid'])]
        baris.append(dict(nama=nama, keluarga=fam, gaya=peta[fam], teks=kp.teks(fam, p), n=k[0],
                          terus=k[1], a_terus=k[2], kl_terus=k[1] - k[2] if k[0] else np.nan, n8=len(e8),
                          besar=float(V8[e8, 0].mean()) if len(e8) else np.nan,
                          kl_besar=float((V8[e8, 0] - V8[e8, 1]).mean()) if len(e8) else np.nan))
    return pd.DataFrame(baris)


def main(kerja):
    T = lapisan(kerja)
    G = gaya(kerja)
    d_ = os.path.join(SINI, 'hasil')
    T.to_csv(os.path.join(d_, 'PENGESAHAN.csv'), index=False, float_format='%.5f')
    G.to_csv(os.path.join(d_, 'PENGESAHAN_keluarga.csv'), index=False, float_format='%.5f')
    Y = T[T.dipercayai]
    p = lambda x, k=1, t=False: '–' if x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    md = lambda kol, D=Y: float(D[kol].median())
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    lulus = {v: int(((Y[f'terus_{v}'] > Y.terus_v0) & (Y[f'tp_{v}'] > Y.tp_v0)).sum()) for v in ('s1', 's2')}
    A = ['# Analisis pengesahan: "tunggu confirmation, contohnya higher high, baru entry" (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_sahkan.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (ac) [asalnya (r) di cawangan lama], dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.** Amalan pakar dan sumber: `kajian/KAJIAN_PENGESAHAN.md`.', '',
         '## 1. Gaya masuk yang mana lebih kerap menangkap? (pencetus SAHAJA, tanpa prasyarat atau penapis; kumpulan B)', '',
         'Setiap baris = median merentas semua varian parameter keluarga dalam gaya itu. Kelebihan = kadar tangkap pencetus tolak '
         'saham rawak hari sama (mata peratus). Swing = naik ≥ 5 % minggu pertama dan naik lagi hingga minggu ke-4; trend = naik '
         '≥ 50 % sebelum jatuh 15 % dalam 6 bulan.', '',
         '| Gaya masuk | Varian | Swing: kelebihan median | Swing: % varian > 0 | Trend: kelebihan median | Trend: % varian > 0 |',
         '|---|---|---|---|---|---|']
    for g_ in GAYA:
        d = G[G.gaya == g_]
        A.append(f"| {g_} | {len(d)} | {p(d.kl_terus.median(), 2, True)} | {(d.kl_terus > 0).mean():.0%} | "
                 f"{p(d.kl_besar.median(), 2, True)} | {(d.kl_besar > 0).mean():.0%} |")
    hh = G[G.keluarga == 'K10']
    A += ['', f"- Keluarga `K10` (pecah tinggi n hari = \"higher high\" paling terus, {len(hh)} varian): swing kelebihan median "
          f"{p(hh.kl_terus.median(), 2, True)} mata ({(hh.kl_terus > 0).mean():.0%} varian > 0); trend {p(hh.kl_besar.median(), 2, True)} "
          f"mata ({(hh.kl_besar > 0).mean():.0%} > 0).",
          '- Lima varian terbaik setiap label:', '']
    for lab, kol in (('swing', 'kl_terus'), ('trend', 'kl_besar')):
        t5 = G[G.n >= 300].sort_values(kol, ascending=False).head(5)
        A.append(f"  - {lab}: " + '; '.join(f"{r.teks} ({p(getattr(r, kol), 1, True)})" for r in t5.itertuples()))
    A += ['', f'## 2. Lapisan pengesahan atas setup F ({len(T)} setup; kumpulan B; isyarat yang sama bagi ketiga-tiga cara)', '',
          '- **V0** = beli pada buka esok (cara sekarang). **S1** = tunggu satu TUTUP di atas tinggi hari isyarat dalam 3 sesi, beli '
          'pada buka berikutnya. **S2** = letak buy-stop pada tinggi hari isyarat; dibeli sebaik harga melepasinya dalam 3 sesi. '
          'Jika tiada pengesahan, tiada belian. Semua kadar diukur dari harga beli sebenar; henti dan keluar setup sendiri.', '',
          f'Median {len(Y)} setup dipercayai:', '',
          '| Cara | % isyarat dibeli | Harga beli lawan V0 | Naik ≥ 5 % minggu 1 % | **Naik lagi hingga minggu 4 %** | Tangkap penuh % | '
          'Menang % | Rugi ≥ 8 % % | Purata % |', '|---|---|---|---|---|---|---|---|---|',
          f"| V0 beli buka esok | 100 | – | {p(md('m5_v0'))} | **{p(md('terus_v0'))}** | {p(md('tp_v0'))} | {p(md('menang_v0'), 0)} | "
          f"{p(md('rugi8_v0'))} | {p(md('purata_v0'), 2, True)} |",
          f"| S1 tutup sahkan | {p(md('sah1'), 0)} | {p(md('premium1'), 1, True)} % | {p(md('m5_s1'))} | **{p(md('terus_s1'))}** | "
          f"{p(md('tp_s1'))} | {p(md('menang_s1'), 0)} | {p(md('rugi8_s1'))} | {p(md('purata_s1'), 2, True)} |",
          f"| S2 pecah tinggi (buy-stop) | {p(md('sah2'), 0)} | {p(md('premium2'), 1, True)} % | {p(md('m5_s2'))} | "
          f"**{p(md('terus_s2'))}** | {p(md('tp_s2'))} | {p(md('menang_s2'), 0)} | {p(md('rugi8_s2'))} | {p(md('purata_s2'), 2, True)} |", '',
          f"- **Bacaan dikunci** (kadar \"naik lagi\" DAN tangkap penuh lebih tinggi daripada V0 bagi lebih separuh setup dipercayai): "
          f"S1 {lulus['s1']} daripada {len(Y)} → **{'MENOLONG' if lulus['s1'] > len(Y) / 2 else 'TIDAK menolong'}**; S2 {lulus['s2']} "
          f"daripada {len(Y)} → **{'MENOLONG' if lulus['s2'] > len(Y) / 2 else 'TIDAK menolong'}**.",
          f"- Bilangan tangkapan mutlak (kadar × belian), median lawan V0: S1 {p(float(((Y.terus_s1 * Y.n_s1) / (Y.terus_v0 * Y.n_v0)).median()) - 1, 0, True)} %, "
          f"S2 {p(float(((Y.terus_s2 * Y.n_s2) / (Y.terus_v0 * Y.n_v0)).median()) - 1, 0, True)} %.",
          f"- Adakah pengesahan memisahkan yang jadi daripada yang gagal? Isyarat yang SAMA, dibeli cara V0: yang kemudian memecah "
          f"tinggi hari isyarat → \"naik lagi\" {p(md('v0_terus_sah'))} %, purata {p(md('v0_purata_sah'), 2, True)} %; yang tidak → "
          f"{p(md('v0_terus_tak'))} %, purata {p(md('v0_purata_tak'), 2, True)} %.", '',
          '## 3. Setiap setup dipercayai', '',
          '| # | ID | Dibeli S1 / S2 % | Naik lagi %: V0 / S1 / S2 | Tangkap penuh %: V0 / S1 / S2 | Menang %: V0 / S1 / S2 | '
          'Rugi ≥ 8 %: V0 / S1 / S2 | Purata %: V0 / S1 / S2 |', '|---' * 8 + '|']
    for r in Y.sort_values('kedudukan').itertuples():
        A.append(f"| {r.kedudukan} | `{r.id}` | {p(r.sah1, 0)} / {p(r.sah2, 0)} | {p(r.terus_v0)} / {p(r.terus_s1)} / {p(r.terus_s2)} | "
                 f"{p(r.tp_v0)} / {p(r.tp_s1)} / {p(r.tp_s2)} | {p(r.menang_v0, 0)} / {p(r.menang_s1, 0)} / {p(r.menang_s2, 0)} | "
                 f"{p(r.rugi8_v0, 0)} / {p(r.rugi8_s1, 0)} / {p(r.rugi8_s2, 0)} | {p(r.purata_v0, 2, True)} / "
                 f"{p(r.purata_s1, 2, True)} / {p(r.purata_s2, 2, True)} |")
    A += ['', 'Kaveat: kumpulan B sudah dilihat; tiada saham delist; S2 mengandaikan pesanan buy-stop terisi pada harga pencetus '
          '(tiada gelinciran); prasyarat (cth. earnings 1–5 sesi) dinilai pada hari isyarat, jadi belian yang ditangguh boleh jatuh '
          'selepas tarikh earnings. Backtest sahaja.', '']
    open(os.path.join(d_, 'PENGESAHAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"pengesahan: {len(T)} setup; S1 lulus {lulus['s1']}/{len(Y)}, S2 lulus {lulus['s2']}/{len(Y)}")
    return T, G


if __name__ == '__main__':
    main(sys.argv[1])

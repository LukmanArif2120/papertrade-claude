"""Carian setup — pusingan CS22 (SPEC pindaan 17 Nov 2026 (ai)): setup sepanjang tahun yang dipangkatkan ikut ukuran kedua.

Sasaran = label `c10` (pindaan (ah)): selepas beli, tutup >= +10 % sebelum harga menyentuh -8 %, dalam 63 sesi. Ruang, syarat
kekerapan mingguan dan enjin skor = CS20 (`cs_mingguan20`) tanpa perubahan; hanya label yang ditukar. "Lulus" pada kumpulan B =
kelebihan `c10` > 0 dalam K1, K2 dan K3; pendaftaran juga memerlukan `arah10` > 0 dan bukan kembar kod sedia ada (termasuk
748 kod CS20). Kod F2803 dst., pusingan CS22.
Guna: python3 cs_capai22.py skor|calon|kunci|lapor|daftar <kerja>. Jangan sunting keluaran secara manual."""
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_capai21 as c21  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_daftar13 as d13  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_mingguan20 as m20  # noqa: E402
import cs_tala7 as t7  # noqa: E402

BENIH_KAWALAN = 20261118                                             # dikunci pindaan (ai); selebihnya = pemalar CS20 / CS21
PUSINGAN_SEDIA = ('CS13', 'CS20')                                    # kod format CS13 yang dikira "sedia ada" bagi semakan kembar
PUS, ID_MULA, TARIKH_DAFTAR = 'CS22', 2803, '2026-11-17'
MIN_BELIAN, MIN_TAHUN = 300, 10
N_PAPAR = 60
L21 = ('n21', 'tahun21', 'c10', 'a_c10', 'kl_c10', 'kl_c10_K1', 'kl_c10_K2', 'kl_c10_K3', 'j8', 'a_j8', 'k10', 'a_k10', 'arah10', 'sesi21',
       'tahun_n21', 'tahun_pos21')
F_ = lambda kerja, nama: os.path.join(kerja, f'cs22_{nama}.pkl')


def v_c10(pan):
    """V[bar] = (c10, asas hari sama x tercile ATR %, asas era x tercile) bagi bar dengan tetingkap 63 sesi lengkap (bentuk yang
    diterima enjin skor); bar lain = 0."""
    Lab, As, _, S63 = c21.asas21(pan)
    sah = np.flatnonzero(S63)
    lb = Lab[sah, 0].astype(np.float64)
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(pan['hari'][sah]).rank(pct=True).to_numpy()
    g = pan['tempoh'][sah].astype(np.int64) * 3 + np.minimum((pct * 3).astype(np.int64), 2)
    V = np.zeros((len(pan['c']), 3))
    V[sah, 0], V[sah, 1] = lb, As[sah, 0]
    V[sah, 2] = (np.bincount(g, lb) / np.maximum(np.bincount(g), 1))[g]
    return V


def skor(kerja):
    pan = cari.panel(kerja, 'A')
    luar = int((pan['sah'] & ~c21.sah63(pan)).sum())
    cari.log(f'CS22 skor: sasaran c10; bar layak A tanpa tetingkap 63 sesi lengkap: {luar}')
    return m20.skor(kerja, V=v_c10(pan), F=F_)


def calon(kerja):
    return m20.calon(kerja, F=F_, benih=BENIH_KAWALAN, awalan='X')


def kunci(kerja):
    """Penilaian CS20 (ukuran utama, cara pegang B, kekerapan, audit, belian untuk semakan kembar) + ukuran kedua setiap calon
    dan kawalan pada kumpulan B -> cs22_kunci.pkl"""
    out = m20.kunci(kerja, F=F_, pusingan_sedia=PUSINGAN_SEDIA)
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr = (L['L1'], L['L2'])
    EV = m20.semua_pencetus(kerja, 'B')
    Lab, As, SK, S63 = c21.asas21(pan)
    t0 = time.time()
    for r in pd.concat([C['calon'], C['kawalan']], ignore_index=True).itertuples():
        ev = EV[r.pencetus]
        out[r.id]['c21'] = c21.ukur21(pan, Lab, As, SK, S63, ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)])
    pickle.dump(out, open(F_(kerja, 'kunci'), 'wb'), protocol=4)
    cari.log(f'CS22 kunci: ukuran kedua ditambah · {time.time() - t0:.0f}s')
    return out


def bacaan(T):
    """Bacaan dikunci pindaan (ai) atas peraturan yang cukup belian (ambang CS13 / CS20, label c10)."""
    c, k = T[(T.peranan == 'calon') & T.layak22], T[(T.peranan == 'kawalan') & T.layak22]
    f = lambda x: float(x) if len(c) and len(k) else np.nan
    o = dict(n_calon=int((T.peranan == 'calon').sum()), calon_layak=len(c), kawalan_layak=len(k), n_lulus=int(c.lulus22.sum()),
             lulus_calon=f(c.lulus22.mean()), lulus_kawalan=f(k.lulus22.mean()),
             k3_calon=f((c.kl_c10_K3 > 0).mean()), k3_kawalan=f((k.kl_c10_K3 > 0).mean()))
    o['b1'] = bool(o['lulus_calon'] >= o['lulus_kawalan'] + d13.B1_BEZA)
    o['b2'] = bool(o['k3_calon'] >= d13.B2_MIN and o['k3_calon'] >= o['k3_kawalan'] + d13.B2_BEZA)
    o['ya'] = bool(o['b1'] and o['b2'])
    o['nasib'] = float(o['lulus_kawalan'] / o['lulus_calon']) if o['lulus_calon'] and o['lulus_calon'] == o['lulus_calon'] else np.nan
    return o


def semua(kerja):
    """(C, K, T, bacaan). T = jadual CS20 (ukuran utama dsb.) + lajur ukuran kedua, lulus22, kembar, takrif, kod F."""
    import cs_lapor as lapor
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    K = pickle.load(open(F_(kerja, 'kunci'), 'rb'))
    T = m20.jadual20(C, K)
    peta21 = {'n21': 'n', 'tahun21': 'tahun', 'sesi21': 'sesi', 'tahun_n21': 'tahun_n', 'tahun_pos21': 'tahun_pos'}
    for k_ in L21:
        T[k_] = [K[i].get('c21', {}).get(peta21.get(k_, k_), np.nan) for i in T.id]
    T['layak22'] = (T.n21 >= MIN_BELIAN) & (T.tahun21 >= MIN_TAHUN)
    T['lulus22'] = T.layak22 & (T.kl_c10_K1 > 0) & (T.kl_c10_K2 > 0) & (T.kl_c10_K3 > 0)
    B = bacaan(T)
    c = T[(T.peranan == 'calon') & T.layak22]
    kw = T[(T.peranan == 'kawalan') & T.layak22]
    B.update(tahun_pos_lulus=float(c[c.lulus22].tahun_pos21.median()) if c.lulus22.any() else np.nan,
             tahun_pos_kawalan=float(kw.tahun_pos21.median()) if len(kw) else np.nan,
             arah_pos_lulus=float((c[c.lulus22].arah10 > 0).mean()) if c.lulus22.any() else np.nan,
             arah_pos_kawalan=float((kw.arah10 > 0).mean()) if len(kw) else np.nan)
    T['boleh'] = (T.peranan == 'calon') & T.lulus22 & T.kerap_B & (T.arah10 > 0)
    T2 = T.copy()
    T2['lulus'] = T2.boleh
    kb = d13.kembar(T2, K)
    T['kembar_kepada'] = [kb.get(i, '') if p == 'calon' else '' for i, p in zip(T.id, T.peranan)]
    T['takrif'] = [d13.takrif13(r.pencetus, int(r.q1), int(r.q2), int(r.f1), int(r.f2)) if r.peranan == 'calon' else '' for r in T.itertuples()]
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('')
    baru = dict(zip(reg.takrif[reg.pusingan == PUS], reg.id[reg.pusingan == PUS]))
    lama = dict(zip(reg.takrif[reg.pusingan != PUS], reg.id[reg.pusingan != PUS]))
    T['id_F'] = [baru.get(t, '') if p == 'calon' else (i if p == 'F' else '') for t, p, i in zip(T.takrif, T.peranan, T.id)]
    T['kod_sedia'] = [lama.get(t, '') or (k_ if str(k_).startswith('F') else '') if p == 'calon' else '' for t, p, k_ in zip(T.takrif, T.peranan, T.kembar_kepada)]
    T['untuk_daftar'] = T.boleh & (T.kembar_kepada == '') & ~T.takrif.isin(lama)
    return C, K, T, B


def daftar(kerja):
    """Daftar calon yang layak (lihat pindaan (ai)) sebagai kod F2803 dst. HANYA jika bacaan dikunci lulus."""
    C, K, T, B = semua(kerja)
    if not B['ya']:
        cari.log('CS22 daftar: bacaan dikunci TIDAK lulus -> tiada kod F baharu')
        return 0
    baharu = m20.daftar_baris(T[T.untuk_daftar].sort_values('skor_A', ascending=False, kind='stable'), t7.param_semua(kerja), PUS, TARIKH_DAFTAR)
    cari.log(f"CS22 daftar: {len(baharu)} kod F baharu ({baharu[0]}–{baharu[-1]})" if baharu else 'CS22 daftar: tiada yang baharu')
    return len(baharu)


def lapor_(kerja):
    import cs_lapor as lapor
    C, K, T, B = semua(kerja)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    c, kw = T[T.peranan == 'calon'], T[T.peranan == 'kawalan']
    c.drop(columns=['peranan']).to_csv(os.path.join(d_, 'calon.csv.gz'), index=False, float_format='%.5f')
    kw.drop(columns=['peranan', 'kembar_kepada', 'takrif', 'id_F', 'kod_sedia', 'untuk_daftar', 'boleh']).to_csv(
        os.path.join(d_, 'kawalan.csv'), index=False, float_format='%.5f')
    L = c[c.lulus22]
    Lb = c[c.boleh]
    D = c[c.untuk_daftar]
    U = c[c.id_F != ''].sort_values(['kl_c10', 'c10'], ascending=False, kind='stable').reset_index(drop=True)
    U.insert(0, 'kedudukan', np.arange(1, len(U) + 1))
    S = Lb[Lb.kod_sedia != ''].sort_values('kl_c10', ascending=False, kind='stable')
    lajur_u = ['kedudukan', 'id_F', 'prasyarat', 'nama', 'penapis', 'n21', 'tahun21', 'setahun_semua', 'mgg_semua', 'mgg_B', 'mgg_min_B',
               'c10', 'a_c10', 'kl_c10', 'kl_c10_K1', 'kl_c10_K2', 'kl_c10_K3', 'j8', 'a_j8', 'arah10', 'k10', 'a_k10', 'tahun_pos21', 'tahun_n21',
               'terus', 'a_terus', 'kl_terus', 'kl_terus_K3', 'm5', 'a_m5', 'j5', 'a_j5', 'n_B', 'menang_B', 'a_menang_B', 'purata_B', 'a_purata_B',
               'rugi15_B', 'a_rugi15_B', 'hari_B', 'jual_hari_beli', 'skor_A', 'takrif']
    U[lajur_u].rename(columns={'id_F': 'id'}).to_csv(os.path.join(d_, 'senarai_c10.csv'), index=False, float_format='%.5f')
    bersih = lambda v: None if isinstance(v, float) and v != v else v
    json.dump({k_: bersih(v) for k_, v in dict(
        B, n_isyarat=C['n_pencetus'], n_cukup=C['n_cukup'], n_ada_boleh=C['n_ada_boleh'], tinjau=C['tinjau'], cuba_kawalan=C['cuba_kawalan'],
        n_kawalan=len(kw), n_lulus_kerap=int((L.kerap_B).sum()), n_boleh=len(Lb), n_kembar=int((Lb.kembar_kepada != '').sum()),
        n_kod_sedia=int((Lb.kod_sedia != '').sum()), kod_sedia_unik=int(Lb.kod_sedia[Lb.kod_sedia != ''].nunique()), n_untuk_daftar=len(D),
        n_berdaftar=len(U), naik=c21.NAIK, jatuh=c21.JATUH, had=c21.HAD).items()}, open(os.path.join(d_, 'bacaan.json'), 'w'), indent=1, sort_keys=True)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    tx = lambda s: s if isinstance(s, str) and s.strip() else '–'
    idf = sorted(U.id_F, key=lambda x: int(x[1:]))
    A = ['# CS22: setup sepanjang tahun yang dicari ikut ukuran kedua — "+10 % sebelum −8 %" (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_capai22.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ai). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Apa yang dibuat', '',
         f"- Carian CS20 diulang dengan satu perubahan: setup dipangkatkan ikut **\"kena\"** — selepas beli, harga TUTUP ≥ +{c21.NAIK:.0%} sebelum "
         f"menyentuh −{c21.JATUH:.0%}, dalam {c21.HAD} sesi (≈ 3 bulan) — bukan ikut \"naik ≥ 5 % dalam minggu pertama\". Prasyarat tarikh laporan "
         'kewangan / kalendar tetap tidak dibenarkan dan setiap setup tetap mesti membeli hampir setiap minggu.',
         f"- {C['n_pencetus']:,} isyarat beli ({C['n_cukup']:,} cukup isyarat); {C['tinjau']:,} peraturan ditinjau; **{B['n_calon']:,} calon**. "
         f"Kawalan = {len(kw)} peraturan rawak daripada ruang yang sama.",
         '- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan "kena" lebih kerap daripada saham rawak hari sama '
         'dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).', '',
         '## 2. Ujian (ditetapkan dahulu)', '',
         f"- **B1** kadar lulus: calon **{p(B['lulus_calon'])} %** lawan kawalan {p(B['lulus_kawalan'])} % (perlu beza ≥ 20 mata) → "
         f"{'lulus' if B['b1'] else 'GAGAL'}.",
         f"- **B2** lebih baik daripada rawak pada 2025–26: calon **{p(B['k3_calon'])} %** lawan kawalan {p(B['k3_kawalan'])} % (perlu ≥ 60 % "
         f"dan beza ≥ 10 mata) → {'lulus' if B['b2'] else 'GAGAL'}.",
         f"- **Keputusan: carian ikut ukuran kedua {'BERHASIL' if B['ya'] else 'TIDAK berhasil — tiada kod F baharu'}.**",
         f"- Dilaporkan sahaja: calon lulus lebih baik daripada rawak dalam {p(B['tahun_pos_lulus'])} % tahun (kawalan {p(B['tahun_pos_kawalan'])} %); "
         f"\"kena\" bertambah lebih daripada \"jatuh dahulu\" bagi {p(B['arah_pos_lulus'])} % calon lulus (kawalan {p(B['arah_pos_kawalan'])} %).", '',
         '## 3. Berapa yang lulus', '',
         f"- Lulus: **{len(L):,}** daripada {B['n_calon']:,} calon; juga membeli hampir setiap minggu pada saham tidak dilihat: {int(L.kerap_B.sum()):,}; "
         f"dan \"kena\" bertambah lebih daripada \"jatuh dahulu\": **{len(Lb):,}**.",
         f"- Daripada {len(Lb):,} itu: {int((Lb.kod_sedia != '').sum()):,} sama atau kembar dengan kod F sedia ada "
         f"({int(Lb.kod_sedia[Lb.kod_sedia != ''].nunique()):,} kod berbeza — \"kod sedia ada yang juga lulus ukuran kedua\"); "
         f"{int(((Lb.kembar_kepada != '') & (Lb.kod_sedia == '')).sum()):,} kembar calon lain.",
         f"- **Setup baharu: {len(D):,}**" + (f" → didaftarkan sebagai **`{idf[0]}`–`{idf[-1]}`** ({len(idf):,} kod)." if idf else
                                             ' (belum / tidak didaftarkan).'),
         f"- Anggaran lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira {p(B['nasib'])} %.", '',
         '## 4. Mutu (nilai tengah setiap kumpulan; saham yang carian tidak lihat; kurungan = saham rawak hari sama)', '',
         '| Kumpulan | Bilangan | **Kena %** | Jatuh dahulu % | Terus naik % (sesi ke-63 masih ≥ +10 %) | Tangkap % (ukuran utama) | Menang % cara B (rawak dipegang sama) | '
         'Purata % cara B | Minggu ada belian |', '|---' * 9 + '|']
    for nm, X in (('Kod baharu CS22', U), ('Kod sedia ada yang juga lulus', S.drop_duplicates('kod_sedia')), ('Calon lulus (semua)', L),
                  ('Kawalan rawak (ruang sama)', kw[kw.layak22])):
        if len(X):
            g = X.median(numeric_only=True)
            A.append(f"| {nm} | {len(X):,} | **{p(g.c10, 1)}** ({p(g.a_c10, 1)}) | {p(g.j8, 1)} ({p(g.a_j8, 1)}) | {p(g.k10, 1)} ({p(g.a_k10, 1)}) | "
                     f"{p(g.terus, 1)} ({p(g.a_terus, 1)}) | {p(g.menang_B)} ({p(g.a_menang_B)}) | {p(g.purata_B, 1, True)} ({p(g.a_purata_B, 1, True)}) | "
                     f"{p(g.mgg_semua)} % |")
    kepala = ['| # | ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 | Jatuh dahulu % '
              '(rawak) | Terus naik % (rawak) | Tangkap % (rawak) | Menang % (rawak) | Purata % (rawak) |', '|---' * 13 + '|']
    baris = lambda k_, idn, r: (f"| {k_} | `{idn}` | {tx(r.prasyarat)} | {r.nama} | {tx(r.penapis)} | {r.setahun_semua:.0f} | **{p(r.c10, 1)}** "
                                f"({p(r.a_c10, 1)}) | {p(r.kl_c10_K1, 1, True)} / {p(r.kl_c10_K2, 1, True)} / {p(r.kl_c10_K3, 1, True)} | {p(r.j8, 1)} "
                                f"({p(r.a_j8, 1)}) | {p(r.k10, 1)} ({p(r.a_k10, 1)}) | {p(r.terus, 1)} ({p(r.a_terus, 1)}) | {p(r.menang_B)} "
                                f"({p(r.a_menang_B)}) | {p(r.purata_B, 1, True)} ({p(r.a_purata_B, 1, True)}) |")
    if len(U):
        A += ['', '## 5. Kod baharu: pecahan', '',
              '- Prasyarat paling kerap: ' + '; '.join(f'{k_ or "tiada"} ({v})' for k_, v in U.prasyarat.value_counts().head(8).items()) + '.',
              '- Penapis saham paling kerap: ' + '; '.join(f'{k_ or "tiada"} ({v})' for k_, v in U.penapis.value_counts().head(8).items()) + '.',
              f"- Isyarat beli: {U.induk.nunique()} kaedah / keluarga berbeza; paling kerap " +
              ', '.join(f'{k_} ({v})' for k_, v in U.induk.value_counts().head(8).items()) + '.',
              f"- Tangkap (ukuran utama) juga melebihi rawak: {int((U.terus > U.a_terus).sum()):,} daripada {len(U):,}; menang cara B melebihi rawak "
              f"dipegang sama: {int((U.menang_B > U.a_menang_B).sum()):,}; purata melebihi: {int((U.purata_B > U.a_purata_B).sum()):,}.",
              f"- Jualan pada hari beli: {int(U.jual_hari_beli.sum())} (mesti 0).", '',
              f'## 6. Kod baharu (teratas {min(N_PAPAR, len(U))} ikut beza "kena" lawan rawak; senarai penuh `senarai_c10.csv`)', ''] + kepala
        A += [baris(r.kedudukan, r.id_F, r) for r in U.head(N_PAPAR).itertuples()]
    if len(S):
        S1 = S.drop_duplicates('kod_sedia')
        A += ['', f'## 7. Kod sedia ada yang juga lulus ukuran kedua ({len(S1):,} kod; teratas {min(30, len(S1))})', ''] + kepala
        A += [baris(k_, r.kod_sedia, r) for k_, r in enumerate(S1.head(30).itertuples(), 1)]
    A += ['', '## 8. Kaveat', '',
          '- Saham rawak sendiri "kena" kira-kira 40 daripada 100 kali dalam 3 bulan; yang bermakna hanya beza lawan rawak, dan beza itu kecil.',
          '- 2025–26 ialah syarat lulus, bukan tempoh di luar sampel; ukuran longgar pernah gagal pada tahun tidak dilihat (CS12).',
          '- Ukuran kedua tidak bergantung pada cara pegang; angka menang dan purata di sini memakai cara pegang B seperti kod lain.',
          '- Tiada saham delist dalam data ("kena" condong ke atas bagi semua, termasuk saham rawak). Backtest sahaja; tiada papertrade tanpa '
          'keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'CARIAN_C10.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS22 lapor: calon {B['n_calon']}, layak {B['calon_layak']}, lulus {B['n_lulus']} ({B['lulus_calon']:.0%} lawan kawalan "
             f"{B['lulus_kawalan']:.0%}); K3 {B['k3_calon']:.0%} lawan {B['k3_kawalan']:.0%} -> {'BERHASIL' if B['ya'] else 'TIDAK'}; boleh {len(Lb)}, "
             f"kod sedia {int((Lb.kod_sedia != '').sum())}, untuk daftar {len(D)}, berdaftar {len(U)}")
    return T, B, U


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'skor':
        skor(kerja)
    elif cmd == 'calon':
        calon(kerja)
    elif cmd == 'kunci':
        kunci(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    elif cmd == 'daftar':
        daftar(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')

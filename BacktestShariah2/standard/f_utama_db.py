# f_utama_db.py — dokumen db dashboard `carian/f_utama` (+ `_2`…): senarai utama setup F (Rujukan → Setup F).
# Sumber: kajian/carian_setup/hasil/CS13/senarai_utama.csv dan bacaan.json (dijana cs_daftar13.py, pindaan (v)); cara pegang
# kedua "pegang lebih lama" (keputusan pengguna 16 Nov 2026 "B" selepas CS14): hasil/CS14/setup.csv.gz dan cara.csv
# (cs_pegang14.py, pindaan (x); cara `r0.t2.0` = jual bila tutup di bawah purata 50 hari, tiada had masa).
# Dokumen STATIK: ia berubah hanya apabila senarai utama dijana semula, jadi ia TIDAK ditulis oleh jana_db.py dan
# tidak berada dalam daftar versi `meta/versi_db`; tolak secara manual selepas setiap pusingan carian yang mengubahnya:
#   python3 BacktestShariah2/standard/f_utama_db.py --keluar <folder>
#   -> <folder>/carian/f_utama.json, f_utama_2.json …; senarai fail dicetak. Tolak SEMUA dalam SATU batch ArtifactData
#   (collection `carian`; if_version bagi dokumen yang sudah wujud). Halaman membacanya dengan subBhg().
# v189 (17 Nov 2026): baris setup sepanjang tahun CS20 (dan CS22 jika ada kod) ditambah SELEPAS baris senarai utama; meta n_utama,
#   n_mingguan, mingguan{…}, ukuran_kedua{…}, jeda{…}; sumber tambahan hasil/CS20/calon.csv.gz, hasil/CS21/unit.csv.gz, hasil/CS22/.
# v190 (17 Nov 2026): lajur markah CS23 (mk, mka..mke, gn, tk, tg, sr23, mgb) dan meta skor{…}; sumber tambahan hasil/CS23/.
# Bentuk: {tajuk, sumber, dibina, n, n_pilihan, n_lama, n_baharu, ujian{…}, semak_masa{…}, pegang, pegang2, banding{…}, kol[],
#          kamus{pra, nama, pen, jenis}, kawalan{…}, solid{…}, rows[[…]]}; baris padat sejajar `kol`: peratus x10 (tangkap, rawak, m5, am5,
#          menang, rugi15, menang2, rugi2, k10, m10, am10, m10d, am10d, rugi8), x100 (purata, k3, purata2, k1, k2). Lajur baharu hanya DITAMBAH di hujung `kol` (halaman membaca ikut nama).
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(SINI)
sys.path.insert(0, SINI)
sys.path.insert(0, os.path.join(BS2, 'kajian', 'carian_setup'))
from bahagi_db import bahagi, bait, padat, HAD_DB  # noqa: E402

CS13 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS13')
CS14 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS14')
CS16 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS16')
CS19 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS19')
CS20 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS20')
CS21 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS21')
CS22 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS22')
CS23 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS23')
ASAS_EARN = 'earnings dalam 1-5 sesi akan datang'
CARA1, CARA2 = 'r0.t1.126', 'r0.t2.0'                    # cara sekarang (pegang B) dan "pegang lebih lama" (pilihan pengguna B, 16 Nov 2026)
KOL = ['id', 'asal', 'pil', 'pra', 'nama', 'pen', 'beli', 'shar', 'tangkap', 'rawak', 'm5', 'menang', 'purata', 'rugi15', 'hari', 'k3', 'n',
       'menang2', 'purata2', 'rugi2', 'hari2', 'jenis', 'am5', 'k10', 'k1', 'k2',
       'solid', 'wakil', 'boleh', 'm10', 'am10', 'm10d', 'am10d', 'tpos', 'tbil', 'rugi8', 'serupa',
       'j5', 'aj5', 'am', 'ap', 'aud', 'aun', 'pt',
       'mg', 'mgg', 'bs', 'c10', 'ac10', 'j8', 'aj8',
       'mk', 'mka', 'mkb', 'mkc', 'mkd', 'mke', 'gn', 'tk', 'tg', 'sr23', 'mgb']
# v190 (17 Nov 2026; keputusan pengguna "ya dua dua"): MARKAH 0-100 dan "Kegunaan bila?" (CS23, pindaan (aj); hasil/CS23/skor.csv.gz).
# mk = markah x10 (None = tidak dinilai); mka..mke = markah bahagian A (35), B (15), C (20), D (20), E (10) x10; gn = indeks GUNA
# ("Kegunaan bila?"); tk = kedudukan keseluruhan antara setup berbeza (0 = serupa dengan setup bermarkah lebih tinggi, atau tidak
# dinilai); tg = kedudukan dalam kumpulan "Kegunaan bila?" sendiri (0 = tiada); sr23 = setup bermarkah lebih tinggi yang beliannya
# bertindih >= 50 %; mgb = bahagian minggu yang ada belian x1000, diukur seragam pada separuh saham (asas label "Setiap minggu").
GUNA = ['Setiap minggu', 'Musim laporan kewangan', 'Keadaan tertentu', 'Lain-lain']
# v189 (17 Nov 2026; keputusan pengguna "ya utk 1, 2, 3"): setup SEPANJANG TAHUN dan ukuran kedua. mg = 0 senarai utama CS13, 1 = setup
# sepanjang tahun CS20 (membeli hampir setiap minggu; pindaan (ag)), 2 = CS22 (dicari ikut ukuran kedua; pindaan (ai)); mgg = bahagian
# minggu yang ada belian pada semua saham; bs = belian setahun pada semua saham; c10 / ac10 = daripada 100 belian, berapa yang TUTUP
# >= +10 % sebelum menyentuh -8 % dalam 63 sesi (setup / saham rawak hari sama; CS21, pindaan (ah)); j8 / aj8 = menyentuh -8 % dahulu.
# Baris senarai utama kekal DAHULU dan dalam susunan asal (n_utama baris); baris mg ditambah selepasnya. Bagi baris mg, lajur CS14 /
# CS16 / gred audit CS19 tiada (None / 0); j5, aj5, am, ap datang daripada penilaian CS20 / CS22 sendiri (cs_audit19.ukur).
# CS19 audit bebas (pindaan (ae), 16 Nov 2026; SERAHAN_CARIAN_SETUP.md §9t): j5 / aj5 = daripada 100 belian, berapa JATUH >= 5 % minggu
# pertama (setup / saham rawak hari sama); am / ap = kadar menang dan purata saham rawak hari sama yang DIPEGANG DENGAN CARA YANG SAMA
# (cara sekarang); aud = gred audit (0 tiada, 1 A, 2 B, 3 C, 4 D -- BUKAN gred "tangkap ÷ rawak" halaman); aun = nota audit (x k i h y t);
# pt = 1 jika setup dalam kohort papertrade gred A (jejak_f2). Terus daripada hasil/CS19/audit.csv.gz; None jika setup tidak diaudit.
GRED_AUDIT = ['', 'A', 'B', 'C', 'D']
# CS16 "ujian solid" (pindaan (z), 16 Nov 2026; SERAHAN_CARIAN_SETUP.md §9o): solid (lulus S1-S7), wakil (setup berbeza: 224 daripada
# 290), boleh (masih positif dengan tarikh laporan DITEKA, S8), tiga angka pengguna daripada 100 belian dengan saham rawak hari sama
# (m5/am5 sedia ada; m10/am10 = tutup hari ke-5 >= +10 %; m10d/am10d = tutup hari ke-10 >= +10 %), tahun lebih baik daripada rawak
# (tpos daripada tbil), jatuh >= 8 % (rugi8), serupa = wakil bagi setup solid yang bukan wakil. Terus daripada hasil/CS16/solid.csv.gz.
# v182 reka bentuk (16 Nov 2026; selepas lajur CS14): jenis isyarat beli (indeks kamus `jenis`), naik >= 5 % minggu 1 bagi saham rawak hari sama (am5), dagangan dijual
# >= +10 % (k10), kelebihan tangkap 2010-19 (k1) dan 2020-24 (k2); semuanya terus daripada senarai_utama.csv, tiada kiraan baharu.
JENIS = ['Terlebih jual', 'Kaedah M asal', 'Undur dalam trend', 'Momentum', 'Pecah paras', 'Silang purata', 'Kaedah N / P asal',
         'Volum, gap & corak bar']
_K = {1: 0, 2: 0, 3: 0, 4: 0, 13: 0, 17: 2, 18: 2, 22: 2, 9: 3, 11: 3, 12: 3, 23: 3, 10: 4, 19: 4, 20: 4, 21: 4, 25: 4, 5: 5, 7: 5, 8: 5,
      14: 7, 15: 7, 16: 7, 6: 7, 24: 7}


def jenis(nama):
    """Kumpulan jenis isyarat beli (indeks JENIS) daripada kod pencetus: Kxx.yyy = keluarga indikator cs_param, M = benih M, N/P = benih N/P."""
    import re
    m = re.match(r'^K(\d+)\.', str(nama))
    if m:
        return _K.get(int(m.group(1)), 7)
    return 1 if str(nama).startswith('M') else 6


HAD_BAHAGI = 200000
PEGANG = ('Beli pada buka esok · stop loss 4×ATR14 · pegang sekurang-kurangnya 20 hari (20 hari ialah minimum, bukan had), kemudian jual '
          'bila harga tutup di bawah purata 20 hari · paling lama 6 bulan · tiada jualan pada hari beli')
PEGANG2 = ('Sama hingga hari ke-20; selepas itu jual hanya bila harga tutup di bawah purata 50 hari · tiada had masa')


def banding(folder14=CS14):
    """Ringkasan dua cara pegang (nilai tengah semua setup, saham yang carian tidak lihat) + saham rawak dengan cara sama."""
    T = pd.read_csv(os.path.join(folder14, 'cara.csv'))
    T = T[T.set == 'B'].set_index('cara')
    g = lambda c, awal='': {k: round(float(T.loc[c, awal + k]), 4) for k in ('purata', 'menang', 'rugi15')}
    return dict(kini=dict(g(CARA1), hari=float(T.loc[CARA1, 'sesi_med'])), lama=dict(g(CARA2), hari=float(T.loc[CARA2, 'sesi_med'])),
                rawak_kini=g(CARA1, 'rawak_'), rawak_lama=g(CARA2, 'rawak_'))


def solid_ringkas(folder16=CS16):
    """Meta CS16: bilangan, bacaan dikunci B1/B2, dan asas "laporan kewangan dalam 1-5 sesi" SAHAJA (prasyarat.csv q1 = -1)."""
    B = json.load(open(os.path.join(folder16, 'bacaan.json'), encoding='utf-8'))
    P = pd.read_csv(os.path.join(folder16, 'prasyarat.csv'))
    a = P[(P.q1 == -1) & (P.prasyarat == ASAS_EARN)]
    assert len(a) == 1, 'baris asas laporan kewangan tiada dalam prasyarat.csv'
    a = a.iloc[0]
    r4 = lambda x: round(float(x), 4)
    return dict(n_solid=int(B['solid_utama']), n_wakil=int(B['wakil']), boleh_solid=int(B['solid_boleh']), boleh_wakil=int(B['wakil_boleh']),
                kawalan_lulus=r4(B['kadar_K1']), calon_lulus=r4(B['kadar_calon']), b1=bool(B['b1']), b2=bool(B['b2']),
                asas=dict(prasyarat=ASAS_EARN, n=int(a.n), thn_pos=int(a.thn_pos), thn_bil=int(a.thn_bil), rugi8=r4(a.rugi8),
                          **{k: r4(a[k]) for k in ('m5', 'a_m5', 'm10', 'a_m10', 'm10d', 'a_m10d', 'terus', 'a_terus', 'menang', 'purata')}),
                sumber='kajian/carian_setup/hasil/CS16/solid.csv.gz, prasyarat.csv, bacaan.json (cs_solid16.py, pindaan (z))')


def audit_ringkas(folder19=CS19):
    """Meta CS19: bilangan gred, kohort papertrade, dan gabungan belian unik (300 teratas; kawalan "laporan sahaja")."""
    B = json.load(open(os.path.join(folder19, 'bacaan.json'), encoding='utf-8'))
    G = pd.read_csv(os.path.join(folder19, 'gabungan.csv'))
    r4 = lambda x: round(float(x), 4)

    def g(awalan):
        x = G[G.kumpulan.str.startswith(awalan)].set_index('tempoh')
        return {t: {k: r4(x.loc[t, k]) for k in ('tangkap', 'r_tangkap', 'naik5', 'r_naik5', 'jatuh5', 'r_jatuh5', 'menang', 'r_menang',
                                                 'purata', 'r_purata')} | {'belian': int(x.loc[t, 'belian'])} for t in ('semua', '2025-26')}
    return dict(n=int(B['n_utama']), diaudit=int(B['diaudit']), pariti=int(B['pariti']), gred_300=B['gred_300'], gred_semua=B['gred_semua'],
                kohort=B['kohort'], atas=g('300 teratas'), laporan_sahaja=g('KAWALAN: semua saham'), intai=int(B['intai_setup']),
                sumber='kajian/carian_setup/hasil/CS19/audit.csv.gz, gabungan.csv, bacaan.json (cs_audit19.py, pindaan (ae))')


def mingguan(folder20=CS20, folder22=CS22):
    """Baris setup sepanjang tahun yang BERDAFTAR: CS20 (mg = 1) dan CS22 (mg = 2), daripada calon.csv.gz setiap pusingan."""
    out = []
    for mg, folder in ((1, folder20), (2, folder22)):
        f = os.path.join(folder, 'calon.csv.gz')
        if not os.path.exists(f):
            continue
        c = pd.read_csv(f)
        c = c[c.id_F.notna() & (c.id_F.astype(str) != '')].copy()
        if not len(c):
            continue
        c['mg'] = mg
        c['_n'] = c.id_F.str[1:].astype(int)
        out.append(c.sort_values('_n'))
    if not out:
        return None
    M = pd.concat(out, ignore_index=True).fillna({'prasyarat': '', 'penapis': ''})
    assert M.id_F.is_unique
    return M


def ukuran_kedua(folder21=CS21, folder22=CS22):
    """id -> (c10, a_c10, j8, a_j8) daripada CS21 (senarai utama + kod CS20) dan CS22 (kod sendiri); + ringkasan kumpulan."""
    f = os.path.join(folder21, 'unit.csv.gz')
    if not os.path.exists(f):
        return {}, None
    T = pd.read_csv(f)
    T = T[T.kumpulan.str.startswith('F ') & T.id.astype(str).str.startswith('F') & (T.n > 0)]
    peta = {r.id: (r.c10, r.a_c10, r.j8, r.a_j8) for r in T.itertuples()}
    f22 = os.path.join(folder22, 'calon.csv.gz')
    if os.path.exists(f22):
        c = pd.read_csv(f22)
        for r in c[c.id_F.notna() & (c.id_F.astype(str) != '')].itertuples():
            peta[r.id_F] = (r.c10, r.a_c10, r.j8, r.a_j8)
    B = json.load(open(os.path.join(folder21, 'bacaan.json'), encoding='utf-8'))
    r4 = lambda x: None if x is None or x != x else round(float(x), 4)
    nama = {'isyarat M sahaja': 'M', 'isyarat N sahaja': 'N', 'F senarai utama: laporan kewangan': 'laporan', 'F senarai utama: bukan laporan': 'lain',
            'F sepanjang tahun CS20: kod berdaftar': 'mingguan', 'kawalan rawak sepanjang tahun (CS20)': 'kawalan'}
    ring = dict(dasar={k: r4(B['dasar'][k]) for k in ('c10', 'j8', 'k10')}, had=int(B['had']),
                kumpulan={nama[k]: {a: r4(v.get(a)) for a in ('unit', 'c10', 'a_c10', 'j8', 'a_j8', 'pos', 'pos_tiga')} for k, v in B['kumpulan'].items() if k in nama},
                sumber='kajian/carian_setup/hasil/CS21/unit.csv.gz, bacaan.json (cs_capai21.py, pindaan (ah))')
    f22 = os.path.join(folder22, 'bacaan.json')
    if os.path.exists(f22):
        b = json.load(open(f22, encoding='utf-8'))
        ring['cs22'] = {k: (r4(b[k]) if isinstance(b.get(k), float) else b.get(k)) for k in ('n_calon', 'n_lulus', 'lulus_calon', 'lulus_kawalan', 'k3_calon',
                                                                                            'k3_kawalan', 'ya', 'n_boleh', 'n_kod_sedia', 'kod_sedia_unik', 'n_berdaftar')}
    return peta, ring


def markah(folder23=CS23):
    """id -> [mk, mka..mke, gn, tk, tg, sr23, mgb] daripada CS23 skor.csv.gz, + ringkasan; ({}, None) jika pusingan belum dijana."""
    f = os.path.join(folder23, 'skor.csv.gz')
    if not os.path.exists(f):
        return {}, None
    T = pd.read_csv(f)
    B = json.load(open(os.path.join(folder23, 'bacaan.json'), encoding='utf-8'))
    b10 = lambda x: None if x != x else int(round(float(x) * 10))
    peta = {}
    for r in T.itertuples():
        ya = bool(r.dinilai)
        peta[r.id] = ([b10(r.markah), b10(r.mA), b10(r.mB), b10(r.mC), b10(r.mD), b10(r.mE)] if ya else [None] * 6) + [
            GUNA.index(r.kegunaan), int(r.kedudukan) if ya else 0, int(r.kedudukan_guna) if ya else 0,
            r.serupa_dengan if isinstance(r.serupa_dengan, str) and r.serupa_dengan else None,
            None if r.minggu != r.minggu else int(round(float(r.minggu) * 1000))]
    ring = dict(n=int(B['n']), dinilai=int(B['dinilai']), tidak_dinilai=int(B['n'] - B['dinilai']), serupa=int(B['serupa']),
                disimpan=int(B['disimpan']), n_top=int(B['n_top']), berat=B['berat'], guna=GUNA, markah_maks=B['markah_maks'],
                markah_tengah=B['markah_tengah'], top_min=B['top_min'], top_kegunaan=B['top_kegunaan'],
                disimpan_kegunaan=B['disimpan_kegunaan'], semua_kegunaan=B['semua_kegunaan'], top_guna=B['top_guna'],
                sumber='kajian/carian_setup/hasil/CS23/skor.csv.gz, bacaan.json, TOP100.md (cs_skor23.py, pindaan (aj))')
    return peta, ring


def bina(folder=CS13, folder14=CS14, folder16=CS16, folder19=CS19, folder20=CS20, folder21=CS21, folder22=CS22, folder23=CS23):
    """Dokumen penuh (belum dibahagi) daripada senarai_utama.csv + cara pegang kedua (CS14); None jika fail tiada."""
    import cs_ringkas
    f = os.path.join(folder, 'senarai_utama.csv')
    if not os.path.exists(f):
        return None
    U = pd.read_csv(f).fillna({'prasyarat': '', 'penapis': ''})
    X = pd.read_csv(os.path.join(folder14, 'setup.csv.gz')).set_index('id').loc[U.id]
    assert (abs(X[CARA1 + ':menang'].to_numpy() - U.menang_B.to_numpy()) < 2e-4).all(), 'CS14 tidak sepadan dengan senarai utama'
    for k, a in (('menang2', 'menang'), ('purata2', 'purata'), ('rugi2', 'rugi15'), ('hari2', 'sesi_med')):
        U[k] = X[f'{CARA2}:{a}'].to_numpy()
    Z = pd.read_csv(os.path.join(folder16, 'solid.csv.gz')).set_index('id').loc[U.id]
    assert (abs(Z.m5.to_numpy() - U.m5.to_numpy()) < 6e-4).all(), 'CS16 tidak sepadan dengan senarai utama'
    for k, a in (('z_solid', 'solid'), ('z_wakil', 'wakil'), ('z_boleh', 'boleh_dibuat'), ('z_m10', 'm10'), ('z_am10', 'a_m10'), ('z_m10d', 'm10d'),
                 ('z_am10d', 'a_m10d'), ('z_tpos', 'thn_pos'), ('z_tbil', 'thn_bil'), ('z_rugi8', 'rugi8'), ('z_serupa', 'serupa_dengan')):
        U[k] = Z[a].to_numpy()
    ada19 = os.path.exists(os.path.join(folder19, 'audit.csv.gz'))
    if ada19:
        A = pd.read_csv(os.path.join(folder19, 'audit.csv.gz')).set_index('id').loc[U.id]
        ya = A.diaudit.to_numpy(bool)
        assert (abs(A.terus.to_numpy()[ya] - U.terus.to_numpy()[ya]) < 6e-4).all(), 'CS19 tidak sepadan dengan senarai utama'
        kohort = set(json.load(open(os.path.join(folder19, 'bacaan.json'), encoding='utf-8'))['kohort'])
        for k, a in (('u_j5', 'j5'), ('u_aj5', 'a_j5'), ('u_am', 'a_menang_B'), ('u_ap', 'a_purata_B')):
            U[k] = np.where(ya, A[a].to_numpy(float), np.nan)
        U['u_aud'] = [GRED_AUDIT.index(g) if d and isinstance(g, str) else 0 for g, d in zip(A.gred, ya)]
        U['u_aun'] = [n if d and isinstance(n, str) and n else None for n, d in zip(A.nota, ya)]
        U['u_pt'] = [int(i in kohort) for i in U.id]
    else:
        for k in ('u_j5', 'u_aj5', 'u_am', 'u_ap'):
            U[k] = np.nan
        U['u_aud'], U['u_aun'], U['u_pt'] = 0, None, 0
    J = json.load(open(os.path.join(folder, 'bacaan.json'), encoding='utf-8'))
    U['nama_p'] = U.nama.map(cs_ringkas.nama_pendek)
    M = mingguan(folder20, folder22)
    if M is not None:
        M['nama_p'] = M.nama.map(cs_ringkas.nama_pendek)
    C10, ring10 = ukuran_kedua(folder21, folder22)
    MK, ring23 = markah(folder23)
    mk = lambda idn: MK.get(idn, [None] * 6 + [None, 0, 0, None, None])
    kamus, ix = {}, {}
    for k, kol in (('pra', 'prasyarat'), ('nama', 'nama_p'), ('pen', 'penapis')):
        kamus[k] = sorted(set(U[kol]) | (set(M[kol]) if M is not None else set()))
        ix[k] = {v: i for i, v in enumerate(kamus[k])}
    b = lambda x, kali: None if x is None or x != x else int(round(float(x) * kali))
    c10 = lambda idn: [b(v, 1000) for v in C10.get(idn, (None, None, None, None))]
    rows = []
    for r in U.itertuples():
        rows.append([r.id, int(r.asal == 'baharu'), int(bool(r.pilihan)), ix['pra'][r.prasyarat], ix['nama'][r.nama_p], ix['pen'][r.penapis],
                     b(r.setahun, 1), b(r.shariah_setahun, 1), b(r.terus, 1000), b(r.a_terus, 1000), b(r.m5, 1000), b(r.menang_B, 1000),
                     b(r.purata_B, 10000), b(r.rugi15_B, 1000), b(r.hari_B, 1), b(r.kl_terus_K3, 10000), int(r.n),
                     b(r.menang2, 1000), b(r.purata2, 10000), b(r.rugi2, 1000), b(r.hari2, 1),
                     jenis(r.nama), b(r.a_m5, 1000), b(r.k10_B, 1000), b(r.kl_terus_K1, 10000), b(r.kl_terus_K2, 10000),
                     int(bool(r.z_solid)), int(bool(r.z_wakil)), int(bool(r.z_boleh)), b(r.z_m10, 1000), b(r.z_am10, 1000), b(r.z_m10d, 1000),
                     b(r.z_am10d, 1000), int(r.z_tpos), int(r.z_tbil), b(r.z_rugi8, 1000), None if r.z_serupa != r.z_serupa else str(r.z_serupa),
                     b(r.u_j5, 1000), b(r.u_aj5, 1000), b(r.u_am, 1000), b(r.u_ap, 10000), int(r.u_aud),
                     r.u_aun if isinstance(r.u_aun, str) else None, int(r.u_pt), 0, None, None] + c10(r.id) + mk(r.id))
    n_utama = len(rows)
    for r in (M.itertuples() if M is not None else ()):
        tbil = int(r.tahun_n) if r.tahun_n == r.tahun_n else 0
        rows.append([r.id_F, 1, int(r.menang_B >= 0.5 and r.purata_B >= 0.02), ix['pra'][r.prasyarat], ix['nama'][r.nama_p], ix['pen'][r.penapis],
                     b(r.setahun, 1), None, b(r.terus, 1000), b(r.a_terus, 1000), b(r.m5, 1000), b(r.menang_B, 1000),
                     b(r.purata_B, 10000), b(r.rugi15_B, 1000), b(r.hari_B, 1), b(r.kl_terus_K3, 10000), int(r.n),
                     None, None, None, None,
                     jenis(r.nama), b(r.a_m5, 1000), b(r.k10_B, 1000), b(r.kl_terus_K1, 10000), b(r.kl_terus_K2, 10000),
                     0, 0, 0, None, None, None, None, int(round(r.tahun_pos * tbil)) if tbil else 0, tbil, b(r.rugi8_J20, 1000), None,
                     b(r.j5, 1000), b(r.a_j5, 1000), b(r.a_menang_B, 1000), b(r.a_purata_B, 10000), 0, None, 0,
                     int(r.mg), b(r.mgg_semua, 1000), b(r.setahun_semua, 1)] + c10(r.id_F) + mk(r.id_F))
    ixk = {k: i for i, k in enumerate(KOL)}
    mgr = None
    if M is not None:
        M1 = M[M.mg == 1]
        J20 = json.load(open(os.path.join(folder20, 'bacaan.json'), encoding='utf-8'))
        md = lambda X, k: round(float(X[k].median()), 4)
        mgr = dict(n=int(len(M1)), n_c10=int((M.mg == 2).sum()),
                   ujian={k: (round(v, 4) if isinstance(v, float) else v) for k, v in J20.items() if k in (
                       'n_calon', 'n_lulus', 'lulus_calon', 'lulus_kawalan', 'k3_calon', 'k3_kawalan', 'nasib', 'n_kembar', 'n_berdaftar')},
                   tengah={k: md(M1, k) for k in ('terus', 'a_terus', 'm5', 'a_m5', 'j5', 'a_j5', 'menang_B', 'a_menang_B', 'purata_B', 'a_purata_B',
                                                  'mgg_semua', 'setahun_semua')},
                   tiada_prasyarat=int((M1.prasyarat == '').sum()),
                   sumber='kajian/carian_setup/hasil/CS20/calon.csv.gz, bacaan.json (cs_mingguan20.py, pindaan (ag))')
    sm = J.get('semak_masa') or {}
    kamus['jenis'] = JENIS
    K = pd.read_csv(os.path.join(folder, 'kawalan.csv'))
    K = K[K.layak.astype(bool)] if 'layak' in K else K
    kawalan = dict(n=int(len(K)), menang=round(float(K.menang_B.median()), 4), purata=round(float(K.purata_B.median()), 5))
    return dict(
        tajuk='Setup F: sepanjang tahun (mingguan) + senarai utama (saham naik laju), cara pegang B',
        sumber='kajian/carian_setup/hasil/CS13/senarai_utama.csv + hasil/CS20/calon.csv.gz + hasil/CS21/unit.csv.gz',
        dibina=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'), n=len(rows), n_utama=n_utama,
        n_pilihan=int(sum(1 for x in rows if x[ixk['pil']])),
        n_lama=int((U.asal == 'lama').sum()), n_baharu=int((U.asal == 'baharu').sum()),
        n_mingguan=int(sum(1 for x in rows if x[ixk['mg']])), mingguan=mgr, ukuran_kedua=ring10, skor=ring23,
        jeda=dict(papertrade=os.path.exists(os.path.join(BS2, 'jejak_f2', 'JEDA')), tarikh='2026-11-17'),
        n_earnings=int(U.prasyarat.str.contains('earnings dalam 1-').sum()),
        ujian=dict(calon=J.get('n_calon'), lulus=J.get('n_lulus'), kembar=J.get('n_kembar'), lulus_calon=J.get('lulus_calon'),
                   lulus_kawalan=J.get('lulus_kawalan'), k3_calon=J.get('k3_calon'), k3_kawalan=J.get('k3_kawalan')),
        semak_masa={k: {a: (round(x, 4) if isinstance(x, float) else x) for a, x in v.items()} for k, v in sm.items()},
        kawalan=kawalan, solid=solid_ringkas(folder16), audit=audit_ringkas(folder19) if ada19 else None, pegang=PEGANG, pegang2=PEGANG2, banding=banding(folder14), kol=KOL, kamus=kamus, rows=rows,
        nota='Pangkat backtest pada saham yang carian tidak lihat (2010–2026); BUKAN bukti dan BUKAN keputusan wang sebenar. '
             'Tiada saham delist dalam data. Tiada papertrade tanpa keputusan pengguna.')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', required=True)
    a = ap.parse_args(argv)
    doc = bina()
    if doc is None:
        raise SystemExit('senarai_utama.csv tiada: jalankan cs_daftar13.py lapor dahulu')
    out = []
    for doc_id, dd in bahagi(doc, 'f_utama', HAD_BAHAGI):
        sz = bait(dd)
        if sz >= HAD_DB:
            raise SystemExit(f'carian/{doc_id}: {sz} bait melebihi had db {HAD_DB}')
        p = os.path.join(a.keluar, 'carian', doc_id + '.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(padat(dd))
        out.append(dict(collection='carian', doc_id=doc_id, file_path=os.path.abspath(p), bait=sz))
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return out


if __name__ == '__main__':
    main()

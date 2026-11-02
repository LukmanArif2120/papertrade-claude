#!/usr/bin/env python3
"""kejar.py — proses sesi papertrade yang TERTINGGAL, mengikut urutan, sebelum sesi terkini.

SEBAB IA WUJUD (diukur, bukan teori). Pada 31 Okt 2026 `harian.yml` gagal enam larian berturut
kerana satu dokumen db melebihi had saiz. Langkah "Commit dan push" tidak pernah berjalan, jadi
isyarat dan senarai_beli sesi 2026-10-30 tidak pernah masuk repo. Cron Sel–Sab bermakna tiada
larian 1–2 Nov. Apabila larian seterusnya berjaya, `harian_c.py malam` mengambil **bar terakhir
stor** sebagai sesi — iaitu 2026-11-02 — dan sesi 2026-10-30 hilang SELAMANYA tanpa sesiapa
memutuskan ia patut hilang. Itu kehilangan senyap: tiada ralat, tiada amaran, cuma satu hari
pengumpulan data yang tidak pernah wujud.

Jadi pemulihan satu kegagalan bukan memadai. Selagi `malam` hanya memandang bar terakhir, SETIAP
kegagalan berbilang hari membuang sesi di tengah-tengah. Skrip ini menutup lubang itu: ia
membandingkan `status_harian.json` dengan senarai sesi dalam stor harga dan memproses setiap sesi
yang tertinggal mengikut urutan, termasuk BELIAN yang sepatutnya berlaku pada pagi selepasnya.

TIADA LOOK-AHEAD. `harian_c.cmd_malam` memotong stor harga kepada sesi yang diproses
(`stor_hingga`), jadi imbasan sesi lampau hanya melihat bar hingga sesi itu. Belian lampau diberi
harga buka SEBENAR hari itu daripada `data/harga/terkini.csv` (fail yang sama yang dipakai aliran
malam), bukan harga semasa.

GRED SENGAJA DILANGKAU bagi sesi yang dikejar. `harian_c.py gred` menarik berita dan pemangkin
SEMASA; memakainya pada sesi lampau akan mengisi medan gred dengan maklumat masa hadapan relatif
kepada tarikh isyarat. Posisi yang dipulihkan jadi tiada gred — itu betul dan boleh dilihat,
berbanding gred yang tercemar yang kelihatan sah.

Guna:
    python3 BacktestShariah2/standard/kejar.py --folder BacktestShariah2/papertrade \
        --isyarat BacktestShariah2/data/isyarat [--proses 4] [--maks 5] [--kering]

Keluaran: satu baris JSON {dikejar: [...], belian: [...], langkau: [...], nota: [...]}.
Kod keluar 0 walaupun tiada apa-apa untuk dikejar (keadaan biasa).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
TERKINI = os.path.join(BS2, 'data', 'harga', 'terkini.csv')


def sesi_stor(stor):
    """Senarai sesi (YYYY-MM-DD) dalam stor harga, mengikut urutan. Sumbernya harga_idx.csv —
    fail yang sama yang `harian_c.cmd_malam` pakai untuk memilih sesi lalai, jadi tiada
    percanggahan antara apa yang dikejar dan apa yang akan diproses."""
    p = os.path.join(stor, 'harga_idx.csv')
    d = pd.read_csv(p, usecols=['date'])
    return [str(pd.Timestamp(str(int(x))).date()) for x in sorted(set(d.date))]


def baca_json(teks):
    """Rekod larian daripada stdout harian_c.py, atau {} jika tiada.

    `cmd_malam` mencetak dengan `indent=1`, jadi rekodnya MERENTAS banyak baris. Versi pertama
    skrip ini membaca baris terakhir yang boleh di-parse JSON, dan itu gagal dengan cara yang
    paling buruk: ia tidak mengembalikan ralat, ia mengembalikan baris dalaman seperti
    `  "2026-10-30",` yang di-parse menjadi RENTETAN, kemudian `.get` padanya membuang
    AttributeError selepas imbasan 15 minit selesai. Ditangkap oleh ujian hujung-ke-hujung,
    bukan oleh ujian unit — sebab itu ujian hujung-ke-hujung dijalankan.
    """
    teks = (teks or '').strip()
    calon = [teks]
    if '{' in teks:
        calon.append(teks[teks.index('{'):])
    calon += [b for b in reversed(teks.splitlines()) if b.strip().startswith('{')]
    for c in calon:
        try:
            v = json.loads(c)
        except ValueError:
            continue
        if isinstance(v, dict):
            return v
    return {}


def jalan(arg, kering):
    """Jalankan harian_c.py dalam SUBPROSES dengan laluan import yang sama seperti produksi.
    Pelajaran 1 Nov 2026 (CLAUDE.md): ujian yang mengimport modul terus boleh lulus sambil
    produksi gagal, kerana pemuat produksi menetapkan sys.path secara berbeza."""
    cmd = [sys.executable, os.path.join(HERE, 'harian_c.py')] + arg
    if kering:
        return dict(kering=True, cmd=' '.join(arg))
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = baca_json(p.stdout)
    if p.returncode:
        out = dict(out, ralat=(p.stderr or '').strip()[-400:] or f'kod keluar {p.returncode}')
    return out


def buka_sesi(terkini, D, keluar):
    """Tulis CSV ticker,open,volume bagi tarikh D daripada data/harga/terkini.csv.
    Pulang laluan fail, atau None jika tiada bar bagi D (contohnya pasaran belum dibuka)."""
    if not os.path.exists(terkini):
        return None
    d = pd.read_csv(terkini)
    hari = d[d.date == int(str(D).replace('-', ''))]
    hari = hari[hari.open > 0]
    if not len(hari):
        return None
    p = os.path.join(keluar, f'buka_{D}.csv')
    hari[['ticker', 'open', 'volume']].to_csv(p, index=False)
    return p


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=PT)
    ap.add_argument('--isyarat', default=os.path.join(BS2, 'data', 'isyarat'))
    ap.add_argument('--stor', default=STOR)
    ap.add_argument('--terkini', default=TERKINI)
    ap.add_argument('--proses', type=int, default=4)
    ap.add_argument('--maks', type=int, default=5,
                    help='had sesi tertinggal yang dikejar dalam satu larian; lebih daripada ini '
                         'bermakna sesuatu yang lebih besar rosak dan manusia patut melihat dahulu')
    ap.add_argument('--tanpa-beli', action='store_true', help='kejar imbasan sahaja, jangan rekod belian lampau')
    ap.add_argument('--kering', action='store_true', help='cetak apa yang akan dijalankan, jangan tulis')
    a = ap.parse_args(argv)

    sp = os.path.join(a.folder, 'status_harian.json')
    st = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
    akhir_diproses = (st.get('malam') or {}).get('sesi') or ''
    SES = sesi_stor(a.stor)
    if not SES:
        print(json.dumps(dict(dikejar=[], nota=['stor harga kosong']), ensure_ascii=False)); return 0

    # Sesi TERTINGGAL = selepas yang terakhir diproses, tetapi BUKAN yang terakhir dalam stor:
    # sesi terakhir ialah kerja biasa langkah `malam` dalam harian.yml, dan ia ada pengawal
    # datanya sendiri (data_belum_muktamad). Kejar hanya menangani lubang di BELAKANGnya.
    tertinggal = [s for s in SES[:-1] if s > akhir_diproses] if akhir_diproses else []
    if not akhir_diproses:
        nota = ['status_harian.json tiada malam.sesi — tiada rujukan untuk mengejar; dilangkau']
        print(json.dumps(dict(dikejar=[], nota=nota), ensure_ascii=False)); return 0
    if not tertinggal:
        print(json.dumps(dict(dikejar=[], akhir_diproses=akhir_diproses, sesi_stor_akhir=SES[-1]),
                         ensure_ascii=False)); return 0
    if len(tertinggal) > a.maks:
        print(json.dumps(dict(dikejar=[], tertinggal=tertinggal,
                              nota=[f'{len(tertinggal)} sesi tertinggal > had --maks {a.maks}: '
                                    f'tidak dikejar automatik, perlu semakan manual']),
                         ensure_ascii=False), file=sys.stderr)
        return 2

    kerja = tempfile.mkdtemp(prefix='kejar_')
    dikejar, belian, langkau, nota = [], [], [], []
    for i, S in enumerate(tertinggal):
        r = jalan(['malam', '--folder', a.folder, '--isyarat', a.isyarat,
                   '--sesi', S, '--proses', str(a.proses)], a.kering)
        if r.get('ralat'):
            nota.append(f'malam {S}: {r["ralat"]}')
            break                                   # jangan teruskan ke sesi lebih baharu atas keadaan separa
        if r.get('ditangguh') or r.get('langkau'):
            langkau.append(dict(sesi=S, sebab=r.get('ditangguh') or r.get('langkau')))
            continue
        dikejar.append(S)
        if a.tanpa_beli:
            continue
        # Belian sesi S sepatutnya berlaku pada pagi hari dagangan BERIKUTNYA. Hari itu diambil
        # daripada senarai sesi stor, bukan kalendar, supaya cuti tidak boleh menyebabkan
        # tarikh yang tidak pernah didagangkan.
        j = SES.index(S)
        D = SES[j + 1] if j + 1 < len(SES) else None
        if not D:
            continue
        # "Sudah direkod" mesti bermakna belian BENAR-BENAR dinilai, bukan sekadar ada entri bagi
        # tarikh itu. Pada 2 Nov 2026 `beli.yml` menulis rekod `direkod: 0` dengan nota "senarai_beli
        # belum dikemas kini" — itu KESAN kegagalan yang kita sedang pulihkan, jadi melayannya
        # sebagai "sudah direkod" akan membuang semula kohort yang sama yang kita datang untuk
        # selamatkan. Rekod sedemikian ditulis ganti dengan --paksa; rekod sebenar tidak disentuh.
        beli_ada = (st.get('beli') or {})
        kosong = beli_ada.get('tarikh') == D and not beli_ada.get('direkod')
        if beli_ada.get('tarikh') == D and beli_ada.get('direkod') and not a.kering:
            langkau.append(dict(beli=D, sebab=f"sudah direkod ({beli_ada.get('direkod')} posisi)")); continue
        if beli_ada.get('tarikh') == D and 'pasaran AS tutup' in str(beli_ada.get('nota') or ''):
            langkau.append(dict(beli=D, sebab='pasaran tutup')); continue
        fb = None if a.kering else buka_sesi(a.terkini, D, kerja)
        if not a.kering and not fb:
            langkau.append(dict(beli=D, sebab='tiada harga buka dalam terkini.csv'))
            continue
        rb = jalan(['beli', '--folder', a.folder, '--tarikh', D, '--akhir'] +
                   (['--paksa'] if kosong else []) +
                   ([] if a.kering else ['--buka', fb, '--sumber-buka', f'kejar: buka sebenar {D} (terkini.csv)']),
                   a.kering)
        if rb.get('ralat'):
            nota.append(f'beli {D}: {rb["ralat"]}')
            break
        belian.append(dict(tarikh=D, direkod=rb.get('direkod'), dilangkau=rb.get('dilangkau'), nota=rb.get('nota')))
        st = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else st

    hasil = dict(dikejar=dikejar, belian=belian, langkau=langkau, nota=nota,
                 akhir_diproses=akhir_diproses, tertinggal=tertinggal, sesi_stor_akhir=SES[-1],
                 gred='dilangkau dengan sengaja bagi sesi dikejar (pemangkin semasa = maklumat masa hadapan)')
    print(json.dumps(hasil, ensure_ascii=False))
    return 1 if nota else 0


if __name__ == '__main__':
    raise SystemExit(main())

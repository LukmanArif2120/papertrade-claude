#!/usr/bin/env python3
"""pengawal.py — semak bahawa pengumpulan data papertrade M DAN N berjalan, dan betulkan yang boleh.

SEBAB IA WUJUD. Papertrade ialah mekanisme pengumpulan data, bukan dagangan: setiap sesi yang
terlepas ialah lubang KEKAL dalam rekod, kerana isyarat hari itu tidak boleh dijana semula pada
harga hari itu kemudian. Audit 3 Nov 2026 menemui dua kegagalan yang berjalan SENYAP selama
berhari-hari - 835 posisi Nxx tidak dikemas kini, dan satu susunan yang akan meranapkan lejar -
dan kedua-duanya hanya ditemui kerana seseorang pergi mencari. Pengawal ini mencari setiap hari.

SEMPADAN AUTO-BETUL. Hanya remedi yang (a) sudah wujud sebagai alat yang diuji, (b) idempoten,
dan (c) tidak membuat keputusan baharu, dijalankan sendiri. Selebihnya dilaporkan sahaja. Contoh
yang SENGAJA tidak diauto-betulkan:

  * dokumen db melepasi had - pembetulannya mesti `subBhg()` + TERBIT dahulu, baru `jana_db.PECAH`;
    urutan terbalik membuat halaman kehilangan baris secara SENYAP, iaitu lebih buruk daripada
    masalah asal;
  * gred yang hilang - mengisinya dengan nilai hari ini menukar medan titik-masa menjadi maklumat
    masa hadapan relatif kepada tarikh isyarat;
  * kaedah yang membuang ralat - ia perlu didiagnosis, bukan dicuba semula;
  * belian yang terlepas pada hari lepas - merekodnya selepas fakta ialah keputusan pengguna.

Guna:
    python3 BacktestShariah2/standard/pengawal.py                 # semak sahaja
    python3 BacktestShariah2/standard/pengawal.py --betulkan      # semak + jalankan remedi selamat
    python3 BacktestShariah2/standard/pengawal.py --ntfy          # satu baris untuk amaran telefon

Kod keluar: 0 semua baik (atau semua yang gagal sudah dibetulkan) · 1 ada masalah yang TINGGAL.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
LEJAR = os.path.join(BS2, 'lejar')
KOD = os.path.join(BS2, 'kod')

KELUARGA = ('M', 'N')          # keluarga yang MESTI kedua-duanya bergerak setiap sesi


def sesi_stor(stor=STOR):
    p = os.path.join(stor, 'harga_idx.csv')
    if not os.path.exists(p):
        return []
    d = pd.read_csv(p, usecols=['date'])
    return [str(pd.Timestamp(str(int(x))).date()) for x in sorted(set(d.date))]


def fam(mid):
    s = str(mid or '')
    return 'N' if s.startswith('N') else 'GB' if s.startswith('GB') else 'M' if s.startswith('M') else '?'


def baca_csv(p):
    import csv
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def jalan(arg, kering):
    """Jalankan alat repo dalam subproses - laluan import yang SAMA seperti produksi."""
    if kering:
        return dict(dijalankan=False, cmd=' '.join(arg))
    p = subprocess.run([sys.executable] + arg, capture_output=True, text=True, cwd=os.path.dirname(BS2))
    return dict(dijalankan=True, rc=p.returncode, ralat=(p.stderr or '').strip()[-200:] if p.returncode else None)


class Semakan:
    def __init__(self):
        self.hasil = []

    def tambah(self, nama, ok, butiran='', remedi=None, boleh_betul=False, cetus=None):
        self.hasil.append(dict(nama=nama, ok=bool(ok), butiran=butiran, remedi=remedi,
                               boleh_betul=bool(boleh_betul), dibetulkan=None, cetus=cetus))

    def gagal(self):
        return [h for h in self.hasil if not h['ok']]

    def tinggal(self):
        return [h for h in self.hasil if not h['ok'] and h['dibetulkan'] is not True]


def semak(folder, stor, lejar_dir, a):
    S = Semakan()
    ses = sesi_stor(stor)
    akhir = ses[-1] if ses else None
    sp = os.path.join(folder, 'status_harian.json')
    st = {}
    if os.path.exists(sp):
        with open(sp, encoding='utf-8') as f:
            st = json.load(f)
    m = st.get('malam') or {}
    b = st.get('beli') or {}

    # 1. Sesi terkini stor sudah diproses.
    #
    #    Remedi bergantung pada BENTUK jurang, dan membezakannya penting: `kejar.py` sengaja tidak
    #    menyentuh sesi TERKINI (itu kerja langkah `malam` harian.yml, yang ada pengawal datanya
    #    sendiri), jadi memanggilnya apabila yang hilang ialah sesi terkini tidak melakukan apa-apa.
    #    Ujian 3 Nov 2026 mendedahkan ini: pengawal melaporkan "remedi jalan tetapi semakan masih
    #    gagal" - jujur, tetapi tidak berguna.
    #
    #    Jadi: lubang DI BELAKANG -> kejar.py (pengawal betulkan sendiri). Sesi TERKINI belum
    #    diproses -> harian.yml belum menjalankan tugasnya, dan pembetulan yang betul ialah
    #    MENCETUS harian.yml, bukan meniru imbasannya di sini. pengawal.yml membaca bendera
    #    `cetus` dalam keluaran dan mencetusnya. Pengawal mencetus saluran yang diuji; ia tidak
    #    membina saluran kedua yang tidak pernah diuji.
    diproses = m.get('sesi') or ''
    lubang = [x for x in ses[:-1] if x > diproses] if diproses else []
    ok1 = bool(akhir) and diproses == akhir
    S.tambah('sesi terkini diproses', ok1,
             f"stor {akhir} · diproses {diproses}" +
             (f" · {len(lubang)} lubang di belakang" if lubang else
              (' · sesi terkini belum diproses (harian.yml)' if not ok1 else '')),
             remedi=(['BacktestShariah2/standard/kejar.py', '--folder', folder,
                      '--maks', str(a.maks_kejar if a else 2)] if lubang else None),
             boleh_betul=bool(lubang), cetus=(None if ok1 or lubang else 'harian.yml'))

    # 2. KEDUA-DUA keluarga ada dalam senarai beli. Ini semakan paling penting dalam fail ini:
    #    ia menjawab "adakah kohort N masih hidup" dengan satu nombor, setiap hari.
    sk = m.get('senarai_keluarga') or {}
    for k in KELUARGA:
        S.tambah(f'senarai beli ada {k}xx', sk.get(k, 0) > 0, f"{k} {sk.get(k, 0)} baris")

    # 3. KEDUA-DUA keluarga ada posisi dengan harga dikemas kini pada sesi terakhir.
    pos = []
    for p in sorted(glob.glob(os.path.join(folder, 'claude*.csv'))):
        pos += baca_csv(p)
    hidup = [r for r in pos if r.get('tarikh_beli') and r.get('harga_beli')
             and r.get('tidak_dibeli') not in ('1', 'ya', 'True', 'benar')
             and r.get('keluar') not in ('1', 'ya', 'True', 'benar')]
    for k in KELUARGA:
        g = [r for r in hidup if fam(r.get('kaedah')) == k]
        kemas = sum(1 for r in g if r.get('harga_terkini'))
        S.tambah(f'posisi {k}xx dikemas kini', not g or kemas == len(g),
                 f"{kemas}/{len(g)} ada harga_terkini")

    # 4. Tiada kaedah yang membuang ralat, tiada posisi tanpa modul. TIDAK diauto-betulkan.
    r1 = m.get('ralat_kaedah') or []
    S.tambah('tiada kaedah ralat', not r1, '; '.join(r1[:3]) or 'tiada')
    r2 = m.get('kaedah_tanpa_modul') or []
    S.tambah('tiada posisi tanpa modul', not r2, '; '.join(map(str, r2[:3])) or 'tiada')

    # 5. Setiap modul kaedah boleh dimuat melalui laluan import PRODUKSI (kod/, bukan kod/kaedah/).
    #    Pelajaran 1 Nov 2026: ujian unit lulus sambil produksi gagal ModuleNotFoundError.
    mods = sorted(os.path.basename(x)[:-3] for pola in ('M*.py', 'N*.py', 'GB*.py')
                  for x in glob.glob(os.path.join(KOD, 'kaedah', pola)))
    kod = ('import sys, importlib, json\n'
           f'sys.path.insert(0, {KOD!r})\n'
           'g = []\n'
           f'for m in {mods!r}:\n'
           '    try: importlib.import_module("kaedah." + m)\n'
           '    except Exception as e: g.append(m + ": " + type(e).__name__)\n'
           'print(json.dumps(g))')
    p = subprocess.run([sys.executable, '-c', kod], capture_output=True, text=True)
    try:
        rosak = json.loads(p.stdout.strip() or '[]')
    except ValueError:
        rosak = ['(pengawal tidak dapat menyemak: ' + (p.stderr or '')[-80:] + ')']
    S.tambah('semua modul kaedah dimuat', not rosak, f'{len(mods) - len(rosak)}/{len(mods)} ok' +
             ('; ' + '; '.join(rosak[:3]) if rosak else ''))

    # 6. Lorong 2 dinilai bagi setiap posisi YANG BOLEH DINILAI. `keluar_lorong` sendiri melaporkan
    #    `tidak_dinilai` bagi posisi yang stor harganya tiada bar pada hari beli (3 Nov 2026: KVUE
    #    M14, ticker yang memang tiada bar 11-02). Membandingkan dengan sifar akan menjadikan
    #    jurang data ticker kelihatan sebagai kegagalan saluran, dan pengawal yang menjerit setiap
    #    hari tentang perkara yang tidak boleh dibetulkan akan diabaikan - itu lebih buruk daripada
    #    tiada pengawal. Jadi baki yang SAMA dengan `tidak_dinilai` diterima dan dinyatakan.
    l2 = [k for k in (hidup[0] if hidup else {}) if k.endswith('_henti')]
    if l2 and hidup:
        k0 = l2[0]
        belum = sum(1 for r in hidup if not r.get(k0))
        # Baki SAH dikira terus daripada stor (baca sahaja): posisi yang tickernya tiada bar pada
        # hari beli tidak boleh dinilai oleh sesiapa. `keluar_lorong` sendiri mengira perkara yang
        # sama dan melaporkannya sebagai `tidak_dinilai`, tetapi memanggilnya di sini akan MENULIS
        # fail - dan semakan tidak boleh mempunyai kesan sampingan, atau laporan "sebelum" tidak
        # lagi bermakna.
        td = 0
        if belum:
            bar = set()
            for f_ in ('harga_A.csv', 'harga_B.csv'):
                q = os.path.join(stor, f_)
                if os.path.exists(q):
                    d_ = pd.read_csv(q, usecols=['ticker', 'date'])
                    bar |= set(zip(d_.ticker, d_.date.astype(str)))
            for r_ in hidup:
                if r_.get(k0):
                    continue
                kunci = (r_.get('saham'), str(r_.get('tarikh_beli', '')).replace('-', ''))
                if kunci not in bar:
                    td += 1
        S.tambah('lorong 2 dinilai', belum <= td,
                 f'{belum} belum dinilai, {td} memang tidak boleh (tiada bar hari beli)',
                 remedi=['BacktestShariah2/standard/keluar_lorong.py', '--folder', folder, '--stor', stor],
                 boleh_betul=True)

    # 7. Tiada fail posisi yang unjuran dokumennya melebihi had db. Remedi: pecah_claude --pecah.
    p = jalan(['BacktestShariah2/standard/pecah_claude.py', '--folder', folder], kering=True)
    r = subprocess.run([sys.executable, 'BacktestShariah2/standard/pecah_claude.py', '--folder', folder],
                       capture_output=True, text=True, cwd=os.path.dirname(BS2))
    try:
        lebih = json.loads(r.stdout or '{}').get('melebihi') or []
    except ValueError:
        lebih = []
    S.tambah('fail posisi dalam had db', not lebih, f'{len(lebih)} melebihi',
             remedi=['BacktestShariah2/standard/pecah_claude.py', '--pecah', '--folder', folder],
             boleh_betul=True)

    # 8. sahkan.py 0 ralat. Remedi: sahkan.py --betulkan (alat rasmi, sudah dalam aliran malam).
    r = subprocess.run([sys.executable, 'BacktestShariah2/standard/sahkan.py', '--folder', folder],
                       capture_output=True, text=True, cwd=os.path.dirname(BS2))
    akhir_baris = (r.stdout or '').strip().splitlines()[-1:] or ['']
    n_ralat = 0
    if 'ralat' in akhir_baris[0]:
        try:
            n_ralat = int(akhir_baris[0].split('Ringkasan:')[1].split('ralat')[0].strip())
        except Exception:
            n_ralat = 0 if r.returncode == 0 else 1
    S.tambah('sahkan.py 0 ralat', n_ralat == 0, akhir_baris[0][:90],
             remedi=['BacktestShariah2/standard/sahkan.py', '--betulkan', '--folder', folder],
             boleh_betul=True)

    # 9. Lejar Penuh segar. TIDAK diauto-betulkan: lejar.yml memilikinya dan larian berganda mahal.
    stl = os.path.join(lejar_dir, 'status.json')
    sl = {}
    if os.path.exists(stl):
        with open(stl, encoding='utf-8') as f:
            sl = json.load(f)
    S.tambah('lejar segar', akhir and sl.get('sesi_terakhir') == akhir,
             f"lejar {sl.get('sesi_terakhir')} · stor {akhir}",
             cetus=None if (akhir and sl.get('sesi_terakhir') == akhir) else 'lejar.yml')

    # 10. Belian direkod bagi hari dagangan terakhir yang sudah berlalu. Laporan sahaja.
    S.tambah('belian direkod', bool(b.get('tarikh')), f"{b.get('tarikh')} · {b.get('direkod')} direkod")
    return S


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=PT)
    ap.add_argument('--stor', default=STOR)
    ap.add_argument('--lejar', default=LEJAR)
    ap.add_argument('--maks-kejar', type=int, default=2, dest='maks_kejar',
                    help='had sesi yang kejar.py kejar dalam SATU larian pengawal. Lalai 2, bukan 5 '
                         '(had kejar sendiri), kerana pengawal memegang kunci concurrency '
                         '`papertrade` sambil berjalan dan beli.yml berkongsi kunci itu. beli.yml '
                         'ada pintu KERAS 09:31-17:00 NY: jika rantaian beratur menolaknya melepasi '
                         '17:00 NY, belian hari itu TIDAK berlaku dan isyarat itu hilang kekal. Dua '
                         'sesi (~90 minit) mengehadkan pegangan kunci; lubang yang tinggal dikejar '
                         'oleh harian.yml, yang berjalan empat kali sehari dan boleh mengejar 5.')
    ap.add_argument('--betulkan', action='store_true', help='jalankan remedi selamat bagi semakan yang gagal')
    ap.add_argument('--ntfy', action='store_true', help='cetak satu baris ringkas untuk amaran telefon')
    a = ap.parse_args(argv)

    S = semak(a.folder, a.stor, a.lejar, a)
    if a.betulkan:
        for h in S.gagal():
            if not h['boleh_betul'] or not h['remedi']:
                continue
            r = jalan(h['remedi'], kering=False)
            h['dibetulkan'] = r.get('rc') == 0
            h['nota_remedi'] = r.get('ralat') or ('dijalankan' if h['dibetulkan'] else 'gagal')
        if any(h['dibetulkan'] for h in S.hasil if h['dibetulkan'] is not None):
            S2 = semak(a.folder, a.stor, a.lejar, a)   # semak semula selepas remedi
            for lama, baru in zip(S.hasil, S2.hasil):
                if lama['dibetulkan'] is True and not baru['ok']:
                    lama['dibetulkan'] = False
                    lama['nota_remedi'] = 'remedi jalan tetapi semakan masih gagal'
                elif baru['ok']:
                    lama['ok'] = True

    tinggal = S.tinggal()
    if a.ntfy:
        if not tinggal:
            dib = [h['nama'] for h in S.hasil if h['dibetulkan'] is True]
            print('Pengawal: semua baik' + (f" (dibetulkan: {', '.join(dib)})" if dib else ''))
        else:
            print('⚠ Pengawal: ' + '; '.join(f"{h['nama']} — {h['butiran']}" for h in tinggal)[:180])
    else:
        cetus = sorted({h['cetus'] for h in S.tinggal() if h.get('cetus')})
        print(json.dumps(dict(ok=not tinggal, cetus=cetus, semakan=S.hasil), ensure_ascii=False, indent=1))
    return 1 if tinggal else 0


if __name__ == '__main__':
    raise SystemExit(main())

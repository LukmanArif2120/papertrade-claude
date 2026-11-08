"""Rekod Lejar TAMBAH-SAHAJA: bila setiap posisi mula-mula direkod, dengan kod apa, dan hasil tutup yang DIBEKUKAN.

Masalah (audit 7 Nov 2026): `lejar.bina_semula` memadam terbuka/tutup/isyarat dan mengira semula SEMUA sesi dengan kod
dan stor harga semasa (enam kali 19 Okt–3 Nov, sekali lagi 7 Nov 2026). Tiada baris membawa versi kod atau bendera
"direkod malam itu", jadi data hadapan boleh berubah secara senyap dan isian tidak boleh dibezakan daripada rekod
langsung. Skrip ini TIDAK mengubah Lejar; ia menyimpan saksi di luar lejar/ (`data/konteks/`, selamat daripada bina
semula, disandarkan mingguan oleh sandaran.yml):

  rekod_lejar_YYYYMM.csv   satu baris bagi setiap kunci posisi (id_kaedah|saham|tarikh_isyarat|belian_ke) pada kali
                           PERTAMA ia dilihat: tarikh dilihat, lewat_hari (tarikh dilihat − tarikh isyarat), langsung
                           (lewat_hari <= LANGSUNG_HARI), sha kod kaedah (modul + _nxx.py bagi N/GB), versi peraturan
                           Lejar (tidak_layak + lorong2 + keluar dalam status.json), sumber ('malam' atau 'benih').
  rekod_tutup_YYYYMM.csv   hasil keluar lorong 1 pada kali PERTAMA posisi dilihat ditutup (tarikh, harga, untung, sebab).
  rekod_status.json        hanyut: posisi yang hasil tutup bekunya kini berbeza, hilang, atau dibuka semula (cth.
                           selepas bina semula atau pembetulan peraturan) — DIUKUR, bukan dibaiki.

Fail dibuka dalam mod 'a' (tambah): baris sedia ada tidak pernah ditulis semula.
Benih (`--benih`, sekali): posisi yang sudah wujud direkod dengan sumber 'benih'; `langsung` mengikut takrif
pradaftar kad skor (`lift_kaedah.MULA_LANGSUNG`: Mxx sejak isyarat 2026-10-15, Nxx/GB sejak 2026-11-03) kerana masa
sebenar ia mula-mula direkod tidak diketahui (bina semula 7 Nov 2026 mengira semula kesemuanya).

  python3 BacktestShariah2/standard/rekod_lejar.py            # selepas lejar.py jalan (lejar.yml)
  python3 BacktestShariah2/standard/rekod_lejar.py --benih    # sekali, mengisi saksi bagi posisi sedia ada
Rekod sahaja: tiada order, tiada wang sebenar.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
KONTEKS = os.environ.get('KONTEKS_DIR', os.path.join(BS2, 'data', 'konteks'))
KAEDAH = os.environ.get('REKOD_KAEDAH_DIR', os.path.join(BS2, 'kod', 'kaedah'))
LANGSUNG_HARI = 4        # isyarat Jumaat diproses Sabtu/Isnin; lewat yfinance sehari; lebih daripada ini = isian
L_REKOD = ['id_kaedah', 'saham', 'tarikh_isyarat', 'belian_ke', 'tarikh_beli', 'dilihat', 'lewat_hari', 'langsung',
           'sumber', 'sha_kaedah', 'versi_peraturan']
L_TUTUP = ['id_kaedah', 'saham', 'tarikh_isyarat', 'belian_ke', 'tarikh_keluar', 'harga_keluar', 'untung_pct',
           'sebab_keluar', 'dilihat']
KUNCI = ['id_kaedah', 'saham', 'tarikh_isyarat', 'belian_ke']


def kunci(r):
    return '|'.join(str(r[k]) for k in KUNCI)


def posisi(lejar=None):
    lejar = lejar or LEJAR
    f = [os.path.join(lejar, 'terbuka.csv')] + sorted(glob.glob(os.path.join(lejar, 'tutup', '*.csv')))
    P = [pd.read_csv(x, dtype=str, keep_default_na=False) for x in f if os.path.exists(x)]
    return pd.concat(P, ignore_index=True) if P else pd.DataFrame(columns=KUNCI)


def _baca(pola, konteks):
    """Gabung fail bulanan CSV dan benih termampat (`*_benih.csv.gz`)."""
    f = sorted(glob.glob(os.path.join(konteks, pola)) + glob.glob(os.path.join(konteks, pola + '.gz')))
    return pd.concat([pd.read_csv(x, dtype=str, keep_default_na=False) for x in f], ignore_index=True) if f \
        else pd.DataFrame()


def sha_kaedah(mid, kaedah=None):
    """sha1[:10] kod kaedah: modul sendiri (+ _nxx.py dikongsi bagi N/GB). '' jika modul tiada."""
    kaedah = kaedah or KAEDAH
    f = [os.path.join(kaedah, f'{mid}.py')]
    if not os.path.exists(f[0]):
        return ''
    if mid.startswith(('N', 'GB')):
        f.append(os.path.join(kaedah, '_nxx.py'))
    h = hashlib.sha1()
    for x in f:
        if os.path.exists(x):
            with open(x, 'rb') as f:
                h.update(f.read())
    return h.hexdigest()[:10]


def versi_peraturan(lejar=None):
    p = os.path.join(lejar or LEJAR, 'status.json')
    if not os.path.exists(p):
        return ''
    with open(p, encoding='utf-8') as f:
        s = json.load(f)
    return hashlib.sha1('|'.join(str(s.get(k, '')) for k in ('tidak_layak', 'lorong2', 'keluar')).encode()).hexdigest()[:10]


def _tambah(path, kol, rows):
    """Tambah baris ke CSV (mod 'a'); tulis tajuk hanya jika fail baharu. Baris sedia ada tidak disentuh."""
    if not rows:
        return
    baru = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=kol)
        if baru:
            w.writeheader()
        w.writerows(rows)


def langsung_benih(mid, tarikh_isyarat):
    sys.path.insert(0, HERE)
    import lift_kaedah as lk
    return str(tarikh_isyarat) >= lk.mula_langsung(mid)


def rekod(sekarang=None, benih=False, lejar=None, konteks=None, kaedah=None):
    """Kemas saksi. Pulang dict ringkasan (juga ditulis ke rekod_status.json)."""
    konteks = konteks or KONTEKS
    os.makedirs(konteks, exist_ok=True)
    sekarang = pd.Timestamp(sekarang) if sekarang is not None else pd.Timestamp.now(tz='UTC').tz_localize(None)
    hari = sekarang.strftime('%Y-%m-%d')
    bulan = sekarang.strftime('%Y%m')
    P = posisi(lejar)
    R, T = _baca('rekod_lejar_*.csv', konteks), _baca('rekod_tutup_*.csv', konteks)
    ada = set(R.apply(kunci, axis=1)) if len(R) else set()
    beku = {kunci(r): r for r in T.to_dict('records')} if len(T) else {}
    vp = versi_peraturan(lejar)
    sha = {}
    baru_r, baru_t = [], []
    semasa = {}
    for r in P.to_dict('records'):
        k = kunci(r)
        semasa[k] = r
        if k not in ada:
            mid = r['id_kaedah']
            if mid not in sha:
                sha[mid] = sha_kaedah(mid, kaedah)
            lewat = (sekarang.normalize() - pd.Timestamp(r['tarikh_isyarat'])).days if r['tarikh_isyarat'] else ''
            baru_r.append(dict(id_kaedah=mid, saham=r['saham'], tarikh_isyarat=r['tarikh_isyarat'],
                               belian_ke=r['belian_ke'], tarikh_beli=r.get('tarikh_beli', ''), dilihat=hari,
                               lewat_hari='' if benih else lewat,
                               langsung=langsung_benih(mid, r['tarikh_isyarat']) if benih
                               else (lewat != '' and lewat <= LANGSUNG_HARI),
                               sumber='benih' if benih else 'malam', sha_kaedah=sha[mid], versi_peraturan=vp))
            ada.add(k)
        if r.get('tarikh_keluar') and k not in beku:
            baru_t.append(dict(id_kaedah=r['id_kaedah'], saham=r['saham'], tarikh_isyarat=r['tarikh_isyarat'],
                               belian_ke=r['belian_ke'], tarikh_keluar=r['tarikh_keluar'],
                               harga_keluar=r.get('harga_keluar', ''), untung_pct=r.get('untung_pct', ''),
                               sebab_keluar=r.get('sebab_keluar', ''), dilihat=hari))
    if benih:
        # Benih ditulis SEKALI, termampat (tidak pernah berubah; ~64k baris), supaya saiz repo tidak melonjak.
        for nama, kol, rows in (('rekod_lejar_benih.csv.gz', L_REKOD, baru_r), ('rekod_tutup_benih.csv.gz', L_TUTUP, baru_t)):
            p = os.path.join(konteks, nama)
            if os.path.exists(p):
                raise SystemExit(f'{nama} sudah wujud: benih hanya sekali')
            pd.DataFrame(rows, columns=kol).to_csv(p, index=False, compression='gzip')
    else:
        _tambah(os.path.join(konteks, f'rekod_lejar_{bulan}.csv'), L_REKOD, baru_r)
        _tambah(os.path.join(konteks, f'rekod_tutup_{bulan}.csv'), L_TUTUP, baru_t)
    # hanyut: hasil tutup beku lawan Lejar semasa
    berubah, hilang, dibuka = [], [], []
    for k, b in beku.items():
        c = semasa.get(k)
        if c is None:
            hilang.append(k)
        elif not c.get('tarikh_keluar'):
            dibuka.append(k)
        elif (c['tarikh_keluar'], c.get('untung_pct', '')) != (b['tarikh_keluar'], b['untung_pct']):
            berubah.append(k)
    st = dict(dikemas=sekarang.strftime('%Y-%m-%d %H:%M UTC'), versi_peraturan=vp,
              rekod=int(len(ada)), tutup_beku=int(len(beku) + len(baru_t)), baharu=len(baru_r), tutup_baharu=len(baru_t),
              hanyut=dict(berubah=len(berubah), hilang=len(hilang), dibuka_semula=len(dibuka)),
              contoh=dict(berubah=berubah[:15], hilang=hilang[:15], dibuka_semula=dibuka[:15]),
              nota='Hanyut = posisi yang hasil tutup PERTAMA yang direkod kini berbeza dalam Lejar (bina semula, '
                   'pembetulan peraturan atau data). Diukur sahaja; Lejar tidak diubah.')
    with open(os.path.join(konteks, 'rekod_status.json'), 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', action='store_true', help='rekod posisi sedia ada sebagai benih (sekali)')
    a = ap.parse_args()
    st = rekod(benih=a.benih)
    h = st['hanyut']
    print(f"rekod_lejar: {st['baharu']} posisi baharu, {st['tutup_baharu']} tutup dibekukan; jumlah {st['rekod']} | "
          f"hanyut: berubah {h['berubah']}, hilang {h['hilang']}, dibuka semula {h['dibuka_semula']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Ujian keluarga kaedah merentas saluran: Mxx · Nxx · GBxx.

Dua pepijat yang ujian ini kunci, kedua-duanya ditemui semasa audit 3 Nov 2026 selepas 94
kombinasi Nxx masuk produksi:

1. `harian_c.kumpul_posisi` menapis `mid.startswith('M')`. Tapisan itu betul ketika Mxx
   satu-satunya keluarga; selepas Nxx ia menjadi lubang SENYAP - 835 posisi Nxx tidak
   dikumpul, jadi lorong 1 tidak pernah dinilai dan harga tidak pernah dikemas kini, tanpa
   satu pun ralat. Kegagalan senyap tidak boleh ditangkap oleh pemerhatian; ia perlu ujian.

2. `lejar.py` menyusun dengan `int(kaedah[1:])`, yang membuang ValueError pada 'N19X13'
   dan 'GB02'. Itu ralat KERAS yang menamatkan larian lejar selepas imbasan siap.

Kedua-duanya kelas masalah yang sama: kod yang menganggap satu huruf + nombor.
"""
import os
import sys
import unittest

import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))

import harian_c as H  # noqa: E402
import lejar as L  # noqa: E402

# ID sebenar daripada produksi, satu setiap bentuk
CONTOH = ['M01', 'M166', 'N19X13', 'N124X15', 'GB02']


class TestAwalanKaedah(unittest.TestCase):
    def test_awalan_diterbitkan_daripada_pola(self):
        """AWALAN_KAEDAH mesti datang daripada POLA_KAEDAH, bukan ditaip semula."""
        self.assertEqual(H.AWALAN_KAEDAH, ('M', 'N', 'GB'))
        self.assertEqual(H.AWALAN_KAEDAH, tuple(x.split('*')[0] for x in H.POLA_KAEDAH))

    def test_setiap_keluarga_diterima(self):
        for mid in CONTOH:
            self.assertTrue(mid.startswith(H.AWALAN_KAEDAH), mid)

    def test_bukan_kaedah_ditolak(self):
        """'X13' ialah ID KELUAR, bukan kaedah; '' ialah baris rosak. Kedua-duanya ditolak."""
        for mid in ['X13', 'U14', '', 'luar']:
            self.assertFalse(mid.startswith(H.AWALAN_KAEDAH), mid)


class TestNomborKaedah(unittest.TestCase):
    """Susunan mesti stabil dan tidak boleh membuang ValueError pada mana-mana bentuk ID."""

    def test_tiga_bentuk_tidak_membuang(self):
        for mid in CONTOH:
            for fn in (H.nombor_kaedah, L.nombor_kaedah):
                k = fn(mid)
                self.assertIsInstance(k, tuple, mid)

    def test_keluarga_berurutan(self):
        urut = sorted(CONTOH, key=H.nombor_kaedah)
        self.assertEqual(urut, ['M01', 'M166', 'N19X13', 'N124X15', 'GB02'])

    def test_kombinasi_tidak_seri(self):
        """Sebelum pembetulan setiap Nxx dapat n = 10**6, jadi semua 94 kombinasi seri dan
        susunan fail yang dikomit setiap malam tidak stabil."""
        a, b, c = H.nombor_kaedah('N19X13'), H.nombor_kaedah('N19X15'), H.nombor_kaedah('N19X36')
        self.assertEqual(len({a, b, c}), 3)
        self.assertEqual([a, b, c], sorted([c, b, a]))

    def test_dua_fail_setuju(self):
        """harian_c dan lejar menyimpan salinan sendiri; ia mesti memberi kunci yang sama."""
        for mid in CONTOH + ['X13', '']:
            self.assertEqual(H.nombor_kaedah(mid), L.nombor_kaedah(mid), mid)

    def test_int_ringkas_memang_gagal(self):
        """Merakam SEBAB fungsi ini wujud: cara ringkas membuang pada dua daripada tiga bentuk."""
        self.assertEqual(int('M01'[1:]), 1)
        for mid in ['N19X13', 'GB02']:
            with self.assertRaises(ValueError):
                int(mid[1:])


class TestKumpulPosisi(unittest.TestCase):
    """kumpul_posisi mesti mengumpul SETIAP keluarga, bukan Mxx sahaja."""

    def sediakan(self, tmp):
        import csv
        lajur = ['saham', 'kaedah', 'id_kaedah', 'tarikh_beli', 'tarikh_isyarat', 'harga_beli',
                 'keluar', 'tidak_dibeli', 'sumber']
        baris = [
            dict(saham='AAA', kaedah='M01', id_kaedah='M01', tarikh_beli='2026-11-02',
                 tarikh_isyarat='2026-10-30', harga_beli='10', keluar='', tidak_dibeli='', sumber='isyarat'),
            dict(saham='BBB', kaedah='N19X13', id_kaedah='N19X13', tarikh_beli='2026-11-02',
                 tarikh_isyarat='2026-10-30', harga_beli='20', keluar='', tidak_dibeli='', sumber='isyarat'),
            dict(saham='CCC', kaedah='GB02', id_kaedah='GB02', tarikh_beli='2026-11-02',
                 tarikh_isyarat='2026-10-30', harga_beli='30', keluar='', tidak_dibeli='', sumber='isyarat'),
            dict(saham='DDD', kaedah='M02', id_kaedah='M02', tarikh_beli='2026-11-02',
                 tarikh_isyarat='2026-10-30', harga_beli='40', keluar='', tidak_dibeli='', sumber='luar'),
        ]
        p = os.path.join(tmp, 'claude.csv')
        with open(p, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=lajur)
            w.writeheader()
            for r in baris:
                w.writerow(r)
        return p

    def test_semua_keluarga_dikumpul(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self.sediakan(tmp)
            k = H.kumpul_posisi(tmp, pd.Timestamp('2026-11-02'), [pd.Timestamp('2026-10-30')])
            self.assertIn('M01', k)
            self.assertIn('N19X13', k)      # gagal sebelum pembetulan 3 Nov 2026
            self.assertIn('GB02', k)        # gagal sebelum pembetulan 3 Nov 2026

    def test_sumber_luar_masih_dilangkau(self):
        """Posisi yang diimport dari luar tidak dinilai oleh modul kaedah; itu BUKAN pepijat
        dan pembetulan di atas tidak boleh membukanya."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self.sediakan(tmp)
            k = H.kumpul_posisi(tmp, pd.Timestamp('2026-11-02'), [pd.Timestamp('2026-10-30')])
            self.assertNotIn('M02', k)


class TestSusunanLejar(unittest.TestCase):
    """Meniru TEPAT tiga tempat susunan dalam lejar.py yang dahulu membuang ValueError.
    Diuji dengan campuran tiga keluarga, kerana itulah keadaan produksi sejak 2 Nov 2026."""

    CAMPUR = ['N19X15', 'M10', 'GB02', 'N19X13', 'M02', 'N124X15']

    def test_sort_values_pandas(self):
        """lejar.py:574 — kunci tuple mesti boleh disusun oleh pandas, bukan hanya oleh Python."""
        d = pd.DataFrame(dict(kaedah=self.CAMPUR, saham=list('BACAZB')))
        d['_n'] = d.kaedah.map(L.nombor_kaedah)
        urut = list(d.sort_values(['_n', 'saham']).kaedah)
        self.assertEqual(urut, ['M02', 'M10', 'N19X13', 'N19X15', 'N124X15', 'GB02'])

    def test_sort_senarai_posisi(self):
        """lejar.py:577/578 — susunan terbuka.csv dan tunggu.csv."""
        T = [dict(id_kaedah=k, tarikh_beli='2026-11-02', saham='A') for k in self.CAMPUR]
        T.sort(key=lambda p: (L.nombor_kaedah(p['id_kaedah']), p['tarikh_beli'], p['saham']))
        self.assertEqual([p['id_kaedah'] for p in T],
                         ['M02', 'M10', 'N19X13', 'N19X15', 'N124X15', 'GB02'])


class TestModulNxx(unittest.TestCase):
    """94 kombinasi: setiap satu mesti lengkap masuk + keluar + cara, bukan separuh."""

    @classmethod
    def setUpClass(cls):
        import glob
        cls.fail = sorted(glob.glob(os.path.join(AKAR, 'BacktestShariah2', 'kod', 'kaedah', 'N*.py')))

    def test_bilangan(self):
        self.assertEqual(len(self.fail), 94)

    def test_id_sepadan_nama_fail(self):
        import re
        for p in self.fail:
            nama = os.path.basename(p)[:-3]
            with open(p, encoding='utf-8') as f:
                teks = f.read()
            m = re.search(r"^ID = '([^']+)'", teks, re.M)
            self.assertIsNotNone(m, nama)
            self.assertEqual(m.group(1), nama)

    def test_setiap_satu_masuk_kali_keluar(self):
        """Nama mesti berbentuk N<masuk>X<keluar>: kombinasi, bukan masuk sahaja."""
        import re
        for p in self.fail:
            nama = os.path.basename(p)[:-3]
            self.assertRegex(nama, r'^N\d+X\d+$')

    def test_tiada_henti_tiada_sasaran(self):
        """stop = NaN dan tgt = NaN ialah keputusan reka bentuk (KOLAM_EKOR.md §4a kecacatan
        henti hari-0; KOMBINASI.md sasaran 1xATR menukar asas positif jadi negatif). Jika satu
        modul memperkenalkan henti, kohort itu tidak lagi mengukur perkara yang sama."""
        for p in self.fail:
            with open(p, encoding='utf-8') as f:
                teks = f.read()
            self.assertIn('ADA_HENTI = False', teks, os.path.basename(p))


if __name__ == '__main__':
    unittest.main()

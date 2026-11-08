"""Ujian unit bagi standard/rekod_lejar.py (saksi Lejar tambah-sahaja, 8 Nov 2026).

Dikunci: (1) baris sedia ada tidak pernah ditulis semula; (2) hasil tutup dibekukan pada kali pertama dilihat dan
hanyut selepas bina semula DIKESAN; (3) isian lewat (bina semula) tidak dilabel langsung; (4) sha kod berubah apabila
modul berubah.
"""
import os
import sys
import tempfile
import unittest

import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import rekod_lejar as RL  # noqa: E402

LAJUR = ['id_kaedah', 'saham', 'sumber', 'tarikh_isyarat', 'rank', 'tarikh_beli', 'harga_beli', 'henti', 'sasaran',
         'tmax', 'belian_ke', 'dinilai_hingga', 'keluar_esok', 'laras', 'tarikh_keluar', 'harga_keluar', 'sebab_keluar',
         'hari', 'untung_pct']


def baris(mid, s, isy, keluar='', untung=''):
    d = {k: '' for k in LAJUR}
    d.update(id_kaedah=mid, saham=s, tarikh_isyarat=isy, tarikh_beli=isy, belian_ke='1', harga_beli='10',
             tarikh_keluar=keluar, harga_keluar='11' if keluar else '', untung_pct=untung,
             sebab_keluar='kaedah' if keluar else '')
    return d


class TestRekod(unittest.TestCase):

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        r = self.d.name
        self.lej, self.kon, self.kae = (os.path.join(r, x) for x in ('lejar', 'konteks', 'kaedah'))
        os.makedirs(os.path.join(self.lej, 'tutup'))
        os.makedirs(self.kae)
        for p, t in ((os.path.join(self.kae, 'M01.py'), 'X = 1\n'),
                     (os.path.join(self.lej, 'status.json'), '{"tidak_layak": "v3", "lorong2": "c4", "keluar": "k1"}')):
            with open(p, 'w') as f:
                f.write(t)

    def tearDown(self):
        self.d.cleanup()

    def tulis(self, terbuka, tutup):
        pd.DataFrame(terbuka, columns=LAJUR).to_csv(os.path.join(self.lej, 'terbuka.csv'), index=False)
        pd.DataFrame(tutup, columns=LAJUR).to_csv(os.path.join(self.lej, 'tutup', '2026-11.csv'), index=False)

    def jalan(self, bila, benih=False):
        return RL.rekod(sekarang=bila, benih=benih, lejar=self.lej, konteks=self.kon, kaedah=self.kae)

    def baca(self, pola):
        return RL._baca(pola, self.kon)

    def test_tambah_sahaja_dan_langsung(self):
        self.tulis([baris('M01', 'AAA', '2026-11-09')], [])
        self.jalan('2026-11-10 06:30')
        with open(os.path.join(self.kon, 'rekod_lejar_202611.csv')) as f:
            isi = f.read()
        # posisi lama baharu muncul (isian bina semula): lewat 25 hari -> bukan langsung
        self.tulis([baris('M01', 'AAA', '2026-11-09'), baris('M01', 'BBB', '2026-10-16')], [])
        st = self.jalan('2026-11-10 07:00')
        self.assertEqual(st['baharu'], 1)
        with open(os.path.join(self.kon, 'rekod_lejar_202611.csv')) as f:
            isi2 = f.read()
        self.assertTrue(isi2.startswith(isi))                   # baris lama tidak disentuh
        R = self.baca('rekod_lejar_*.csv').set_index('saham')
        self.assertEqual(R.loc['AAA', 'langsung'], 'True')      # dilihat 1 hari selepas isyarat
        self.assertEqual(R.loc['BBB', 'langsung'], 'False')
        self.assertEqual(R.loc['BBB', 'lewat_hari'], '25')
        self.assertEqual(self.jalan('2026-11-10 08:00')['baharu'], 0)    # idempoten

    def test_hasil_tutup_beku_dan_hanyut(self):
        self.tulis([], [baris('M01', 'AAA', '2026-11-02', '2026-11-05', '4.0'),
                        baris('M01', 'CCC', '2026-11-02', '2026-11-04', '-2.0'),
                        baris('M01', 'DDD', '2026-11-02', '2026-11-04', '1.0')])
        self.jalan('2026-11-06')
        # bina semula: AAA hasil berubah, CCC dibuka semula, DDD hilang
        self.tulis([baris('M01', 'CCC', '2026-11-02')], [baris('M01', 'AAA', '2026-11-02', '2026-11-06', '9.0')])
        st = self.jalan('2026-11-07')
        self.assertEqual(st['hanyut'], dict(berubah=1, hilang=1, dibuka_semula=1))
        T = self.baca('rekod_tutup_*.csv')
        self.assertEqual(T[T.saham == 'AAA'].untung_pct.tolist(), ['4.0'])   # hasil PERTAMA kekal beku

    def test_benih_ikut_takrif_pradaftar(self):
        self.tulis([baris('N19X13', 'AAA', '2026-10-20'), baris('N19X13', 'BBB', '2026-11-04'),
                    baris('M01', 'CCC', '2026-10-20')], [])
        self.jalan('2026-11-08', benih=True)
        R = self.baca('rekod_lejar_*.csv').set_index('saham')
        self.assertEqual(R.loc['AAA', 'langsung'], 'False')     # Nxx sebelum 2026-11-03 = isian
        self.assertEqual(R.loc['BBB', 'langsung'], 'True')
        self.assertEqual(R.loc['CCC', 'langsung'], 'True')      # Mxx sejak 2026-10-15
        self.assertTrue((R.sumber == 'benih').all())
        self.assertTrue(os.path.exists(os.path.join(self.kon, 'rekod_lejar_benih.csv.gz')))
        with self.assertRaises(SystemExit):                     # benih hanya sekali
            self.jalan('2026-11-09', benih=True)
        # larian malam selepas benih: tiada pendua, posisi baharu ke fail bulanan biasa
        self.tulis([baris('N19X13', 'AAA', '2026-10-20'), baris('N19X13', 'EEE', '2026-11-09')], [])
        self.assertEqual(self.jalan('2026-11-10')['baharu'], 1)

    def test_sha_kod_berubah(self):
        a = RL.sha_kaedah('M01', self.kae)
        with open(os.path.join(self.kae, 'M01.py'), 'w') as f:
            f.write('X = 2\n')
        self.assertNotEqual(a, RL.sha_kaedah('M01', self.kae))
        self.assertEqual(RL.sha_kaedah('M99', self.kae), '')

    def test_di_luar_lejar(self):
        self.assertFalse(os.path.abspath(RL.KONTEKS).startswith(os.path.abspath(RL.LEJAR) + os.sep))


if __name__ == '__main__':
    unittest.main()

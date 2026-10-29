"""Ujian unit bagi standard/banding_spus.py (MDD berasas, kuasa statistik, muat data)."""
import os
import sys
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import banding_spus as BS  # noqa: E402


class TestMdd(unittest.TestCase):
    def test_mdd_asas_termasuk_sesi_pertama(self):
        # Ekuiti sesi pertama ialah TUTUP hari itu; penurunan daripada asas 1.0 mesti dikira.
        E = pd.DataFrame({'ekuiti': [0.90, 0.95, 1.05]})
        self.assertAlmostEqual(BS.mdd_lorong(E), -10.0, places=4)

    def test_mdd_lajur_sahaja_terlepas_penurunan(self):
        # Menunjukkan sebab mdd_lorong ada: mdd() atas lajur sahaja memberi 0, bukan -10.
        E = pd.DataFrame({'ekuiti': [0.90, 0.95, 1.05]})
        self.assertAlmostEqual(BS.mdd(E.ekuiti.to_numpy()), 0.0, places=6)
        self.assertLess(BS.mdd_lorong(E), BS.mdd(E.ekuiti.to_numpy()))

    def test_mdd_menaik_sifar(self):
        self.assertAlmostEqual(BS.mdd_lorong(pd.DataFrame({'ekuiti': [1.1, 1.2]})), 0.0, places=6)

    def test_mdd_siri_pendek_nan(self):
        self.assertTrue(np.isnan(BS.mdd(np.array([1.0]))))


class TestSesiPerlu(unittest.TestCase):
    def test_kelebihan_besar_perlu_sesi_sedikit(self):
        a = BS.sesi_perlu(1.5, 8, 20.0)
        b = BS.sesi_perlu(1.5, 8, 5.0)
        self.assertLess(a, b)

    def test_skala_kuasa_dua_songsang(self):
        # Separuh kelebihan -> empat kali sesi.
        a = BS.sesi_perlu(1.5, 8, 10.0)
        b = BS.sesi_perlu(1.5, 8, 5.0)
        self.assertAlmostEqual(b / a, 4.0, places=4)

    def test_hingar_lebih_besar_perlu_lebih_lama(self):
        self.assertGreater(BS.sesi_perlu(3.0, 8, 10.0), BS.sesi_perlu(1.5, 8, 10.0))

    def test_input_tidak_sah_nan(self):
        for args in ((1.5, 8, 0.0), (1.5, 8, -5.0), (0.0, 8, 10.0), (1.5, 0, 10.0)):
            self.assertTrue(np.isnan(BS.sesi_perlu(*args)), args)


class TestData(unittest.TestCase):
    def test_spus_harian_boleh_dimuat(self):
        S = BS.muat_spus()
        self.assertGreater(len(S), 10)
        self.assertEqual(list(S.columns), ['tarikh', 'buka', 'tutup'])
        self.assertTrue((S.buka > 0).all() and (S.tutup > 0).all())
        self.assertTrue(S.tarikh.is_monotonic_increasing)

    def test_lorong_kecualikan_jalur(self):
        # Fail jalur berakhir dengan _ekuiti.csv tetapi BUKAN lorong.
        L = BS.lorong()
        self.assertNotIn('rawak_jalur', L)
        self.assertTrue(all('jalur' not in k for k in L))

    def test_lorong_ada_lajur_wajib(self):
        for nm, E in BS.lorong().items():
            self.assertIn('ekuiti', E.columns, nm)
            self.assertIn('tarikh', E.columns, nm)


if __name__ == '__main__':
    unittest.main()

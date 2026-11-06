"""Ujian unit bagi standard/lift_kaedah.py.

Dua sifat yang MESTI dikunci, kerana kedua-duanya ialah sebab skrip ini ada:

1. `nilai()` menilai posisi TERBUKA dengan tanda-ke-pasaran, bukan meninggalkannya. Jika ia
   tergelincir kembali kepada posisi ditutup sahaja, laporan ini menjadi pendua
   `KAEDAH_TERBAIK.md` dengan bias penapisan keluar yang sama.
2. `lift_tsk()` mengeluarkan baris kaedah itu sendiri daripada asas selnya. Tanpa itu, kaedah
   yang menguasai selnya mencairkan asasnya sendiri dan liftnya ditarik ke sifar secara
   mekanikal — ia akan kelihatan seperti "tiada kelebihan" pada data yang direka khusus untuk
   mempunyai kelebihan.
"""
import os
import sys
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import lift_kaedah as LK  # noqa: E402


def pos(**k):
    """Satu rangka posisi Lejar minimum (lajur yang `nilai()` baca)."""
    n = len(k['saham'])
    d = dict(id_kaedah=['M01'] * n, tarikh_beli=['2026-10-16'] * n, harga_beli=[100.0] * n,
             tarikh_keluar=[''] * n, untung_pct=[np.nan] * n, hari=[np.nan] * n)
    d.update(k)
    return pd.DataFrame(d)


class TestNilai(unittest.TestCase):
    """Posisi terbuka DITANDA-KE-PASARAN; posisi tutup guna untung akhir. Kos ditolak sekali."""

    def setUp(self):
        self.akhir = pd.Series({'AAA': 110.0, 'BBB': 90.0})
        self.idx = {'20261016': 0, '20261017': 1, '20261018': 2, '20261019': 3}

    def test_terbuka_ditanda_ke_pasaran(self):
        P = LK.nilai(pos(saham=['AAA', 'BBB']), self.akhir, self.idx)
        self.assertEqual(len(P), 2, 'posisi terbuka tidak boleh dibuang')
        self.assertAlmostEqual(float(P.pul.iloc[0]), 10.0 - LK.KOS, places=6)
        self.assertAlmostEqual(float(P.pul.iloc[1]), -10.0 - LK.KOS, places=6)

    def test_tutup_guna_untung_akhir_bukan_harga_kini(self):
        # AAA naik kepada 110 dalam stor, tetapi posisi ini sudah keluar pada +3%.
        P = LK.nilai(pos(saham=['AAA'], tarikh_keluar=['2026-10-17'], untung_pct=[3.0], hari=[1.0]),
                     self.akhir, self.idx)
        self.assertAlmostEqual(float(P.pul.iloc[0]), 3.0 - LK.KOS, places=6)
        self.assertAlmostEqual(float(P.hari_pegang.iloc[0]), 1.0, places=6)

    def test_hari_pegang_terbuka_dikira_dari_sesi_terakhir(self):
        P = LK.nilai(pos(saham=['AAA']), self.akhir, self.idx)
        self.assertAlmostEqual(float(P.hari_pegang.iloc[0]), 3.0, places=6)

    def test_saham_tanpa_harga_dibuang_bukan_sifar(self):
        P = LK.nilai(pos(saham=['ZZZ']), self.akhir, self.idx)
        self.assertEqual(len(P), 0)


class TestLiftTinggalSatuKeluar(unittest.TestCase):
    def rangka(self, ids, pul):
        return pd.DataFrame(dict(id_kaedah=ids, pul=pul, tarikh_beli=['d1'] * len(ids),
                                 baldi=['3-5'] * len(ids)))

    def test_asas_mengecualikan_kaedah_sendiri(self):
        # M01 = +10 (satu baris), M02 = 0 (tiga baris). Asas M01 = purata M02 = 0 -> lift +10.
        P = self.rangka(['M01', 'M02', 'M02', 'M02'], [10.0, 0.0, 0.0, 0.0])
        lf = LK.lift_tsk(P, ['tarikh_beli', 'baldi'])
        self.assertAlmostEqual(float(lf[0]), 10.0, places=6)
        # Purata sel biasa ialah 2.5, jadi lift tanpa pengecualian hanya +7.5.
        self.assertNotAlmostEqual(float(lf[0]), 7.5, places=3)

    def test_kaedah_menguasai_sel_tidak_ditarik_ke_sifar(self):
        # M01 memegang 9 daripada 10 baris sel dan mengatasi satu baris lain sebanyak 5 mata.
        P = self.rangka(['M01'] * 9 + ['M02'], [5.0] * 9 + [0.0])
        lf = LK.lift_tsk(P, ['tarikh_beli', 'baldi'])
        self.assertAlmostEqual(float(lf[0]), 5.0, places=6)

    def test_sel_satu_kaedah_sahaja_jadi_nan(self):
        # Tiada asas untuk dibanding: baris itu mesti dibuang, bukan dikira lift sifar.
        P = self.rangka(['M01', 'M01'], [5.0, 7.0])
        lf = LK.lift_tsk(P, ['tarikh_beli', 'baldi'])
        self.assertTrue(np.isnan(lf).all())

    def test_sel_berbeza_tidak_bercampur(self):
        P = pd.DataFrame(dict(id_kaedah=['M01', 'M02', 'M01', 'M02'], pul=[10.0, 0.0, 1.0, 100.0],
                              tarikh_beli=['d1', 'd1', 'd2', 'd2'], baldi=['3-5'] * 4))
        lf = LK.lift_tsk(P, ['tarikh_beli', 'baldi'])
        self.assertAlmostEqual(float(lf[0]), 10.0, places=6)    # d1: asas = M02 d1 = 0
        self.assertAlmostEqual(float(lf[2]), -99.0, places=6)   # d2: asas = M02 d2 = 100


class TestUji(unittest.TestCase):
    def rangka(self, mid, pul, hari_beli):
        n = len(pul)
        return pd.DataFrame(dict(id_kaedah=[mid] * n + ['ASAS'] * n, pul=list(pul) + [0.0] * n,
                                 tarikh_beli=list(hari_beli) * 2, baldi=['3-5'] * 2 * n,
                                 hari_pegang=[5.0] * 2 * n, terbuka=[False] * 2 * n))

    def test_n_bawah_minimum_dilangkau(self):
        P = self.rangka('M01', [3.0] * (LK.MIN_N - 1), [f'd{i}' for i in range(LK.MIN_N - 1)])
        self.assertNotIn('M01', LK.uji(P, ['tarikh_beli', 'baldi']).index)

    def test_kluster_bawah_minimum_dilangkau(self):
        n = LK.MIN_N + 10
        hari = [f'd{i % (LK.MIN_KLUSTER - 1)}' for i in range(n)]
        P = self.rangka('M01', [3.0] * n, hari)
        self.assertNotIn('M01', LK.uji(P, ['tarikh_beli', 'baldi']).index)

    def test_lift_dan_sebulan_dikira(self):
        # Sedikit variasi diperlukan: SE berkelompok sifar bermakna t tidak tertakrif, dan uji()
        # melangkau kaedah itu (sengaja) — jadi sampel pemalar tidak boleh menguji lift.
        n = LK.MIN_N + 20
        pul = [2.0 + (0.1 if i % 2 else -0.1) for i in range(n)]
        P = self.rangka('M01', pul, [f'd{i}' for i in range(n)])
        R = LK.uji(P, ['tarikh_beli', 'baldi'])
        self.assertAlmostEqual(float(R.loc['M01', 'lift']), 2.0, places=6)
        # hari pegang 5 -> lift sebulan = 2.0 / 5 * 21
        self.assertAlmostEqual(float(R.loc['M01', 'sebulan']), 2.0 / 5 * 21, places=6)

    def test_ambang_bh_menaik_dan_lulus_konsisten(self):
        n = LK.MIN_N + 20
        P = pd.concat([self.rangka(f'M{i:02d}',
                                   [float(i) + (0.1 if j % 2 else -0.1) for j in range(n)],
                                   [f'd{j}' for j in range(n)])
                       for i in (1, 2, 3)], ignore_index=True)
        R = LK.uji(P, ['tarikh_beli', 'baldi'])
        self.assertTrue(R.bh.is_monotonic_increasing)
        self.assertTrue(((R.p <= R.bh) == R.lulus).all())


class TestHariPerlu(unittest.TestCase):
    def test_lift_lebih_besar_perlukan_lebih_sedikit_hari(self):
        a = LK.hari_perlu(3.3, 180, 1.0)
        b = LK.hari_perlu(3.3, 180, 2.0)
        self.assertGreater(a, b)
        self.assertAlmostEqual(a / b, 4.0, delta=0.6)   # skala ~ 1/lift^2

    def test_lebih_banyak_kaedah_perlukan_lebih_banyak_hari(self):
        self.assertGreater(LK.hari_perlu(3.3, 180, 2.0), LK.hari_perlu(3.3, 10, 2.0))


class TestStatus(unittest.TestCase):
    def test_label(self):
        self.assertEqual(LK.status(14, 56), 'BELUM CUKUP')
        self.assertEqual(LK.status(60, 56), 'BOLEH DIBACA')


if __name__ == '__main__':
    unittest.main()

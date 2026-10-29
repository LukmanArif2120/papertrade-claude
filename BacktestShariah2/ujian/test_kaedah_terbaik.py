"""Ujian unit bagi standard/kaedah_terbaik.py (t berkelompok, korelasi separa, BH-FDR)."""
import os
import sys
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import kaedah_terbaik as KT  # noqa: E402


def posisi(nilai, hari):
    return pd.DataFrame({'untung_akhir_pct': nilai, 'tarikh_beli': hari})


class TestTBerkelompok(unittest.TestCase):
    def test_purata_betul(self):
        g = posisi([1.0, 3.0, 5.0], ['d1', 'd2', 'd3'])
        m, t, nk = KT.t_berkelompok(g)
        self.assertAlmostEqual(m, 3.0, places=6)
        self.assertEqual(nk, 3)

    def test_kluster_terlalu_sedikit_nan(self):
        g = posisi([1.0] * 10, ['d1'] * 5 + ['d2'] * 5)
        m, t, nk = KT.t_berkelompok(g)
        self.assertEqual(nk, 2)
        self.assertTrue(np.isnan(t))

    def test_kelompok_mengurangkan_t(self):
        # 40 posisi tetapi hanya 4 hari beli: t berkelompok mesti jauh lebih kecil daripada
        # t naif yang melayan 40 posisi sebagai bebas.
        rng = np.random.default_rng(3)
        hari = np.repeat(['d1', 'd2', 'd3', 'd4'], 10)
        kesan = {'d1': 2.0, 'd2': 2.2, 'd3': 1.8, 'd4': 2.0}
        nilai = [kesan[h] + rng.normal(0, 0.05) for h in hari]
        g = posisi(nilai, list(hari))
        m, t, nk = KT.t_berkelompok(g)
        naif = m / (np.std(nilai, ddof=1) / np.sqrt(len(nilai)))
        self.assertEqual(nk, 4)
        self.assertLess(abs(t), abs(naif))

    def test_varians_sifar_nan_atau_inf_dilindungi(self):
        g = posisi([2.0] * 9, ['d1', 'd2', 'd3'] * 3)
        m, t, nk = KT.t_berkelompok(g)
        self.assertAlmostEqual(m, 2.0, places=6)
        self.assertTrue(np.isnan(t) or np.isinf(t))


class TestSpearmanSepara(unittest.TestCase):
    def test_pengantara_penuh_memberi_sifar(self):
        # y bergantung HANYA pada z, dan x berkorelasi dengan z: separa mesti hampir sifar.
        rng = np.random.default_rng(11)
        z = rng.normal(size=200)
        x = z + rng.normal(0, 0.1, 200)
        y = z * 2 + rng.normal(0, 0.1, 200)
        d = pd.DataFrame({'x': x, 'y': y, 'z': z})
        r, p, n = KT.spearman_separa(d, 'x', 'y', 'z')
        self.assertLess(abs(r), 0.25)
        self.assertEqual(n, 200)

    def test_hubungan_bebas_kekal(self):
        # y bergantung pada x, z hanya hingar: separa mesti kekal tinggi.
        rng = np.random.default_rng(12)
        x = rng.normal(size=200)
        d = pd.DataFrame({'x': x, 'y': x * 2 + rng.normal(0, 0.1, 200),
                          'z': rng.normal(size=200)})
        r, p, n = KT.spearman_separa(d, 'x', 'y', 'z')
        self.assertGreater(r, 0.8)

    def test_sampel_kecil_nan(self):
        d = pd.DataFrame({'x': [1.0, 2.0], 'y': [1.0, 2.0], 'z': [1.0, 2.0]})
        r, p, n = KT.spearman_separa(d, 'x', 'y', 'z')
        self.assertTrue(np.isnan(r))


class TestUjiKaedah(unittest.TestCase):
    def _B(self, ids):
        return pd.DataFrame({'nama': ids, 'hari': 10.0, 'bt_purata': 1.0,
                             'n_lulus': 0}, index=pd.Index(ids, name='id'))

    def test_bawah_min_n_dibuang(self):
        k = pd.concat([posisi([1.0] * 5, [f'd{i}' for i in range(5)]).assign(id_kaedah='MA')])
        R = KT.uji_kaedah(k, self._B(['MA']))
        self.assertEqual(len(R), 0)

    def test_ambang_bh_menaik(self):
        bhg = []
        for j, nm in enumerate(['MA', 'MB', 'MC']):
            rng = np.random.default_rng(j)
            bhg.append(posisi(list(rng.normal(-3 - j, 0.5, 30)),
                              [f'd{i % 10}' for i in range(30)]).assign(id_kaedah=nm))
        R = KT.uji_kaedah(pd.concat(bhg), self._B(['MA', 'MB', 'MC']))
        self.assertEqual(len(R), 3)
        self.assertTrue(R.ambang_bh.is_monotonic_increasing)
        self.assertTrue(R.p.is_monotonic_increasing)

    def test_negatif_kuat_lulus_fdr(self):
        rng = np.random.default_rng(5)
        k = posisi(list(rng.normal(-5.0, 0.3, 40)),
                   [f'd{i % 12}' for i in range(40)]).assign(id_kaedah='MA')
        R = KT.uji_kaedah(k, self._B(['MA']))
        self.assertTrue(bool(R.lulus_bh.iloc[0]))
        self.assertLess(R.real.iloc[0], 0)

    def test_hingar_tanpa_kesan_tidak_lulus(self):
        rng = np.random.default_rng(6)
        k = posisi(list(rng.normal(0.0, 3.0, 40)),
                   [f'd{i % 12}' for i in range(40)]).assign(id_kaedah='MA')
        R = KT.uji_kaedah(k, self._B(['MA']))
        self.assertFalse(bool(R.lulus_bh.iloc[0]))


if __name__ == '__main__':
    unittest.main()

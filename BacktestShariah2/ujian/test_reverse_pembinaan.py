"""Ujian unit bagi REVERSE/pembinaan.py (peraturan keluar, ekuiti, MDD/CAGR)."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from REVERSE import pembinaan as PB  # noqa: E402


class PanelPalsu:
    """Panel minimum: 2 ticker, harga ditetapkan, ATR tetap 1.0, cair."""

    def __init__(self, c, n_tick=2):
        c = np.asarray(c, 'float64')
        m = len(c)
        self.tarikh = pd.date_range('2020-01-01', periods=m, freq='B').to_numpy()
        self.tick = np.array([f'T{i}' for i in range(n_tick)])
        self.O = np.tile(c, (n_tick, 1)).astype('float32')
        self.H = self.O + 0.5
        self.L = np.tile(c, (n_tick, 1)).astype('float32') - 0.5
        self.C = np.tile(c, (n_tick, 1)).astype('float32')
        self.A = np.full((n_tick, m), 1.0, 'float32')
        self.N = np.full((n_tick, m), 1e9, 'float32')

    def layak(self, a):
        return np.arange(len(self.tick))


class TestKeluar(unittest.TestCase):
    def test_h63_ufuk_tetap(self):
        P = PanelPalsu(np.full(200, 100.0))
        k, masuk, px = PB.keluar(P, 0, 0, 'H63', {})
        self.assertEqual(k, 1 + PB.UFUK + 1)
        self.assertAlmostEqual(masuk, 100.0, places=4)

    def test_h63s_tanpa_sentuhan_sama_dengan_h63(self):
        P = PanelPalsu(np.full(200, 100.0))
        a = PB.keluar(P, 0, 0, 'H63', {})
        # Tanpa jurang, rendah = 99.5 > paras 98.0, jadi henti tidak tercetus.
        b = PB.keluar(P, 0, 0, 'H63S', {})
        self.assertEqual(a[0], b[0])

    def test_h63s_tercetus_pada_jurang(self):
        c = np.full(200, 100.0)
        c[20] = 90.0            # rendah 89.5 < paras 98.0
        P = PanelPalsu(c)
        k, _, _ = PB.keluar(P, 0, 0, 'H63S', {})
        self.assertEqual(k, 21)  # syarat pada bar 20, keluar pada buka 21

    def test_trail_tiada_had_ufuk(self):
        # Menaik berterusan: Chandelier tidak tercetus, jadi lebih lama daripada UFUK.
        P = PanelPalsu(100.0 + 0.5 * np.arange(300))
        k, _, _ = PB.keluar(P, 0, 0, 'TRAIL', {})
        self.assertGreater(k, 1 + PB.UFUK + 1)

    def test_trail_tercetus_selepas_puncak(self):
        c = np.concatenate([100.0 + np.arange(50), np.full(150, 100.0)])
        P = PanelPalsu(c)
        k, _, _ = PB.keluar(P, 0, 0, 'TRAIL', {})
        self.assertLess(k, 1 + PB.TRAIL_MAKS)

    def test_cache_diguna(self):
        P = PanelPalsu(np.full(200, 100.0))
        cache = {}
        PB.keluar(P, 0, 0, 'H63', cache)
        self.assertIn((0, 0, 'H63'), cache)
        self.assertEqual(len(cache), 1)
        PB.keluar(P, 0, 0, 'H63', cache)
        self.assertEqual(len(cache), 1)


class TestSimulasi(unittest.TestCase):
    def test_harga_tetap_ekuiti_jatuh_hanya_kos(self):
        P = PanelPalsu(np.full(200, 100.0))
        ek = PB.simulasi(P, [0], 2, 'H63', 1, {})
        akhir = ek[np.isfinite(ek)][-1]
        self.assertLess(akhir, 1.0)          # kos dua sisi
        self.assertGreater(akhir, 0.99)      # tetapi kecil

    def test_tidak_melebihi_slot(self):
        P = PanelPalsu(np.full(200, 100.0), n_tick=50)
        ek = PB.simulasi(P, [0], 3, 'H63', 1, {})
        self.assertTrue(np.all(np.isfinite(ek[1:]) | np.isnan(ek[1:])))
        self.assertLessEqual(ek[np.isfinite(ek)][-1], 1.01)

    def test_tiada_leverage(self):
        # Ekuiti tidak boleh melebihi 1.0 apabila harga tetap: tiada wang dicipta.
        P = PanelPalsu(np.full(300, 100.0), n_tick=10)
        ek = PB.simulasi(P, [0, 70, 140], 5, 'H63', 7, {})
        self.assertLessEqual(float(np.nanmax(ek)), 1.0 + 1e-9)

    def test_benih_berbeza_memberi_hasil_berbeza(self):
        # Setiap ticker hanyutan berbeza, jadi subset yang dipilih menentukan hasil. Dengan 3
        # slot daripada 12 nama, benih berbeza mesti menghasilkan sekurangnya dua hasil berbeza.
        P = PanelPalsu(np.full(300, 100.0), n_tick=12)
        for i in range(12):
            c = (100.0 + 0.05 * i * np.arange(300)).astype('float32')
            P.O[i] = P.C[i] = c
            P.H[i] = c + 0.5
            P.L[i] = c - 0.5
        akhir = set()
        for b in range(1, 9):
            ek = PB.simulasi(P, [0], 3, 'H63', b, {})
            akhir.add(round(float(ek[np.isfinite(ek)][-1]), 6))
        self.assertGreater(len(akhir), 1, 'benih sepatutnya memilih subset berbeza')


class TestUkuran(unittest.TestCase):
    def test_mdd_menurun_sahaja(self):
        self.assertAlmostEqual(PB.mdd(np.array([1.0, 0.5])), -50.0, places=4)

    def test_mdd_menaik_sifar(self):
        self.assertAlmostEqual(PB.mdd(np.array([1.0, 2.0, 3.0])), 0.0, places=6)

    def test_cagr_dua_kali_satu_tahun(self):
        h = pd.DatetimeIndex(['2020-01-01', '2021-01-01'])
        self.assertAlmostEqual(PB.cagr(np.array([1.0, 2.0]), h), 100.0, delta=0.5)

    def test_cagr_nan_bila_terlalu_pendek(self):
        self.assertTrue(np.isnan(PB.cagr(np.array([1.0]), pd.DatetimeIndex(['2020-01-01']))))


class TestGrid(unittest.TestCase):
    def test_grid_tetap_enam(self):
        # Spec §6 menetapkan tepat 6 konfigurasi; melebarkannya memerlukan pradaftar baharu.
        self.assertEqual(len(PB.GRID), 6)
        self.assertEqual({r for _, _, r in PB.GRID}, {'H63S', 'H63', 'TRAIL'})
        self.assertEqual({s for _, s, _ in PB.GRID}, {8, 40})


if __name__ == '__main__':
    unittest.main()

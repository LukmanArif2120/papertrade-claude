"""Ujian unit bagi REVERSE/kolam_ekor.py (ATR, bahagian ekor, sauh dan henti)."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from REVERSE import kolam_ekor as KE  # noqa: E402


def rangka(n=320, mula='2014-11-03', naik=0.0, rendah=None):
    """OHLCV sintetik: tutup menaik linear, julat harian tetap."""
    d = pd.bdate_range(mula, periods=n)
    c = 100.0 + naik * np.arange(n)
    lo = c - 1.0 if rendah is None else np.where(np.arange(n) == rendah, c - 50.0, c - 1.0)
    return pd.DataFrame({'ticker': 'T', 'date': d, 'high': c + 1.0, 'low': lo,
                         'close': c, 'volume': 1_000_000.0})


class TestAtr(unittest.TestCase):
    def test_nan_sebelum_pemanasan(self):
        g = rangka(40)
        a = KE.atr(g.high.to_numpy(), g.low.to_numpy(), g.close.to_numpy())
        self.assertTrue(np.all(np.isnan(a[:KE.ATR_N])))
        self.assertTrue(np.isfinite(a[KE.ATR_N]))

    def test_julat_tetap_memberi_atr_tetap(self):
        g = rangka(60)
        a = KE.atr(g.high.to_numpy(), g.low.to_numpy(), g.close.to_numpy())
        self.assertAlmostEqual(a[50], 2.0, places=6)

    def test_terlalu_pendek_semua_nan(self):
        g = rangka(10)
        a = KE.atr(g.high.to_numpy(), g.low.to_numpy(), g.close.to_numpy())
        self.assertTrue(np.all(np.isnan(a)))

    def test_tiada_pandang_hadapan(self):
        # Mengubah bar TERAKHIR tidak boleh menukar ATR pada bar sebelumnya.
        g = rangka(60)
        a1 = KE.atr(g.high.to_numpy(), g.low.to_numpy(), g.close.to_numpy())
        h = g.high.to_numpy().copy()
        h[-1] = 500.0
        a2 = KE.atr(h, g.low.to_numpy(), g.close.to_numpy())
        np.testing.assert_allclose(a1[:-1], a2[:-1])


class TestEkor(unittest.TestCase):
    def test_semua_sama_bahagian_berkadar(self):
        self.assertAlmostEqual(KE._ekor(np.ones(100), 10), 10.0, places=6)

    def test_satu_pemenang_menguasai(self):
        x = np.concatenate([[100.0], np.zeros(99)])
        self.assertAlmostEqual(KE._ekor(x, 1), 100.0, places=6)

    def test_jumlah_negatif_nan(self):
        self.assertTrue(np.isnan(KE._ekor(-np.ones(50), 5)))

    def test_sekurang_kurangnya_satu_nama(self):
        # k% yang membundar ke 0 masih mesti mengambil satu nama, bukan sifar.
        self.assertFalse(np.isnan(KE._ekor(np.arange(1.0, 11.0), 1)))


class TestSauh(unittest.TestCase):
    def test_sauh_bulanan_dalam_tahun_sahaja(self):
        g = rangka(520, mula='2014-01-02')
        g.name = 'T'
        b, t = KE.satu_ticker(g, 2015, 'T')
        self.assertTrue(b)
        self.assertTrue(all(r[0] == 2015 for r in b))
        self.assertTrue(all(str(r[1]).startswith('2015') for r in b))

    def test_henti_sama_bila_tiada_sentuhan(self):
        g = rangka(520, mula='2014-01-02', naik=0.05)
        b, t = KE.satu_ticker(g, 2015, 'T')
        for r in b:
            self.assertAlmostEqual(r[5], r[6], places=6)

    def test_henti_mengurangkan_bila_disentuh(self):
        g = rangka(520, mula='2014-01-02', naik=0.05, rendah=300)
        b, _ = KE.satu_ticker(g, 2015, 'T')
        kena = [r for r in b if r[6] < r[5] - 1e-9]
        self.assertTrue(kena, 'jurang 50 mata sepatutnya mencetuskan henti pada sekurangnya satu sauh')

    def test_bar_terlalu_sedikit_dibuang(self):
        g = rangka(30, mula='2015-11-02')
        b, t = KE.satu_ticker(g, 2015, 'T')
        self.assertEqual((b, t), ([], []))

    def test_sauh_tahunan_satu_sahaja(self):
        g = rangka(800, mula='2014-01-02')
        _, t = KE.satu_ticker(g, 2015, 'T')
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0][1], 'T')


if __name__ == '__main__':
    unittest.main()

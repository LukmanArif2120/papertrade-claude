# Ujian standard/gred.py
import os, sys, unittest
from datetime import date
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred as G  # noqa: E402


class UjiGred(unittest.TestCase):
    def test_rs_pangkat(self):
        ix = pd.bdate_range('2025-01-01', periods=260)
        c = pd.DataFrame({'KUAT': np.linspace(10, 30, 260), 'SEDERHANA': np.linspace(10, 12, 260),
                          'LEMAH': np.linspace(30, 10, 260)}, index=ix)
        rs = G.rs_rating(c)
        self.assertGreater(rs['KUAT'], rs['SEDERHANA'])
        self.assertGreater(rs['SEDERHANA'], rs['LEMAH'])
        self.assertTrue(((rs >= 1) & (rs <= 99)).all())

    def test_rs_data_pendek(self):
        c = pd.DataFrame({'X': range(100)}, index=pd.bdate_range('2025-01-01', periods=100))
        self.assertTrue(G.rs_rating(c).empty)

    def test_sempadan_gred(self):
        self.assertEqual([G.gred_rs(x) for x in [99, 90, 89, 80, 79, 60, 59, 40, 39, None]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', '–'])
        self.assertEqual([G.gred_kumpulan(x) for x in [80, 79.9, 60, 40, 20, 19, None]],
                         ['A', 'B', 'B', 'C', 'D', 'E', '–'])
        self.assertEqual([G.gred_qr(x) for x in [None, 22, 21, 16, 15, 11, 10, 6, 5, 0]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'])

    def test_hari_dagangan(self):
        self.assertEqual(G.hari_dagangan(date(2026, 10, 9), date(2026, 10, 13)), 2)  # Jumaat -> Selasa
        self.assertEqual(G.hari_dagangan(date(2026, 10, 13), date(2026, 10, 13)), 0)

    def test_tajuk_berita(self):
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Upgrades KB Home to Buy, Raises Target Price to $60'), 1)
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Maintains KB Home With Hold Rating, Cuts Target Price to $56'), -1)
        self.assertEqual(G.nilai_tajuk('Morgan Stanley Initiates KB Home With Sell Rating'), -1)
        self.assertEqual(G.nilai_tajuk('DHI, LEN, KBH: Trending With Analysts'), 0)

    def test_mata_pemangkin(self):
        m, ring = G.mata_pemangkin({'berita': [{'tajuk': 'X upgrades Y', 'hari_lalu': 1},
                                               {'tajuk': 'Y beats estimates', 'hari_lalu': 2},
                                               {'tajuk': 'Y news', 'hari_lalu': 3}],
                                    'earnings_lalu_hari': 5, 'earnings_gerak_pct': 6.0,
                                    'volum_nisbah': 2.5, 'naik_5h': 4.0, 'institusi': 'kumpul'})
        self.assertEqual(m, 2 + 1 + 2 + 1 + 1)
        self.assertEqual(G.gred_pemangkin(m), 'A')
        self.assertEqual(G.mata_pemangkin({})[0], 0)
        self.assertEqual(G.gred_pemangkin(-1), 'E')
        m, _ = G.mata_pemangkin({'berita': [{'tajuk': 'old upgrade', 'hari_lalu': 20}]})
        self.assertEqual(m, 0)

    def test_keseluruhan(self):
        self.assertEqual(G.gred_keseluruhan(['A', 'A', '–', 'B']), 'A')
        self.assertEqual(G.gred_keseluruhan(['–', '–']), '–')
        self.assertEqual(G.gred_keseluruhan(['C', 'C', 'D']), 'C')


if __name__ == '__main__':
    unittest.main()

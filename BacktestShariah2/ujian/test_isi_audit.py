# Ujian audit 23 Okt 2026: gred.rs_pendek (RS anggaran saham baru disenarai) dan henti_isi.paras_henti (henti harga / ikut tutup).
import os, sys, types, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import gred as G  # noqa: E402
import henti_isi as HI  # noqa: E402


class RsPendek(unittest.TestCase):
    def test_pangkat_dan_had_bar(self):
        ix = pd.bdate_range('2025-01-02', periods=300)
        c = pd.DataFrame({'PENUH': np.linspace(10, 20, 300)}, index=ix)
        c['BARU'] = np.r_[np.full(150, np.nan), np.linspace(10, 30, 150)]     # 150 bar, naik kuat
        c['SINGKAT'] = np.r_[np.full(260, np.nan), np.linspace(10, 11, 40)]   # < 64 bar: tiada RS
        ruj = pd.Series([-0.1, 0.0, 0.05, 0.1])
        r = G.rs_pendek(c, ruj)
        self.assertEqual(set(r.index), {'BARU'})                            # PENUH (>= 253 bar) dan SINGKAT tidak
        self.assertEqual(r['BARU'], 99)                                      # di atas semua skor rujukan

    def test_harga_bawah_minimum(self):
        ix = pd.bdate_range('2025-01-02', periods=100)
        c = pd.DataFrame({'MURAH': np.linspace(1, 4, 100)}, index=ix)
        self.assertTrue(G.rs_pendek(c, pd.Series([0.0])).empty)


class ParasHenti(unittest.TestCase):
    def test_harga_dahulu_kemudian_tutup(self):
        g = pd.DataFrame({'stop': [np.nan, 9.5], '_lo': [8.0, 8.5]})
        m = types.SimpleNamespace(HENTI_TUTUP='_lo')
        self.assertEqual(HI.paras_henti(m, g, 1), (9.5, 'harga'))
        self.assertEqual(HI.paras_henti(m, g, 0), (8.0, 'tutup'))
        self.assertEqual(HI.paras_henti(types.SimpleNamespace(), g, 0), (None, None))


if __name__ == '__main__':
    unittest.main()

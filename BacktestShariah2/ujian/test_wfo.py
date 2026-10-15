# Ujian kod/wfo.py (W01). Data sebenar data_mentah dipakai (subset kecil) supaya enjin v1.2 diuji tanpa olok-olok.
import os, sys, unittest, warnings
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import wfo, enjin

TK = ['ADSK', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'ANET', 'CRWD', 'LLY', 'COST', 'ORCL', 'AVGO', 'KLAC']


class UjiWFO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        fr, cls.idx, _ = wfo.muat_data()
        cls.fr = {t: fr[t] for t in TK if t in fr}

    def test_buang_8(self):
        fr, _, sub = wfo.muat_data()
        self.assertFalse(set(wfo.BUANG8) & set(fr)); self.assertEqual(len(fr), 423); self.assertEqual(set(sub), set(fr))

    def test_had_henti(self):
        g = self.fr['ADSK']
        for s in wfo.STOPS:
            st = wfo.lajur_stop(g, s, pd.Series(np.nan, g.index))
            self.assertTrue((st >= 0.85 * g.close - 1e-9).all(), s)

    def test_gabungan_tidak_sah(self):
        self.assertFalse(wfo.sah('PCT8', 'TIADA', 0)); self.assertTrue(wfo.sah('PCT8', 'TIADA', 21))

    def test_suku(self):
        q = wfo.suku_ujian(pd.Timestamp('2026-10-02'))
        self.assertEqual(q[0][0], pd.Timestamp('2023-01-01')); self.assertEqual(q[-1][1], pd.Timestamp('2026-10-02'))
        for (a, z), (a2, _) in zip(q, q[1:]): self.assertEqual(z + pd.Timedelta(days=1), a2)

    def test_potong_setara_data_dipotong(self):
        """Dagangan data penuh yang dipotong = dagangan enjin atas data yang berakhir pada tarikh potong."""
        akhir = pd.Timestamp('2022-12-30'); mula = pd.Timestamp('2020-01-01')
        k = wfo.Kaedah('M37', self.fr, self.idx)
        frp = {t: g[g.index <= akhir] for t, g in self.fr.items()}
        kp = wfo.Kaedah('M37', frp, {a: b[b.index <= akhir] for a, b in self.idx.items()})
        for cfg in [('ATR3', 'SMA50', 0), ('PCT8', 'CHAN3', 42), ('ASAL', 'ASAL', 0)]:
            A = wfo.potong(k.dagangan(*cfg), mula, akhir, self.fr).sort_values(['ticker', 'ent']).reset_index(drop=True)
            B = kp.dagangan(*cfg); B = B[B.ent >= mula].sort_values(['ticker', 'ent']).reset_index(drop=True)
            self.assertEqual(len(A), len(B), cfg)
            self.assertTrue(np.allclose(A.ret.values, B.ret.values), cfg)
            self.assertTrue((A.ex.values == B.ex.values).all(), cfg)

    def test_tiada_pandang_ke_hadapan_M37(self):
        self.assertIsNone(wfo.semak_kaedah('M37', self.fr, self.idx))

    def test_dikecualikan(self):
        self.assertIsNotNone(wfo.semak_kaedah('M40', self.fr, self.idx))


if __name__ == '__main__':
    unittest.main()

# Ujian standard/trend_status.py (status trend D10+H2, dashboard harian/trend) dan standard/lorong2_siri.py (posisi/lorong2).
import os, sys, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import trend_status as T  # noqa: E402
import lorong2_siri as L2  # noqa: E402
import keluar_lorong as KL  # noqa: E402


def frame(c, o=None, h=None, l=None, mula='2025-01-02'):
    c = np.asarray(c, float); o = c.copy() if o is None else np.asarray(o, float)
    h = np.maximum(o, c) * 1.005 if h is None else np.asarray(h, float)
    l = np.minimum(o, c) * 0.995 if l is None else np.asarray(l, float)
    d = [int(x.strftime('%Y%m%d')) for x in pd.bdate_range(mula, periods=len(c))]
    return pd.DataFrame(dict(date=d, open=o, high=h, low=l, close=c))


class Mesin(unittest.TestCase):
    def test_pengesahan_dua_tutup(self):
        m = np.array([np.nan, 0, 0, 1, 0, 1, 1, 1, 0, -1, -1], float)
        st, ev, i0 = T.mesin(m)
        self.assertEqual(i0, 2)                       # status pertama: dua mentah sama berturut
        self.assertTrue(np.isnan(st[1]))
        self.assertEqual(list(st[2:]), [0, 0, 0, 0, 1, 1, 1, 1, -1])   # 1 sehari (bar 3) ditapis; bertukar pada tutup kedua
        self.assertEqual(ev, [(5, 6, 0, 1), (9, 10, 1, -1)])

    def test_mentah_kesamaan_neutral(self):
        c = np.array([10., 10.]); s = np.array([9., 10.])
        m = T.mentah(c, s, np.array([8., 9.]), np.array([7., 8.]))
        self.assertEqual(list(m), [1.0, 0.0])         # C = SMA50 -> Neutral


class Kira(unittest.TestCase):
    def test_bullish_umur_dan_titik(self):
        c = np.r_[np.full(230, 100.0), np.linspace(100, 130, 40)]
        g = frame(c)
        r = T.kira(g)
        self.assertEqual(r['status'], 1)
        st, ev, _ = T.mesin(T.mentah(c, T.sma(c, 50), T.sma(c, 150), T.sma(c, 200)))
        i_sah = ev[-1][1]
        self.assertEqual(r['umur'], len(c) - i_sah)   # tarikh sah = 1
        self.assertEqual(r['sah'], int(g.date[i_sah]))
        self.assertEqual(r['sub'], 'baharu' if r['umur'] <= 20 else ('lama' if r['umur'] > 60 else ''))
        lo = g.low.to_numpy(); a = max(0, i_sah - 62)
        self.assertAlmostEqual(r['titik_harga'], lo[a:i_sah + 1].min())
        self.assertIsNone(r['tembus'])

    def test_sejarah_pendek(self):
        r = T.kira(frame(np.linspace(10, 20, 150)))
        self.assertIsNone(r['status'])
        self.assertIn('atr_pct', r)

    def test_titik_seri_bar_akhir(self):
        lo = np.array([5, 3, 4, 3, 6.]); hi = lo + 1
        self.assertEqual(T.titik_mula(lo, hi, 4, 1), (3, 3.0))


class Dokumen(unittest.TestCase):
    def test_kuintil_dan_baris(self):
        rng = np.random.default_rng(1)
        H = {f'S{i}': frame(100 * np.exp(np.cumsum(rng.normal(0.0005, 0.01 + i / 5000, 260)))) for i in range(60)}
        doc = T.dokumen(H, {'S0', 'S59', 'XX'})
        self.assertEqual(doc['lajur'], T.LAJUR)
        self.assertEqual(len(doc['atr_ambang']), 4)
        R = {r[0]: r for r in doc['rows']}
        self.assertIsNone(R['XX'][T.K['s']])
        self.assertLessEqual(R['S0'][T.K['atr_q']], R['S59'][T.K['atr_q']])
        self.assertIsNone(doc['rejim'])

    def test_bawa_semalam(self):
        L = T.LAJUR; K = T.K
        lama = dict(lajur=L, rows=[[None] * len(L)]); r0 = lama['rows'][0]
        r0[:] = [None] * len(L); r0[K['saham']] = 'A'; r0[K['s']] = 1; r0[K['tepat']] = 1; r0[K['sah']] = 20240102
        r0[K['umur']] = 400; r0[K['c_sah']] = 50.0; r0[K['titik_harga']] = 40.0; r0[K['tarikh_data']] = 20261021; r0[K['dari']] = 0
        baru = dict(rows=[[None] * len(L)]); b = baru['rows'][0]
        b[K['saham']] = 'A'; b[K['s']] = 1; b[K['tepat']] = 0; b[K['umur']] = 319; b[K['c']] = 60.0; b[K['tarikh_data']] = 20261022
        T.bawa_semalam(baru, lama)
        self.assertEqual((b[K['sah']], b[K['umur']], b[K['tepat']], b[K['sub']]), (20240102, 401, 1, 'lama'))
        self.assertAlmostEqual(b[K['pct_sejak']], 20.0)
        self.assertAlmostEqual(b[K['pct_titik']], 50.0)


class Lorong2(unittest.TestCase):
    def test_sama_dengan_keluar_lorong(self):
        rng = np.random.default_rng(7)
        for _ in range(20):
            c = 50 * np.exp(np.cumsum(rng.normal(0, 0.02, 120))); o = c * (1 + rng.normal(0, 0.005, 120))
            g = frame(c, o); k = 30
            x = L2.siri(g, int(g.date[k]))
            ref = KL.lorong_henti(g.open.to_numpy(), g.high.to_numpy(), g.low.to_numpy(), c, k)
            st = [b[4] for b in x]
            if ref['jenis'] == 'keluar':
                j = st.index('jual'); self.assertAlmostEqual(x[j][5], round(ref['harga'], 2))
                self.assertEqual(x[j][0], int(g.date[ref['j']]) % 10000)
            elif ref['jenis'] == 'terbuka':
                self.assertNotIn('bawah', st); self.assertAlmostEqual(x[-1][2], round(ref['paras'], 2))
            self.assertEqual(st[L2.SEBELUM], 'beli')


if __name__ == '__main__':
    unittest.main()

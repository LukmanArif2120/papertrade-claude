# Ujian enjin_at: (1) semua perubahan dimatikan = enjin v1.2 bait demi bait (data 431, beberapa kaedah asal);
# (2) setiap perubahan SPEC §3 diuji berasingan atas data sintetik.
import os, sys, unittest, warnings, importlib
import numpy as np, pandas as pd

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'teras'))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'kod'))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'kod', 'kaedah'))
import enjin, enjin_at as E

TK = ['ADSK', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'ANET', 'COST', 'AVGO', 'SHOP', 'TRI', 'PODD', 'SEDG', 'GNRC', 'DOCU', 'DXCM', 'IOVA']
_DATA = {}


def data_431():
    """(fr, idx) data_mentah 431 — guna teras/data.muat_431 jika ada, jika tidak muat CSV terus."""
    if not _DATA:
        try:
            sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'teras'))
            import data as D
            fr, idx = D.muat_431()
        except Exception:
            import tambahan
            enjin.cari = lambda n: os.path.join(AKAR, 'data_mentah', n); tambahan.cari = enjin.cari
            fr, idx, _ = tambahan.muat()
        _DATA['fr'], _DATA['idx'] = fr, idx
    return _DATA['fr'], _DATA['idx']


def salin(fr):
    return {t: g[['open', 'high', 'low', 'close', 'volume']].copy() for t, g in fr.items()}


def sama_T(A, B):
    if len(A) == 0 and len(B) == 0: return True, ''
    if len(A) != len(B): return False, f'n {len(A)} lawan {len(B)}'
    for k in ('ticker', 'why'):
        if not (np.asarray(A[k], object) == np.asarray(B[k], object)).all(): return False, k
    for k in ('sig', 'ent', 'ex'):
        if not (pd.to_datetime(A[k]).values == pd.to_datetime(B[k]).values).all(): return False, k
    if not (A.days.values == B.days.values).all(): return False, 'days'
    for k in ('ret', 'rank', 'mfe'):
        if not np.array_equal(A[k].values.astype(float), B[k].values.astype(float), equal_nan=True): return False, k
    return True, ''


MATI = dict(gap=False, kos=False, had60=False)


class UjiSetara(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        fr, cls.idx = data_431()
        cls.fr = {t: fr[t] for t in TK if t in fr}

    def _banding(self, mid):
        m = importlib.import_module(mid)
        f = salin(self.fr); m.sedia(f, self.idx); f = {t: enjin.siap(g) for t, g in f.items()}
        A = enjin.trades(f, m.TMAX, m.WARM)
        B = E.trades(f, m.TMAX, m.WARM, **MATI)
        ok, why = sama_T(A, B); self.assertTrue(ok, f'{mid}: {why}')
        self.assertGreater(len(A), 5)
        a = enjin.portfolio(A, f); b = E.portfolio(B, f)
        self.assertTrue((a.index == b.index).all() and np.array_equal(a.values, b.values), f'{mid} portfolio')

    def test_M54(self): self._banding('M54')
    def test_M06_silang(self): self._banding('M06')
    def test_M37(self): self._banding('M37')
    def test_M116_tmax(self): self._banding('M116')


def sintetik(n=300, harga=50.0, vol=2e6, mula='2020-01-01'):
    ix = pd.bdate_range(mula, periods=n)
    c = np.full(n, harga)
    g = pd.DataFrame(dict(open=c.copy(), high=c * 1.01, low=c * 0.99, close=c.copy(), volume=np.full(n, vol)), index=ix)
    g['sig'] = False; g['stop'] = np.nan; g['tgt'] = np.nan; g['exitc'] = False; g['rank'] = 0.0
    return g


class UjiPerubahan(unittest.TestCase):
    def test_gap_hari_pertama(self):
        g = sintetik(); i = 250
        g.iloc[i, g.columns.get_loc('sig')] = True; g.iloc[i, g.columns.get_loc('stop')] = 49.0
        g.iloc[i + 1, :4] = [48.0, 48.5, 47.0, 48.2]          # buka hari masuk 48 <= henti 49
        T = E.trades({'X': g.copy()}, None, 200, gap=True, kos=False, had60=False)
        self.assertEqual(T.why.iloc[0], 'henti'); self.assertEqual(T.days.iloc[0], 1)
        self.assertAlmostEqual(T.ret.iloc[0], (1 - E.COST) / (1 + E.COST) - 1)
        T0 = E.trades({'X': g.copy()}, None, 200, **MATI)        # v1.2: keluar pada henti 49 (low 47 <= 49)
        self.assertAlmostEqual(T0.ret.iloc[0], 49 / 48 * (1 - E.COST) / (1 + E.COST) - 1)

    def test_kos_ikut_nilai_dagangan(self):
        for vol, slip in [(2e6, 0.0005), (5e5, 0.0010), (1e5, 0.0025)]:   # tutup 50 → 1e8, 2.5e7, 5e6
            g = sintetik(vol=vol); g.iloc[250, g.columns.get_loc('sig')] = True
            g.iloc[252, g.columns.get_loc('exitc')] = True
            T = E.trades({'X': g}, None, 200, gap=False, kos=True, had60=False)
            k = 0.001 + slip
            self.assertAlmostEqual(T.kos.iloc[0], k)
            self.assertAlmostEqual(T.ret.iloc[0], (1 - k) / (1 + k) - 1)
        self.assertAlmostEqual(E.kos_sisi([np.nan])[0], 0.0035)

    def test_had60(self):
        g = sintetik(); g.iloc[210, g.columns.get_loc('sig')] = True
        T = E.trades({'X': g.copy()}, None, 200, gap=False, kos=False, had60=True)
        self.assertEqual((T.days.iloc[0], T.why.iloc[0]), (60, 'masa'))
        T = E.trades({'X': g.copy()}, 10, 200, gap=False, kos=False, had60=True)
        self.assertEqual(T.days.iloc[0], 10)
        T = E.trades({'X': g.copy()}, 126, 200, gap=False, kos=False, had60=True)
        self.assertEqual(T.days.iloc[0], 60)
        T = E.trades({'X': g.copy()}, None, 200, **MATI)
        self.assertEqual(T.why.iloc[0], 'hujung')

    def test_topeng(self):
        g = sintetik(); g.iloc[[210, 230], g.columns.get_loc('sig')] = True
        g.iloc[[212, 232], g.columns.get_loc('exitc')] = True
        tp = {'X': pd.Series(g.index >= g.index[220], g.index)}
        T = E.trades({'X': g.copy()}, None, 200, topeng=tp, **MATI)
        self.assertEqual(list(T.sig), [g.index[230]])
        self.assertEqual(len(E.trades({'X': g.copy()}, None, 200, topeng={}, **MATI)), 0)
        T = E.trades({'X': g.copy()}, None, 200, topeng=lambda gg, t: np.ones(len(gg), bool), **MATI)
        self.assertEqual(len(T), 2)

    def test_tetingkap(self):
        g = sintetik(); c = g.columns.get_loc
        g.iloc[[205, 240, 280], c('sig')] = True        # 205 sebelum mula (pegang hingga 245 jika tiada had)
        mula, akhir = g.index[230], g.index[285]
        T = E.trades({'X': g.copy()}, None, 200, mula=mula, akhir=akhir, **MATI)
        self.assertEqual(list(T.sig), [g.index[240]])    # 205 tidak masuk; tidak menyekat 240
        self.assertEqual((T.ex.iloc[0], T.why.iloc[0]), (akhir, 'hujung'))
        self.assertTrue((T.ent >= mula).all() and (T.ex <= akhir).all())
        g.iloc[285, c('close')] = 55.0
        T = E.trades({'X': g.copy()}, None, 200, mula=mula, akhir=akhir, **MATI)
        self.assertAlmostEqual(T.ret.iloc[0], 55 / 50 * (1 - E.COST) / (1 + E.COST) - 1)
        cv = E.portfolio(T, {'X': g}, mula=mula, akhir=akhir)
        self.assertEqual((cv.index[0], cv.index[-1]), (mula, akhir))
        self.assertAlmostEqual(cv.iloc[-1], 1 + 0.125 * T.ret.iloc[0])
        r = E.pulangan_harian(cv); self.assertAlmostEqual(float(np.prod(1 + r.values)), cv.iloc[-1])

    def test_portfolio_8_slot_ikut_rank(self):
        fr = {}
        for q in range(10):
            g = sintetik(); g.iloc[250, g.columns.get_loc('sig')] = True; g.iloc[250, g.columns.get_loc('rank')] = q
            g.iloc[251:, g.columns.get_loc('close')] = 50 * (1 + 0.01 * q)
            g.iloc[260, g.columns.get_loc('exitc')] = True
            fr[f'T{q}'] = g
        T = E.trades(fr, None, 200, **MATI)
        cv = E.portfolio(T, fr, mula=fr['T0'].index[200])
        terpilih = T.sort_values('rank', ascending=False).head(8)
        self.assertAlmostEqual(cv.iloc[-1], 1 + 0.125 * terpilih.ret.sum())


if __name__ == '__main__':
    unittest.main()

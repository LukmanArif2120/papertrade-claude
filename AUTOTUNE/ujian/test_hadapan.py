# Ujian imbasan pandang ke hadapan (AUTOTUNE/kaedah/semak_hadapan.py) atas dua kes kecil sintetik.
import os, sys, types, unittest

import numpy as np, pandas as pd

AKAR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'kaedah'))
import semak_hadapan as S   # noqa: E402


def data(n=80):
    ix = pd.bdate_range('2021-05-03', periods=n)
    r = np.random.default_rng(1)
    fr = {}
    for t in ('AAA', 'BBB'):
        c = 50 * np.exp(np.cumsum(r.normal(0, 0.02, n)))
        o = c * (1 + r.normal(0, 0.005, n))
        fr[t] = pd.DataFrame(dict(open=o, high=np.maximum(o, c) * 1.01, low=np.minimum(o, c) * 0.99, close=c,
                                  volume=1e6 + r.integers(0, 1000, n), turnover=c * 1e6), index=ix)
    idx = {'SPY': fr['AAA'].copy()}
    return fr, idx


def _bersih(fr, idx, P=None):
    """Isyarat tutup > SMA5 dan buka esok > henti (dibenarkan: buka c+1 sahaja); exitc tutup < SMA5."""
    for g in fr.values():
        s5 = g.close.rolling(5).mean()
        g['stop'] = g.close * 0.95
        g['sig'] = g.open.shift(-1) > g['stop']          # langkau jika buka esok <= henti
        g['tgt'] = np.nan
        g['exitc'] = g.close < s5
        g['rank'] = g.close.pct_change(3)


def _hadapan(fr, idx, P=None):
    """Seperti M81 asal: exitc[j-1] ditanda daripada rendah[j] (pandang ke hadapan)."""
    _bersih(fr, idx)
    for g in fr.values():
        g['exitc'] = (g.low.shift(-1) < g.close * 0.99).fillna(False)
        g['sig'] = (g.close.shift(-1) - g.open.shift(-1)).abs() > 0   # tutup esok: dilarang


def _pengawal(fr, idx, P=None):
    """exitc dengan pengawal j + 1 < n (hanya kewujudan bar esok, bukan nilainya): dibenarkan."""
    _bersih(fr, idx)
    for g in fr.values():
        g['exitc'] = np.arange(len(g)) < len(g) - 1


class UjiHadapan(unittest.TestCase):
    def setUp(self):
        self.fr, self.idx = data()
        self.potong = ('2021-06-30', '2021-07-30')

    def test_bersih(self):
        m = types.SimpleNamespace(sedia=_bersih)
        r = S.imbas(m, self.fr, self.idx, self.potong)
        self.assertEqual(r['langgar'], {})
        # isyarat hari c yang bergantung buka c+1 direkod sebagai dibenarkan
        self.assertEqual(set(r['dibenar']), {'sig'})
        self.assertEqual(r['dibenar']['sig']['sifat'], {'hari c bergantung buka c+1 sahaja'})
        self.assertEqual(r['dibenar']['sig']['hari'], set(self.potong))

    def test_pengawal_dibenarkan(self):
        r = S.imbas(types.SimpleNamespace(sedia=_pengawal), self.fr, self.idx, self.potong)
        self.assertEqual(r['langgar'], {})
        self.assertEqual(r['dibenar']['exitc']['sifat'], {'exitc hari c bergantung kewujudan bar c+1 sahaja (pengawal j+1<n)'})

    def test_hadapan_dikesan(self):
        m = types.SimpleNamespace(sedia=_hadapan)
        r = S.imbas(m, self.fr, self.idx, self.potong)
        self.assertEqual(set(r['langgar']), {'exitc', 'sig'})
        self.assertEqual(r['langgar']['sig']['sifat'], {'hari c bergantung high/low/close/volume bar c+1'})
        self.assertEqual(r['langgar']['exitc']['sifat'], {'exitc hari c bergantung nilai bar c+1'})
        self.assertLessEqual(r['langgar']['exitc']['hari'], set(self.potong))


if __name__ == '__main__':
    unittest.main()

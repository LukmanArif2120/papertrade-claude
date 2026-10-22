# Ujian standard/harga_yf.py (tanpa rangkaian)
import os, sys, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import harga_yf as H  # noqa: E402


def bingkai_yf(tickers, hari=3):
    """Tiru output yf.download(group_by='column'): lajur MultiIndex (Price, Ticker)."""
    ix = pd.DatetimeIndex(pd.bdate_range('2026-10-07', periods=hari), name='Date')
    data = {}
    for i, t in enumerate(tickers):
        b = 10.0 * (i + 1)
        data[('Open', t)] = [b] * hari
        data[('High', t)] = [b * 1.02] * hari
        data[('Low', t)] = [b * 0.98] * hari
        data[('Close', t)] = [b * 1.01] * hari
        data[('Adj Close', t)] = [b] * hari
        data[('Volume', t)] = [1000.0] * hari
    df = pd.DataFrame(data, index=ix)
    df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Price', 'Ticker'])
    return df


class UjiHargaYf(unittest.TestCase):
    def test_ticker_kelas(self):
        self.assertEqual(H.ke_yahoo('BRK.B'), 'BRK-B')
        self.assertEqual(H.dari_yahoo('BRK-B'), 'BRK.B')

    def test_panjang(self):
        d = H.panjang(bingkai_yf(['AAPL', 'BRK-B']))
        self.assertEqual(list(d.columns), H.LAJ)
        self.assertEqual(sorted(d.ticker.unique()), ['AAPL', 'BRK.B'])
        self.assertEqual(int(d.date.min()), 20261007)
        self.assertEqual(len(d), 6)

    def test_bersih_buang_bar_rosak(self):
        df = bingkai_yf(['X'])
        df.loc[df.index[0], ('Close', 'X')] = np.nan
        df.loc[df.index[1], ('High', 'X')] = 5.0   # high < open
        d = H.panjang(df)
        self.assertEqual(len(d), 1)

    def test_gabung_tambah_dan_laras(self):
        lama = pd.DataFrame({'ticker': 'AAA', 'date': [20261005, 20261006, 20261007],
                             'open': 10.0, 'high': 11.0, 'low': 9.0, 'close': 10.0, 'volume': 100})
        # bar baharu: 7 Okt bertindih dengan close 20 (split 1:2 terbalik) + 8 Okt baharu
        baru = pd.DataFrame({'ticker': 'AAA', 'date': [20261007, 20261008],
                             'open': 20.0, 'high': 22.0, 'low': 18.0, 'close': 20.0, 'volume': 50})
        idx = pd.DataFrame({'ticker': 'SPY', 'date': [20261007], 'open': 1.0, 'high': 1.0, 'low': 1.0,
                            'close': 1.0, 'volume': 1})
        stor = {'harga_A.csv': lama, 'harga_B.csv': pd.DataFrame(columns=H.LAJ), 'harga_idx.csv': idx}
        lain = pd.DataFrame({'ticker': 'BBB', 'date': [20261008], 'open': 5.0, 'high': 5.0, 'low': 5.0,
                             'close': 5.0, 'volume': 1})
        stor, nota = H.gabung(stor, pd.concat([baru, lain]))
        a = stor['harga_A.csv'].set_index('date')
        self.assertEqual(list(a.index), [20261005, 20261006, 20261007, 20261008])
        self.assertAlmostEqual(a.loc[20261005, 'close'], 20.0)   # dilaras ×2
        self.assertEqual(list(stor['harga_B.csv'].ticker), ['BBB'])
        self.assertEqual(len(stor['harga_idx.csv']), 1)

    def test_banding(self):
        a = pd.DataFrame({'date': [1, 2], 'open': [10, 10], 'high': [11, 11], 'low': [9, 9], 'close': [10, 10.1]})
        b = pd.DataFrame({'date': [2], 'open': [10], 'high': [11], 'low': [9], 'close': [10]})
        r = H.banding(a, b)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(r.close.iloc[0], 0.01)

    def test_liputan_sesi(self):
        import tempfile
        with tempfile.TemporaryDirectory() as dd:
            p = os.path.join(dd, 'terkini.csv')
            self.assertEqual(H.liputan_sesi(p, 20261021), 0)
            pd.DataFrame(dict(ticker=['A', 'A', 'B', 'C'], date=[20261020, 20261021, 20261021, 20261020])).to_csv(p, index=False)
            self.assertEqual(H.liputan_sesi(p, 20261021), 2)

    def test_universe(self):
        s, idx = H.universe()
        self.assertEqual(idx, ['SPY', 'QQQ'])
        self.assertGreater(len(s), 400)
        self.assertNotIn('SPY', s)


if __name__ == '__main__':
    unittest.main()

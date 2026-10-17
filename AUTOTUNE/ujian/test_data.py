"""Ujian unit saluran data AUTOTUNE (tanpa rangkaian): python3 -m unittest discover -s AUTOTUNE/ujian -p 'test_data.py'"""
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))


def _muat_modul(nama, laluan):
    sp = importlib.util.spec_from_file_location(nama, laluan)
    m = importlib.util.module_from_spec(sp)
    sys.modules[nama] = m
    sp.loader.exec_module(m)
    return m


gabung = _muat_modul('at_gabung', AKAR / 'AUTOTUNE/data/gabung.py')
calon = _muat_modul('at_calon', AKAR / 'AUTOTUNE/data/senarai_calon.py')
mt = _muat_modul('at_muat_turun', AKAR / 'AUTOTUNE/data/muat_turun.py')
from AUTOTUNE.teras import data as D  # noqa: E402


def bar(t, tarikh, harga, vol, lompat=None):
    n = len(tarikh)
    c = np.full(n, float(harga)) if np.isscalar(harga) else np.asarray(harga, dtype=float)
    return pd.DataFrame({'ticker': t, 'date': tarikh, 'open': c, 'high': c * 1.01, 'low': c * 0.99, 'close': c,
                         'volume': np.full(n, float(vol))})


class TestKumpulan(unittest.TestCase):
    def test_md5(self):
        for t in ('AAPL', 'MSFT', 'BRK-B', 'X'):
            jangka = 'A' if int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 == 0 else 'B'
            self.assertEqual(gabung.kumpulan(t), jangka)

    def test_tetap(self):
        self.assertEqual(gabung.kumpulan('AAPL'), gabung.kumpulan('AAPL'))
        k = {gabung.kumpulan(f'T{i}') for i in range(50)}
        self.assertEqual(k, {'A', 'B'})


class TestQC(unittest.TestCase):
    def test_bersih(self):
        t = pd.bdate_range('2020-01-01', periods=6)
        d = bar('X', t, 10, 100)
        d.loc[1, 'close'] = 0          # harga <= 0
        d.loc[2, 'open'] = np.nan      # NaN
        d.loc[3, 'high'] = 5           # high < low
        d.loc[4, 'volume'] = np.nan    # volume NaN -> 0, bar kekal
        o, n = gabung.bersih(d)
        self.assertEqual(n, 3)
        self.assertEqual(len(o), 3)
        self.assertEqual(o.loc[4, 'volume'], 0)

    def test_lompat(self):
        t = pd.bdate_range('2020-01-01', periods=20)
        c = np.full(20, 10.0)
        c[3::3] = [20, 10, 20, 10, 20, 10]   # 6 lompat 100% / -50%
        a = bar('A', t, c, 100)
        b = bar('B', t, 10, 100)
        d = pd.concat([a, b], ignore_index=True)
        j = gabung.bilangan_lompat(d)
        self.assertEqual(j['A'], 3)  # 3 naik +100%; turun -50% tepat tidak > 0.5
        self.assertEqual(j['B'], 0)

    def test_lompat_antara_ticker(self):
        t = pd.bdate_range('2020-01-01', periods=3)
        d = pd.concat([bar('A', t, 100, 1), bar('B', t, 1, 1)], ignore_index=True)
        self.assertEqual(gabung.bilangan_lompat(d).sum(), 0)  # sempadan A->B bukan lompat


def _lebar(spek, tarikh):
    """spek: ticker -> (harga/array, volume, mula_indeks). Pulang close, vol lebar."""
    C, V = {}, {}
    for t, (h, v, m) in spek.items():
        c = np.full(len(tarikh), np.nan)
        vv = np.full(len(tarikh), np.nan)
        c[m:] = h if np.isscalar(h) else h[m:]
        vv[m:] = v
        C[t], V[t] = c, vv
    return pd.DataFrame(C, index=tarikh), pd.DataFrame(V, index=tarikh)


class TestUniverse(unittest.TestCase):
    def setUp(self):
        self.kal = pd.bdate_range('2019-01-01', '2020-12-31')
        self._n = gabung.N_UNIVERSE

    def tearDown(self):
        gabung.N_UNIVERSE = self._n

    def test_syarat(self):
        n = len(self.kal)
        jatuh = np.where(self.kal < '2020-03-01', 50.0, 5.0)   # jatuh < $10 mulai Mac 2020
        spek = {
            'BESAR': (100.0, 5e6, 0),     # layak
            'MURAH': (5.0, 5e6, 0),       # harga <= 10
            'NIPIS': (50.0, 1e3, 0),      # nilai dagangan 5e4 < 1e6
            'BARU': (100.0, 5e6, n - 100),  # hanya 100 bar
            'JATUH': (jatuh, 5e6, 0),
        }
        C, V = _lebar(spek, self.kal)
        u = gabung.bina_universe(C, V, self.kal)
        feb = set(u[u.bulan == '2020-02'].ticker)    # berdasarkan tutup Jan 2020
        mac = set(u[u.bulan == '2020-03'].ticker)    # berdasarkan tutup Feb 2020: JATUH masih 50
        apr = set(u[u.bulan == '2020-04'].ticker)    # tutup Mac 2020: JATUH = 5
        self.assertEqual(feb, {'BESAR', 'JATUH'})
        self.assertEqual(mac, {'BESAR', 'JATUH'})
        self.assertEqual(apr, {'BESAR'})
        self.assertNotIn('2019-01', set(u.bulan))     # bar < 200 pada Jan 2019
        self.assertNotIn('BARU', set(u.ticker))       # 100 bar sahaja hingga akhir 2020: tidak pernah >= 200
        self.assertEqual(sorted(u.bulan.unique())[-1], '2021-01')  # berkuat kuasa bulan berikutnya

    def test_barubar_200(self):
        C, V = _lebar({'LAMA': (100.0, 5e6, 0), 'BARU': (100.0, 5e6, 300)}, self.kal)
        u = gabung.bina_universe(C, V, self.kal)
        pertama = u[u.ticker == 'BARU'].bulan.min()
        # bar ke-200 BARU = indeks 499; hari dagangan terakhir bulan itu >= 499 -> berkuat kuasa bulan berikutnya
        self.assertEqual(pertama, str(self.kal[499].to_period('M') + 1))

    def test_kedudukan_had_dan_kumpulan(self):
        gabung.N_UNIVERSE = 2
        C, V = _lebar({'T1': (100.0, 1e6, 0), 'T2': (100.0, 3e6, 0), 'T3': (100.0, 2e6, 0)}, self.kal)
        u = gabung.bina_universe(C, V, self.kal)
        m = u[u.bulan == '2020-06'].sort_values('kedudukan')
        self.assertEqual(list(m.ticker), ['T2', 'T3'])
        self.assertEqual(list(m.kedudukan), [1, 2])
        for _, r in m.iterrows():
            self.assertEqual(r.kumpulan, gabung.kumpulan(r.ticker))

    def test_dikecualikan_dan_benchmark(self):
        C, V = _lebar({'OK': (100.0, 5e6, 0), 'RUSAK': (100.0, 5e6, 0), 'SPY': (300.0, 9e7, 0)}, self.kal)
        u = gabung.bina_universe(C, V, self.kal, dikecualikan=['RUSAK'])
        self.assertEqual(set(u.ticker), {'OK'})


class TestShardDanLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        t = Path(cls.tmp.name)
        cls.masuk, cls.keluar = t / 'masuk', t / 'keluar'
        cls.masuk.mkdir()
        (t / 'repo').mkdir()
        kal = pd.bdate_range('2019-01-01', '2020-12-31')
        rng = np.random.default_rng(1)
        bahagian = []
        for i, tk in enumerate(['AAA', 'BBB', 'CCC', 'DDD', 'SPY', 'QQQ']):
            c = 50 * np.cumprod(1 + rng.normal(0, 0.01, len(kal)))
            bahagian.append(bar(tk, kal, c, 2e5))
        rusak = np.where(np.arange(len(kal)) % 20 == 0, 100.0, 10.0)  # lompat berulang > 5 kali
        bahagian.append(bar('RUSAK', kal, rusak * 5, 1e6))
        bahagian.append(bar('MURAH', kal, 3.0, 1e7))
        df = pd.concat(bahagian, ignore_index=True)
        for c in ('open', 'high', 'low', 'close'):
            df[c] = df[c].astype('float32')
        df.iloc[5, df.columns.get_loc('close')] = np.nan          # satu bar rosak dibuang
        df.iloc[:len(df) // 2].to_parquet(cls.masuk / 'shard_0.parquet', index=False)
        df.iloc[len(df) // 2:].to_parquet(cls.masuk / 'shard_1.parquet', index=False)
        (cls.masuk / 'shard_0.json').write_text(json.dumps({'gagal': 2}))
        cls.man, cls.univ, cls.qc = gabung.proses(cls.masuk, cls.keluar, tarikan='2026-10-18T00:00Z',
                                              repo_dir=t / 'repo')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_qc(self):
        self.assertTrue(self.qc.set_index('ticker').loc['RUSAK', 'bendera'])
        self.assertNotIn('RUSAK', set(self.univ.ticker))
        self.assertNotIn('MURAH', set(self.univ.ticker))
        self.assertTrue({'AAA', 'BBB', 'CCC', 'DDD'} <= set(self.univ.ticker))

    def test_fail(self):
        nama = {f['nama'] for f in self.man['fail']}
        self.assertTrue({'harga_2019.parquet', 'harga_2020.parquet', 'idx.parquet', 'universe.parquet',
                         'qc.csv'} <= nama)
        for f in self.man['fail']:
            p = self.keluar / f['nama']
            self.assertEqual(p.stat().st_size, f['bait'])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), f['sha256'])
        h = pd.read_parquet(self.keluar / 'harga_2019.parquet')
        self.assertEqual(list(h.columns), ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
        self.assertEqual(str(h.close.dtype), 'float32')
        self.assertEqual(str(h.volume.dtype), 'float64')
        self.assertNotIn('RUSAK', set(h.ticker))
        self.assertNotIn('SPY', set(h.ticker))
        self.assertEqual(set(pd.read_parquet(self.keluar / 'idx.parquet').ticker), {'SPY', 'QQQ'})

    def test_ambil_cache_lengkap(self):
        # cache lengkap + sha256 betul -> tiada akses rangkaian
        self.assertEqual(D.ambil(cache=str(self.keluar)), self.keluar)

    def test_muat(self):
        fr, idx, u = D.muat('2020-01-01', '2020-06-30', 'AB', dir=self.keluar)
        self.assertEqual(set(idx), {'SPY', 'QQQ'})
        self.assertTrue(len(fr) > 0)
        for t, g in fr.items():
            self.assertEqual(list(g.columns), ['open', 'high', 'low', 'close', 'volume', 'turnover'])
            self.assertEqual(g.index.name, 'date')
            self.assertTrue(g.index.min() >= pd.Timestamp('2020-01-01'))
            self.assertTrue(g.index.max() <= pd.Timestamp('2020-06-30'))
            self.assertTrue((g.dtypes == 'float64').all())
            self.assertTrue(np.allclose(g.turnover, g.close * g.volume))
        fa, _, _ = D.muat('2020-01-01', '2020-06-30', 'A', dir=self.keluar)
        fb, _, _ = D.muat('2020-01-01', '2020-06-30', 'B', dir=self.keluar)
        self.assertTrue(all(gabung.kumpulan(t) == 'A' for t in fa))
        self.assertTrue(all(gabung.kumpulan(t) == 'B' for t in fb))
        self.assertEqual(set(fa) | set(fb), set(fr))

    def test_topeng(self):
        fr, idx, u = D.muat('2019-01-01', '2020-12-31', 'AB', dir=self.keluar)
        t = sorted(fr)[0]
        g = fr[t]
        m = D.topeng(g, t, u, 'AB')
        self.assertEqual(m.dtype, bool)
        self.assertTrue(m.index.equals(g.index))
        bulan_u = set(u[u.ticker == t].bulan)
        jangka = [f'{d.year}-{d.month:02d}' in bulan_u for d in g.index]
        self.assertEqual(list(m), jangka)
        self.assertFalse(D.topeng(g, t, u, 'B' if gabung.kumpulan(t) == 'A' else 'A').any())
        self.assertFalse(D.topeng(g, 'TIADA', u, 'AB').any())


class TestMuat431(unittest.TestCase):
    def test_format(self):
        fr, idx = D.muat_431()
        self.assertTrue(len(fr) > 100)
        self.assertEqual(set(idx), {'SPY', 'QQQ'})
        g = next(iter(fr.values()))
        self.assertEqual(list(g.columns), ['open', 'high', 'low', 'close', 'volume', 'turnover'])
        self.assertIsInstance(g.index, pd.DatetimeIndex)
        self.assertEqual(g.index.name, 'date')
        self.assertTrue(g.index.is_monotonic_increasing)
        self.assertTrue((g.dtypes == 'float64').all())


class TestMuatTurunDanCalon(unittest.TestCase):
    def test_urai_multiindeks(self):
        t = pd.date_range('2020-01-01', periods=3, tz='America/New_York')
        kol = pd.MultiIndex.from_product([['AAA', 'BBB'], ['Open', 'High', 'Low', 'Close', 'Volume']])
        df = pd.DataFrame(np.arange(30, dtype=float).reshape(3, 10) + 1, index=t, columns=kol)
        df[('BBB', 'Close')] = np.nan
        df[('BBB', 'Open')] = np.nan
        df[('BBB', 'High')] = np.nan
        df[('BBB', 'Low')] = np.nan
        r = mt.urai(df, ['AAA', 'BBB', 'CCC'])
        self.assertEqual(set(r), {'AAA'})
        self.assertEqual(list(r['AAA'].columns), ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
        self.assertIsNone(r['AAA']['date'].dt.tz)

    def test_urai_tunggal_dan_kosong(self):
        t = pd.date_range('2020-01-01', periods=2)
        df = pd.DataFrame({'Open': [1., 2], 'High': [2., 3], 'Low': [1., 1], 'Close': [2., 2], 'Volume': [5., 6]}, index=t)
        self.assertEqual(set(mt.urai(df, ['ZZZ'])), {'ZZZ'})
        self.assertEqual(mt.urai(pd.DataFrame(), ['ZZZ']), {})

    def test_calon(self):
        n = ('Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares\n'
             'AAPL|Apple Inc. - Common Stock|Q|N|N|100|N|N\n'
             'QQQ|Invesco QQQ Trust|G|N|N|100|Y|N\n'
             'TEST|Zzzz Test Stock|G|Y|N|100|N|N\n'
             'ABCDW|Foo Acquisition Corp - Warrant|S|N|N|100|N|N\n'
             'XYZ|Foo Acquisition Corp. - Class A Ordinary Shares|S|N|N|100|N|N\n'
             'FOOU|Foo Holdings - Units|S|N|N|100|N|N\n'
             'FOOR|Foo Holdings - Rights|S|N|N|100|N|N\n'
             'BABA|Alibaba Group - American Depositary Shares|S|N|N|100|N|N\n'
             'File Creation Time: 1017202600:00|||||||\n')
        o = ('ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol\n'
             'BRK.B|Berkshire Hathaway Inc. Class B Common Stock|N|BRK.B|N|100|N|BRK.B\n'
             'BAC$L|Bank of America Preferred|N|BAC$L|N|100|N|BAC-L\n'
             'SPY|SPDR S&P 500 ETF Trust|P|SPY|Y|100|N|SPY\n'
             'NTE|Foo 6.5% Notes due 2030|N|NTE|N|100|N|NTE\n'
             'F|Ford Motor Company Common Stock|N|F|N|100|N|F\n'
             'File Creation Time: 1017202600:00|||||||\n')
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / 'data_mentah').mkdir()
            (Path(td) / 'data_mentah/dataset_S1.csv').write_text('ticker,date\nZZZ,20190102\nBF.B,20190102\n')
            lst, ns, nd = calon.calon_senarai(n, o, akar=Path(td))
        self.assertEqual(lst, sorted(['AAPL', 'BABA', 'BRK-B', 'F', 'BF-B', 'ZZZ']))
        self.assertEqual(calon.yahoo('BRK.B'), 'BRK-B')
        self.assertIsNone(calon.yahoo('BAC$L'))


if __name__ == '__main__':
    unittest.main()

"""Ujian unit saluran data A02 (sintetik, tanpa rangkaian): python3 -m unittest discover -s AUTOTUNE/ujian -p 'test_data_a02.py'"""
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


mt = _muat_modul('at_muat_turun_a02', AKAR / 'AUTOTUNE/data/muat_turun_a02.py')
gb = _muat_modul('at_gabung_a02', AKAR / 'AUTOTUNE/data/gabung_a02.py')
from AUTOTUNE.teras import data as D  # noqa: E402


def _bar(t, tarikh, close, vol=1e6, fak=1.0):
    return pd.DataFrame({'ticker': t, 'date': tarikh, 'open': close, 'high': np.asarray(close) * 1.01,
                         'low': np.asarray(close) * 0.99, 'close': close, 'volume': vol, 'faktor_split': fak})


class TestFaktorSplit(unittest.TestCase):
    def test_selepas_secara_ketat(self):
        t = pd.bdate_range('2020-01-01', periods=10)
        sp = pd.Series([4.0, 0.5], index=pd.DatetimeIndex([t[3], t[6]]))
        f = mt.faktor_split(t, sp)
        # sebelum split pertama: 4*0.5; pada tarikh split pertama: split itu BUKAN 'selepas' -> 0.5
        np.testing.assert_allclose(f, [2, 2, 2, 0.5, 0.5, 0.5, 1, 1, 1, 1])

    def test_tiada_split(self):
        np.testing.assert_allclose(mt.faktor_split(pd.bdate_range('2020-01-01', periods=3), None), [1, 1, 1])

    def test_satu_dari_yfinance(self):
        t = pd.bdate_range('2020-01-01', periods=6, tz='America/New_York')
        d = pd.DataFrame({'Open': 10., 'High': 11., 'Low': 9., 'Close': 10., 'Volume': 100.,
                          'Stock Splits': [0, 0, 2.0, 0, 0, 0]}, index=t)
        r = mt._satu(d, 'XYZ')
        self.assertEqual(list(r.faktor_split), [2, 2, 1, 1, 1, 1])
        self.assertEqual(str(r.faktor_split.dtype), 'float32')
        d2 = d.drop(columns='Stock Splits')
        self.assertTrue((mt._satu(d2, 'XYZ').faktor_split == 1.0).all())


class TestQc(unittest.TestCase):
    def test_lonjakan_bar_t_sahaja(self):
        t = pd.bdate_range('2020-01-01', periods=8)
        c = [10, 10, 10, 20, 10, 10, 10, 10]   # +100% lalu -50%: bar ke-3 dibuang
        d = pd.concat([_bar('A', t, c), _bar('B', t, [10] * 8)], ignore_index=True)
        bersih, db = gb.qc_bar(d)
        self.assertEqual(len(db), 1)
        self.assertEqual((db.ticker[0], db.sebab[0], db.date[0]), ('A', 'lonjakan', str(t[3].date())))
        self.assertEqual(len(bersih), 15)

    def test_lompatan_kekal_tidak_dibuang(self):
        t = pd.bdate_range('2020-01-01', periods=6)
        _, db = gb.qc_bar(_bar('A', t, [10, 10, 25, 25, 25, 25]))     # +150% tanpa berbalik
        self.assertEqual(len(db), 0)
        _, db = gb.qc_bar(_bar('A', t, [10, 10, 14, 10, 10, 10]))     # +40% tepat bukan > 40%
        self.assertEqual(len(db), 0)

    def test_harga_tidak_sah(self):
        t = pd.bdate_range('2020-01-01', periods=4)
        d = _bar('A', t, [10, 0, 10, 10])
        d.loc[2, 'low'] = 12.0        # high < low
        d.loc[3, 'volume'] = np.nan
        bersih, db = gb.qc_bar(d)
        self.assertEqual(sorted(db.sebab), ['harga_tidak_sah', 'high<low'])
        self.assertEqual(len(bersih), 2)
        self.assertEqual(bersih.volume.iloc[-1], 0.0)

    def test_tiada_pergaulan_antara_ticker(self):
        t = pd.bdate_range('2020-01-01', periods=3)
        d = pd.concat([_bar('A', t, [10, 10, 10]), _bar('B', t, [30, 30, 30])], ignore_index=True)
        self.assertEqual(len(gb.qc_bar(d)[1]), 0)


class TestUniverse(unittest.TestCase):
    def test_harga_tidak_dilaras_dan_split_invariant(self):
        kal = pd.bdate_range('2020-01-01', '2021-06-30')
        # S: dilaras 0.25 tetapi faktor 40 -> mentah 10.0 (tidak > 10) ; T: dilaras 0.3, faktor 40 -> 12 (layak)
        close = pd.DataFrame({'S': 0.25, 'T': 0.3, 'P': 5.0, 'H': 50.0}, index=kal)
        fak = pd.DataFrame({'S': 40.0, 'T': 40.0, 'P': 1.0, 'H': 1.0}, index=kal)
        vol = pd.DataFrame({'S': 1e8, 'T': 1e8, 'P': 1e7, 'H': 1e5}, index=kal)   # H: 50*1e5=5e6
        u = gb.bina_universe(close, vol, fak, kal)
        pada = u[u.bulan == '2021-06']
        self.assertEqual(set(pada.ticker), {'T', 'H'})
        self.assertEqual(pada.set_index('ticker').kedudukan['T'], 1)       # 0.3*1e8 = 3e7 > 5e6
        self.assertTrue(set(u.kumpulan) <= {'A', 'B'})

    def test_bar_minimum_200(self):
        kal = pd.bdate_range('2020-01-01', '2020-12-31')
        close = pd.DataFrame({'X': 20.0}, index=kal)
        close.loc[kal[:150], 'X'] = np.nan
        fak = pd.DataFrame({'X': 1.0}, index=kal)
        vol = pd.DataFrame({'X': 1e6}, index=kal)
        u = gb.bina_universe(close, vol, fak, kal)
        self.assertEqual(len(u), 0)            # hanya 111 bar pada Dis 2020 (< 200)
        u2 = gb.bina_universe(pd.DataFrame({'X': 20.0}, index=kal), vol, fak, kal)
        self.assertEqual(list(u2.bulan[u2.ticker == 'X'].iloc[[-1]]), ['2021-01'])
        self.assertNotIn('2020-03', set(u2.bulan))     # baru ~64 bar pada Mac 2020


class TestPemuat(unittest.TestCase):
    def test_tag_dan_cache_bukan_lalai(self):
        import AUTOTUNE.teras.data as dd
        with tempfile.TemporaryDirectory() as tmp:
            # cache yang lengkap dikembalikan terus tanpa rangkaian
            c = Path(tmp)
            (c / 'manifest.json').write_text(json.dumps({'tag': 'autotune-data-a02', 'fail': []}))
            self.assertEqual(dd.ambil(cache=c, tag='autotune-data-a02'), c)

    def test_muat_dengan_faktor(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            t = pd.bdate_range('2020-01-02', periods=5)
            x = _bar('AAA', t, 20.0, fak=[2, 2, 1, 1, 1])
            for c in ('open', 'high', 'low', 'close', 'faktor_split'):
                x[c] = x[c].astype('float32')
            x.to_parquet(d / 'harga_2020.parquet', index=False)
            pd.concat([_bar('SPY', t, 300.0), _bar('QQQ', t, 200.0)]).to_parquet(d / 'idx.parquet', index=False)
            pd.DataFrame({'bulan': ['2020-01'], 'ticker': ['AAA'], 'kedudukan': [1], 'kumpulan': ['A']}).to_parquet(
                d / 'universe.parquet', index=False)
            fr, idx, univ = D.muat('2020-01-01', '2020-12-31', dir=d)
            self.assertNotIn('faktor_split', fr['AAA'].columns)
            self.assertEqual(list(fr['AAA'].columns), D.LAJUR_OUT)
            fr2, idx2, _ = D.muat('2020-01-01', '2020-12-31', dir=d, faktor=True)
            self.assertEqual(list(fr2['AAA'].faktor_split), [2, 2, 1, 1, 1])
            self.assertEqual(set(idx2), {'SPY', 'QQQ'})


if __name__ == '__main__':
    unittest.main()

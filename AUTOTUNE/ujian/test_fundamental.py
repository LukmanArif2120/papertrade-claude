"""Ujian unit saluran fundamental A03 (sintetik, tanpa rangkaian):
python3 -m unittest discover -s AUTOTUNE/ujian -p 'test_fundamental.py'"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))

from AUTOTUNE.fundamental import ciri, gabung_eps as ge, muat_eps as me  # noqa: E402

NY = 'America/New_York'
HARI = np.array(pd.bdate_range('2020-01-01', '2023-12-29').values, dtype='datetime64[D]')


def _mentah(ticker, tarikh, eps, masa='selepas', sumber='yahoo', jam=None):
    """Baris shard sintetik; tarikh_laporan ISO bertz New York."""
    out = []
    for i, (tg, e) in enumerate(zip(tarikh, eps)):
        m = masa[i] if isinstance(masa, list) else masa
        j = jam or {'sebelum': '07:00', 'selepas': '16:30', 'tidak diketahui': '12:00'}[m]
        ts = pd.Timestamp(f'{tg} {j}').tz_localize(NY)
        out.append([ticker, ts.isoformat(), m, e, '', sumber])
    return out


def _df(baris):
    return pd.DataFrame(baris, columns=me.LAJUR)


def _suku(mula, n, langkah_hari=91):
    return [(pd.Timestamp(mula) + pd.Timedelta(days=langkah_hari * i)).strftime('%Y-%m-%d') for i in range(n)]


class TestMasa(unittest.TestCase):
    def test_sempadan(self):
        k = me.klasifikasi_masa
        self.assertEqual(k(0, 0), 'tidak diketahui')
        self.assertEqual(k(6, 0), 'sebelum')
        self.assertEqual(k(9, 29), 'sebelum')
        self.assertEqual(k(9, 30), 'tidak diketahui')
        self.assertEqual(k(15, 59), 'tidak diketahui')
        self.assertEqual(k(16, 0), 'selepas')
        self.assertEqual(k(20, 0), 'selepas')

    def test_baris_dari_df_tz_dan_eps_kosong(self):
        idx = pd.DatetimeIndex(['2024-05-02 16:00', '2024-02-01 07:00', '2024-08-01 13:00', '2023-11-01 20:30']).tz_localize(NY)
        d = pd.DataFrame({'EPS Estimate': [1.0, 0.9, 1.1, np.nan], 'Reported EPS': [np.nan, 0.95, 1.2, 0.8],
                          'Surprise(%)': [np.nan, 5.0, 9.0, np.nan]}, index=idx)
        b = me.baris_dari_df('XYZ', d)
        self.assertEqual(len(b), 3)          # baris tanpa Reported EPS (akan datang) dibuang
        peta = {r[1][:10]: r for r in b}
        self.assertEqual(peta['2024-02-01'][2], 'sebelum')
        self.assertEqual(peta['2024-08-01'][2], 'tidak diketahui')
        self.assertEqual(peta['2023-11-01'][2], 'selepas')
        self.assertEqual(peta['2023-11-01'][4], '')      # anggaran NaN -> kosong
        # indeks UTC ditukar ke New York: 2024-02-01 12:00 UTC = 07:00 EST
        d2 = pd.DataFrame({'Reported EPS': [0.5]}, index=pd.DatetimeIndex(['2024-02-01 12:00']).tz_localize('UTC'))
        r = me.baris_dari_df('XYZ', d2)[0]
        self.assertTrue(r[1].startswith('2024-02-01T07:00:00-05:00'))
        self.assertEqual(r[2], 'sebelum')


class TestMuat(unittest.TestCase):
    def test_had_lebih_kecil_selepas_ralat(self):
        panggilan = []
        idx = pd.DatetimeIndex(['2024-02-01 16:00']).tz_localize(NY)

        def ambil(s, had):
            panggilan.append(had)
            if had == 100:
                raise RuntimeError('ralat sementara')
            return pd.DataFrame({'Reported EPS': [1.0], 'EPS Estimate': [0.9]}, index=idx)
        baris, ralat = me.tarik_satu('BRK.B', ambil, tidur=lambda s: None)
        self.assertEqual(len(baris), 1)
        self.assertIsNone(ralat)
        self.assertEqual(panggilan, [100, 100, 40])

    def test_tiada_data_tanpa_ulang(self):
        n = []

        def ambil(s, had):
            n.append(1)
            raise ValueError('No earnings dates found, symbol may be delisted')
        baris, ralat = me.tarik_satu('ZZZ', ambil, tidur=lambda s: None)
        self.assertEqual((baris, ralat, len(n)), ([], 'kosong', 1))

    def test_benih_apabila_yahoo_gagal(self):
        with tempfile.TemporaryDirectory() as td:
            benih_fail = Path(td) / 'eps.csv'
            benih_fail.write_text('ticker,tarikh,masa,eps_anggaran,eps_sebenar,kejutan_pct\n'
                                  'BIO.B,2020-02-10,16:00,1.0,1.2,20\nBIO.B,2020-05-10,07:00,,0.4,\nBIO.B,2020-08-10,16:00,1,,\n')
            benih = me.baca_benih(benih_fail)
            self.assertEqual(len(benih['BIO-B']), 2)       # baris tanpa eps_sebenar dibuang; ticker dinormalkan
            idx = pd.DatetimeIndex(['2024-02-01 16:00']).tz_localize(NY)

            def ambil(s, had):
                if s == 'BIO-B':
                    raise RuntimeError('Yahoo down')
                return pd.DataFrame({'Reported EPS': [2.0]}, index=idx)
            semua, gagal = me.jalankan(['AAA', 'BIO-B'], benih, Path(td) / 'out', 3, fn_ambil=ambil, rehat=0,
                                       tidur=lambda s: None, senyap=True)
            d = pd.read_csv(Path(td) / 'out' / 'eps_shard_3.csv')
            self.assertEqual(sorted(d['sumber'].unique()), ['repo', 'yahoo'])
            self.assertEqual(len(d[d['ticker'] == 'BIO-B']), 2)
            self.assertEqual(len(gagal), 1)
            self.assertIn('ganti=repo', (Path(td) / 'out' / 'gagal_3.txt').read_text())


class TestTersedia(unittest.TestCase):
    def test_peraturan_hari(self):
        # 2021-03-10 = Rabu; 2021-03-12 = Jumaat; 2021-03-13 = Sabtu
        tg = pd.to_datetime(['2021-03-10', '2021-03-10', '2021-03-10', '2021-03-12', '2021-03-13', '2021-03-13'])
        masa = ['sebelum', 'selepas', 'tidak diketahui', 'selepas', 'sebelum', 'selepas']
        t = ge.hitung_tersedia(tg, masa, HARI)
        esp = ['2021-03-10', '2021-03-11', '2021-03-11', '2021-03-15', '2021-03-15', '2021-03-15']
        self.assertEqual([str(x.date()) for x in t], esp)

    def test_melepasi_hari_terakhir(self):
        t = ge.hitung_tersedia(pd.to_datetime(['2023-12-29', '2023-12-29']), ['selepas', 'sebelum'], HARI)
        self.assertTrue(pd.isna(t[0]))
        self.assertEqual(str(t[1].date()), '2023-12-29')


class TestBina(unittest.TestCase):
    def test_yoy_dan_nyahpendua(self):
        tg = _suku('2020-02-05', 8)
        eps = [1.0, 1.1, 1.2, 1.3, 1.5, -0.5, 1.8, 2.6]
        baris = _mentah('AAA', tg, eps)
        baris += _mentah('AAA', [(pd.Timestamp(tg[2]) + pd.Timedelta(days=3)).strftime('%Y-%m-%d')], [9.9])   # pendua suku ke-3
        e = ge.bina(_df(baris), HARI).reset_index(drop=True)
        self.assertEqual(len(e), 8)
        self.assertAlmostEqual(e.eps_sebenar[2], 1.2)                      # baris terawal dikekalkan
        self.assertTrue(e.eps_yoy[:4].isna().all())                        # tiada suku 4 lalu
        self.assertAlmostEqual(e.eps_yoy[4], 0.5)                          # (1.5-1.0)/1.0
        self.assertAlmostEqual(e.eps_yoy[5], (-0.5 - 1.1) / 1.1)           # EPS semasa negatif: dikira (EPS lalu > 0)
        self.assertAlmostEqual(e.eps_yoy[7], (2.6 - 1.3) / 1.3)
        self.assertAlmostEqual(e.eps_yoy_sebelum[5], 0.5)
        self.assertTrue(np.isnan(e.eps_yoy_sebelum[4]))                    # yoy suku sebelumnya tiada
        self.assertAlmostEqual(e.eps_yoy_sebelum[7], e.eps_yoy[6])

    def test_yoy_nan_jika_eps_lalu_tidak_positif(self):
        tg = _suku('2020-02-05', 6)
        e = ge.bina(_df(_mentah('AAA', tg, [-1.0, 0.0, 1.0, 1.0, 2.0, 2.0])), HARI).reset_index(drop=True)
        self.assertTrue(np.isnan(e.eps_yoy[4]) and np.isnan(e.eps_yoy[5]))   # EPS lalu -1 dan 0 -> NaN

    def test_yoy_nan_jika_suku_hilang(self):
        tg = _suku('2020-02-05', 7)
        del tg[2]                                                          # satu suku hilang -> i-4 bukan tahun lepas
        e = ge.bina(_df(_mentah('AAA', tg, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5])), HARI)
        self.assertTrue(e.eps_yoy.isna().all())

    def test_ticker_berbeza_tidak_bercampur(self):
        a = _mentah('AAA', _suku('2020-02-05', 2), [1.0, 1.0])
        b = _mentah('BBB', _suku('2020-02-05', 5), [1.0, 1.0, 1.0, 1.0, 2.0])
        e = ge.bina(_df(a + b), HARI)
        self.assertEqual(e[e.ticker == 'AAA'].eps_yoy.notna().sum(), 0)
        self.assertEqual(e[e.ticker == 'BBB'].eps_yoy.notna().sum(), 1)


class TestLajurF(unittest.TestCase):
    def _fr(self, tickers):
        ix = pd.DatetimeIndex(HARI[HARI >= np.datetime64('2020-06-01')].astype('datetime64[ns]'))
        return {t: pd.DataFrame({'close': 1.0}, index=ix) for t in tickers}

    def _eps(self, baris):
        return ge.bina(_df(baris), HARI)

    def test_tiada_pandang_hadapan_selepas(self):
        # 5 suku; suku ke-5 dilapor Rabu 2021-02-03 SELEPAS tutup, yoy = +100% -> F benar mulai Khamis 2021-02-04
        tg = ['2020-02-05', '2020-05-06', '2020-08-05', '2020-11-04', '2021-02-03']
        e = self._eps(_mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 2.0], masa='selepas'))
        f = ciri.lajur_f(self._fr(['AAA']), e)['AAA']
        self.assertFalse(f[pd.Timestamp('2021-02-03')])
        self.assertTrue(f[pd.Timestamp('2021-02-04')])
        self.assertFalse(f[pd.Timestamp('2021-02-02')])
        self.assertEqual(int(f[:'2021-02-03'].sum()), 0)

    def test_sebelum_hari_sama(self):
        tg = ['2020-02-05', '2020-05-06', '2020-08-05', '2020-11-04', '2021-02-03']
        e = self._eps(_mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 2.0], masa='sebelum'))
        f = ciri.lajur_f(self._fr(['AAA']), e)['AAA']
        self.assertFalse(f[pd.Timestamp('2021-02-02')])
        self.assertTrue(f[pd.Timestamp('2021-02-03')])

    def test_suku_terkini_menggantikan_yang_lama(self):
        # suku ke-5 layak (+100%), suku ke-6 tidak (+10%): selepas laporan ke-6 F kembali palsu (bukan jatuh ke suku lama)
        tg = _suku('2020-02-05', 6)
        e = self._eps(_mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 2.0, 1.1], masa='sebelum'))
        f = ciri.lajur_f(self._fr(['AAA']), e)['AAA']
        t5, t6 = pd.Timestamp(tg[4]), pd.Timestamp(tg[5])
        t5, t6 = [x if x.weekday() < 5 else x + pd.offsets.BDay(1) for x in (t5, t6)]
        self.assertTrue(f[t5 + pd.offsets.BDay(1)])
        self.assertFalse(f[t6 + pd.offsets.BDay(1)])

    def test_ambang_dan_eps_negatif_dan_tiada_data(self):
        tg = _suku('2020-02-05', 5)
        a = _mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 1.2], masa='sebelum')      # yoy +20%
        b = _mentah('BBB', tg, [1.0, 1.0, 1.0, 1.0, -2.0], masa='sebelum')     # EPS negatif
        e = self._eps(a + b)
        fr = self._fr(['AAA', 'BBB', 'CCC'])
        f25 = ciri.lajur_f(fr, e, ambang=0.25)
        f15 = ciri.lajur_f(fr, e, ambang=0.15)
        self.assertFalse(f25['AAA'].any())
        self.assertTrue(f15['AAA'].iloc[-1])
        self.assertFalse(f15['BBB'].any())
        self.assertFalse(f15['CCC'].any())                                      # tiada EPS -> tidak layak
        for s in f25.values():
            self.assertTrue(s.index.equals(fr['AAA'].index))
            self.assertEqual(s.dtype, bool)

    def test_usia_maks(self):
        tg = _suku('2020-02-05', 5)
        e = self._eps(_mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 2.0], masa='sebelum'))
        fr = self._fr(['AAA'])
        self.assertTrue(ciri.lajur_f(fr, e)['AAA'].iloc[-1])                    # tiada had usia: kekal benar
        self.assertFalse(ciri.lajur_f(fr, e, usia_maks=135)['AAA'].iloc[-1])    # lapuk


class TestGabungHujungKeHujung(unittest.TestCase):
    def test_gabung(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / 'shards' / 'shard-0').mkdir(parents=True)
            tg = _suku('2020-02-05', 8)
            b = _mentah('AAA', tg, [1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0], masa='sebelum')
            b += _mentah('BBB', tg[:4], [1.0] * 4, masa='selepas', sumber='repo')
            _df(b).to_csv(td / 'shards' / 'shard-0' / 'eps_shard_0.csv', index=False)
            (td / 'shards' / 'shard-0' / 'gagal_0.txt').write_text('# shard 0\nCCC\tkosong\tganti=tiada\tbaris=0\n')
            bulan = [f'{y}-{m:02d}' for y in (2020, 2021) for m in range(1, 13)]
            univ = pd.DataFrame([[bl, t, 1, 'A'] for bl in bulan for t in ('AAA', 'BBB', 'CCC')],
                                columns=['bulan', 'ticker', 'kedudukan', 'kumpulan'])
            univ.to_parquet(td / 'universe.parquet')
            idx = pd.DataFrame({'ticker': 'SPY', 'date': pd.DatetimeIndex(HARI.astype('datetime64[ns]')), 'close': 1.0})
            idx.to_parquet(td / 'idx.parquet')
            eps, man = ge.gabung(td / 'shards', td / 'universe.parquet', td / 'idx.parquet', td / 'keluar', td / 'repo')
            self.assertTrue((td / 'keluar' / 'eps_a03.parquet').exists())
            m = json.loads((td / 'keluar' / 'manifest.json').read_text())
            self.assertEqual(m['fail'][0]['nama'], 'eps_a03.parquet')
            self.assertEqual((m['n_ticker_universe'], m['n_ticker_eps'], m['n_baris']), (3, 2, 12))
            self.assertTrue((td / 'repo' / 'LIPUTAN.md').exists() and (td / 'repo' / 'manifest_a03.json').exists())
            txt = (td / 'repo' / 'LIPUTAN.md').read_text()
            self.assertIn('| 2020 |', txt)
            self.assertIn('CCC', txt)
            baca = pd.read_parquet(td / 'keluar' / 'eps_a03.parquet')
            self.assertEqual(str(baca['tarikh_laporan'].dt.tz), NY)
            self.assertTrue((baca['tersedia'].dropna() >= baca['tarikh'].loc[baca['tersedia'].notna()]).all())


if __name__ == '__main__':
    unittest.main()

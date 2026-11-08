"""Ujian kaedah_siri.py (helaian kaedah dashboard v160)."""
import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import kaedah_siri as KS  # noqa: E402
import kad_skor  # noqa: E402


def posisi(rows):
    P = pd.DataFrame(rows, columns=['saham', 'tarikh_isyarat', 'tarikh_beli', 'tarikh_keluar', 'sebab_keluar',
                                    'harga_beli', 'harga_keluar', 'henti', 'hari', 'pul'])
    P['terbuka'] = P.tarikh_keluar == ''
    return P


class TestKategori(unittest.TestCase):
    def setUp(self):
        self.P = posisi([
            ['A', '2026-11-04', '2026-11-05', '2026-11-05', 'henti', 10, 9.8, 9.8, 1, -2.2],
            ['B', '2026-11-03', '2026-11-04', '2026-11-06', 'henti', 10, 9.5, 9.5, 3, -5.2],
            ['C', '2026-11-03', '2026-11-04', '2026-11-06', 'isyarat keluar', 10, 10.5, 9, 3, 4.8],
            ['D', '2026-11-03', '2026-11-04', '2026-11-06', 'sasaran', 10, 11, 9, 3, 9.8],
            ['E', '2026-11-03', '2026-11-04', '2026-11-06', 'masa', 10, 10, 9, 3, -0.2],
            ['F', '2026-11-03', '2026-11-04', '2026-11-06', 'delist', 10, 7, 9, 3, -30.2],
            ['G', '2026-11-03', '2026-11-04', '', '', 10, None, 9, None, 12.0],
        ])

    def test_kategori(self):
        self.assertEqual(list(KS.kategori(self.P)), ['henti0', 'henti', 'isyarat', 'sasaran', 'masa', 'lain', 'terbuka'])

    def test_henti_hari0_sama_dengan_g4(self):
        """Bar 'henti hari-0' dan G4 kad skor mesti dikira dengan definisi yang sama."""
        k = KS.kategori(self.P)
        self.assertEqual(int((k == 'henti0').sum()), kad_skor.statistik(self.P)['hari0'])

    def test_kat_jumlah_n(self):
        r = KS.ringkas('M99', self.P, {}, None)
        self.assertEqual(sum(r['kat']), r['n'])
        self.assertEqual(sum(r['h']), r['n'])
        self.assertEqual(r['ex'], [])  # tiada bar harga -> tiada contoh, bukan ralat


class TestMa(unittest.TestCase):
    def test_keluar_dahulu(self):
        k = dict(masuk='MA20 silang naik', keluar='Tutup di bawah SMA50 -> jual buka esok.')
        self.assertEqual(KS.ma_kaedah(k), ('SMA', 50))

    def test_ema_dan_huruf_kecil(self):
        self.assertEqual(KS.ma_kaedah(dict(masuk='tutup > ema21')), ('EMA', 21))
        self.assertEqual(KS.ma_kaedah(dict(masuk='ma10 silang naik ma20')), ('SMA', 10))

    def test_tiada(self):
        self.assertIsNone(KS.ma_kaedah(dict(masuk='rsi14 < 30', keluar='maks 10 hari')))
        self.assertIsNone(KS.ma_kaedah(None))


class TestTaburan(unittest.TestCase):
    def test_hujung_dipotong(self):
        h = KS.taburan([-50, -20, 0, 29.9, 30, 80])
        self.assertEqual(len(h), len(KS.BALDI) - 1)
        self.assertEqual(sum(h), 6)
        self.assertEqual(h[0], 2)
        self.assertEqual(h[-1], 3)


class TestTetingkap(unittest.TestCase):
    def bars(self, n):
        d = pd.bdate_range('2026-01-01', periods=n).strftime('%Y%m%d')
        c = np.linspace(10, 20, n)
        return pd.DataFrame(dict(date=d, open=c, high=c + 1, low=c - 1, close=c, ma=c))

    def test_pendek_tanpa_himpun(self):
        h = self.bars(60)
        bar, ib, ik, ii = KS.tetingkap(h, 30, 35, 29)
        self.assertEqual(len(bar), (35 + KS.PASCA + 1) - (29 - KS.PRA))  # bermula PRA bar sebelum isyarat
        self.assertEqual(bar[ib][0], int(h.date.iloc[30][4:]))
        self.assertEqual(bar[ik][0], int(h.date.iloc[35][4:]))
        self.assertEqual(ii, ib - 1)

    def test_panjang_dihimpun(self):
        h = self.bars(300)
        bar, ib, ik, ii = KS.tetingkap(h, 20, 200, 19)
        self.assertLessEqual(len(bar), KS.MAKS_BAR)
        self.assertTrue(0 <= ii <= ib < ik < len(bar))
        lo = min(b[3] for b in bar)
        self.assertAlmostEqual(lo, h.low.iloc[20 - KS.PRA if ii is None else 19 - KS.PRA], places=2)


if __name__ == '__main__':
    unittest.main()

"""Ujian unit bagi standard/konteks_isyarat.py (konteks isyarat dibekukan, 7 Nov 2026).

Sifat yang dikunci: (1) TAMBAH-SAHAJA — larian kedua tidak menulis semula atau menggandakan baris; (2) ciri dikira hanya
daripada bar sehingga hari isyarat (tiada pandang-hadapan); (3) rejim sama dengan gate G1 (QQQ > SMA50 DAN SMA10 > SMA20);
(4) fail di luar lejar/ supaya bina semula Lejar tidak memadamnya.
"""
import gzip
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import konteks_isyarat as KI  # noqa: E402


def stor(d, n=260, naik_mulai=None):
    """Stor tiruan: AAA naik 1% sehari, BBB rata; QQQ/SPY menaik kemudian (pilihan) jatuh."""
    tarikh = pd.bdate_range('2025-10-01', periods=n).strftime('%Y%m%d')
    rows = []
    for i, t in enumerate(tarikh):
        a = 100 * 1.01 ** i
        rows.append(('AAA', t, a, a * 1.01, a * 0.99, a, 1e6))
        rows.append(('BBB', t, 50.0, 50.5, 49.5, 50.0, 1e6))
    pd.DataFrame(rows, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']).to_csv(
        os.path.join(d, 'harga_A.csv'), index=False)
    pd.DataFrame(columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']).to_csv(
        os.path.join(d, 'harga_B.csv'), index=False)
    ix = []
    for i, t in enumerate(tarikh):
        q = 300 + i if (naik_mulai is None or i < naik_mulai) else 300 + naik_mulai - 3 * (i - naik_mulai)
        ix.append(('QQQ', t, q, q, q, q, 1))
        ix.append(('SPY', t, q, q, q, q, 1))
    pd.DataFrame(ix, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']).to_csv(
        os.path.join(d, 'harga_idx.csv'), index=False)
    return list(tarikh)


class TestKonteks(unittest.TestCase):

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        r = self.d.name
        self.stor, self.lejar, self.kon, self.pem = (os.path.join(r, x) for x in ('stor', 'lejar', 'kon', 'pem'))
        for x in (self.stor, os.path.join(self.lejar, 'isyarat'), self.pem):
            os.makedirs(x)
        self.sesi = stor(self.stor, naik_mulai=240)
        for s in self.sesi[-3:]:
            with gzip.open(os.path.join(self.lejar, 'isyarat', f'{s}.csv.gz'), 'wt') as f:
                f.write('sesi,kaedah,saham\n' + f'{s},M01,AAA\n{s},M02,AAA\n{s},M01,BBB\n')
        pd.DataFrame(dict(ticker=['AAA'], d0=[pd.Timestamp(KI._ymd(self.sesi[-1])) + pd.Timedelta(days=10)])).assign(
            d0=lambda x: x.d0.dt.strftime('%Y-%m-%d')).to_csv(os.path.join(self.pem, 'tarikh_pendapatan.csv'), index=False)
        self.asal = (KI.RS, KI.TV, KI.EARN)
        KI.RS, KI.TV, KI.EARN = os.path.join(r, 'tiada_rs.csv'), os.path.join(r, 'tiada_tv.csv'), self.pem

    def tearDown(self):
        KI.RS, KI.TV, KI.EARN = self.asal
        self.d.cleanup()

    def jalan(self, sesi):
        return KI.kira(sesi, lejar=self.lejar, stor=self.stor, konteks=self.kon)

    def baca(self):
        import glob
        return pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(self.kon, 'saham_*.csv.gz'))])

    def test_tambah_sahaja_idempoten(self):
        s = KI.sesi_isyarat(self.lejar)
        self.assertEqual(self.jalan(s), (3, 6))
        n1 = len(self.baca())
        # larian kedua: semua sesi sudah ada -> tiada baris baharu
        baru = [x for x in s if x not in KI.sudah_ada(self.kon)]
        self.assertEqual(baru, [])
        self.assertEqual(self.jalan(baru), (0, 0))
        # memaksa sesi sedia ada TIDAK menggandakan baris
        self.jalan(s[-1:])
        self.assertEqual(len(self.baca()), n1)

    def test_ciri_dan_n_kaedah(self):
        self.jalan(KI.sesi_isyarat(self.lejar))
        B = self.baca()
        a = B[(B.saham == 'AAA') & (B.sesi == KI._ymd(self.sesi[-1]))].iloc[0]
        self.assertEqual(a.n_kaedah, 2)
        self.assertTrue(bool(a.templat))                     # naik berterusan: tutup > SMA50 > SMA150 > SMA200
        self.assertAlmostEqual(a.jarak52, -0.99, delta=0.05)   # tutup ~1% di bawah tinggi intrahari hari itu
        self.assertAlmostEqual(a.roc63, (1.01 ** 63 - 1) * 100, delta=0.1)
        self.assertEqual(a.hari_ke_earnings, 10)
        self.assertTrue(bool(a.langsung))                    # sesi terakhir stor = dikira pada malamnya

    def test_tiada_pandang_hadapan(self):
        """Ciri sesi lama tidak berubah apabila bar baharu ditambah ke stor."""
        X1 = KI.ciri_harga(self.stor)
        H = pd.read_csv(os.path.join(self.stor, 'harga_A.csv'))
        tambahan = H[H.date == H.date.max()].assign(date=99991231, close=1.0, high=1.0, low=1.0, open=1.0)
        pd.concat([H, tambahan]).to_csv(os.path.join(self.stor, 'harga_A.csv'), index=False)
        X2 = KI.ciri_harga(self.stor)
        k = self.sesi[-1]
        a = X1[X1.date == k].set_index('ticker')[['atr_pct', 'jarak52', 'roc63']]
        b = X2[X2.date == k].set_index('ticker')[['atr_pct', 'jarak52', 'roc63']]
        pd.testing.assert_frame_equal(a, b)

    def test_rejim_sama_dengan_g1(self):
        P = KI.pasaran(self.stor)
        self.assertTrue(P[self.sesi[239]]['qqq_on'])         # menaik: tutup > SMA50 dan SMA10 > SMA20
        self.assertFalse(P[self.sesi[-1]]['qqq_on'])         # jatuh 20 sesi: SMA10 < SMA20
        self.assertIsNone(P[self.sesi[10]]['qqq_on'])        # SMA50 belum wujud: tidak diketahui

    def test_folder_di_luar_lejar(self):
        self.assertFalse(os.path.abspath(KI.KONTEKS).startswith(os.path.abspath(KI.LEJAR) + os.sep))


if __name__ == '__main__':
    unittest.main()

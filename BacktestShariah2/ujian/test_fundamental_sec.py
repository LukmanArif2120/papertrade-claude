# Ujian standard/fundamental_sec.py (27 Okt 2026): penghurai companyfacts (suku, Q4 terbitan, nilai pertama difail,
# keutamaan tag), penghurai 8-K Item 2.02 dan pengiraan SUE / pecutan hasil (tanpa rangkaian).
import os, sys, unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import fundamental_sec as F  # noqa: E402


def _x(mula, akhir, val, filed, form='10-Q', accn='a'):
    return dict(start=mula, end=akhir, val=val, filed=filed, form=form, accn=accn, fy=2024)


FAKTA = {'facts': {'us-gaap': {
    'EarningsPerShareDiluted': {'units': {'USD/shares': [
        _x('2024-01-01', '2024-03-31', 1.0, '2024-05-01', accn='q1'),
        _x('2024-01-01', '2024-03-31', 0.9, '2025-05-01', accn='q1-2025'),     # pernyataan semula: diabaikan
        _x('2024-01-01', '2024-06-30', 2.1, '2024-08-01', accn='q2'),          # YTD 6 bulan: bukan suku
        _x('2024-04-01', '2024-06-30', 1.1, '2024-08-01', accn='q2'),
        _x('2024-07-01', '2024-09-30', 1.2, '2024-11-01', accn='q3'),
        _x('2024-01-01', '2024-12-31', 4.5, '2025-02-15', form='10-K', accn='k'),
    ]}},
    'EarningsPerShareBasic': {'units': {'USD/shares': [
        _x('2024-01-01', '2024-03-31', 1.05, '2024-05-01', accn='q1'),         # tag rendah: diabaikan
    ]}},
}}}

SUB = {'filings': {'recent': {
    'form': ['10-Q', '8-K', '8-K', '4', '8-K/A'],
    'items': ['', '2.02,9.01', '5.02', '', '2.02'],
    'filingDate': ['2024-11-01', '2024-10-24', '2024-09-01', '2024-08-20', '2024-07-25'],
    'acceptanceDateTime': ['2024-11-01T16:05:00.000Z', '2024-10-24T20:01:00.000Z', '', '', '2024-07-25T20:00:00.000Z'],
    'accessionNumber': ['A1', 'A2', 'A3', 'A4', 'A5'],
}}}


class TestFakta(unittest.TestCase):
    def test_suku_dan_q4_terbitan(self):
        q = F.suku(F.hurai_fakta(FAKTA, F.TAG_EPS, 'USD/shares'))
        self.assertEqual(list(q.akhir), ['2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31'])
        self.assertAlmostEqual(q.nilai.iloc[0], 1.0)                 # nilai pertama difail, tag cair didahulukan
        self.assertEqual(q.tarikh_fail.iloc[0], '2024-05-01')
        self.assertAlmostEqual(q.nilai.iloc[3], 4.5 - 3.3)          # Q4 = tahunan − 3 suku
        self.assertEqual(int(q.terbitan.iloc[3]), 1)
        self.assertEqual(q.tarikh_fail.iloc[3], '2025-02-15')
        self.assertEqual(int(q.terbitan.iloc[:3].sum()), 0)

    def test_q4_dilapor_terus_tidak_diterbitkan(self):
        f = {'facts': {'us-gaap': {'Revenues': {'units': {'USD': [
            _x('2024-01-01', '2024-03-31', 10, '2024-05-01'), _x('2024-04-01', '2024-06-30', 11, '2024-08-01'),
            _x('2024-07-01', '2024-09-30', 12, '2024-11-01'), _x('2024-10-01', '2024-12-31', 14, '2025-02-15', '10-K'),
            _x('2024-01-01', '2024-12-31', 47, '2025-02-15', '10-K')]}}}}}
        q = F.suku(F.hurai_fakta(f, F.TAG_HASIL, 'USD'))
        self.assertEqual(len(q), 4)
        self.assertEqual(q.nilai.iloc[3], 14)
        self.assertEqual(int(q.terbitan.sum()), 0)

    def test_kosong(self):
        self.assertTrue(F.suku(F.hurai_fakta({}, F.TAG_EPS, 'USD/shares')).empty)


class Test8K(unittest.TestCase):
    def test_item_202_sahaja(self):
        k = F.hurai_8k(SUB)
        self.assertEqual(list(k.akses), ['A2', 'A5'])
        self.assertEqual(k.tarikh_fail.iloc[0], '2024-10-24')

    def test_fail_lama_tanpa_blok_recent(self):
        k = F.hurai_8k(SUB['filings']['recent'])
        self.assertEqual(len(k), 2)

    def test_akses_lapor_terkini(self):
        self.assertEqual(F.akses_lapor_terkini(SUB), 'A1')


class TestSUE(unittest.TestCase):
    def _suku(self, nilai, mula='2021-03-31'):
        akhir = pd.date_range(mula, periods=len(nilai), freq='QE')
        return pd.DataFrame(dict(akhir=akhir.strftime('%Y-%m-%d'), nilai=nilai,
                                 tarikh_fail=(akhir + pd.Timedelta(days=40)).strftime('%Y-%m-%d')))

    def test_formula_sue(self):
        eps = [1.0, 1.0, 1.0, 1.0, 1.1, 1.2, 1.0, 1.3, 1.2, 1.4, 1.1, 1.5, 2.0]
        k8 = pd.DataFrame(dict(tarikh_fail=['2024-01-25']))          # dalam (akhir Q4 2023, fail] -> tarikh_umum
        s = F.kira_sue(self._suku(eps), pd.DataFrame(columns=['akhir', 'nilai']), k8)
        d = [eps[i] - eps[i - 4] for i in range(4, len(eps))]       # perbezaan bermusim
        jangka = d[-1] / np.std(d[:-1][-8:], ddof=1)
        self.assertAlmostEqual(s.sue.iloc[-1], jangka, places=6)
        self.assertTrue(np.isnan(s.sue.iloc[6]))                    # < 4 perbezaan sejarah
        r = s[s.akhir == '2023-12-31'].iloc[0]
        self.assertEqual((r.tarikh_umum, r.sumber_tarikh), ('2024-01-25', '8k'))
        self.assertEqual(s.sumber_tarikh.iloc[0], 'fail')

    def test_banding_pemfailan_sama_merentasi_pecahan_saham(self):
        # 2023 difail sebelum pecahan 4:1 (EPS 4.0); 10-Q 2024 mencetak perbandingan 2023 dilaras (1.0)
        f = {'facts': {'us-gaap': {'EarningsPerShareDiluted': {'units': {'USD/shares': [
            _x('2023-01-01', '2023-03-31', 4.0, '2023-05-01', accn='q1-23'),
            _x('2024-01-01', '2024-03-31', 1.1, '2024-05-01', accn='q1-24'),
            _x('2023-01-01', '2023-03-31', 1.0, '2024-05-01', accn='q1-24')]}}}}}
        mentah = F.hurai_fakta(f, F.TAG_EPS, 'USD/shares')
        q = F.suku(mentah)
        self.assertEqual(list(q.nilai), [4.0, 1.1])                  # siri kekal nilai pertama difail
        b = F.nilai_banding(mentah, q)
        self.assertEqual(b.to_dict(), {'2024-03-31': 1.0})
        s = F.kira_sue(q, pd.DataFrame(columns=['akhir', 'nilai']), pd.DataFrame(columns=['tarikh_fail']), b)
        self.assertAlmostEqual(s.eps_lalu.iloc[1], 1.0)              # bukan 4.0 (sebelum pecahan)

    def test_penyebut_minimum(self):
        eps = [1.0] * 12 + [1.05]                                    # perbezaan sejarah semua 0
        s = F.kira_sue(self._suku(eps), pd.DataFrame(columns=['akhir', 'nilai']), pd.DataFrame(columns=['tarikh_fail']))
        self.assertAlmostEqual(s.sue.iloc[-1], 0.05 / F.SUE_MIN_SP)

    def test_penapis_kewarasan_eps(self):
        eps = [0.4, 0.5, 0.3, 0.4, 0.5, 0.6, 0.4, 0.5, 0.6, 0.7, -40000.0, 0.6, 0.7]   # ralat unit XBRL
        s = F.kira_sue(self._suku(eps), pd.DataFrame(columns=['akhir', 'nilai']), pd.DataFrame(columns=['tarikh_fail']))
        self.assertTrue(np.isnan(s.sue.iloc[10]))
        self.assertTrue(np.isfinite(s.sue.iloc[12]))
        self.assertLess(abs(s.sue.iloc[12]), 50)

    def test_tumbuh_dan_pecutan_hasil(self):
        h = self._suku([100, 100, 100, 100, 110, 120, 100, 100])
        s = F.kira_sue(self._suku([1.0] * 8), h, pd.DataFrame(columns=['tarikh_fail']))
        self.assertAlmostEqual(s.tumbuh_hasil.iloc[4], 0.10)
        self.assertAlmostEqual(s.tumbuh_hasil.iloc[5], 0.20)
        self.assertAlmostEqual(s.pecutan_hasil.iloc[5], 0.10)
        self.assertTrue(np.isnan(s.tumbuh_hasil.iloc[0]))


class TestUniverse(unittest.TestCase):
    def test_univ_sec_kesatuan_tidak_susut(self):
        # Universe SEC = data/univ_sec.txt U tawaran_edgar.universe(); liputan lama tidak boleh hilang.
        import tawaran_edgar as TE
        u, lama = F.univ_sec(), set(TE.universe())
        self.assertTrue(lama <= u)
        self.assertGreaterEqual(len(u), 3260)       # 3260 ticker A02

    def test_univ_sec_langkau_komen(self):
        with open(F.UNIV_SEC, encoding='utf-8') as f:
            baris = [x.strip() for x in f if x.strip()]
        self.assertTrue(baris[0].startswith('#'))   # kepala penerangan ada
        self.assertFalse(any(t.startswith('#') for t in F.univ_sec()))

    def test_putaran_semua_bila_maks_sifar(self):
        p = [(i, t) for i, t in enumerate('abcdef')]
        self.assertEqual(F.putaran(p, '', 0), (p, ''))
        self.assertEqual(F.putaran(p, 'c', 99), (p, ''))

    def test_putaran_sambung_selepas_kursor(self):
        p = [(i, t) for i, t in enumerate('abcdef')]
        pilih, kursor = F.putaran(p, 'b', 2)
        self.assertEqual([t for _, t in pilih], ['c', 'd'])
        self.assertEqual(kursor, 'd')

    def test_putaran_berputar_di_hujung(self):
        p = [(i, t) for i, t in enumerate('abcdef')]
        pilih, kursor = F.putaran(p, 'e', 3)
        self.assertEqual([t for _, t in pilih], ['f', 'a', 'b'])
        self.assertEqual(kursor, 'b')

    def test_putaran_meliputi_semua_selepas_cukup_larian(self):
        p = [(i, t) for i, t in enumerate('abcdefghij')]
        k, dilihat = '', set()
        for _ in range(4):                          # 4 x 3 >= 10
            pilih, k = F.putaran(p, k, 3)
            dilihat |= {t for _, t in pilih}
        self.assertEqual(dilihat, {t for _, t in p})


if __name__ == '__main__':
    unittest.main()

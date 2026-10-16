import csv, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import skrin_tv as st


class TestSkrinTv(unittest.TestCase):
    def test_semak_shariah_status(self):
        etf = {'AAPL': {'SPUS', 'SPTE'}, 'MSFT': {'SPUS'}}
        rows = {r['ticker']: r for r in st.semak_shariah({'AAPL', 'XOM', 'ZZZ'}, {'MSFT'}, etf, {'AAPL', 'MSFT', 'XOM'})}
        self.assertEqual(rows['AAPL']['status'], 'disahkan_etf')
        self.assertEqual(rows['AAPL']['etf'], 'SPTE+SPUS')
        self.assertEqual(rows['MSFT']['status'], 'disahkan_etf')
        self.assertEqual(rows['XOM']['status'], 'sp500_tiada_spus')   # ahli S&P 500, tiada dalam SPUS
        self.assertEqual(rows['ZZZ']['status'], 'tiada_maklumat')     # bukan S&P 500: tiada pendapat kedua
        self.assertEqual(rows['MSFT']['papertrade'], 1)
        self.assertEqual(rows['MSFT']['univ_moomoo'], 0)

    def test_ticker_papertrade_posisi_terbuka_sahaja(self):
        with tempfile.TemporaryDirectory() as d:
            def tulis(nama, lajur, baris):
                with open(os.path.join(d, nama), 'w', encoding='utf-8', newline='') as f:
                    w = csv.writer(f)
                    w.writerow(lajur)
                    w.writerows(baris)
            tulis('claude.csv', ['saham', 'keluar'], [['AAA', 'False'], ['BBB', 'True']])
            tulis('claude_7.csv', ['saham', 'keluar'], [['CCC', '']])
            tulis('watchlist.csv', ['Saham', 'Kaedah'], [['DDD', 'M02']])
            tulis('senarai_beli.csv', ['saham', 'kaedah'], [['EEE', 'M02']])
            tulis('sektor.csv', ['saham'], [['FFF']])
            self.assertEqual(st.baca_ticker_papertrade(d), {'AAA', 'CCC', 'DDD', 'EEE'})

    def test_ringkas_medan_kosong(self):
        tiada, sh = st.ringkas([{'close': 1, 'is_shariah_compliant': None}])
        self.assertIn('is_shariah_compliant', tiada)
        self.assertNotIn('close', tiada)
        self.assertEqual(sh, {'benar': 0, 'salah': 0, 'tiada': 1})


if __name__ == '__main__':
    unittest.main()

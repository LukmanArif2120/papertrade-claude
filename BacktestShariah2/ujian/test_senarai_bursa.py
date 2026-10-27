# Ujian standard/senarai_bursa.py (27 Okt 2026): penghurai SymDir Nasdaq Trader, pengelasan saham biasa, dan
# peristiwa harian asas/tambah/buang/tukar_nama (tanpa rangkaian).
import os, sys, unittest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import senarai_bursa as S  # noqa: E402

N = """Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
AAPL|Apple Inc. - Common Stock|Q|N|N|100|N|N
QQQ|Invesco QQQ Trust, Series 1|G|N|N|100|Y|N
ZXZZT|NASDAQ TEST STOCK|G|Y|N|100|N|N
ABCDW|ABC Acquisition Corp - Warrant|S|N|N|100|N|N
File Creation Time: 1027202600:00|||||||
"""
O = """ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol
BRK.B|Berkshire Hathaway Inc. Class B|N|BRK.B|N|100|N|BRK.B
XYZ$A|XYZ Corp Preferred Series A|N|XYZpA|N|100|N|XYZ-A
IBM|International Business Machines|N|IBM|N|100|N|IBM
File Creation Time: 1027202600:00|||||||
"""


class TestSenarai(unittest.TestCase):
    def test_hurai_dan_kelas(self):
        d, masa = S.senarai(N, O)
        self.assertEqual(list(d.simbol), ['AAPL', 'ABCDW', 'BRK.B', 'IBM', 'QQQ'])     # tanpa Test Issue dan '$'
        x = d.set_index('simbol')
        self.assertEqual(x.loc['AAPL', 'biasa'], 1)
        self.assertEqual((x.loc['QQQ', 'etf'], x.loc['QQQ', 'biasa']), (1, 0))
        self.assertEqual(x.loc['ABCDW', 'biasa'], 0)                                  # waran
        self.assertEqual(x.loc['BRK.B', 'bursa'], 'NYSE')
        self.assertEqual(masa, ['1027202600:00', '1027202600:00'])

    def test_peristiwa(self):
        d1, _ = S.senarai(N, O)
        sem, per = S.banding(pd.DataFrame(), d1, '2026-10-27')
        self.assertEqual(set(per.peristiwa), {'asas'})
        self.assertEqual(set(sem.pertama_dilihat), {'2026-10-27'})
        O2 = O.replace('IBM|International Business Machines', 'IBM|IBM Corporation').replace(
            'BRK.B|Berkshire Hathaway Inc. Class B|N|BRK.B|N|100|N|BRK.B\n', '')
        d2, _ = S.senarai(N + 'NEWC|New Co - Common Stock|Q|N|N|100|N|N\n', O2)
        sem2, per2 = S.banding(sem, d2, '2026-10-28')
        k = {(r.simbol, r.peristiwa) for r in per2.itertuples()}
        self.assertEqual(k, {('NEWC', 'tambah'), ('BRK.B', 'buang'), ('IBM', 'tukar_nama')})
        p = sem2.set_index('simbol').pertama_dilihat
        self.assertEqual((p['AAPL'], p['NEWC']), ('2026-10-27', '2026-10-28'))


if __name__ == '__main__':
    unittest.main()

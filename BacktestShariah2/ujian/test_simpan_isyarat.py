# Ujian rekod kekal semua isyarat imbasan (scanner.simpan_isyarat).
import os, sys, tempfile, unittest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import scanner


class UjiSimpanIsyarat(unittest.TestCase):
    def test_tulis_dan_baca(self):
        rows = [dict(tarikh_data='2026-10-16', kaedah='M96', saham='AAPL', rank=1.5, henti=200.0, sasaran=None,
                     tutup=230.1, sumber='431', dirancang=True),
                dict(tarikh_data='2026-10-16', kaedah='M119', saham='DXC', rank=None, henti=11.2, sasaran=None,
                     tutup=12.5, sumber='lain', dirancang=False)]
        with tempfile.TemporaryDirectory() as d:
            p = scanner.simpan_isyarat(rows, os.path.join(d, 'isyarat'), '2026-10-16', 'malam')
            self.assertTrue(p.endswith('2026-10-16_malam.csv.gz'))
            b = pd.read_csv(p)
            self.assertEqual(list(b.columns), ['tarikh_data', 'kaedah', 'saham', 'rank', 'henti', 'sasaran', 'tutup', 'sumber', 'dirancang'])
            self.assertEqual(len(b), 2); self.assertEqual(b.dirancang.tolist(), [True, False])
            self.assertTrue(pd.isna(b.loc[1, 'rank']))

    def test_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = scanner.simpan_isyarat([], d, '2026-10-16', 'tutup')
            self.assertEqual(len(pd.read_csv(p)), 0)


if __name__ == '__main__':
    unittest.main()

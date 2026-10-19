# Ujian kod/scanner.py: saham yang sudah keluar layak dibeli semula (belian ke-2, ke-3 ...)
import csv, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import scanner as S  # noqa: E402


class UjiBelianSemula(unittest.TestCase):
    def test_terbuka(self):
        self.assertTrue(S.terbuka({'saham': 'X'}))
        self.assertTrue(S.terbuka({'keluar': {'menunggu': True, 'harga': None}}))
        self.assertFalse(S.terbuka({'keluar': {'tarikh': '2026-10-12', 'harga': 26.27, 'sebab': 'henti'}}))

    def test_pegangan_c(self):
        with tempfile.TemporaryDirectory() as d:
            lajur = ['tarikh_beli', 'saham', 'kaedah', 'keluar', 'tidak_dibeli', 'tidak_sah']
            with open(os.path.join(d, 'claude.csv'), 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f); w.writerow(lajur)
                w.writerows([['2026-10-09', 'FSLY', 'M13', 'True', '', ''],      # kena henti: layak semula
                             ['2026-10-12', 'FSLY', 'M20', 'True', '', ''],
                             ['2026-10-16', 'FSLY', 'M20', 'False', '', ''],     # belian ke-2 masih terbuka
                             ['', 'AAA', 'M13', 'False', 'True', ''],            # tidak dibeli
                             ['2026-10-09', 'BBB', 'M13', 'False', '', 'True']])  # tidak sah
            with open(os.path.join(d, 'claude_7.csv'), 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f); w.writerow(lajur); w.writerow(['2026-10-15', 'FSLY', 'M81', 'False', '', ''])
            buka, bil = S.pegangan_c(d)
        self.assertEqual(buka, {('M20', 'FSLY'), ('M81', 'FSLY')})
        self.assertEqual((bil[('M13', 'FSLY')], bil[('M20', 'FSLY')], bil[('M13', 'AAA')]), (1, 2, 0))

    def test_dua_lorong(self):
        # sejak 19 Okt 2026: belian semula selepas lorong 1 (kaedah) keluar; lorong 2 yang masih terbuka tidak menyekat
        with tempfile.TemporaryDirectory() as d:
            lajur = ['tarikh_beli', 'saham', 'kaedah', 'keluar', 'tidak_dibeli', 'tidak_sah', 'tutup_semua']
            with open(os.path.join(d, 'claude.csv'), 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f); w.writerow(lajur)
                w.writerows([['2026-10-09', 'FSLY', 'M13', 'True', '', '', 'True'],    # semua lorong keluar: layak semula
                             ['2026-10-12', 'NCNO', 'M20', 'True', '', '', 'False'],   # lorong 1 keluar, lorong 2 belum: layak
                             ['2026-10-16', 'AAA', 'M20', 'False', '', '', '']])       # baharu, belum dinilai
            buka, _ = S.pegangan_c(d)
        self.assertEqual(buka, {('M20', 'AAA')})


if __name__ == '__main__':
    unittest.main()

# Ujian standard/keluar_tiga.py: lorong 2 (henti / pegang selagi untung) dan lorong 3 (+10% kemudian tutup < low semalam).
import csv, os, sys, tempfile, unittest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import keluar_tiga as K  # noqa: E402

IX = [f'2026-10-{d:02d}' for d in range(1, 21)]


def bar(c, o=None, h=None, l=None):
    c = np.array(c, float); o = c.copy() if o is None else np.array(o, float)
    h = np.maximum(o, c) if h is None else np.array(h, float); l = np.minimum(o, c) if l is None else np.array(l, float)
    return IX[:len(c)], o, h, l, c


class UjiLorong(unittest.TestCase):
    def test_henti_rendah(self):
        ix, o, h, l, c = bar([100, 101, 99, 97], l=[99, 100, 95, 96])
        L2, L3 = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 96.0)
        self.assertEqual((L2['keluar_henti'], L2['tarikh_keluar_henti'], L2['harga_keluar_henti']), ('True', ix[2], '96'))
        self.assertEqual((L3['keluar_10'], L3['capai_10']), ('True', 'False'))
        self.assertIn('sebelum +10%', L3['status_10'])

    def test_henti_buka_jurang_hari_kedua(self):
        ix, o, h, l, c = bar([100, 94], o=[100, 93])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertEqual((L2['harga_keluar_henti'], L2['untung_henti_pct']), ('93', '-7.00'))

    def test_tanpa_henti_pegang_selagi_untung(self):
        ix, o, h, l, c = bar([101, 103, 99.5, 98], o=[100, 102, 103, 97])
        L2, L3 = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, None)
        # tutup 99.5 < harga beli pada hari ke-3 -> jual buka hari ke-4
        self.assertEqual((L2['tarikh_keluar_henti'], L2['harga_keluar_henti']), (ix[3], '97'))
        self.assertEqual(L3['tarikh_keluar_10'], ix[3])

    def test_tanpa_henti_menunggu(self):
        ix, o, h, l, c = bar([101, 99])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, None)
        self.assertEqual(L2['keluar_henti'], 'False'); self.assertIn('menunggu', L2['status_henti'])

    def test_capai_10_kemudian_low_semalam(self):
        # tutup 110 (capai) -> 114 (low 111) -> 112 (>= low semalam 111? ya, pegang; low 110) -> 109 < 110 -> jual buka esok 108
        c = [104, 110, 114, 112, 109, 107]
        l = [102, 106, 111, 110, 108, 105]
        o = [100, 105, 111, 113, 111, 108]
        ix, o, h, l, c = bar(c, o=o, l=l)
        L2, L3 = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertEqual((L3['capai_10'], L3['tarikh_capai_10']), ('True', ix[1]))
        self.assertEqual((L3['tarikh_keluar_10'], L3['harga_keluar_10'], L3['untung_10_pct']), (ix[5], '108', '8.00'))
        self.assertEqual(L2['keluar_henti'], 'False')

    def test_capai_tanpa_keluar(self):
        ix, o, h, l, c = bar([105, 111, 113], l=[100, 104, 110])
        _, L3 = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertEqual((L3['capai_10'], L3['keluar_10']), ('True', 'False'))
        self.assertIn('tutup < 110.00', L3['status_10'])

    def test_harga_tidak_sepadan(self):
        ix, o, h, l, c = bar([50, 51])
        L2, sebab = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertIsNone(L2); self.assertIn('tidak sepadan', sebab)


class UjiBaris(unittest.TestCase):
    def test_beku_dan_tutup_semua(self):
        H = {'X': bar([100, 90], l=[99, 89])}
        r = dict(saham='X', kaedah='M01', tarikh_beli=IX[0], harga_beli='100', henti='95', keluar='True')
        K.kemas_baris(r, H, [])
        self.assertEqual((r['keluar_henti'], r['keluar_10'], r['tutup_semua']), ('True', 'True', 'True'))
        r['harga_keluar_henti'] = '94.5'          # lorong yang sudah keluar dibekukan
        K.kemas_baris(r, H, [])
        self.assertEqual(r['harga_keluar_henti'], '94.5')

    def test_tidak_dibeli_kosong(self):
        r = dict(saham='X', kaedah='M01', tarikh_beli='', tidak_dibeli='True')
        K.kemas_baris(r, {}, [])
        self.assertEqual(r['tutup_semua'], '')

    def test_fail(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'claude.csv'), 'w', newline='') as f:
                w = csv.writer(f); w.writerow(['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'henti', 'keluar'])
                w.writerow([IX[0], 'X', 'M01', '100', '95', 'False'])
            H = {'X': bar([100, 112, 113], l=[99, 105, 111])}
            K.muat_harga = lambda stor: H
            K.main(['--folder', d, '--stor', d])
            r = list(csv.DictReader(open(os.path.join(d, 'claude.csv'))))[0]
        self.assertEqual((r['capai_10'], r['keluar_10'], r['tutup_semua']), ('True', 'False', 'False'))


if __name__ == '__main__':
    unittest.main()

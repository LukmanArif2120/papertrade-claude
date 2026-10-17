# Ujian standard/keluar_lorong.py: lorong 2 (pegang selagi naik: 2 tutup turun berturut atau henti).
import csv, os, sys, tempfile, unittest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import keluar_lorong as K  # noqa: E402

IX = [f'2026-10-{d:02d}' for d in range(1, 21)]


def bar(c, o=None, h=None, l=None):
    c = np.array(c, float); o = c.copy() if o is None else np.array(o, float)
    h = np.maximum(o, c) if h is None else np.array(h, float); l = np.minimum(o, c) if l is None else np.array(l, float)
    return IX[:len(c)], o, h, l, c


class UjiLorong(unittest.TestCase):
    def test_henti_rendah(self):
        ix, o, h, l, c = bar([100, 101, 99, 97], l=[99, 100, 95, 96])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 96.0)
        self.assertEqual((L2['keluar_henti'], L2['tarikh_keluar_henti'], L2['harga_keluar_henti']), ('True', ix[2], '96'))

    def test_henti_buka_jurang_hari_kedua(self):
        ix, o, h, l, c = bar([100, 94], o=[100, 93])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertEqual((L2['harga_keluar_henti'], L2['untung_henti_pct']), ('93', '-7.00'))

    def test_lorong2_dua_tutup_turun(self):
        # turun (1), naik (kosong), turun (1), turun (2) -> jual buka bar berikutnya
        ix, o, h, l, c = bar([100, 102, 101, 103, 102, 100, 99], o=[100, 101, 102, 101, 103, 101, 98.5])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, None)
        self.assertEqual((L2['tarikh_keluar_henti'], L2['harga_keluar_henti'], L2['untung_henti_pct']), (ix[6], '98.5', '-1.50'))
        self.assertIn('2 tutup turun berturut', L2['status_henti'])

    def test_lorong2_satu_turun_pegang(self):
        ix, o, h, l, c = bar([100, 103, 102, 105])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertEqual(L2['keluar_henti'], 'False')
        self.assertIn('turun berturut 0/2', L2['status_henti']); self.assertIn('henti 95.00', L2['status_henti'])

    def test_lorong2_menunggu(self):
        ix, o, h, l, c = bar([100, 99, 98])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, None)
        self.assertEqual(L2['keluar_henti'], 'False'); self.assertIn('menunggu', L2['status_henti'])

    def test_lorong2_lima_hari_naik_kemudian_jatuh(self):
        c = [104, 110, 114, 112, 109, 107]
        o = [100, 105, 111, 113, 111, 108]
        ix, o, h, l, c = bar(c, o=o)
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        # 112 < 114 (1), 109 < 112 (2) -> jual buka bar ke-6 = 108
        self.assertEqual((L2['tarikh_keluar_henti'], L2['harga_keluar_henti'], L2['untung_henti_pct']), (ix[5], '108', '8.00'))

    def test_harga_tidak_sepadan(self):
        ix, o, h, l, c = bar([50, 51])
        L2, sebab = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0, 95.0)
        self.assertIsNone(L2); self.assertIn('tidak sepadan', sebab)


class UjiBaris(unittest.TestCase):
    def test_beku_dan_tutup_semua(self):
        H = {'X': bar([100, 90], l=[99, 89])}
        r = dict(saham='X', kaedah='M01', tarikh_beli=IX[0], harga_beli='100', henti='95', keluar='True')
        K.kemas_baris(r, H, [])
        self.assertEqual((r['keluar_henti'], r['tutup_semua']), ('True', 'True'))
        r['harga_keluar_henti'] = '94.5'          # lorong yang sudah keluar dibekukan
        K.kemas_baris(r, H, [])
        self.assertEqual(r['harga_keluar_henti'], '94.5')

    def test_semula_kira_lorong_yang_sudah_keluar(self):
        H = {'X': bar([100, 103, 105], l=[99, 101, 104])}
        r = dict(saham='X', kaedah='M01', tarikh_beli=IX[0], harga_beli='100', henti='95', keluar='False',
                 keluar_henti='True', tarikh_keluar_henti=IX[1], harga_keluar_henti='95', untung_henti_pct='-5.00')
        K.kemas_baris(r, H, [])
        self.assertEqual(r['harga_keluar_henti'], '95')            # beku
        K.kemas_baris(r, H, [], semula=('henti',))
        self.assertEqual((r['keluar_henti'], r['harga_keluar_henti']), ('False', ''))

    def test_tidak_dibeli_kosong(self):
        r = dict(saham='X', kaedah='M01', tarikh_beli='', tidak_dibeli='True')
        K.kemas_baris(r, {}, [])
        self.assertEqual(r['tutup_semua'], '')

    def test_fail(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'claude.csv'), 'w', newline='') as f:
                w = csv.writer(f); w.writerow(['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'henti', 'keluar', 'capai_10', 'keluar_10'])
                w.writerow([IX[0], 'X', 'M01', '100', '95', 'False', 'True', 'False'])
            H = {'X': bar([100, 112, 113], l=[99, 105, 111])}
            K.muat_harga = lambda stor: H
            K.main(['--folder', d, '--stor', d])
            r = list(csv.DictReader(open(os.path.join(d, 'claude.csv'))))[0]
        self.assertEqual((r['keluar_henti'], r['tutup_semua']), ('False', 'False'))
        self.assertNotIn('capai_10', r); self.assertNotIn('keluar_10', r)   # lajur lorong 10% dibuang


if __name__ == '__main__':
    unittest.main()

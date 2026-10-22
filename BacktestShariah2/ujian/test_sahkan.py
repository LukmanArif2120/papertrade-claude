# Ujian standard/sahkan.py atas folder papertrade sementara.
import csv, io, os, sys, tempfile, unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import sahkan  # noqa: E402

ASAS = dict(tarikh_beli='2026-10-13', saham='AAA', kaedah='M01', id_kaedah='M01', sektor='Technology',
            industri='Software', harga_beli='100', unit='1', harga_terkini='105', untung_pct='5.0', hari='1',
            isyarat_keluar='Pegang', keluar='False', tarikh_keluar='', harga_keluar='', untung_akhir_pct='',
            sumber='harian_c')


def tulis(folder, nama, rows, lajur=None):
    lajur = lajur or list(rows[0].keys())
    with open(os.path.join(folder, nama), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=lajur)
        w.writeheader()
        w.writerows(rows)


class UjiSahkan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        tulis(self.d, 'moomoo.csv', [dict(ASAS, saham='MMM', unit='19')])
        tulis(self.d, 'claude.csv', [dict(ASAS)])
        tulis(self.d, 'watchlist.csv', [{'Saham': 'BBB', 'Kaedah': 'M02', 'Sektor': 'Energy',
                                        'Industri': 'Oil', '% hampir': '95'}])

    def tearDown(self):
        self.tmp.cleanup()

    def jalan(self, *arg):
        out = io.StringIO()
        with redirect_stdout(out):
            kod = sahkan.main(['--folder', self.d, *arg])
        return kod, out.getvalue()

    def test_dua_lorong(self):
        dua = dict(keluar_henti='True', tarikh_keluar_henti='2026-10-14', harga_keluar_henti='95', untung_henti_pct='-5.00',
                   status_henti='Keluar: kena henti', tutup_semua='False')
        tulis(self.d, 'claude.csv', [dict(ASAS, **dua)])
        self.assertEqual(self.jalan()[0], 0)
        tulis(self.d, 'claude.csv', [dict(ASAS, **dict(dua, tutup_semua='True'))])   # lorong 1 belum keluar
        kod, out = self.jalan()
        self.assertEqual(kod, 1); self.assertIn('tutup_semua', out)
        tulis(self.d, 'claude.csv', [dict(ASAS, **dict(dua, untung_henti_pct='-4'))])
        kod, out = self.jalan()
        self.assertEqual(kod, 1); self.assertIn('untung_henti_pct', out)

    def test_data_bersih_lulus(self):
        kod, out = self.jalan()
        self.assertEqual(kod, 0, out)

    def test_untung_tidak_sepadan(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, untung_pct='7.0')])
        kod, out = self.jalan()
        self.assertEqual(kod, 1)
        self.assertIn('untung_pct', out)

    def test_pemangkin_url(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, pemangkin_url='[{"tajuk": "X", "url": "https://a/1"}]')])
        self.assertEqual(self.jalan()[0], 0)
        tulis(self.d, 'claude.csv', [dict(ASAS, pemangkin_url='http://a/1')])
        kod, out = self.jalan()
        self.assertNotEqual(kod, 0)
        self.assertIn('pemangkin_url', out)

    def test_sektor_kosong(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, sektor='-')])
        self.assertIn('sektor/industri kosong', self.jalan()[1])

    def test_tidak_sah_tanpa_sebab(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, tidak_sah='True')])
        self.assertIn('tidak_sah tanpa sebab_tidak_sah', self.jalan()[1])

    def test_bertindih_merentas_fail_claude(self):
        tulis(self.d, 'claude_2.csv', [dict(ASAS)])
        kod, out = self.jalan()
        self.assertEqual(kod, 1)
        self.assertIn('bertindih', out)

    def test_moomoo_dan_claude_kunci_berasingan(self):
        tulis(self.d, 'moomoo.csv', [dict(ASAS)])
        self.assertEqual(self.jalan()[0], 0)

    def test_claude_mesti_satu_unit(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, unit='2')])
        self.assertIn('1 unit', self.jalan()[1])

    def test_keluar_tanpa_harga_keluar(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, keluar='True')])
        self.assertIn('keluar=True tetapi', self.jalan()[1])

    def test_untung_akhir(self):
        tulis(self.d, 'claude.csv', [dict(ASAS, keluar='True', tarikh_keluar='2026-10-14', harga_keluar='110',
                                          untung_akhir_pct='10.0')])
        self.assertEqual(self.jalan()[0], 0)
        tulis(self.d, 'claude.csv', [dict(ASAS, keluar='True', tarikh_keluar='2026-10-14', harga_keluar='110',
                                          untung_akhir_pct='12.0')])
        self.assertIn('untung_akhir_pct', self.jalan()[1])

    def test_tidak_dibeli(self):
        ok = dict(ASAS, harga_beli='', harga_terkini='', untung_pct='', hari='', isyarat_keluar='TIDAK DIBELI',
                  tidak_dibeli='True', tidak_sah='True', sebab_tidak_sah='langkau kaedah')
        tulis(self.d, 'claude.csv', [ok])
        self.assertEqual(self.jalan()[0], 0)
        tulis(self.d, 'claude.csv', [dict(ok, harga_beli='100')])
        self.assertIn('tidak_dibeli tetapi harga_beli', self.jalan()[1])

    def test_watchlist_terkeluar_signal(self):
        tulis(self.d, 'watchlist.csv', [{'Saham': 'BBB', 'Kaedah': 'M02', 'Sektor': 'Energy',
                                        'Industri': 'Oil', '% hampir': '85'}])
        self.assertIn('di luar 90', self.jalan()[1])

    def test_betulkan_susun_lajur_tanpa_ubah_nilai(self):
        lajur = list(reversed(list(ASAS.keys()))) + ['lajur_lain']
        tulis(self.d, 'claude.csv', [dict(ASAS, lajur_lain='x')], lajur)
        kod, _ = self.jalan('--betulkan')
        self.assertEqual(kod, 0)
        with open(os.path.join(self.d, 'claude.csv'), newline='') as f:
            r = csv.DictReader(f)
            self.assertEqual(r.fieldnames[:len(sahkan.POSISI)], sahkan.POSISI)
            self.assertEqual(r.fieldnames[-1], 'lajur_lain')
            row = next(r)
        self.assertEqual(row['harga_beli'], '100')
        self.assertEqual(row['lajur_lain'], 'x')


if __name__ == '__main__':
    unittest.main()

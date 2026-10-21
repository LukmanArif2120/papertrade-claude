# Ujian kod/tidak_layak.py: saham tidak cair ditapis, gabungan dengan ambil alih, dan posisi C saham delist ditutup.
import csv, os, sys, tempfile, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import tidak_layak as TL  # noqa: E402
from test_ambil_alih import saham, IX, TestPosisi  # noqa: E402


class TestCair(unittest.TestCase):
    def test_saham_biasa_lulus(self):
        self.assertIsNone(TL.tidak_cair(saham(umum=None)))

    def test_bar_tanpa_julat(self):
        g = saham(umum=None); i = g.index[-5:-2]
        g.loc[i, 'high'] = g.close[i]; g.loc[i, 'low'] = g.close[i]
        self.assertIn('3 tanpa julat', TL.tidak_cair(g))

    def test_tanpa_volum_dan_nilai_rendah(self):
        g = saham(umum=None); g.loc[g.index[-3:-1], 'volume'] = 0
        self.assertIn('2 tanpa volum', TL.tidak_cair(g))
        g = saham(umum=None); g['volume'] = 1000.0   # ~USD50 ribu sehari
        self.assertIn('median nilai', TL.tidak_cair(g))

    def test_tapis_gabung_tanpa_pandang_depan(self):
        g = saham(umum=None); g.loc[g.index[-3:], 'volume'] = 0
        fr = {'X': saham(), 'Y': g, 'Z': saham(umum=None)}
        x = TL.tapis(fr, None, senarai=[])
        self.assertEqual({t: v['sebab'] for t, v in x.items()}, {'X': 'ambil alih', 'Y': 'tidak cair'})
        self.assertEqual(set(TL.tapis(fr, IX[100], senarai=[])), set())


class TestDelist(unittest.TestCase):
    def test_posisi_delist_ditutup(self):
        g = saham(umum=None, n=180)
        sesi = list(IX[:186])          # 6 sesi selepas bar terakhir (indeks 179)
        rows = [dict(tarikh_beli=str(IX[170].date()), saham='Y', kaedah='M01', harga_beli='50', keluar='False', keluar_henti='False'),
                dict(tarikh_beli=str(IX[160].date()), saham='Y', kaedah='M02', harga_beli='50', keluar='True', tarikh_keluar=str(IX[165].date()),
                     harga_keluar='51', untung_akhir_pct='2.00', keluar_henti='False')]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_3.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, TestPosisi.LAJUR); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in TestPosisi.LAJUR})
            self.assertEqual(TL.tutup_delist(d, {'Y': g}, sesi[:183]), [])     # 3 sesi: belum
            x = TL.tutup_delist(d, {'Y': g}, sesi)
            self.assertEqual(len(x), 2)
            with open(p) as f:
                out = list(csv.DictReader(f))
            akhir = str(IX[179].date())
            self.assertEqual((out[0]['keluar'], out[0]['tarikh_keluar'], out[0]['keluar_henti'], out[0]['tutup_semua'], out[0]['tidak_sah']),
                             ('True', akhir, 'True', 'True', ''))
            self.assertEqual((out[1]['tarikh_keluar'], out[1]['harga_keluar'], out[1]['tarikh_keluar_henti']),
                             (str(IX[165].date()), '51', akhir))
            self.assertEqual(TL.tutup_delist(d, {'Y': g}, sesi), [])


if __name__ == '__main__':
    unittest.main()

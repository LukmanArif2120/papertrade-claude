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
        sesi = list(IX[:190])          # 10 sesi selepas bar terakhir (indeks 179)
        rows = [dict(tarikh_beli=str(IX[170].date()), saham='Y', kaedah='M01', harga_beli='50', keluar='False', keluar_henti='False'),
                dict(tarikh_beli=str(IX[160].date()), saham='Y', kaedah='M02', harga_beli='50', keluar='True', tarikh_keluar=str(IX[165].date()),
                     harga_keluar='51', untung_akhir_pct='2.00', keluar_henti='False')]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_3.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, TestPosisi.LAJUR); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in TestPosisi.LAJUR})
            self.assertEqual(TL.tutup_delist(d, {'Y': g}, sesi[:189]), [])     # 9 sesi: belum
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


class TestKelasBerganda(unittest.TestCase):
    def test_tapis_dan_tanda(self):
        # 22 Okt 2026: hanya kelas paling cair diimbas; kaedah sama membeli dua kelas hari sama -> kelas kurang cair tidak_sah
        a = saham(umum=None, n=180); b = saham(umum=None, n=180, benih=2); b['volume'] = 3e5   # B kurang cair (tetapi > USD100k)
        kump = {'A': 'Syk', 'B': 'Syk'}
        x = TL.kelas_berganda({'A': a, 'B': b}, None, kump)
        self.assertEqual(list(x), ['B'])
        tb, ti = str(IX[170].date()), str(IX[169].date())
        rows = [dict(tarikh_beli=tb, tarikh_isyarat=ti, saham=s, kaedah=k, harga_beli='50', keluar='False')
                for s, k in (('A', 'M01'), ('B', 'M01'), ('B', 'M02'))]
        lajur = TestPosisi.LAJUR + ['tarikh_isyarat']
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_6.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
            y = TL.tanda_kelas_berganda(d, {'A': a, 'B': b}, kump=kump)
            self.assertEqual([(z[1], z[2]) for z in y], [('B', 'M01')])          # M02 hanya membeli B: bukan berganda
            with open(p) as f:
                out = list(csv.DictReader(f))
            self.assertEqual([r['tidak_sah'] for r in out], ['', 'True', ''])
            self.assertEqual(TL.tanda_kelas_berganda(d, {'A': a, 'B': b}, kump=kump), [])


class TestTidakCairPosisi(unittest.TestCase):
    def test_tidak_sah_ikut_sesi_isyarat(self):
        # 22 Okt 2026: posisi C tidak cair pada sesi isyarat -> tidak_sah (tidak ditutup); cair pada isyarat -> kekal
        g = saham(umum=None, n=180); g.loc[g.index[150:153], 'volume'] = 0   # tidak cair 150–172 sahaja
        rows = [dict(tarikh_beli=str(IX[156].date()), tarikh_isyarat=str(IX[155].date()), saham='Y', kaedah='M01', harga_beli='50', keluar='False'),
                dict(tarikh_beli=str(IX[120].date()), tarikh_isyarat=str(IX[119].date()), saham='Y', kaedah='M02', harga_beli='50', keluar='False')]
        lajur = TestPosisi.LAJUR + ['tarikh_isyarat']
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_4.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
            x = TL.tanda_tidak_cair(d, {'Y': g})
            self.assertEqual([y[2] for y in x], ['M01'])
            with open(p) as f:
                out = list(csv.DictReader(f))
            self.assertEqual((out[0]['tidak_sah'], out[0]['keluar'], out[1]['tidak_sah']), ('True', 'False', ''))
            self.assertIn('tidak cair', out[0]['sebab_tidak_sah'])
            self.assertEqual(TL.tanda_tidak_cair(d, {'Y': g}), [])


if __name__ == '__main__':
    unittest.main()

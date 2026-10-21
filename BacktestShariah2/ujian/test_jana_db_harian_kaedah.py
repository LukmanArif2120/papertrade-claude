import os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd


class UjianHarianKaedah(unittest.TestCase):
    """prestasi/harian_kaedah: untung harian setiap kaedah (Σ perubahan nilai ÷ Σ nilai awal hari), akaun M, C, G."""

    def stor(self, d):
        with open(os.path.join(d, 'harga_A.csv'), 'w') as f:
            f.write('ticker,date,open,high,low,close,volume\n'
                    'AAA,20261001,10,10,10,10,1\nAAA,20261002,10,11,10,11,1\nAAA,20261005,11,12,11,12,1\n'
                    'BBB,20261001,20,20,20,20,1\nBBB,20261002,20,22,20,22,1\nBBB,20261005,22,22,20,21,1\n'
                    'CCC,20261001,5,5,5,5,1\nCCC,20261002,5,5,5,5,1\nCCC,20261005,5,5,5,5,1\nDDD,20261006,1,1,1,1,1\n')
        with open(os.path.join(d, 'harga_idx.csv'), 'w') as f:
            f.write('ticker,date,open,high,low,close,volume\nSPY,20260930,100,100,100,100,1\nSPY,20261001,100,100,100,101,1\n'
                    'SPY,20261002,100,100,100,99.99,1\n')

    def test_harian(self):
        C = [dict(saham='AAA', kaedah='M01', tarikh_beli='2026-10-01', harga_beli='10', keluar='False', untung_pct='20'),
             dict(saham='BBB', kaedah='M01', tarikh_beli='2026-10-02', harga_beli='20', keluar='True', tarikh_keluar='2026-10-05',
                  harga_keluar='23', untung_akhir_pct='15'),
             dict(saham='CCC', kaedah='M02', tarikh_beli='2026-10-01', harga_beli='5', tidak_dibeli='True')]
        M = [dict(saham='AAA', kaedah='M01', tarikh_beli='2026-10-02', harga_beli='10', keluar='False', untung_pct='20')]
        with tempfile.TemporaryDirectory() as d:
            self.stor(d)
            with open(os.path.join(d, 'terkini.csv'), 'w') as f:      # bar terbaharu: mengatasi stor dan menambah sesi
                f.write('ticker,date,open,high,low,close,volume\nAAA,20261005,11,12,11,12,1\nSPY,20261005,1,1,1,100.99,1\n')
            h = jd.harian_kaedah(M, C, d, os.path.join(d, 'terkini.csv'))
        # 6 Okt diabaikan (sesi separa: 1 daripada 3 saham)
        self.assertEqual(h['tarikh'], [20261001, 20261002, 20261005])
        R = {(r['a'], r['k']): r for r in h['rows']}
        self.assertEqual(set(R), {(a, k) for a in 'MCG' for k in ('M01', 'Semua')})    # tidak dibeli diabaikan
        self.assertEqual(h['spy'], [1.0, -1.0, 1.0])
        self.assertEqual(R[('C', 'Semua')]['d'], R[('C', 'M01')]['d'])
        c = R[('C', 'M01')]
        # 1 Okt: AAA hari beli 10→10 = 0; 2 Okt: AAA 10→11 (+100) + BBB beli 20→22 (+100) atas 2000; 5 Okt: AAA 11→12 (+100 atas 1100)
        # + BBB keluar 22→23 (+50 atas 1100) = 150/2200
        self.assertEqual(c['d'], [0.0, 10.0, round(100 * 150 / 2200, 2)])
        self.assertEqual(c['n'], [1, 2, 2])
        self.assertEqual((c['np'], c['j']), (2, 17.5))
        self.assertEqual(c['ev'], [[0, 1, 0, 0], [1, 1, 0, 0], [2, 0, 1, 0]])   # beli 1 & 2 Okt, keluar untung 5 Okt
        m = R[('M', 'M01')]
        self.assertEqual(m['d'], [None, 10.0, round(100 / 11, 2)])
        g = R[('G', 'M01')]
        self.assertEqual(g['n'], [1, 3, 3]); self.assertEqual(g['np'], 3)
        self.assertEqual(g['d'][1], round(100 * 300 / 3000, 2))

    def test_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            self.stor(d)
            self.assertEqual(jd.harian_kaedah([], [], d), dict(tarikh=[], spy=[], rows=[]))


if __name__ == '__main__':
    unittest.main()

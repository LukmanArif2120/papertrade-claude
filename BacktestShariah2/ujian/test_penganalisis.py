# Ujian Papan Penganalisis (standard/penganalisis.py): kos bersih sama dengan enjin, posisi matang sahaja dikira, kohort C
# sebelum Lejar sahaja (tiada kiraan berganda), pengecutan skor, status, semakan luar sampel, dan larian penuh atas data repo.
import json, math, os, sys, tempfile, unittest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import penganalisis as pg
import enjin

LAJUR = ['id', 'saham', 'tarikh_isyarat', 'tarikh_beli', 'tutup1', 'hasil1', 'hasil2', 'sumber']


def pos(rows):
    return pd.DataFrame(rows, columns=LAJUR)


class TestPenganalisis(unittest.TestCase):
    def test_bersih_sama_enjin(self):
        x, e = 110.0, 100.0
        self.assertAlmostEqual(pg.bersih((x / e - 1) * 100), (x / e * (1 - enjin.COST) / (1 + enjin.COST) - 1) * 100)

    def test_umur_matang(self):
        self.assertEqual(pg.umur_matang(5), 14)          # minimum 14 hari kalendar
        self.assertEqual(pg.umur_matang(30), 63)         # 1.5 x 30 x 7/5
        self.assertEqual(pg.umur_matang(None), 21)       # tiada data: anggap 10 hari

    def test_hanya_posisi_matang(self):
        P = pos([['M01', 'A', '2026-09-30', '2026-10-01', True, -5.0, -5.0, 'C'],
                 ['M01', 'B', '2026-09-30', '2026-10-01', False, 8.0, 8.0, 'C'],      # terbuka tetapi matang: untung semasa
                 ['M01', 'C', '2026-10-14', '2026-10-15', True, -6.0, -6.0, 'lejar']])  # belum matang: tidak dikira
        h = pg.ringkas_hadapan(P, 5, '2026-10-20')
        self.assertEqual((h['posisi'], h['tutup'], h['matang']), (3, 2, 2))
        self.assertAlmostEqual(h['purata'], 1.5)
        self.assertAlmostEqual(h['menang'], 0.5)
        self.assertEqual(h['matang_mula'], '2026-10-15')
        self.assertIsNone(h['matang_20'])

    def test_c_sebelum_lejar_sahaja(self):
        L = pos([['M01', 'A', '2026-10-15', '2026-10-16', False, 1.0, 1.0, 'lejar']])
        C = pos([['M01', 'X', '2026-10-08', '2026-10-09', True, 2.0, 2.0, 'C'],
                 ['M01', 'A', '2026-10-15', '2026-10-16', False, 1.1, 1.1, 'C']])      # isyarat sama dengan Lejar
        H, mula = pg.gabung_hadapan(L, C)
        self.assertEqual(mula, '2026-10-16')
        self.assertEqual(sorted(zip(H.saham, H.sumber)), [('A', 'lejar'), ('X', 'C')])

    def test_berat_dan_skor(self):
        self.assertAlmostEqual(pg.berat_backtest(10 ** 9), pg.N0, places=3)
        self.assertAlmostEqual(pg.berat_backtest(30), 15.0)
        mu, lo, hi = pg.skor(2.0, 10.0, 0, 0.0, None)
        self.assertEqual(mu, 2.0)
        self.assertAlmostEqual(hi - mu, 1.96 * 10 / math.sqrt(pg.N0))
        mu, lo, hi = pg.skor(2.0, 10.0, 970, -1.0, 8.0)      # data hadapan banyak menguasai jangkaan
        self.assertAlmostEqual(mu, (30 * 2.0 + 970 * -1.0) / 1000)
        self.assertAlmostEqual(hi - mu, 1.96 * 8.0 / math.sqrt(1000))

    def test_status(self):
        self.assertEqual(pg.status_kaedah(5, -9.0, 4.0, 2.0, -1, 3), 'BELUM CUKUP')
        self.assertEqual(pg.status_kaedah(12, -3.0, 4.0, 2.0, -1, 3), 'AMARAN')   # t = -5/(4/√12) < -2
        self.assertEqual(pg.status_kaedah(25, 1.0, 9.0, 1.0, 0.2, 2.0), 'KUAT')
        self.assertEqual(pg.status_kaedah(25, 0.5, 9.0, 0.5, -3.0, -0.1), 'LEMAH')
        self.assertEqual(pg.status_kaedah(25, 0.5, 9.0, 0.5, -1.0, 2.0), 'PERHATI')

    def test_semakan(self):
        reg = dict(subset_menang=3, subset_n=4)
        wfo = dict(cagr=0.40, ew=0.326)
        at = dict(cagr_a=0.16, spy_a=0.146, cagr_b=0.10, spy_b=0.146)
        self.assertEqual(pg.semakan(reg, wfo, at), (True, True, False))
        self.assertEqual(pg.semakan({}, None, None), (None, None, None))

    def test_harga_sandaran_stor(self):
        with tempfile.TemporaryDirectory() as d:
            tk, st = os.path.join(d, 'terkini.csv'), os.path.join(d, 'stor')
            os.makedirs(st)
            pd.DataFrame([['A', '20261016', 10.0], ['A', '20261019', 11.0]], columns=['ticker', 'date', 'close']).to_csv(tk, index=False)
            pd.DataFrame([['A', '20261019', 99.0], ['B', '20261016', 5.0], ['B', '20261019', 6.0], ['B', '20261020', 7.0]],
                         columns=['ticker', 'date', 'close']).to_csv(os.path.join(st, 'harga_A.csv'), index=False)
            akhir, t = pg.harga_akhir(tk, st)
            self.assertEqual(t, '2026-10-19')
            self.assertEqual(akhir, {'A': 11.0, 'B': 6.0})      # terkini didahulukan; stor hanya bagi saham tiada, hingga tarikh sama

    def test_larian_penuh(self):
        with tempfile.TemporaryDirectory() as d:
            md, js = os.path.join(d, 'P.md'), os.path.join(d, 'p.json')
            pg.main(['--md', md, '--json', js])
            doc = json.load(open(js, encoding='utf-8'))
            kat = json.load(open(pg.KATALOG, encoding='utf-8'))['rows']
            self.assertEqual(len(doc['rows']), len(kat))
            self.assertLess(os.path.getsize(js), 250_000)                  # had dokumen db dashboard
            self.assertEqual(len(doc['penemuan']), 3)
            self.assertTrue(set(r['status'] for r in doc['rows']) <= set(pg.STATUS))
            k = [r['kedudukan'] for r in doc['rows'] if r['kedudukan']]
            self.assertEqual(k, list(range(1, len(k) + 1)))
            self.assertTrue(all(r['swing'] and not r['sampel_kecil'] for r in doc['rows'] if r['kedudukan']))
            self.assertIn('## 3 penemuan utama', open(md, encoding='utf-8').read())


if __name__ == '__main__':
    unittest.main()

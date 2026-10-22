# Ujian Papan Penganalisis (standard/penganalisis.py): kos bersih sama dengan enjin, posisi matang sahaja dikira, kohort C
# sebelum Lejar sahaja (tiada kiraan berganda), pengecutan skor, status, semakan luar sampel, dan larian penuh atas data repo.
import json, math, os, sys, tempfile, unittest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import penganalisis as pg
import enjin

LAJUR = pg.LAJUR_POS


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
        P = pos([['M01', 'A', '2026-09-30', '2026-10-01', '2026-10-02', True, -5.0, -5.0, 'C'],
                 ['M01', 'B', '2026-09-30', '2026-10-01', '', False, 8.0, 8.0, 'C'],      # terbuka tetapi matang: untung semasa
                 ['M01', 'C', '2026-10-14', '2026-10-15', '2026-10-16', True, -6.0, -6.0, 'lejar']])  # belum matang
        h = pg.ringkas_hadapan(P, 5, '2026-10-20')
        self.assertEqual((h['posisi'], h['tutup'], h['matang']), (3, 2, 2))
        self.assertAlmostEqual(h['purata'], 1.5)
        self.assertAlmostEqual(h['menang'], 0.5)
        self.assertEqual(h['matang_mula'], '2026-10-15')
        self.assertIsNone(h['matang_20'])

    def test_c_sebelum_lejar_sahaja(self):
        L = pos([['M01', 'A', '2026-10-15', '2026-10-16', '', False, 1.0, 1.0, 'lejar']])
        C = pos([['M01', 'X', '2026-10-08', '2026-10-09', '2026-10-12', True, 2.0, 2.0, 'C'],
                 ['M01', 'A', '2026-10-15', '2026-10-16', '', False, 1.1, 1.1, 'C']])      # isyarat sama dengan Lejar
        H, mula, tindih = pg.gabung_hadapan(L, C)
        self.assertEqual((mula, tindih), ('2026-10-16', 0))
        self.assertEqual(sorted(zip(H.saham, H.sumber)), [('A', 'lejar'), ('X', 'C')])

    def test_lejar_bertindih_c_dibuang(self):
        # C pra-Lejar masih memegang M01 W (atau keluar pada hari isyarat Lejar): enjin mengabaikan isyarat Lejar itu
        L = pos([['M01', 'W', '2026-10-15', '2026-10-16', '', False, 1.0, 1.0, 'lejar'],
                 ['M01', 'Y', '2026-10-15', '2026-10-16', '', False, 1.0, 1.0, 'lejar'],
                 ['M01', 'Z', '2026-10-15', '2026-10-16', '', False, 1.0, 1.0, 'lejar'],
                 ['M02', 'W', '2026-10-15', '2026-10-16', '', False, 1.0, 1.0, 'lejar']])   # kaedah lain: kekal
        C = pos([['M01', 'W', '2026-10-09', '2026-10-12', '', False, 3.0, 3.0, 'C'],
                 ['M01', 'Y', '2026-10-09', '2026-10-12', '2026-10-15', True, -2.0, -2.0, 'C'],
                 ['M01', 'Z', '2026-10-09', '2026-10-12', '2026-10-14', True, -2.0, -2.0, 'C']])  # keluar sebelum isyarat: kekal
        H, mula, tindih = pg.gabung_hadapan(L, C)
        self.assertEqual(tindih, 2)
        self.assertEqual(sorted(zip(H.id, H.saham, H.sumber)),
                         [('M01', 'W', 'C'), ('M01', 'Y', 'C'), ('M01', 'Z', 'C'), ('M01', 'Z', 'lejar'), ('M02', 'W', 'lejar')])

    def test_laras_beli_split(self):
        buka = {('S', '2026-10-16'): 50.0, ('T', '2026-10-16'): 100.2}
        self.assertEqual(pg.laras_beli(100.0, 'S', '2026-10-16', buka, pg.TOL_LARAS), 50.0)    # split 2:1 dalam stor
        self.assertEqual(pg.laras_beli(100.0, 'T', '2026-10-16', buka, pg.TOL_LARAS), 100.0)   # beza 0.2% < toleransi
        self.assertEqual(pg.laras_beli(100.0, 'U', '2026-10-16', buka, pg.TOL_LARAS), 100.0)   # tiada bar

    def test_c_lorong2_harga_semasa(self):
        with tempfile.TemporaryDirectory() as d:
            lajur = ['tarikh_beli', 'saham', 'kaedah', 'id_kaedah', 'harga_beli', 'untung_pct', 'keluar', 'untung_akhir_pct',
                     'tarikh_keluar', 'tarikh_isyarat', 'tidak_sah', 'tidak_dibeli', 'keluar_henti', 'untung_henti_pct']
            pd.DataFrame([['2026-10-09', 'Q', 'M01', 'M01', '10', '-5', 'True', '-5', '2026-10-13', '2026-10-08', '', '', 'False', '']],
                         columns=lajur).to_csv(os.path.join(d, 'claude.csv'), index=False)
            C = pg.muat_c(d, akhir={'Q': 12.0}, buka={})
            self.assertAlmostEqual(C.hasil1.iloc[0], pg.bersih(-5.0))     # lorong 1: untung akhir C
            self.assertAlmostEqual(C.hasil2.iloc[0], pg.bersih(20.0))     # lorong 2 masih dipegang: tutup terakhir, bukan harga beku
            self.assertEqual(C.tarikh_keluar.iloc[0], '2026-10-13')

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

    def test_kukuh_pangkas_kluster_hari(self):
        # 22 Okt 2026 (R5–R7): satu squeeze tidak menguasai; posisi hari sama = sedikit maklumat bebas; < 10 hari beli -> BELUM CUKUP
        import numpy as np
        x = [1.0] * 39 + [300.0]
        self.assertAlmostEqual(pg.purata_pangkas(x), 1.0)
        self.assertGreater(sum(x) / len(x), 8)
        self.assertEqual(pg.n_berkesan(np.arange(40.0), ['2026-10-16'] * 40), 1.0)          # satu hari beli
        r = np.random.default_rng(3)
        hari = np.repeat(np.arange(10), 20); kesan = r.normal(0, 5, 10)[hari]               # 10 hari, kesan pasaran kuat setiap hari
        nb = pg.n_berkesan(kesan + r.normal(0, 1, 200), hari.astype(str))
        self.assertLess(nb, 40)
        self.assertGreater(pg.n_berkesan(r.normal(0, 1, 200), hari.astype(str)), 100)    # tiada kesan hari: hampir n
        self.assertEqual(pg.status_kaedah(25, 1.0, 9.0, 1.0, 0.2, 2.0, hari=9), 'BELUM CUKUP')
        self.assertEqual(pg.status_kaedah(25, 1.0, 9.0, 1.0, 0.2, 2.0, hari=10), 'KUAT')

    def test_lintas_earnings(self):
        P = pos([dict(id='M01', saham='A', tarikh_isyarat='2026-10-14', tarikh_beli='2026-10-15', tarikh_keluar='2026-10-20', tutup1=True,
                      hasil1=1.0, hasil2=1.0, sumber='lejar'),
                 dict(id='M01', saham='A', tarikh_isyarat='2026-10-21', tarikh_beli='2026-10-22', tarikh_keluar='', tutup1=False,
                      hasil1=1.0, hasil2=1.0, sumber='lejar'),
                 dict(id='M01', saham='B', tarikh_isyarat='2026-10-14', tarikh_beli='2026-10-15', tarikh_keluar='', tutup1=False,
                      hasil1=1.0, hasil2=1.0, sumber='lejar')])
        E = {'A': ['2026-10-16'], 'B': ['2026-10-15']}     # B: kesan pada hari beli (jurang sebelum buka) -> bukan lintas
        self.assertEqual(list(pg.lintas_earnings(P, E, '2026-10-30')), [True, False, False])
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, 'tv.csv')
            pd.DataFrame(dict(ticker=['A', 'B'], earnings_release_date=['1792526400', ''],          # 2026-10-20 16:00 NY -> 21 Okt
                              earnings_release_next_date=['1793109600', '1792497600'])).to_csv(f, index=False)  # 27 Okt 10:00; 20 Okt 08:00
            e = pg.muat_earnings(f, os.path.join(d, 'tiada.csv'))
            self.assertEqual(e, {'A': ['2026-10-21', '2026-10-27'], 'B': ['2026-10-20']})

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


class TestKedudukanSebelum(unittest.TestCase):
    def test_sesi_baharu_dan_larian_semula(self):
        rows = [dict(id='M01', kedudukan=1), dict(id='M02', kedudukan=2), dict(id='M09', kedudukan=3)]
        lama = dict(kini='2026-10-19', rows=[dict(id='M01', kedudukan=2, kedudukan_sebelum=5), dict(id='M02', kedudukan=1)])
        pg.kedudukan_sebelum(rows, '2026-10-20', lama)          # sesi baharu: rujukan = kedudukan lama
        self.assertEqual([r.get('kedudukan_sebelum') for r in rows], [2, 1, None])
        rows2 = [dict(id='M01', kedudukan=1)]
        pg.kedudukan_sebelum(rows2, '2026-10-19', lama)         # larian semula data sama: rujukan lama kekal
        self.assertEqual(rows2[0]['kedudukan_sebelum'], 5)
        rows3 = [dict(id='M01', kedudukan=1)]
        pg.kedudukan_sebelum(rows3, '2026-10-20', None)         # tiada fail lama
        self.assertNotIn('kedudukan_sebelum', rows3[0])


if __name__ == '__main__':
    unittest.main()

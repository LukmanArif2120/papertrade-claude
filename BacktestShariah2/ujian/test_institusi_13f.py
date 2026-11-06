# Ujian standard/institusi_13f.py (fungsi tulen: tempoh set, pilihan pindaan, pecahan saham, aliran, kumpulan)
import os, sys, unittest
from datetime import date

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import institusi_13f as I  # noqa: E402


class TestTempoh(unittest.TestCase):
    def test_tempoh_set(self):
        self.assertEqual(I.tempoh_set('/x/01jun2026-31aug2026_form13f.zip'),
                         (date(2026, 6, 1), date(2026, 8, 31), date(2026, 6, 30)))
        self.assertEqual(I.tempoh_set('01dec2025-28feb2026_form13f.zip')[2], date(2025, 12, 31))
        self.assertEqual(I.tempoh_set('01mar2026-31may2026_form13f.zip')[2], date(2026, 3, 31))
        self.assertIsNone(I.tempoh_set('form13f.zip'))

    def test_suku_lalu(self):
        self.assertEqual(I.suku_lalu(date(2026, 6, 30)), date(2026, 3, 31))
        self.assertEqual(I.suku_lalu(date(2026, 3, 31)), date(2025, 12, 31))
        self.assertEqual(I.suku_lalu(date(2025, 12, 31)), date(2025, 9, 30))


def sub(rows):
    return pd.DataFrame(rows, columns=['akses', 'tarikh_fail', 'jenis', 'pindaan'])


class TestPilihAkses(unittest.TestCase):
    def test_asal_sahaja(self):
        self.assertEqual(I.pilih_akses(sub([('a1', '2026-08-01', '13F-HR', '')])), ['a1'])

    def test_pernyataan_semula_ganti_asal(self):
        s = sub([('a1', '2026-08-01', '13F-HR', ''), ('a2', '2026-08-20', '13F-HR/A', 'RESTATEMENT')])
        self.assertEqual(I.pilih_akses(s), ['a2'])

    def test_pegangan_baharu_ditambah(self):
        s = sub([('a1', '2026-08-01', '13F-HR', ''), ('a2', '2026-08-20', '13F-HR/A', 'NEW HOLDINGS')])
        self.assertEqual(I.pilih_akses(s), ['a1', 'a2'])

    def test_pegangan_baharu_sebelum_asal_terakhir_dibuang(self):
        s = sub([('a1', '2026-08-01', '13F-HR', ''), ('a2', '2026-08-02', '13F-HR/A', 'NEW HOLDINGS'),
                 ('a3', '2026-08-10', '13F-HR', '')])
        self.assertEqual(I.pilih_akses(s), ['a3'])

    def test_pindaan_tanpa_asas(self):
        self.assertEqual(I.pilih_akses(sub([('a2', '2026-08-20', '13F-HR/A', 'NEW HOLDINGS')])), [])


class TestPecahan(unittest.TestCase):
    def test_tiada_pecahan(self):
        self.assertEqual(I.faktor_pecahan(1.1, 1.2), 1.0)
        self.assertEqual(I.faktor_pecahan(np.nan, 1.0), 1.0)

    def test_pecahan_2_untuk_1(self):
        self.assertEqual(I.faktor_pecahan(2.01, 0.52), 2.0)

    def test_pecahan_songsang(self):
        self.assertAlmostEqual(I.faktor_pecahan(0.1, 9.5), 0.1)

    def test_harga_tidak_sepadan_bukan_pecahan(self):
        # saham pemegang berganda tetapi harga juga naik: belian sebenar, bukan pecahan
        self.assertEqual(I.faktor_pecahan(2.0, 1.1), 1.0)

    def test_pemegang_luas_abaikan_harga(self):
        # penyatuan 1:2 serentak spin-off: harga hampir rata, median 0.5 pada 3,000 pemegang = pecahan
        self.assertEqual(I.faktor_pecahan(0.5, 0.99, 3000), 0.5)
        self.assertEqual(I.faktor_pecahan(0.5, 0.99, 5), 1.0)

    def test_buang_salah_lapor(self):
        d = pd.DataFrame(dict(cusip=['A'] * 4 + ['B'], saham=[10, 10, 10, 10_000, 5], nilai=[100, 110, 90, 100, 5]))
        self.assertEqual(list(I.buang_salah_lapor(d).saham), [10, 10, 10, 5])

    def test_nisbah_janggal_bukan_pecahan(self):
        self.assertEqual(I.faktor_pecahan(2.6, 0.38), 1.0)


def pg(rows):
    return pd.DataFrame(rows, columns=['cik', 'ticker', 'saham', 'nilai'])


class TestAliran(unittest.TestCase):
    def test_baru_keluar_aliran(self):
        lalu = pg([('1', 'AAA', 100, 1000), ('2', 'AAA', 100, 1000), ('3', 'AAA', 50, 500)])
        kini = pg([('1', 'AAA', 150, 1800), ('2', 'AAA', 100, 1200), ('4', 'AAA', 50, 600)])
        r = I.aliran(kini, lalu).set_index('ticker').loc['AAA']
        self.assertEqual((r.pemegang, r.pemegang_lalu, r.baru, r.keluar, r.bersih), (3, 3, 1, 1, 0))
        self.assertEqual((r.saham_inst, r.saham_inst_lalu), (300, 250))
        self.assertAlmostEqual(r.harga, 12.0)
        self.assertAlmostEqual(r.aliran_usd, 50 * 12.0)
        self.assertAlmostEqual(r.ubah_saham_pct, 20.0)
        self.assertEqual(r.faktor_pecahan, 1.0)

    def test_pecahan_tidak_jadi_aliran(self):
        lalu = pg([(str(i), 'SPL', 100, 10000) for i in range(5)])
        kini = pg([(str(i), 'SPL', 200, 10200) for i in range(5)])
        r = I.aliran(kini, lalu).set_index('ticker').loc['SPL']
        self.assertEqual(r.faktor_pecahan, 2.0)
        self.assertAlmostEqual(r.ubah_saham_pct, 0.0)
        self.assertAlmostEqual(r.aliran_usd, 0.0)

    def test_keluar_penuh(self):
        r = I.aliran(pg([('1', 'B', 1, 10)]), pg([('1', 'B', 1, 10), ('2', 'X', 10, 100)])).set_index('ticker')
        self.assertEqual((r.loc['X'].pemegang, r.loc['X'].keluar, r.loc['X'].saham_inst), (0, 1, 0))
        self.assertAlmostEqual(r.loc['X'].aliran_usd, -100.0)   # harga lalu dipakai bila tiada pegangan kini


class TestNamaDanSah(unittest.TestCase):
    def test_nama_norm(self):
        self.assertEqual(I.nama_norm('EXXON MOBIL CORP COM'), 'EXXONMOBIL')
        self.assertEqual(I.nama_norm('ExxonMobil Holdings Corp'), 'EXXONMOBIL')
        self.assertEqual(I.nama_norm('EXXON MOBIL (REGISTERED)'), 'EXXONMOBIL')
        self.assertNotEqual(I.nama_norm('ALPHABET INC CL A'), I.nama_norm('ALPHABET INC CL C'))

    def test_peta_nama_unik_sahaja(self):
        tick = {'NEW000001': 'XOM', 'OLD000001': '', 'GA0000001': 'GOOGL', 'GC0000001': 'GOOG', 'GX0000001': ''}
        nama = pd.Series({'NEW000001': 'EXXONMOBIL', 'OLD000001': 'EXXONMOBIL', 'GA0000001': 'ALPHABET',
                          'GC0000001': 'ALPHABET', 'GX0000001': 'ALPHABET'})
        self.assertEqual(I.peta_nama(tick, nama), {'OLD000001': 'XOM'})   # ALPHABET -> 2 ticker: tidak dipeta

    def test_tanda_sah(self):
        d = pd.DataFrame(dict(pemegang=[100, 390, 106, 2452, 100], pemegang_lalu=[95, 4, 0, 2048, 3],
                              ubah_saham_pct=[3.0, 9e4, np.nan, 920.0, 10.0]))
        self.assertEqual(list(I.tanda_sah(d)), [True, False, False, False, False])

    def test_aliran_ada_sah(self):
        r = I.aliran(pg([(str(i), 'A', 10, 100) for i in range(6)]), pg([(str(i), 'A', 10, 100) for i in range(6)]))
        self.assertTrue(bool(r.sah.iloc[0]))


class TestKumpulan(unittest.TestCase):
    def test_skor_dan_teratas(self):
        rows = []
        for ind, ubah in [('Semiconductors', 0.3), ('Banks - Regional', 0.0), ('Oil & Gas E&P', -0.3)]:
            for i in range(4):
                sl = 1000.0
                sk = sl * (1 + ubah + 0.01 * i)
                rows.append(dict(tempoh='2026-06-30', ticker=f'{ind[:3]}{i}', pemegang=10, pemegang_lalu=10,
                                 baru=3 if ubah > 0 else 0, keluar=3 if ubah < 0 else 0,
                                 bersih=3 if ubah > 0 else -3 if ubah < 0 else 0, saham_inst=sk, saham_inst_lalu=sl,
                                 ubah_saham_pct=(sk / sl - 1) * 100, harga=10.0, aliran_usd=(sk - sl) * 10,
                                 nilai_inst_usd=sk * 10, faktor_pecahan=1.0, sah=True))
        s = pd.DataFrame(rows)
        peta = pd.DataFrame(dict(ticker=s.ticker, industri=[t for t in ['Semiconductors', 'Banks - Regional',
                                                                         'Oil & Gas E&P'] for _ in range(4)]))
        k = I.kumpulan(s, peta, I_SEKTOR, 'x')
        ind = k[k.jenis == 'Industri'].set_index('nama')
        self.assertEqual(ind.loc['Semiconductors'].gred, 'A')
        self.assertEqual(ind.index[0], 'Semiconductors')
        self.assertAlmostEqual(ind.loc['Semiconductors'].aliran_pct, 31.5)
        self.assertTrue(ind.loc['Semiconductors'].teratas.startswith('Sem3'))
        self.assertEqual(ind.loc['Oil & Gas E&P'].pct_bersih_positif, 0)
        self.assertEqual(list(k.columns), I.LAJUR_KUMP)
        d = I.doc_db(s, k, peta, I_SEKTOR, dict(tempoh='2026-06-30', tempoh_lalu='2026-03-31', pemfail_dua=7,
                                                 saham=12, dibina='x'))
        semi = next(r for r in d['rows'] if r['n'] == 'Semiconductors')
        self.assertEqual((semi['j'], semi['g'], semi['t'][0][0]), ('I', 'A', 'Sem3'))
        self.assertEqual(len([r for r in d['rows'] if r['j'] == 'S']), len(set(peta.industri.map(I_SEKTOR))))
        import json
        json.dumps(d, allow_nan=False)   # dokumen db mesti JSON sah (tiada NaN)

    def test_kumpulan_kecil_tiada_skor(self):
        s = pd.DataFrame([dict(tempoh='2026-06-30', ticker='A', pemegang=9, pemegang_lalu=9, baru=0, keluar=0,
                               bersih=0, saham_inst=1.0, saham_inst_lalu=1.0, ubah_saham_pct=0.0, harga=1.0,
                               aliran_usd=0.0, nilai_inst_usd=1.0, faktor_pecahan=1.0, sah=True)])
        k = I.kumpulan(s, pd.DataFrame(dict(ticker=['A'], industri=['Semiconductors'])), I_SEKTOR)
        self.assertTrue(k.skor.isna().all())
        self.assertTrue((k.gred == '').all())


from sektor_pasaran import SEKTOR_INDUSTRI as I_SEKTOR  # noqa: E402

if __name__ == '__main__':
    unittest.main()

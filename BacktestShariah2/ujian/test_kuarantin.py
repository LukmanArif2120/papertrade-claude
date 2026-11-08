# Ujian kuarantin data harga (7 Nov 2026; standard/kuarantin.py, standard/harga_yf.py, kod/peristiwa.py):
# keputusan 'anomali' tidak lagi menimpa bar stor, faktor KEMBAR pada dua saham tidak digunakan dan dikuarantin, peristiwa
# direktori Nasdaq dalam tetingkap bar baharu dikuarantin, kuarantin dilepaskan hanya apabila sejarah segar konsisten, dan
# dikuarantin() / tercemar() untuk mengecualikan ticker-tarikh daripada statistik. Tiada fail repo ditulis (semua dalam temp).
import io, json, os, sys, tempfile, unittest
from contextlib import redirect_stdout

import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import kuarantin as KR  # noqa: E402
import harga_yf as H  # noqa: E402
import peristiwa as P  # noqa: E402

T = [int(x.strftime('%Y%m%d')) for x in pd.bdate_range('2026-09-01', periods=60)]


def bar(tarikh, tutup, t='X', volum=1000):
    c = np.asarray(tutup, float)
    return pd.DataFrame(dict(ticker=t, date=list(tarikh), open=c, high=c * 1.01, low=c * 0.99, close=c, volume=volum))


def tkh(i):
    return KR.tarikh_teks(T[i])


def siri(benih, n=60, asas=40.0):
    r = np.random.default_rng(benih)
    return asas * np.cumprod(1 + r.normal(0, 0.015, n))


class TestFailKuarantin(unittest.TestCase):
    def test_tambah_idempoten_aktif_lepas_dan_selang(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'kuarantin.csv')
            self.assertTrue(KR.tambah('SUPN', '2026-10-21', 'ujian', p, dicatat='2026-11-07 06:00 UTC'))
            self.assertFalse(KR.tambah('SUPN', 20261021, 'ujian lagi', p))          # pasangan sama: tidak berulang
            self.assertTrue(KR.tambah('INDV', '2026-11-03', 'ujian', p, dicatat='2026-11-07 06:00 UTC'))
            self.assertEqual(len(KR.muat(p)), 2)
            self.assertEqual(list(KR.muat(p).columns), KR.LAJUR)
            self.assertEqual(KR.aktif(p), {'SUPN': '2026-10-21', 'INDV': '2026-11-03'})
            self.assertEqual(KR.lepas('SUPN', 'sejarah segar konsisten', p, dicatat='2026-11-10 06:00 UTC'), ['2026-10-21'])
            self.assertEqual(KR.aktif(p), {'INDV': '2026-11-03'})
            self.assertEqual(KR.selang(p)['SUPN'], [('2026-10-21', '2026-11-10')])
            self.assertEqual(KR.selang(p)['INDV'], [('2026-11-03', None)])
            self.assertFalse(KR.tambah('SUPN', '2026-10-21', 'selepas lepas', p))   # sudah dilepaskan: tidak dibuka semula
            self.assertEqual(len(KR.muat(p)), 3)                                     # tambah sahaja (3 baris)

    def test_dikuarantin_tercemar_dan_topeng(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'kuarantin.csv')
            self.assertFalse(KR.dikuarantin('SUPN', '2026-10-25', p))                # fail tiada
            KR.tambah('SUPN', '2026-10-21', 'ujian', p, dicatat='2026-11-07 06:00 UTC')
            self.assertFalse(KR.dikuarantin('SUPN', '2026-10-20', p))
            self.assertTrue(KR.dikuarantin('SUPN', 20261021, p))
            self.assertTrue(KR.dikuarantin('SUPN', pd.Timestamp('2026-12-31'), p))   # aktif: terbuka ke hadapan
            self.assertFalse(KR.dikuarantin('INDV', '2026-10-25', p))
            KR.lepas('SUPN', 'ujian', p, dicatat='2026-11-10 06:00 UTC')
            self.assertTrue(KR.dikuarantin('SUPN', '2026-11-10', p))                 # selang kekal selepas pelepasan
            self.assertFalse(KR.dikuarantin('SUPN', '2026-11-11', p))
            self.assertFalse(KR.tercemar('SUPN', '2026-10-01', '2026-10-20', p))
            self.assertTrue(KR.tercemar('SUPN', '2026-10-01', '2026-10-21', p))
            self.assertTrue(KR.tercemar('SUPN', '2026-10-01', None, p))
            self.assertTrue(KR.tercemar('SUPN', '2026-10-01', '', p))
            self.assertFalse(KR.tercemar('SUPN', '2026-11-11', None, p))
            df = pd.DataFrame(dict(saham=['SUPN', 'SUPN', 'AAA', 'SUPN'],
                                   tarikh_beli=['2026-10-01', '2026-10-25', '2026-10-25', '2026-11-12'],
                                   tarikh_keluar=['2026-10-30', '', '', '']))
            self.assertEqual(list(KR.topeng(df, path=p)), [False, True, False, False])
            self.assertEqual(list(KR.topeng_posisi(df, path=p)), [True, True, False, False])

    def test_ditangani_dan_permintaan_sejarah(self):
        with tempfile.TemporaryDirectory() as d:
            p, perlu = os.path.join(d, 'kuarantin.csv'), os.path.join(d, 'perlu_sejarah.txt')
            KR.tambah('SUPN', '2026-10-21', 'ujian', p, dicatat='2026-11-07 06:00 UTC')
            KR.tambah('INDV', '2026-11-03', 'ujian', p, dicatat='2026-11-07 06:00 UTC')
            self.assertTrue(KR.ditangani(p, 'SUPN', 20261103))
            self.assertFalse(KR.ditangani(p, 'SUPN', '2026-11-08'))
            self.assertFalse(KR.ditangani(p, 'AAA', '2026-01-01'))
            # INDV tiada dalam direktori semasa (delist): tidak diminta muat turun semula
            self.assertEqual(KR.perlu_muat_semula(p, semasa={'SUPN', 'AAA'}), ['SUPN'])
            with open(perlu, 'w') as f:
                f.write('BB\n')
            self.assertEqual(KR.minta_sejarah(['SUPN'], perlu), ['SUPN'])
            self.assertEqual(KR.minta_sejarah(['SUPN'], perlu), [])
            with open(perlu) as f:
                self.assertEqual(sorted(x.strip() for x in f), ['BB', 'SUPN'])

    def test_baiki_cli_idempoten(self):
        with tempfile.TemporaryDirectory() as d:
            p, perlu = os.path.join(d, 'kuarantin.csv'), os.path.join(d, 'perlu_sejarah.txt')
            sm = os.path.join(d, 'semasa.csv')
            pd.DataFrame(dict(simbol=['SUPN', 'AAA'])).to_csv(sm, index=False)
            lama = KR.SEMASA_BURSA; KR.SEMASA_BURSA = sm
            try:
                for _ in range(2):
                    with redirect_stdout(io.StringIO()) as out:
                        KR.main(['--fail', p, 'baiki', '--perlu', perlu])
                hasil = json.loads(out.getvalue())
            finally:
                KR.SEMASA_BURSA = lama
            self.assertEqual(hasil['ditambah'], [])                                 # larian kedua: tiada baris baharu
            self.assertEqual(KR.aktif(p), {'SUPN': '2026-10-21', 'INDV': '2026-11-03'})
            self.assertEqual(len(KR.muat(p)), 2)
            with open(perlu) as f:
                self.assertEqual([x.strip() for x in f], ['SUPN'])
            self.assertTrue(KR.dikuarantin('SUPN', '2026-10-21', p))
            self.assertTrue(KR.dikuarantin('INDV', '2026-11-05', p))


class TestAnomaliTidakTimpa(unittest.TestCase):
    def test_gabung_satu_anomali_kekalkan_bar_stor(self):
        lama = bar(T[:30], siri(1, 30))
        baru = bar(T[25:35], siri(2, 10, 30.0))      # saham lain di bawah simbol sama: nisbah tidak seragam
        self.assertEqual(H.nisbah_laras(lama, baru)[1], 'anomali')
        kr = []
        x = H.gabung_satu(lama, baru, log := [], kr)
        x = x.sort_values('date').reset_index(drop=True)
        self.assertEqual(list(x.date), T[:30])                                      # tiada bar baharu ditambah
        np.testing.assert_allclose(x.close.values, lama.close.values)               # bar bertindih TIDAK ditimpa
        self.assertEqual(log[0]['keputusan'], 'anomali')
        self.assertEqual((kr[0]['ticker'], kr[0]['tarikh_mula']), ('X', tkh(25)))

    def test_gabung_tulis_kuarantin_dan_log(self):
        lama = bar(T[:30], siri(1, 30))
        stor = {'harga_A.csv': lama.copy(), 'harga_B.csv': pd.DataFrame(columns=H.LAJ), 'harga_idx.csv': pd.DataFrame(columns=H.LAJ)}
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'kuarantin.csv')
            stor, nota = H.gabung(stor, bar(T[25:35], siri(2, 10, 30.0)), kuarantin=p)
            self.assertEqual(KR.aktif(p), {'X': tkh(25)})
            self.assertEqual([r['keputusan'] for r in nota['log_laras']], ['anomali', 'kuarantin'])
            self.assertEqual(nota['kuarantin']['baru'][0][:2], ['X', tkh(25)])
        a = stor['harga_A.csv'].sort_values('date')
        self.assertEqual(list(a.date), T[:30])
        np.testing.assert_allclose(a.close.values, lama.close.values)

    def test_saham_biasa_tidak_berubah(self):
        # kawalan: bar bertindih sama + bar baharu -> digabung seperti biasa, tiada kuarantin
        c = siri(3, 35)
        stor = {'harga_A.csv': bar(T[:30], c[:30])}
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'kuarantin.csv')
            stor, nota = H.gabung(stor, bar(T[25:35], c[25:35]), kuarantin=p)
            self.assertFalse(os.path.exists(p))
        self.assertEqual(list(stor['harga_A.csv'].sort_values('date').date), T[:35])
        self.assertEqual(nota['kuarantin'], dict(baru=[], dilepaskan=[], kekal_beku={}))


class TestFaktorKembar(unittest.TestCase):
    def faktor(self, d, rows):
        p = os.path.join(d, 'faktor.csv')
        P.tulis(pd.DataFrame([dict(saham=s, tarikh_ex=tkh(i), jenis='dividen_khas', faktor=f, sumber='ujian',
                                   catatan='D=8.13 P=36.28', ditambah='2026-11-04') for s, i, f in rows]), p)
        return p

    def test_asing_kembar(self):
        with tempfile.TemporaryDirectory() as d:
            rows = P.muat(self.faktor(d, [('INDV', 30, '0.775910'), ('SUPN', 30, '0.775910'), ('HMY', 30, '0.972625'),
                                          ('RMR', 31, '0.775910')]))
            sah, kembar = P.asing_kembar(rows)
            self.assertEqual(sorted(kembar.saham), ['INDV', 'SUPN'])
            self.assertEqual(sorted(sah.saham), ['HMY', 'RMR'])       # faktor sama pada TARIKH lain: bukan kembar
            self.assertEqual(len(P.asing_kembar(rows.iloc[0:0])[1]), 0)

    def test_gabung_faktor_kembar_tidak_digunakan_dan_dikuarantin(self):
        with tempfile.TemporaryDirectory() as d:
            fk = self.faktor(d, [('AAA', 30, '0.775910'), ('BBB', 30, '0.775910'), ('CCC', 30, '0.900000')])
            st = os.path.join(d, 'stor'); os.makedirs(st)
            kr = os.path.join(d, 'kuarantin.csv')
            stor = {'harga_A.csv': pd.concat([bar(T[:32], [100.0] * 32, 'AAA'), bar(T[:32], [50.0] * 32, 'BBB'),
                                              bar(T[:32], [80.0] * 32, 'CCC')], ignore_index=True)}
            baru = pd.concat([bar(T[28:36], [100.0] * 8, 'AAA'), bar(T[28:36], [50.0] * 8, 'BBB'),
                              bar(T[28:36], [80.0] * 8, 'CCC')], ignore_index=True)
            lama_f = P.FAKTOR; P.FAKTOR = fk
            try:
                stor, nota = H.gabung(stor, baru, st, kuarantin=kr)
            finally:
                P.FAKTOR = lama_f
            a = stor['harga_A.csv']
            for t, v in (('AAA', 100.0), ('BBB', 50.0)):
                g = a[a.ticker == t]
                np.testing.assert_allclose(g.close.values, v)                       # faktor kembar tidak didarab
                self.assertEqual(int(g.date.max()), T[31])                          # bar baharu tidak ditambah (beku)
            c = a[a.ticker == 'CCC'].sort_values('date')
            np.testing.assert_allclose(c[c.date < T[30]].close.values, 72.0)       # kawalan: faktor tunggal digunakan
            self.assertEqual(int(c.date.max()), T[35])
            self.assertEqual(KR.aktif(kr), {'AAA': tkh(30), 'BBB': tkh(30)})
            self.assertEqual(sorted(r['ticker'] for r in nota['log_laras'] if r['keputusan'] == 'kuarantin'), ['AAA', 'BBB'])
            self.assertNotIn(('AAA', tkh(30)), P._diguna(st)[1])


class TestPeristiwaBursa(unittest.TestCase):
    def jalan(self, tarikh_ev, rekod=()):
        c = siri(4, 40)
        stor = {'harga_A.csv': bar(T[:30], c[:30])}
        with tempfile.TemporaryDirectory() as d:
            ev, kr = os.path.join(d, 'peristiwa.csv'), os.path.join(d, 'kuarantin.csv')
            pd.DataFrame(dict(tarikh=[tarikh_ev], simbol=['X'], peristiwa=['tukar_nama'], nama=['X Inc'], bursa=['NASDAQ'],
                              etf=['0'], biasa=['1'])).to_csv(ev, index=False)
            for f in rekod:
                f(kr)
            stor, nota = H.gabung(stor, bar(T[25:35], c[25:35]), kuarantin=kr, bursa=ev)
            return stor['harga_A.csv'].sort_values('date'), KR.aktif(kr), nota

    def test_peristiwa_dalam_tetingkap_dikuarantin(self):
        a, aktif, nota = self.jalan(tkh(33))
        self.assertEqual(list(a.date), T[:30])                                      # bar baharu tidak ditambah
        self.assertEqual(aktif, {'X': tkh(25)})
        self.assertIn('tukar_nama', nota['kuarantin']['baru'][0][2])

    def test_peristiwa_luar_tetingkap_biasa(self):
        a, aktif, _ = self.jalan(tkh(50))
        self.assertEqual(list(a.date), T[:35])
        self.assertEqual(aktif, {})

    def test_peristiwa_sudah_ditangani_tidak_dikuarantin_semula(self):
        def rekod(kr):
            KR.tambah('X', tkh(20), 'dahulu', kr, dicatat=f'{tkh(34)} 06:00 UTC')
            KR.lepas('X', 'konsisten', kr, dicatat=f'{tkh(34)} 07:00 UTC')
        a, aktif, _ = self.jalan(tkh(33), [rekod])
        self.assertEqual(list(a.date), T[:35])
        self.assertEqual(aktif, {})


class TestSemakKuarantin(unittest.TestCase):
    """Senario SUPN: bar stor < mula ialah sejarah sebenar x 0.77591 (faktor palsu), bar >= mula ialah saham lain."""
    def sedia(self):
        sebenar = siri(5, 60)
        lain = siri(6, 60, 30.0)
        stor_bar = pd.concat([bar(T[:40], sebenar[:40] * 0.77591, 'SUPN'), bar(T[40:50], lain[40:50], 'SUPN')])
        return sebenar, lain, {'harga_B.csv': stor_bar.reset_index(drop=True)}

    def test_terkini_sahaja_kekal_beku(self):
        sebenar, lain, stor = self.sedia()
        with tempfile.TemporaryDirectory() as d:
            kr = os.path.join(d, 'kuarantin.csv'); KR.tambah('SUPN', tkh(40), 'ujian', kr)
            stor, nota = H.gabung(stor, bar(T[45:55], sebenar[45:55], 'SUPN'), kuarantin=kr)
            self.assertEqual(KR.aktif(kr), {'SUPN': tkh(40)})
            self.assertIn('SUPN', nota['kuarantin']['kekal_beku'])
        b = stor['harga_B.csv'].sort_values('date')
        self.assertEqual(int(b.date.max()), T[49])                                  # tiada bar baharu
        np.testing.assert_allclose(b.close.values[40:], lain[40:50])                # bar stor tidak disentuh

    def test_sejarah_segar_konsisten_dilepaskan(self):
        sebenar, lain, stor = self.sedia()
        with tempfile.TemporaryDirectory() as d:
            kr = os.path.join(d, 'kuarantin.csv'); KR.tambah('SUPN', tkh(40), 'ujian', kr)
            segar = bar(T[:55], sebenar[:55], 'SUPN')                               # sejarah penuh + terkini
            stor, nota = H.gabung(stor, segar, kuarantin=kr)
            self.assertEqual(KR.aktif(kr), {})
            self.assertEqual(nota['kuarantin']['dilepaskan'], [['SUPN', tkh(40)]])
            self.assertTrue(KR.dikuarantin('SUPN', tkh(45), kr))                    # selang kekal untuk statistik
            self.assertEqual(KR.muat(kr).status.tolist(), ['aktif', 'lepas'])
        b = stor['harga_B.csv'].sort_values('date')
        self.assertEqual(list(b.date), T[:55])
        np.testing.assert_allclose(b.close.values, sebenar[:55], rtol=1e-5)        # dipercayai x 1/0.77591 + bar segar
        self.assertEqual([r['keputusan'] for r in nota['log_laras']], ['lepas'])

    def test_sambungan_vendor_ditolak(self):
        # sejarah sebenar sebelum mula + bar syarikat lain (volum SAMA dengan ticker 'LAIN' dalam stor) selepasnya:
        # semakan < mula lulus, tetapi cap jari volum menolak pelepasan (senario terkini.csv 7 Nov 2026: INDV di bawah SUPN)
        sebenar, lain, _ = self.sedia()
        vol = [5_000_000 + 7919 * i for i in range(60)]
        stor = {'harga_A.csv': bar(T[40:50], lain[40:50], 'LAIN', vol[40:50]),
                'harga_B.csv': pd.concat([bar(T[:40], sebenar[:40] * 0.77591, 'SUPN'),
                                          bar(T[40:50], lain[40:50] * 0.77591, 'SUPN', vol[40:50])], ignore_index=True)}
        segar = pd.concat([bar(T[:40], sebenar[:40], 'SUPN'), bar(T[40:55], lain[40:55], 'SUPN', vol[40:55])])
        with tempfile.TemporaryDirectory() as d:
            kr = os.path.join(d, 'kuarantin.csv'); KR.tambah('SUPN', tkh(40), 'ujian', kr)
            stor, nota = H.gabung(stor, segar, kuarantin=kr)
            self.assertEqual(KR.aktif(kr), {'SUPN': tkh(40)})
            self.assertIn('berkongsi volum harian dengan LAIN (10/10 bar)', nota['kuarantin']['kekal_beku']['SUPN'])
        b = stor['harga_B.csv'].sort_values('date')
        self.assertEqual(int(b.date.max()), T[49])
        # fungsi terus: kembar yang sudah delist (tiada bar selepas T[49]) tidak dicairkan oleh bar selepasnya
        idx = H.indeks_volum({'harga_A.csv': bar(T[40:50], lain[40:50], 'LAIN', vol[40:50])}, T[40])
        self.assertEqual(H.volum_kembar(bar(T[40:60], lain[40:60], 'SUPN', vol[40:60]), idx, 'SUPN'), ('LAIN', 10, 10))
        self.assertIsNone(H.volum_kembar(bar(T[40:60], lain[40:60], 'SUPN', [123 + i for i in range(20)]), idx, 'SUPN'))
        self.assertIsNone(H.volum_kembar(bar(T[40:50], lain[40:50], 'LAIN', vol[40:50]), idx, 'LAIN'))   # diri sendiri

    def test_sejarah_segar_saham_lain_kekal_kuarantin(self):
        sebenar, lain, stor = self.sedia()
        with tempfile.TemporaryDirectory() as d:
            kr = os.path.join(d, 'kuarantin.csv'); KR.tambah('SUPN', tkh(40), 'ujian', kr)
            stor, nota = H.gabung(stor, bar(T[:55], lain[:55], 'SUPN'), kuarantin=kr)   # vendor masih sajikan saham lain
            self.assertEqual(KR.aktif(kr), {'SUPN': tkh(40)})
            self.assertIn('tidak konsisten', nota['kuarantin']['kekal_beku']['SUPN'])
        b = stor['harga_B.csv'].sort_values('date')
        np.testing.assert_allclose(b.close.values[:40], sebenar[:40] * 0.77591)
        self.assertEqual(int(b.date.max()), T[49])


if __name__ == '__main__':
    unittest.main()

# Ujian delist palsu (7 Nov 2026): posisi ditutup 'delist' HANYA apabila saham benar-benar delist menurut direktori Nasdaq
# (peristiwa 'buang', tiada dalam semasa.csv, atau ambil alih selesai) — bukan sekadar kerana bar berhenti (NEGG keluar
# daripada univ.txt pada 23 Okt 2026 dan 9 posisi Lejarnya ditutup palsu). Juga: universe harga_yf merangkumi saham posisi
# Lejar terbuka/menunggu, dan laluan ambil alih (kod/ambil_alih.py) kekal berfungsi. Tiada fail repo ditulis.
import csv, os, sys, tempfile, unittest

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
sys.path.insert(0, os.path.dirname(__file__))
import tidak_layak as TL  # noqa: E402
import harga_yf as H  # noqa: E402
import lejar  # noqa: E402
import test_ambil_alih as TA  # noqa: E402
from test_ambil_alih import saham, IX, UMUM  # noqa: E402
from test_lejar import modul, data, jalan_lejar  # noqa: E402


def bursa(semasa=(), peristiwa=None, tamat=None):
    return dict(semasa=set(semasa), peristiwa={t: sorted(v) for t, v in (peristiwa or {}).items()}, tamat=tamat or {})


def tulis_c(d, rows, nama='claude_3.csv'):
    p = os.path.join(d, nama)
    with open(p, 'w', newline='') as f:
        w = csv.DictWriter(f, TA.TestPosisi.LAJUR); w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in TA.TestPosisi.LAJUR})
    return p


def baca_c(p):
    with open(p, newline='') as f:
        return list(csv.DictReader(f))


class TestSahDelist(unittest.TestCase):
    def test_peraturan(self):
        b = bursa(semasa={'NEGG', 'SUPN', 'BARU'},
                  peristiwa={'NEGG': [('2026-10-27', 'asas')], 'KVUE': [('2026-10-27', 'asas'), ('2026-11-03', 'buang')],
                             'BARU': [('2026-10-27', 'asas'), ('2026-10-30', 'buang'), ('2026-11-02', 'tambah')]},
                  tamat={'RAMP': '2026-11-02'})
        self.assertTrue(TL.sah_delist('NEGG', '2026-11-06', None)[0])                # tiada data direktori: peraturan lama
        self.assertFalse(TL.sah_delist('NEGG', '2026-11-06', b)[0])                  # masih tersenarai
        self.assertTrue(TL.sah_delist('KVUE', '2026-11-13', b)[0])                   # buang <= S
        self.assertFalse(TL.sah_delist('KVUE', '2026-11-01', b)[0])                  # titik masa: belum dibuang pada S
        self.assertTrue(TL.sah_delist('ACA', '2026-11-06', b)[0])                    # tiada dalam semasa, tiada peristiwa
        self.assertFalse(TL.sah_delist('SUPN', '2026-11-06', b)[0])                  # tersenarai (tukar_nama bukan delist)
        self.assertTrue(TL.sah_delist('RAMP', '2026-11-06', b)[0])                   # ambil alih selesai (data/ambil_alih.csv)
        self.assertTrue(TL.sah_delist('BARU', '2026-10-31', b)[0])
        self.assertFalse(TL.sah_delist('BARU', '2026-11-03', b)[0])                  # disenaraikan semula

    def test_muat_bursa(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(TL.muat_bursa(d, senarai=[]))                           # tiada semasa.csv
            pd.DataFrame(dict(simbol=['NEGG', 'SUPN'], nama='x', bursa='NASDAQ', etf='0', biasa='1', pertama_dilihat='2026-10-27')) \
                .to_csv(os.path.join(d, 'semasa.csv'), index=False)
            pd.DataFrame(dict(tarikh=['2026-10-27', '2026-11-03', '2026-11-03'], simbol=['KVUE', 'KVUE', 'SUPN'],
                              peristiwa=['asas', 'buang', 'tukar_nama'], nama='x', bursa='NYSE', etf='0', biasa='1')) \
                .to_csv(os.path.join(d, 'peristiwa.csv'), index=False)
            b = TL.muat_bursa(d, senarai=[dict(saham='RAMP', tarikh_tamat='2026-11-02', bayaran='tunai'),
                                          dict(saham='INDV', tarikh_tamat='', bayaran='edgar'),
                                          dict(saham='ZZZ', tarikh_tamat='2026-01-01', bayaran='bukan')])
            self.assertEqual(b['semasa'], {'NEGG', 'SUPN'})
            self.assertEqual(b['peristiwa'], {'KVUE': [('2026-10-27', 'asas'), ('2026-11-03', 'buang')]})
            self.assertEqual(b['tamat'], {'RAMP': '2026-11-02'})


class TestPapertradeC(unittest.TestCase):
    def rows(self):
        return [dict(tarikh_beli=str(IX[170].date()), saham='QQZZ', kaedah='M01', harga_beli='50', keluar='False', keluar_henti='False')]

    def test_tersenarai_kekal_terbuka(self):
        g = saham(umum=None, n=180); sesi = list(IX[:195])          # 15 sesi tanpa bar
        with tempfile.TemporaryDirectory() as d:
            p = tulis_c(d, self.rows())
            tahan = []
            self.assertEqual(TL.tutup_delist(d, {'QQZZ': g}, sesi, bursa=bursa(semasa={'QQZZ'}), ditahan=tahan), [])
            self.assertEqual([(x[1], x[3]) for x in tahan], [('QQZZ', 15)])
            out = baca_c(p)
            self.assertEqual((out[0]['keluar'], out[0]['keluar_henti']), ('False', 'False'))

    def test_buang_ditutup(self):
        g = saham(umum=None, n=180); sesi = list(IX[:195])
        with tempfile.TemporaryDirectory() as d:
            p = tulis_c(d, self.rows())
            b = bursa(semasa=set(), peristiwa={'QQZZ': [(str(IX[150].date()), 'asas'), (str(IX[181].date()), 'buang')]})
            x = TL.tutup_delist(d, {'QQZZ': g}, sesi, bursa=b)
            self.assertEqual(len(x), 1)
            out = baca_c(p)
            self.assertEqual((out[0]['keluar'], out[0]['tarikh_keluar'], out[0]['keluar_henti']), ('True', str(IX[179].date()), 'True'))
            self.assertTrue(out[0]['isyarat_keluar'].startswith('Keluar: delist'))

    def test_laluan_ambil_alih_kekal(self):
        # saham sasaran ambil alih yang MASIH tersenarai dan masih ada bar: posisi dibeli selepas pengumuman tetap ditanda
        # isyarat palsu dan ditutup oleh ambil_alih.tanda_posisi (tidak bergantung pada peraturan delist)
        g = saham(n=180)
        rows = [dict(tarikh_beli=str(IX[UMUM + 2].date()), saham='QQZZ', kaedah='M02', harga_beli='70', keluar='False'),
                dict(tarikh_beli=str(IX[140].date()), saham='QQYY', kaedah='M03', harga_beli='50', keluar='False', keluar_henti='False')]
        with tempfile.TemporaryDirectory() as d:
            p = tulis_c(d, rows)
            b = bursa(semasa={'QQZZ', 'QQYY'}, tamat={'QQYY': str(IX[175].date())})   # QQYY: perjanjian selesai
            r = TL.posisi(d, {'QQZZ': g, 'QQYY': saham(umum=None, n=176)}, list(IX[:190]), tulis=True, bursa=b)
            out = baca_c(p)
        self.assertEqual(r['ambil_alih']['saham'], ['QQZZ'])
        self.assertEqual((out[0]['tidak_sah'], out[0]['keluar'], out[0]['tutup_semua']), ('True', 'True', 'True'))
        self.assertEqual(r['delist']['saham'], ['QQYY'])                            # ambil alih selesai -> delist sah
        self.assertEqual((out[1]['keluar'], out[1]['tarikh_keluar']), ('True', str(IX[175].date())))


class TestLejar(unittest.TestCase):
    def setUp(self):
        self._dua, self._bursa = lejar.DUA_LORONG, lejar.BURSA
        lejar.DUA_LORONG = True

    def tearDown(self):
        lejar.DUA_LORONG, lejar.BURSA = self._dua, self._bursa

    def jalan(self, b):
        modul('M9101'); fr, idx = data()
        akhir = fr['AAA'].index[-30]; fr['AAA'] = fr['AAA'][fr['AAA'].index <= akhir]
        lejar.BURSA = b
        T, W, tutup, _ = jalan_lejar('M9101', fr, idx)
        return akhir, fr, T, tutup

    def test_tersenarai_tiada_delist(self):
        akhir, fr, T, tutup = self.jalan(bursa(semasa={'AAA', 'BBB', 'CCC', 'DDD'}))
        self.assertFalse([p for p in tutup if p.get('sebab_keluar') == 'delist'])
        self.assertTrue([p for p in T if p['saham'] == 'AAA'])                      # kekal terbuka, ditanda ke bar akhir

    def test_buang_masa_depan_bukan_delist(self):
        # titik masa: peristiwa 'buang' selepas sesi akhir tidak menutup posisi pada sesi lebih awal
        b = bursa(semasa=set(), peristiwa={'AAA': [('2024-01-01', 'asas'), ('2099-01-01', 'buang')]})
        _, _, T, tutup = self.jalan(b)
        self.assertFalse([p for p in tutup if p.get('sebab_keluar') == 'delist'])

    def test_buang_ditutup_delist(self):
        akhir = data()[0]['AAA'].index[-30]
        b = bursa(semasa={'BBB', 'CCC', 'DDD'},
                  peristiwa={'AAA': [('2024-01-01', 'asas'), (str((akhir + pd.offsets.BDay(1)).date()), 'buang')]})
        akhir, fr, T, tutup = self.jalan(b)
        self.assertFalse(any(p['saham'] == 'AAA' for p in T))
        dl = [p for p in tutup if p.get('sebab_keluar') == 'delist']
        self.assertTrue(dl)
        for p in dl:
            self.assertEqual((p['tarikh_keluar'], p['tutup_semua']), (lejar.tkh(akhir), True))
            self.assertAlmostEqual(float(p['harga_keluar']), float(fr['AAA'].close.iloc[-1]), places=3)


class TestUniverse(unittest.TestCase):
    def test_universe_termasuk_posisi_lejar(self):
        with tempfile.TemporaryDirectory() as d:
            pd.DataFrame(dict(id_kaedah=['M01', 'M02'], saham=['ZQZQ', 'NEGG'])).to_csv(os.path.join(d, 'terbuka.csv'), index=False)
            pd.DataFrame(dict(id_kaedah=['M03'], saham=['QZQZ'])).to_csv(os.path.join(d, 'tunggu.csv'), index=False)
            self.assertEqual(H.saham_lejar(d), {'ZQZQ', 'NEGG', 'QZQZ'})
            s, idx = H.universe(lejar_dir=d)
            self.assertIn('ZQZQ', s); self.assertIn('QZQZ', s); self.assertIn('NEGG', s)
            self.assertNotIn('SPY', s); self.assertEqual(idx, ['SPY', 'QQQ'])
            self.assertEqual(H.saham_lejar(os.path.join(d, 'tiada')), set())


if __name__ == '__main__':
    unittest.main()

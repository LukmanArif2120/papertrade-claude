"""Ujian dokumen db dashboard `carian/f_utama` (standard/f_utama_db.py) dan pembacanya dalam dashboard_v2.html
(Rujukan -> Setup F, v181, 16 Nov 2026)."""
import os
import sys
import tempfile
import unittest

import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SINI, '..', 'standard'))
import f_utama_db as F  # noqa: E402
from bahagi_db import HAD_DB, bait  # noqa: E402

CS13 = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS13')
HTML = os.path.join(SINI, '..', 'standard', 'dashboard_v2.html')


class TestFUtamaDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = F.bina()
        cls.U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv'))

    def test_bentuk_dan_bilangan(self):
        d, U = self.d, self.U
        self.assertEqual(d['kol'], F.KOL)
        self.assertEqual((d['n'], len(d['rows'])), (len(U), len(U)))
        self.assertEqual(d['n_pilihan'], int(U.pilihan.sum()))
        self.assertEqual((d['n_lama'], d['n_baharu']), (int((U.asal == 'lama').sum()), int((U.asal == 'baharu').sum())))
        self.assertTrue(all(len(r) == len(F.KOL) for r in d['rows']))
        self.assertEqual([r[0] for r in d['rows']], U.id.tolist())               # susunan senarai utama dikekalkan
        self.assertEqual(set(d['semak_masa']), {'pilih', 'lain'})

    def test_nyahkod_sepadan_dengan_sumber(self):
        d, U = self.d, self.U.set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        for r in d['rows'][:50] + d['rows'][-50:]:
            u = U.loc[r[ix['id']]]
            self.assertEqual(bool(r[ix['pil']]), bool(u.pilihan))
            self.assertEqual('baharu' if r[ix['asal']] else 'lama', u.asal)
            self.assertAlmostEqual(r[ix['tangkap']] / 1000, u.terus, delta=6e-4)
            self.assertAlmostEqual(r[ix['menang']] / 1000, u.menang_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['purata']] / 10000, u.purata_B, delta=6e-5)
            pra = d['kamus']['pra'][r[ix['pra']]]
            self.assertEqual(pra, '' if pd.isna(u.prasyarat) else u.prasyarat)

    def test_lajur_v182_sepadan_dengan_sumber(self):
        """Lajur v182 (jenis, am5, k10, k1, k2) dan median kawalan dibaca terus daripada CSV CS13, tanpa kiraan baharu."""
        d, U = self.d, self.U.set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kamus']['jenis'], F.JENIS)
        for r in d['rows'][:50] + d['rows'][-50:]:
            u = U.loc[r[ix['id']]]
            self.assertAlmostEqual(r[ix['am5']] / 1000, u.a_m5, delta=6e-4)
            self.assertAlmostEqual(r[ix['k10']] / 1000, u.k10_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['k1']] / 10000, u.kl_terus_K1, delta=6e-5)
            self.assertAlmostEqual(r[ix['k2']] / 10000, u.kl_terus_K2, delta=6e-5)
            self.assertEqual(r[ix['jenis']], F.jenis(u.nama))
        self.assertEqual(F.jenis('K13.009 Stochastic(14) silang naik'), 0)
        self.assertEqual(F.jenis('M105 Supertrend tulen'), 1)
        self.assertEqual(F.jenis('N16 RSI2<10 tanpa penapis'), 6)
        K = pd.read_csv(os.path.join(CS13, 'kawalan.csv'))
        K = K[K.layak.astype(bool)]
        self.assertEqual(d['kawalan']['n'], len(K))
        self.assertAlmostEqual(d['kawalan']['menang'], K.menang_B.median(), places=3)

    def test_cara_pegang_kedua(self):
        """Keputusan pengguna 16 Nov 2026 ("B" selepas CS14): lajur "pegang lebih lama" (r0.t2.0) di sebelah cara sekarang."""
        d = self.d
        X = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS14', 'setup.csv.gz')).set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:17], ['id', 'asal', 'pil', 'pra', 'nama', 'pen', 'beli', 'shar', 'tangkap', 'rawak', 'm5', 'menang', 'purata',
                                         'rugi15', 'hari', 'k3', 'n'])                      # lajur lama tidak berganjak (halaman lama masih membaca)
        self.assertEqual(d['kol'][17:21], ['menang2', 'purata2', 'rugi2', 'hari2'])
        self.assertEqual(d['kol'][21:26], ['jenis', 'am5', 'k10', 'k1', 'k2'])  # v182 reka bentuk, selepas CS14
        self.assertEqual((F.CARA1, F.CARA2), ('r0.t1.126', 'r0.t2.0'))
        for r in d['rows'][:40] + d['rows'][-40:]:
            x = X.loc[r[ix['id']]]
            self.assertAlmostEqual(r[ix['menang2']] / 1000, x['r0.t2.0:menang'], delta=6e-4)
            self.assertAlmostEqual(r[ix['purata2']] / 10000, x['r0.t2.0:purata'], delta=6e-5)
            self.assertAlmostEqual(r[ix['rugi2']] / 1000, x['r0.t2.0:rugi15'], delta=6e-4)
            self.assertEqual(r[ix['hari2']], int(round(x['r0.t2.0:sesi_med'])))
            self.assertAlmostEqual(r[ix['menang']] / 1000, x['r0.t1.126:menang'], delta=6e-4)   # cara sekarang = angka CS14 yang sama
        b = d['banding']
        self.assertEqual(set(b), {'kini', 'lama', 'rawak_kini', 'rawak_lama'})
        self.assertGreater(b['lama']['purata'], b['kini']['purata'])                       # pegang lebih lama: purata naik ...
        self.assertLess(b['lama']['menang'], b['kini']['menang'])                           # ... dan kadar menang turun
        self.assertIn('minimum, bukan had', d['pegang'])
        self.assertIn('purata 50 hari', d['pegang2'])

    def test_lajur_solid_cs16(self):
        """CS16 "ujian solid" (pindaan (z), 16 Nov 2026): lajur di HUJUNG `kol`, dibaca terus daripada hasil/CS16/solid.csv.gz."""
        d = self.d
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:26], F.KOL[:26])                                       # lajur sedia ada tidak berganjak
        self.assertEqual(d['kol'][26:], ['solid', 'wakil', 'boleh', 'm10', 'am10', 'm10d', 'am10d', 'tpos', 'tbil', 'rugi8', 'serupa'])
        Z = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS16', 'solid.csv.gz')).set_index('id')
        self.assertEqual(sum(r[ix['wakil']] for r in d['rows']), int(Z.wakil.sum()))
        self.assertEqual(sum(r[ix['solid']] for r in d['rows']), int(Z.solid.sum()))
        self.assertEqual((d['solid']['n_wakil'], d['solid']['n_solid']), (224, 290))
        for r in d['rows'][:60] + d['rows'][-60:] + [x for x in d['rows'] if x[0] in ('F43', 'F58', 'F89')]:
            z = Z.loc[r[ix['id']]]
            self.assertEqual(bool(r[ix['solid']]), bool(z.solid))
            self.assertEqual(bool(r[ix['wakil']]), bool(z.wakil))
            self.assertEqual(bool(r[ix['boleh']]), bool(z.boleh_dibuat))
            for k, a in (('m10', 'm10'), ('am10', 'a_m10'), ('m10d', 'm10d'), ('am10d', 'a_m10d'), ('rugi8', 'rugi8')):
                self.assertAlmostEqual(r[ix[k]] / 1000, z[a], delta=6e-4, msg=k)
            self.assertEqual((r[ix['tpos']], r[ix['tbil']]), (int(z.thn_pos), int(z.thn_bil)))
            self.assertEqual(r[ix['serupa']], None if pd.isna(z.serupa_dengan) else z.serupa_dengan)
        f43 = [x for x in d['rows'] if x[0] == 'F43'][0]
        self.assertEqual(f43[ix['solid']], 0)                                             # F43 TIDAK solid (gagal S5)
        a = d['solid']['asas']                                                            # "laporan kewangan 1-5 sesi" sahaja
        self.assertEqual(a['prasyarat'], F.ASAS_EARN)
        self.assertAlmostEqual(a['m5'], 0.2404, places=3)
        self.assertAlmostEqual(a['a_m5'], 0.135, places=3)

    def test_saiz_di_bawah_had_db(self):
        with tempfile.TemporaryDirectory() as t:
            out = F.main(['--keluar', t])
            self.assertGreaterEqual(len(out), 1)
            self.assertEqual(out[0]['doc_id'], 'f_utama')
            for o in out:
                self.assertEqual(o['collection'], 'carian')
                self.assertLess(o['bait'], HAD_DB)
                self.assertTrue(os.path.exists(o['file_path']))
        self.assertLess(bait(self.d), 2 * HAD_DB)

    def test_halaman_membaca_dengan_subbhg(self):
        """Dokumen ini dibahagi dengan bahagi(); halaman MESTI membacanya dengan subBhg() (pelajaran jana_db.PECAH)."""
        h = open(HTML, encoding='utf-8').read()
        self.assertIn("subBhg('carian/f_utama','sf',['setupf'])", h)
        self.assertIn('<section class="view" id="v-setupf" hidden></section>', h)
        self.assertIn("['setupf','Setup F']", h)
        self.assertIn('setupf:renderSetupF', h)
        for k in F.KOL:                                                         # setiap lajur yang dibaca halaman wujud dalam dokumen
            if k not in ('beli', 'n', 'm5'):
                self.assertRegex(h, r"ix\.%s\b|'%s'" % (k, k), k)


if __name__ == '__main__':
    unittest.main()

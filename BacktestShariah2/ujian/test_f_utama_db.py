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

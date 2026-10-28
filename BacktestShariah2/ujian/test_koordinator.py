# Ujian halaman koordinator (standard/koordinator.py): keputusan terbuka, umur/tanda kesegaran,
# amaran salinan kerja lama, dan seksyen wajib dalam KOORDINATOR.md.
import os, sys, tempfile, unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import koordinator as ko


class TestKoordinator(unittest.TestCase):
    def test_umur_dan_tanda(self):
        hari_ini = date.today()
        self.assertEqual(ko._umur(hari_ini.strftime('%Y-%m-%d')), 0)
        self.assertEqual(ko._umur(hari_ini.strftime('%Y%m%d')), 0)
        self.assertEqual(ko._umur((hari_ini - timedelta(days=5)).strftime('%Y-%m-%d')), 5)
        self.assertIsNone(ko._umur(''))
        self.assertIsNone(ko._umur('bukan tarikh'))
        self.assertEqual(ko._tanda(0), 'OK')
        self.assertEqual(ko._tanda(ko.LEWAT_HARI), 'OK')
        self.assertIn('LEWAT', ko._tanda(ko.LEWAT_HARI + 1))
        self.assertEqual(ko._tanda(None), 'tiada')

    def test_keputusan_hanya_terbuka(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'k.csv')
            with open(p, 'w', encoding='utf-8') as f:
                f.write('tarikh,perkara,status,catatan\n'
                        '2026-01-01,A,terbuka,x\n2026-01-02,B,selesai,y\n2026-01-03,C,terbuka,z\n')
            asal = ko.KEPUTUSAN
            try:
                ko.KEPUTUSAN = p
                r = ko.keputusan_terbuka()
            finally:
                ko.KEPUTUSAN = asal
        self.assertEqual([x['perkara'] for x in r], ['A', 'C'])

    def test_keputusan_fail_tiada_tidak_meletup(self):
        asal = ko.KEPUTUSAN
        try:
            ko.KEPUTUSAN = '/tiada/fail/keputusan.csv'
            self.assertEqual(ko.keputusan_terbuka(), [])
        finally:
            ko.KEPUTUSAN = asal

    def test_jadual_md(self):
        t = ko.jadual_md([('a', 1, None)], ['X', 'Y', 'Z'])
        self.assertTrue(t.startswith('| X | Y | Z |'))
        self.assertIn('| a | 1 |  |', t)

    def test_git_keadaan_pulangkan_empat_nilai(self):
        cab, head, blkg, ref = ko.git_keadaan()
        self.assertIsInstance(cab, str)
        self.assertTrue(blkg is None or isinstance(blkg, int))

    def test_main_tulis_semua_seksyen(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, 'KOORDINATOR.md')
            os.environ['KOORDINATOR_OUT'] = out
            asal = ko.KELUAR
            try:
                ko.KELUAR = out
                self.assertEqual(ko.main(), 0)
                t = open(out, encoding='utf-8').read()
            finally:
                ko.KELUAR = asal
                os.environ.pop('KOORDINATOR_OUT', None)
        for tajuk in ('## 0. Salinan kerja', '## 1. Perlu keputusan anda',
                      '## 2. Kajian REVERSE', '## 3. Operasi repo', '## 4. Kesegaran data',
                      '## 5. Workflow berjadual', '## 6. Status kajian', '## 7. Jangan ulangi'):
            self.assertIn(tajuk, t)
        self.assertIn('Jangan ubah manual', t)
        # Dua jejak mesti dipisahkan secara eksplisit (kesilapan 28 Okt 2026).
        self.assertIn('BUKAN kaedah Mxx', t)
        self.assertIn('bukan Lejar Penuh', t)


    def test_sec_titik_masa_retrospektif(self):
        # SPEC_FASA2.md §4.1: SEC = nilai pertama difail, jadi liputannya sejarah (bukan ~1 hari seperti RS/gred).
        # Pernah tersalah dilaporkan "tidak cukup" dan menyebabkan leg SEC ditangguh ke Okt 2027.
        f2 = {r['sumber']: r for r in ko.ambang_fasa2()}
        for nama in ('SEC EPS/hasil', 'SEC earnings 8-K'):
            self.assertTrue(f2[nama].get('sec'), nama)
            self.assertGreater(f2[nama]['hari'], ko.F2_HARI, nama)
            self.assertEqual(f2[nama]['sedia'], 'ya', nama)
            self.assertLess(f2[nama]['mula'], '2010-01-01', nama)

    def test_liputan_sec_dilapor(self):
        ada, univ, _ = ko.liputan_sec()
        self.assertGreater(ada, 0)
        self.assertTrue(univ is None or univ >= ada)


if __name__ == '__main__':
    unittest.main()

# Ujian F7: jana_db.py atas fikstur AUTOTUNE/dashboard/contoh (output sebenar laporan.py/pengesahan.py atas data palsu).
#   python3 -m unittest AUTOTUNE/dashboard/test_jana_db.py
import json, os, shutil, sys, tempfile, unittest

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import jana_db as J


class TestJanaDb(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_contoh(self):
        idx = J.main(['--hasil', os.path.join(DIR, 'contoh'), '--keluar', self.d, '--dibina', '2026-10-17T00:00Z'])
        ids = {i['doc_id'] for i in idx}
        self.assertTrue({'status', 'ringkasan', 'gabungan', 'kaedah_M01'} <= ids)
        for i in idx:
            self.assertEqual(i['collection'], 'autotune')
            self.assertLess(i['bait'], J.HAD_DB)
        ring = json.load(open(os.path.join(self.d, 'autotune', 'ringkasan.json')))
        self.assertTrue(ring['contoh'])
        self.assertEqual(ring['kaveat'], J.KAVEAT)
        self.assertEqual(sorted(ring['kaedah_doc']), sorted(x for x in ids if x.startswith('kaedah_')))
        self.assertEqual(sum(ring['kiraan_label'].values()), ring['n_kaedah'])
        gab = json.load(open(os.path.join(self.d, 'autotune', 'gabungan.json')))
        self.assertEqual(gab['dibina'], ring['dibina'])
        self.assertIn('ekuiti_bulanan', gab); self.assertNotIn('param_semasa_penuh', gab)
        b = json.load(open(os.path.join(self.d, '_batch_0.json')))
        self.assertTrue(all(w['op'] == 'set' and os.path.isabs(w['file_path']) for w in b))

    def test_tanpa_f6(self):
        idx = J.main(['--hasil', os.path.join(self.d, 'kosong'), '--keluar', os.path.join(self.d, 'o')])
        self.assertEqual([i['doc_id'] for i in idx], ['status'])

    def test_versi_dan_batch(self):
        h = os.path.join(self.d, 'h'); os.makedirs(h)
        papan = dict(dijana='x', tempoh={}, gabungan=[],
                     kaedah=[dict(id=f'M{i}', nama='n', label='GAGAL', cagr_a=float('nan')) for i in range(120)])
        json.dump(papan, open(os.path.join(h, 'papan.json'), 'w'))
        o = os.path.join(self.d, 'o')
        J.main(['--hasil', h, '--keluar', o])
        v = os.path.join(self.d, 'v.json'); json.dump({'autotune/status': 3}, open(v, 'w'))
        J.main(['--hasil', h, '--keluar', o, '--versi', v])
        ix = json.load(open(os.path.join(o, '_indeks.json')))
        self.assertEqual(len(ix['batch']), 3)  # 122 dokumen, ≤ 50 setiap batch
        semua = [w for p in ix['batch'] for w in json.load(open(p if os.path.isabs(p) else os.path.join(J.REPO, p)))]
        self.assertEqual(len(semua), 122)
        self.assertEqual([w.get('if_version') for w in semua if w['doc_id'] == 'status'], [3])
        k = json.load(open(os.path.join(o, 'autotune', 'kaedah_M0.json')))
        self.assertIsNone(k['cagr_a'])


if __name__ == '__main__':
    unittest.main()

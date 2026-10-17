# Ujian F8 (tala semula suku): cadangan.py dengan fixture kecil, jalan.py (label/laluan), YAML workflow.
import os, sys, json, csv, shutil, tempfile, unittest, datetime

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'suku'))
import cadangan, jalan

WF = os.path.join(AKAR, '.github', 'workflows', 'autotune_suku.yml')


def k13(mid, params, cagr, mdd, status='SIAP', asal=None, lulus=True, tala=('a', 'b'), belum=False):
    H = dict(kaedah=mid, kajian=13, status=status, params=params, tala=list(tala), belum_ditala=belum, ada_lulus=lulus,
             latih_A=dict(cagr=cagr, mdd=mdd))
    if asal: H['latih_A_asal'] = dict(cagr=asal[0], mdd=asal[1])
    return H


class TestCadangan(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.q = '2027-Q1'

    def tearDown(self): shutil.rmtree(self.d, ignore_errors=True)

    def tulis(self, rel, obj):
        f = os.path.join(self.d, rel); os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w') as fh: json.dump(obj, fh)

    def baru(self, mid, H): self.tulis(f'suku/{self.q}/tala/{mid}/k13.json', H)
    def lama(self, mid, H): self.tulis(f'tala/{mid}/k13.json', H)

    def test_beza_param(self):
        self.assertEqual(cadangan.beza_param({'a': 1, 'b': 2.0}, {'a': 1, 'b': 2.0000000001}), {})
        self.assertEqual(cadangan.beza_param({'a': 1, 'b': 2.0}, {'a': 3, 'b': 2.0}), {'a': [1, 3]})
        self.assertEqual(cadangan.beza_param({'a': 1}, {'a': 1, 'c': 5}), {'c': [None, 5]})

    def test_jana_pelbagai_kes(self):
        self.lama('M01', k13('M01', dict(a=10, b=1.5), 0.10, -0.30))
        self.baru('M01', k13('M01', dict(a=12, b=1.5), 0.15, -0.25))                   # UBAH
        self.lama('M02', k13('M02', dict(a=5, b=2), 0.20, -0.20))
        self.baru('M02', k13('M02', dict(a=5, b=2), 0.21, -0.19))                      # KEKAL
        self.baru('M03', k13('M03', dict(a=7, b=1), 0.12, -0.2, asal=(0.05, -0.4)))    # TIADA ASAS (tiada lama/sedia)
        self.baru('M04', k13('M04', {}, None, None, status='RALAT'))                   # GAGAL
        self.baru('M05', k13('M05', {}, 0.1, -0.2, tala=(), belum=True))               # BELUM DITALA
        self.lama('M06', k13('M06', dict(a=1, b=1), 0.1, -0.2))
        self.baru('M06', k13('M06', dict(a=2, b=1), 0.1, -0.2, lulus=False))           # KEKAL (tiada calon lulus)
        with open(os.path.join(self.d, 'parameter_sedia.csv'), 'w', newline='') as fh:  # M07: asas daripada csv
            w = csv.writer(fh); w.writerow(['kaedah', 'label', 'param_semasa'])
            w.writerow(['M07', 'TINGGI', json.dumps(dict(a=1, b=1)).replace('"', '"')])
        self.baru('M07', k13('M07', dict(a=1, b=9), 0.3, -0.1, asal=(0.2, -0.3)))
        C = cadangan.jana(self.q, self.d)
        T = {r['kaedah']: r for r in C['kaedah']}
        self.assertEqual([r['kaedah'] for r in C['kaedah']], ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07'])
        self.assertEqual({k: r['tindakan'] for k, r in T.items()},
                         dict(M01='UBAH', M02='KEKAL', M03='TIADA ASAS', M04='GAGAL', M05='BELUM DITALA',
                              M06='KEKAL (tiada calon lulus)', M07='UBAH'))
        self.assertEqual(T['M01']['ubah'], {'a': [10, 12]})
        self.assertEqual(T['M01']['rujuk'], 'k13'); self.assertAlmostEqual(T['M01']['delta_cagr'], 0.05)
        self.assertEqual(T['M07']['sumber_lama'], 'parameter_sedia'); self.assertEqual(T['M07']['rujuk'], 'asal')
        self.assertEqual(T['M07']['label'], 'TINGGI')
        self.assertEqual(C['kira']['UBAH'], 2)

    def test_tulis_fail_dan_had_baris(self):
        for i in range(1, 201):   # 200 kaedah semuanya berubah → jadual dipotong, ≤120 baris
            m = f'M{i:03d}'
            self.lama(m, k13(m, dict(a=1, b=2), 0.1, -0.3)); self.baru(m, k13(m, dict(a=2 + i, b=2), 0.1 + i / 1000, -0.2))
        cadangan.main(['--suku', self.q, '--hasil', self.d])
        md = open(os.path.join(self.d, 'suku', self.q, 'CADANGAN.md')).read()
        self.assertLessEqual(len(md.splitlines()), 120)
        self.assertIn('Cadangan sahaja; perlu kelulusan pengguna', md)
        self.assertIn('kaedah lagi', md)
        J = json.load(open(os.path.join(self.d, 'suku', self.q, 'cadangan.json')))
        self.assertEqual(J['n_kaedah'], 200); self.assertEqual(J['nota'], 'cadangan sahaja; perlu kelulusan pengguna')
        # hanya fail dalam hasil/suku/<Q>/ ditulis; hasil/tala lama tidak disentuh
        self.assertEqual(sorted(os.listdir(os.path.join(self.d, 'tala')))[:1], ['M001'])
        self.assertEqual(os.listdir(os.path.join(self.d, 'tala', 'M001')), ['k13.json'])

    def test_kosong_dan_label_tidak_sah(self):
        C = cadangan.jana(self.q, self.d)
        self.assertEqual(C['n_kaedah'], 0)
        self.assertIn('Tiada cadangan ubah', cadangan.tulis_md(C))
        with self.assertRaises(ValueError): cadangan.jana('2027-Q5', self.d)


class TestJalan(unittest.TestCase):
    def test_label(self):
        self.assertEqual(jalan.label_suku(datetime.date(2027, 1, 2)), '2027-Q1')
        self.assertEqual(jalan.label_suku(datetime.date(2026, 10, 3)), '2026-Q4')
        self.assertEqual(jalan.label_suku(datetime.date(2026, 7, 4)), '2026-Q3')
        with self.assertRaises(ValueError): jalan.sah_label('2026-Q9')
        with self.assertRaises(ValueError): jalan.sah_label('../x')

    def test_dir_output_berasingan(self):
        d = jalan.dir_tala('2026-Q4')
        self.assertTrue(d.replace(os.sep, '/').endswith('AUTOTUNE/hasil/suku/2026-Q4/tala'))
        self.assertNotEqual(os.path.normpath(d), os.path.normpath(os.path.join(jalan.HASIL, 'tala')))


class TestWorkflow(unittest.TestCase):
    def test_yaml(self):
        try: import yaml
        except ImportError: self.skipTest('PyYAML tiada')
        W = yaml.safe_load(open(WF))
        on = W.get('on', W.get(True))   # YAML 1.1: kunci `on` menjadi True
        self.assertEqual(on['schedule'][0]['cron'], '17 3 1-7 1,4,7,10 6')
        self.assertIn('workflow_dispatch', on)
        self.assertEqual(W['concurrency']['group'], 'autotune-suku')
        self.assertEqual(W['jobs']['tala']['timeout-minutes'], 355)
        self.assertEqual(sorted(W['jobs']), ['cadangan', 'data', 'pintu', 'rancang', 'tala'])
        t = open(WF).read()
        self.assertIn('git add AUTOTUNE/hasil/suku', t)
        self.assertNotIn('git add AUTOTUNE/hasil/tala', t)
        self.assertNotIn('group: autotune-tala', t)


if __name__ == '__main__':
    unittest.main()

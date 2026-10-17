import glob, json, os, re, unittest

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KATALOG = os.path.join(BS2, 'standard', 'katalog_kaedah.json')
MEDAN = ['id', 'nama', 'varian', 'pencipta', 'sumber', 'masuk', 'keluar', 'pegang', 'henti']


class TestKatalogKaedah(unittest.TestCase):
    """Katalog tab Kaedah (db kaedah/katalog) mesti meliputi setiap modul kod/kaedah/Mxx.py."""

    def setUp(self):
        with open(KATALOG, encoding='utf-8') as f:
            self.doc = json.load(f)

    def test_semua_modul_ada(self):
        modul = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(BS2, 'kod', 'kaedah', 'M*.py'))}
        ada = {r['id'] for r in self.doc['rows']}
        self.assertEqual(sorted(modul - ada, key=lambda x: int(x[1:])), [], 'modul tiada dalam katalog')
        self.assertEqual(sorted(ada - modul, key=lambda x: int(x[1:])), [], 'katalog ada ID tanpa modul')

    def test_medan_lengkap_dan_unik(self):
        ids = [r['id'] for r in self.doc['rows']]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.doc['rows']:
            for m in MEDAN:
                self.assertTrue(str(r.get(m, '')).strip(), f'{r.get("id")}: medan {m} kosong')

    def test_nama_sama_dengan_kod(self):
        for r in self.doc['rows']:
            with open(os.path.join(BS2, 'kod', 'kaedah', r['id'] + '.py'), encoding='utf-8') as f:
                m = re.search(r'^NAMA\s*=\s*([\'"])(.*?)\1', f.read(), re.M)
            self.assertIsNotNone(m, r['id'])
            self.assertEqual(r['nama'], m.group(2), r['id'])

    def test_saiz_dokumen_db(self):
        self.assertLess(len(json.dumps(self.doc, ensure_ascii=False, separators=(',', ':')).encode()), 240_000)


if __name__ == '__main__':
    unittest.main()

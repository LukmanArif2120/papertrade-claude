import csv, glob, json, os, re, unittest

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KATALOG = os.path.join(BS2, 'standard', 'katalog_kaedah.json')
MEDAN = ['id', 'nama', 'varian', 'varian_kod', 'pencipta', 'sumber', 'masuk', 'keluar', 'pegang', 'henti']
# Tiga keluarga kaedah sejak 1 Nov 2026 (sama seperti harian_c.POLA_KAEDAH).
POLA = ('M*.py', 'N*.py', 'GB*.py')
KELUARGA = {'M': 0, 'N': 1, 'GB': 2}


def kunci(mid):
    """Kunci susunan merentas keluarga; `int(mid[1:])` gagal pada awalan dua aksara ('GB02')."""
    i = 0
    while i < len(mid) and not mid[i].isdigit():
        i += 1
    try:
        return (KELUARGA.get(mid[:i], 9), int(mid[i:]))
    except ValueError:
        return (KELUARGA.get(mid[:i], 9), 10 ** 6)


class TestKatalogKaedah(unittest.TestCase):
    """Katalog tab Kaedah mesti meliputi setiap modul kod/kaedah/{M,N,GB}xx.py."""

    def setUp(self):
        with open(KATALOG, encoding='utf-8') as f:
            self.doc = json.load(f)

    def test_semua_modul_ada(self):
        modul = {os.path.basename(p)[:-3]
                 for pola in POLA for p in glob.glob(os.path.join(BS2, 'kod', 'kaedah', pola))}
        ada = {r['id'] for r in self.doc['rows']}
        self.assertEqual(sorted(modul - ada, key=kunci), [], 'modul tiada dalam katalog')
        self.assertEqual(sorted(ada - modul, key=kunci), [], 'katalog ada ID tanpa modul')
        self.assertTrue(any(not m.startswith('M') for m in modul),
                        'tiada modul Nxx/GBxx dijumpai — glob POLA mungkin rosak')

    def test_medan_lengkap_dan_unik(self):
        ids = [r['id'] for r in self.doc['rows']]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.doc['rows']:
            for m in MEDAN:
                self.assertTrue(str(r.get(m, '')).strip(), f'{r.get("id")}: medan {m} kosong')

    def test_nama_sama_dengan_kod(self):
        for r in self.doc['rows']:
            with open(os.path.join(BS2, 'kod', 'kaedah', r['id'] + '.py'), encoding='utf-8') as f:
                kod = f.read()
            m = re.search(r'^NAMA\s*=\s*([\'"])(.*?)\1', kod, re.M)
            self.assertIsNotNone(m, r['id'])
            self.assertEqual(r['nama'], m.group(2), r['id'])
            v = re.search(r'^VARIAN\s*=\s*([\'"])(.*?)\1', kod, re.M)
            self.assertEqual(r['varian_kod'], v.group(2), r['id'])

    def test_varian_kod_ada_dalam_registry(self):
        """Lajur Backtest tab Kaedah memadankan registry set 431 dengan varian_kod.

        Hanya Mxx: kaedah Nxx/GBxx TIADA backtest set 431 dengan sengaja — buktinya ialah
        `REVERSE/silang_akhir.csv` (jangkaan setiap dagangan, dua tingkap, BH-FDR), bukan
        set 431. Lajur backtest Papan Penganalisis kekal kosong bagi mereka, dan
        `penganalisis.muat_registry` sudah mengendalikannya (`REG.get(mid) or {}`).
        """
        mxx = [r for r in self.doc['rows'] if r['id'].startswith('M')]
        self.assertGreater(len(mxx), 100, 'baris Mxx hilang — penapis terlalu ketat')
        for r in mxx:
            with open(os.path.join(BS2, 'kod', 'registry', r['id'] + '.csv'), encoding='utf-8') as f:
                ada = [x for x in csv.DictReader(f) if x['set'] == '431' and x['varian'] == r['varian_kod']]
            self.assertEqual(len(ada), 1, r['id'])

    def test_nxx_tiada_registry_431(self):
        """Pasangan songsang: kalau Nxx mula ada registry 431, keputusan itu mesti disengajakan."""
        for r in self.doc['rows']:
            if r['id'].startswith('M'):
                continue
            self.assertFalse(
                os.path.exists(os.path.join(BS2, 'kod', 'registry', r['id'] + '.csv')),
                f"{r['id']}: registry 431 muncul — kemas test_varian_kod_ada_dalam_registry")

    def test_saiz_dokumen_db(self):
        self.assertLess(len(json.dumps(self.doc, ensure_ascii=False, separators=(',', ':')).encode()), 240_000)


if __name__ == '__main__':
    unittest.main()

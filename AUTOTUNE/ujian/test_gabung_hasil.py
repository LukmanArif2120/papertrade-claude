# Ujian gabung_hasil.py: peraturan versi terbaik, fail rosak diabaikan, tulisan atomik, _masa.csv dibina semula.
import os, sys, json, shutil, tempfile, unittest

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'tala'))
import gabung_hasil as G


def tulis(d, H, mentah=None):
    f = os.path.join(d, H['kaedah'], f"k{H['kajian']:02d}.json"); os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, 'w') as fh: fh.write(mentah if mentah is not None else json.dumps(H))
    return f


def H(mid='M01', k=0, status='SIAP', n=120, sas=120, diminta=120, mula='2026-10-17T10:00:00Z', **kw):
    return dict(kaedah=mid, kajian=k, status=status, n_trials=n, n_sasaran=sas, n_trials_diminta=diminta, mula=mula,
                masa={'s_percubaan': 1.0, 'jumlah': 100.0}, **kw)


class UjiGabung(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(); self.keluar = os.path.join(self.t, 'repo')
        self.a = os.path.join(self.t, 'a'); self.b = os.path.join(self.t, 'b')
        for d in (self.keluar, self.a, self.b): os.makedirs(d)

    def tearDown(self): shutil.rmtree(self.t)

    def baca(self, mid, k):
        return json.load(open(os.path.join(self.keluar, mid, f'k{k:02d}.json')))

    def test_peraturan_terbaik(self):
        # M01: lengkap terbaharu menang atas lengkap lama dan separa
        tulis(self.keluar, H(mula='2026-10-16T00:00:00Z', skor=1))
        tulis(self.a, H(mula='2026-10-18T00:00:00Z', skor=2))
        tulis(self.b, H(n=60, mula='2026-10-19T00:00:00Z', skor=3))
        # M02: separa dengan n_trials terbanyak menang atas RALAT
        tulis(self.keluar, H('M02', status='RALAT', n=0, mula='2026-10-19T00:00:00Z'))
        tulis(self.a, H('M02', n=40, skor=4)); tulis(self.b, H('M02', n=80, skor=5))
        # M03: hanya RALAT → RALAT dikekalkan
        tulis(self.a, H('M03', status='RALAT', n=0))
        C = G.gabung([self.a, self.b], self.keluar, percubaan=120)
        self.assertEqual(self.baca('M01', 0)['skor'], 2)
        self.assertEqual(self.baca('M02', 0)['skor'], 5)
        self.assertEqual(self.baca('M03', 0)['status'], 'RALAT')
        self.assertEqual((C['lengkap'], C['separa'], C['RALAT'], C['perlu_kerja']), (1, 1, 1, 2))
        self.assertTrue(os.path.exists(os.path.join(self.keluar, '_masa.csv')))

    def test_fail_rosak_diabaikan(self):
        panjang = json.dumps(H(skor=7, nota='x' * 500))
        pendek = json.dumps(H(status='RALAT', n=0))
        rosak = pendek + panjang[len(pendek):]          # "Extra data": RALAT pendek + ekor fail panjang
        tulis(self.keluar, H(), mentah=rosak)
        tulis(self.a, H(), mentah='{"kaedah": "M01", "kaj')   # terpotong
        tulis(self.b, H(n=50, sas=120, skor=8))
        tulis(self.a, H('M09'), mentah=rosak.replace('M01', 'M09'))   # tiada versi sah → dibuang
        C = G.gabung([self.a, self.b], self.keluar)
        self.assertEqual(self.baca('M01', 0)['skor'], 8)
        self.assertEqual(C['rosak_diabai'], 3)
        self.assertFalse(os.path.exists(os.path.join(self.keluar, 'M09', 'k00.json')))

    def test_lengkap_120_atas_lengkap_20(self):
        tulis(self.a, H(n=20, sas=20, diminta=20, mula='2026-10-19T00:00:00Z', skor=1))
        tulis(self.b, H(mula='2026-10-17T00:00:00Z', skor=2))
        G.gabung([self.a, self.b], self.keluar, masa_csv=False)
        self.assertEqual(self.baca('M01', 0)['skor'], 2)

    def test_laluan_tidak_sepadan_ditolak(self):
        tulis(self.a, H('M05', k=3), mentah=json.dumps(H('M05', k=4)))
        self.assertIsNone(G.baca(os.path.join(self.a, 'M05', 'k03.json')))

    def test_versi_kod_semasa_didahulukan(self):
        """Pindaan 18 Okt 2026: hasil dengan versi_kod = fail kaedah semasa menang atas hasil lama (kod lain)."""
        dk = os.path.join(self.t, 'kaedah'); os.makedirs(dk)
        with open(os.path.join(dk, 'M81.py'), 'w') as fh: fh.write('# dibaiki\n')
        v = G.versi_kod('M81', dk)
        tulis(self.keluar, H('M81', diminta=500, mula='2026-10-19T00:00:00Z', skor=1))          # lama, tiada versi_kod
        tulis(self.a, H('M81', mula='2026-10-18T00:00:00Z', skor=2, versi_kod=v))
        tulis(self.b, H('M81', mula='2026-10-20T00:00:00Z', skor=3, versi_kod='lain'))
        G.gabung([self.a, self.b], self.keluar, masa_csv=False, dir_kaedah=dk)
        self.assertEqual(self.baca('M81', 0)['skor'], 2)
        sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'tala'))
        import pekerja
        f = os.path.join(self.keluar, 'M81', 'k00.json')
        self.assertTrue(pekerja._sudah(f, 120))
        self.assertTrue(pekerja._sudah(f, 120, v))
        self.assertFalse(pekerja._sudah(f, 120, 'lain'))


if __name__ == '__main__':
    unittest.main()

# Ujian F2: salinan berparameter AUTOTUNE/kaedah/Mxx.py.
# (1) Antara muka PARAM/JULAT/TALA konsisten bagi semua salinan. (2) sedia() salinan (PARAM asal) == asal
# atas ~20 saham data 431 bagi beberapa modul wakil. Jalankan: python3 -m unittest discover -s AUTOTUNE/ujian
import glob, os, sys, unittest

AKAR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SINI = os.path.join(AKAR, 'AUTOTUNE', 'kaedah')
sys.path.insert(0, SINI)
import kesetaraan as K   # noqa: E402

WAKIL = ['M54', 'M105', 'M126', 'M12', 'M38', 'M150']   # biasa, gelung, _k145, atribut fungsi, mingguan, tmax
_DATA = {}


def data():
    if not _DATA:
        _DATA['fr'], _DATA['idx'] = K.muat(20)
    return _DATA['fr'], _DATA['idx']


def ids():
    return sorted((os.path.basename(f)[:-3] for f in glob.glob(os.path.join(SINI, 'M*.py'))), key=lambda s: int(s[1:]))


class TestAntaraMuka(unittest.TestCase):
    def test_bilangan(self):
        asal = glob.glob(os.path.join(K.ASAL, 'M*.py'))
        self.assertEqual(len(ids()), len(asal))

    def test_param_julat_tala(self):
        for mid in ids():
            with self.subTest(mid=mid):
                with open(os.path.join(SINI, mid + '.py')) as fh: src = fh.read()
                self.assertTrue(src.startswith(f'# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/{mid}.py'))
                m = K.import_fail('ujian_' + mid, os.path.join(SINI, mid + '.py'))
                for k in ('ID', 'NAMA', 'VARIAN', 'TMAX', 'WARM', 'ADA_HENTI', 'SILANG', 'PERLU_BAR', 'PARAM', 'JULAT',
                          'TALA', 'BELUM_DITALA', 'sedia'):
                    self.assertTrue(hasattr(m, k), k)
                self.assertEqual(m.ID, mid)
                self.assertFalse(hasattr(m, 'hampir'))
                self.assertLessEqual(len(m.TALA), 6)
                self.assertEqual(len(set(m.TALA)), len(m.TALA))
                self.assertTrue(set(m.TALA) <= set(m.JULAT) <= set(m.PARAM))
                if m.BELUM_DITALA:
                    self.assertEqual((m.PARAM, m.JULAT, m.TALA), ({}, {}, []))
                if isinstance(m.TMAX, int) and not isinstance(m.TMAX, bool) and not m.BELUM_DITALA:
                    self.assertEqual(m.PARAM.get('tmax'), m.TMAX)
                for n, (jenis, lo, hi) in m.JULAT.items():
                    self.assertIn(jenis, ('int', 'float'), n)
                    self.assertLess(lo, hi, n)
                    self.assertTrue(lo <= m.PARAM[n] <= hi, n)
                    if jenis == 'int': self.assertTrue(isinstance(lo, int) and isinstance(hi, int), n)
                    if n == 'tmax': self.assertLessEqual(hi, 60)


class TestKesetaraan(unittest.TestCase):
    def test_sama_dengan_asal(self):
        fr, idx = data()
        for mid in WAKIL:
            with self.subTest(mid=mid):
                A = K.import_fail('uasal_' + mid, os.path.join(K.ASAL, mid + '.py'))
                B = K.import_fail('usalin_' + mid, os.path.join(SINI, mid + '.py'))
                fa, fb = K.salin(fr), K.salin(fr)
                A.sedia(fa, idx); B.sedia(fb, idx)
                self.assertEqual(K.banding(fa, fb), [])
                fc = K.salin(fr); B.sedia(fc, idx, dict(B.PARAM))      # P eksplisit = PARAM
                self.assertEqual(K.banding(fa, fc), [])

    def test_p_berkesan(self):
        """Mengubah parameter TALA mengubah output (P benar-benar diguna)."""
        fr, idx = data()
        B = K.import_fail('usalin2_M54', os.path.join(SINI, 'M54.py'))
        fa, fb = K.salin(fr), K.salin(fr)
        B.sedia(fa, idx)
        p = B.TALA[0]; jenis, lo, hi = B.JULAT[p]
        B.sedia(fb, idx, {p: hi})
        self.assertNotEqual(K.banding(fa, fb), [])


if __name__ == '__main__':
    unittest.main()

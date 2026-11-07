"""Ujian unit bagi standard/lift_kaedah.py.

Dua sifat yang MESTI dikunci, kerana kedua-duanya ialah sebab skrip ini ada:

1. `nilai()` menilai posisi TERBUKA dengan tanda-ke-pasaran, bukan meninggalkannya. Jika ia
   tergelincir kembali kepada posisi ditutup sahaja, laporan ini menjadi pendua
   `KAEDAH_TERBAIK.md` dengan bias penapisan keluar yang sama.
2. Lift MASUK (pindaan 7 Nov 2026): ufuk tetap bebas keluar, saham-hari unik, asas tinggal-satu-
   kaedah-keluar dipadan hari x tercile ATR, SE dua hala (saham, minggu) dan BH step-up. Reka bentuk
   ini dipilih kerana ia lulus plasebo (`laporan/PLASEBO_GATE.md`); mengubahnya mesti lulus semula.
"""
import os
import sys
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import lift_kaedah as LK  # noqa: E402


def pos(**k):
    """Satu rangka posisi Lejar minimum (lajur yang `nilai()` baca)."""
    n = len(k['saham'])
    d = dict(id_kaedah=['M01'] * n, tarikh_beli=['2026-10-16'] * n, harga_beli=[100.0] * n,
             tarikh_keluar=[''] * n, untung_pct=[np.nan] * n, hari=[np.nan] * n)
    d.update(k)
    return pd.DataFrame(d)


class TestNilai(unittest.TestCase):
    """Posisi terbuka DITANDA-KE-PASARAN; posisi tutup guna untung akhir. Kos ditolak sekali."""

    def setUp(self):
        self.akhir = pd.Series({'AAA': 110.0, 'BBB': 90.0})
        self.idx = {'20261016': 0, '20261017': 1, '20261018': 2, '20261019': 3}

    def test_terbuka_ditanda_ke_pasaran(self):
        P = LK.nilai(pos(saham=['AAA', 'BBB']), self.akhir, self.idx)
        self.assertEqual(len(P), 2, 'posisi terbuka tidak boleh dibuang')
        self.assertAlmostEqual(float(P.pul.iloc[0]), 10.0 - LK.KOS, places=6)
        self.assertAlmostEqual(float(P.pul.iloc[1]), -10.0 - LK.KOS, places=6)

    def test_tutup_guna_untung_akhir_bukan_harga_kini(self):
        # AAA naik kepada 110 dalam stor, tetapi posisi ini sudah keluar pada +3%.
        P = LK.nilai(pos(saham=['AAA'], tarikh_keluar=['2026-10-17'], untung_pct=[3.0], hari=[1.0]),
                     self.akhir, self.idx)
        self.assertAlmostEqual(float(P.pul.iloc[0]), 3.0 - LK.KOS, places=6)
        self.assertAlmostEqual(float(P.hari_pegang.iloc[0]), 1.0, places=6)

    def test_hari_pegang_terbuka_dikira_dari_sesi_terakhir(self):
        P = LK.nilai(pos(saham=['AAA']), self.akhir, self.idx)
        self.assertAlmostEqual(float(P.hari_pegang.iloc[0]), 3.0, places=6)

    def test_saham_tanpa_harga_dibuang_bukan_sifar(self):
        P = LK.nilai(pos(saham=['ZZZ']), self.akhir, self.idx)
        self.assertEqual(len(P), 0)


class TestLangsung(unittest.TestCase):
    """Hanya isyarat selepas peraturan kaedah dibekukan dikira data hadapan (pindaan 7 Nov 2026)."""

    def test_mula_ikut_keluarga(self):
        self.assertEqual(LK.mula_langsung('M15'), '2026-10-15')
        self.assertEqual(LK.mula_langsung('N19X13'), '2026-11-03')
        self.assertEqual(LK.mula_langsung('GB02_atau3X13'), '2026-11-03')

    def test_isian_nxx_dibuang(self):
        P = pd.DataFrame(dict(id_kaedah=['M01', 'N19X13', 'N19X13'],
                              tarikh_isyarat=['2026-10-20', '2026-10-20', '2026-11-04']))
        self.assertEqual(list(LK.langsung(P)), [True, False, True])


def panel(n_sesi=14, tutup=None):
    """Stor tiruan: sesi YYYYMMDD berturut, tutup = 100 kecuali ditetapkan, ATR% ikut saham."""
    sesi = [f'202611{d:02d}' for d in range(1, n_sesi + 1)]
    sh = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF']
    C = pd.DataFrame(100.0, index=sh, columns=sesi)
    for (t, i), v in (tutup or {}).items():
        C.loc[t, sesi[i]] = v
    A = pd.DataFrame({s: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] for s in sesi}, index=sh)
    return sesi, C, A


def baris(mid, saham, hari_beli, hari_isyarat):
    n = len(saham)
    return pd.DataFrame(dict(id_kaedah=[mid] * n, saham=saham, harga_beli=[100.0] * n,
                             tarikh_beli=[hari_beli] * n, tarikh_isyarat=[hari_isyarat] * n))


class TestSahamHari(unittest.TestCase):

    def test_ufuk_tetap_bebas_keluar(self):
        # Beli sesi index 1; tutup sesi ke-10 = index 10 -> 110 -> +10% tolak kos.
        sesi, C, A = panel(tutup={('AAA', 10): 110.0})
        P = baris('M01', ['AAA'], '2026-11-02', '2026-11-01')
        Q = LK.saham_hari(P, sesi, C, A)
        self.assertAlmostEqual(float(Q.r.iloc[0]), 10.0 - LK.KOS, places=6)

    def test_ufuk_belum_lengkap_dibuang(self):
        sesi, C, A = panel(n_sesi=9)
        P = baris('M01', ['AAA'], '2026-11-01', '2026-10-31')
        self.assertEqual(len(LK.saham_hari(P, sesi, C, A)), 0)

    def test_pendua_kaedah_sama_dibuang(self):
        sesi, C, A = panel()
        P = pd.concat([baris('M01', ['AAA', 'AAA'], '2026-11-02', '2026-11-01')])
        self.assertEqual(len(LK.saham_hari(P, sesi, C, A)), 1)

    def test_tercile_atr_dalam_kolam_hari(self):
        sesi, C, A = panel()
        P = baris('M01', ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF'], '2026-11-02', '2026-11-01')
        Q = LK.saham_hari(P, sesi, C, A).set_index('saham')
        self.assertEqual(list(Q.q), [0, 0, 1, 1, 2, 2])

    def test_kuarantin_dibuang(self):
        sesi, C, A = panel()
        P = baris('M01', ['AAA', 'BBB'], '2026-11-02', '2026-11-01')
        Q = LK.saham_hari(P, sesi, C, A, kuarantin=lambda t, d: t == 'AAA')
        self.assertEqual(list(Q.saham), ['BBB'])


class TestLiftMasuk(unittest.TestCase):

    def q(self, rows):
        return pd.DataFrame(rows, columns=['id_kaedah', 'saham', 'tarikh_beli', 'q', 'r'])

    def test_asas_tanpa_kaedah_sendiri_dan_saham_hari_unik(self):
        # Kolam hari d1 tercile 0: AAA (M01, M02, M03 beli = SATU saham-hari, r 10), BBB (M02, r 0).
        Q = self.q([('M01', 'AAA', 'd1', 0, 10.0), ('M02', 'AAA', 'd1', 0, 10.0), ('M03', 'AAA', 'd1', 0, 10.0),
                    ('M02', 'BBB', 'd1', 0, 0.0)])
        X = LK.lift_masuk(Q).set_index(['id_kaedah', 'saham'])
        self.assertAlmostEqual(float(X.loc[('M01', 'AAA'), 'lift']), 10.0)   # asas = BBB sahaja
        # M02 memegang kedua-dua saham-hari: tiada asas -> dibuang, bukan lift sifar
        self.assertNotIn(('M02', 'AAA'), X.index)

    def test_tercile_berbeza_tidak_bercampur(self):
        Q = self.q([('M01', 'AAA', 'd1', 2, 10.0), ('M02', 'BBB', 'd1', 2, 4.0), ('M02', 'CCC', 'd1', 0, -50.0)])
        X = LK.lift_masuk(Q).set_index(['id_kaedah', 'saham'])
        self.assertAlmostEqual(float(X.loc[('M01', 'AAA'), 'lift']), 6.0)    # bukan lawan CCC tercile 0


class TestSeDuaHala(unittest.TestCase):

    def test_tidak_pernah_lebih_kecil_daripada_satu_hala(self):
        """Lantai max(V1, V2) sebahagian reka bentuk yang lulus plasebo (konservatif)."""
        rng = np.random.default_rng(1)
        x = rng.normal(size=200)
        k1 = np.repeat(np.arange(20), 10)
        k2 = np.arange(200)                       # setiap baris kluster sendiri
        se, df = LK.se_dua_hala(x, k1, k2)
        se1, _ = LK._se_kl(x - x.mean(), k1)
        se2, _ = LK._se_kl(x - x.mean(), k2)
        self.assertAlmostEqual(se, max(se1, se2), places=10)
        self.assertEqual(df, 19)

    def test_saham_berulang_meluaskan_se(self):
        # Saham sama dibeli berulang dengan pulangan sama: SE mesti lebih besar daripada andaian bebas.
        x = np.repeat([3.0, -1.0, 2.0, -2.0, 4.0], 20)
        saham = np.repeat(list('ABCDE'), 20)
        minggu = np.tile(np.arange(20), 5)
        se, _ = LK.se_dua_hala(x, saham, minggu)
        self.assertGreater(se, x.std(ddof=1) / np.sqrt(len(x)))


class TestBhStepUp(unittest.TestCase):

    def test_step_up_meluluskan_p_atas_ambang_sendiri(self):
        # p kedua 0.03 > 0.05*2/3 = 0.033? tidak; contoh klasik: [0.01, 0.04, 0.045] m=3, q=0.05
        # ambang = [0.0167, 0.0333, 0.05]: p(3)=0.045 <= 0.05 -> k=3 -> SEMUA lulus, walaupun p(2) > ambang(2).
        self.assertEqual(list(LK.bh_lulus([0.045, 0.01, 0.04])), [True, True, True])

    def test_tiada_lulus(self):
        self.assertFalse(LK.bh_lulus([0.5, 0.2, 0.9]).any())


class TestUji(unittest.TestCase):

    def rangka(self, mid, n, minggu, lift_asas=2.0):
        tb = pd.to_datetime('2026-11-02') + pd.to_timedelta(np.arange(n) % minggu * 7, unit='D')
        lift = [lift_asas + (0.5 if i % 2 else -0.5) for i in range(n)]
        return pd.DataFrame(dict(id_kaedah=[mid] * n, saham=[f'S{i % 17}' for i in range(n)],
                                 tarikh_beli=tb.strftime('%Y-%m-%d'), r=lift, lift=lift))

    def test_bawah_minimum_dilangkau(self):
        self.assertNotIn('M01', LK.uji(self.rangka('M01', LK.MIN_N - 1, 8)).index)
        self.assertNotIn('M01', LK.uji(self.rangka('M01', 60, LK.MIN_MINGGU - 1)).index)

    def test_lift_dikira(self):
        R = LK.uji(self.rangka('M01', 60, 8))
        self.assertAlmostEqual(float(R.loc['M01', 'lift']), 2.0, places=6)
        self.assertTrue(((R.lift > 0) & R.lulus).all())


class TestSelarasStor(unittest.TestCase):
    """Audit 7 Nov 2026: stor dan Lejar mesti pada sesi sama; stor basi mesti GAGAL, bukan senyap."""

    def setUp(self):
        import tempfile
        self.d = tempfile.TemporaryDirectory()
        self.asal = LK.LEJAR
        LK.LEJAR = self.d.name
        with open(os.path.join(self.d.name, 'status.json'), 'w') as f:
            f.write('{"sesi_terakhir": "2026-11-05"}')

    def tearDown(self):
        LK.LEJAR = self.asal
        self.d.cleanup()

    def test_bar_selepas_lejar_dibuang(self):
        H = pd.DataFrame(dict(date=['20261104', '20261105', '20261106'], close=[1.0, 2.0, 3.0]))
        self.assertEqual(list(LK.potong_sesi(H).date), ['20261104', '20261105'])

    def test_stor_basi_gagal(self):
        H = pd.DataFrame(dict(date=['20261103', '20261104'], close=[1.0, 2.0]))
        with self.assertRaises(SystemExit):
            LK.potong_sesi(H)


class TestHariPerlu(unittest.TestCase):
    def test_lift_lebih_besar_perlukan_lebih_sedikit_hari(self):
        a = LK.hari_perlu(3.3, 180, 1.0)
        b = LK.hari_perlu(3.3, 180, 2.0)
        self.assertGreater(a, b)
        self.assertAlmostEqual(a / b, 4.0, delta=0.6)   # skala ~ 1/lift^2

    def test_lebih_banyak_kaedah_perlukan_lebih_banyak_hari(self):
        self.assertGreater(LK.hari_perlu(3.3, 180, 2.0), LK.hari_perlu(3.3, 10, 2.0))


class TestStatus(unittest.TestCase):
    def test_label(self):
        self.assertEqual(LK.status(14, 56), 'BELUM CUKUP')
        self.assertEqual(LK.status(60, 56), 'BOLEH DIBACA')


if __name__ == '__main__':
    unittest.main()

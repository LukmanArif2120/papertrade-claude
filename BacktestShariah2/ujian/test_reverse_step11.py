"""Penilaian leg SEC (REVERSE/step11_sec_nilai.py; SPEC_FASA2.md §5, §9.4, §9.5).

Ujian mengunci ambang dan set signal yang dipradaftar, supaya ia tidak boleh dilonggarkan selepas
keputusan dilihat.
"""
import os, sys, unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'REVERSE'))
import step11_sec_nilai as T  # noqa: E402


def rangka(rho_ikut_tahun, lajur='sue'):
    """DataFrame tiruan di mana Spearman setiap tahun mengikut tanda yang diminta."""
    bhg = []
    rng = np.random.default_rng(0)
    for i, tanda in enumerate(rho_ikut_tahun):
        n = 4000                      # > AMBANG_TAHUN (§9.7), jika tidak tahun itu dikecualikan
        x = rng.normal(size=n)
        v = tanda * x * 0.5 + rng.normal(size=n) * 0.1
        bhg.append(pd.DataFrame({'tahun': 2012 + i, lajur: x, 'pul_henti2atr': v}))
    d = pd.concat(bhg, ignore_index=True)
    for k in T.LAJUR:
        if k not in d:
            d[k] = np.nan
    return d


class TestAmbangPemangkatan(unittest.TestCase):
    def test_pecahan_sama_dengan_10_daripada_14(self):
        # §9.5: penyataan semula, bukan pelonggaran.
        self.assertEqual(int(np.ceil(T.PECAHAN_KONSISTEN * 14)), 10)

    def test_minimum_tahun_dikunci(self):
        self.assertEqual(T.MIN_TAHUN, 10)

    def test_konsisten_penuh_lulus(self):
        r = T.ujian_51(rangka([1] * 14))
        b = r[r.lajur == 'sue'].iloc[0]
        self.assertEqual(b.n_tahun, 14)
        self.assertEqual(b.konsisten, 14)
        self.assertTrue(b.boleh_dinilai)
        self.assertTrue(b.lulus_51)

    def test_konsisten_9_daripada_14_gagal(self):
        # 9 < ceil(0.71 x 14) = 10
        r = T.ujian_51(rangka([1] * 9 + [-1] * 5))
        b = r[r.lajur == 'sue'].iloc[0]
        self.assertEqual(b.konsisten, 9)
        self.assertFalse(b.lulus_51)

    def test_konsisten_10_daripada_14_lulus(self):
        r = T.ujian_51(rangka([1] * 10 + [-1] * 4))
        b = r[r.lajur == 'sue'].iloc[0]
        self.assertEqual(b.konsisten, 10)
        self.assertTrue(b.lulus_51)

    def test_kurang_10_tahun_belum_boleh_dinilai(self):
        """Tahun tidak cukup mesti BELUM BOLEH DINILAI, bukan lulus."""
        r = T.ujian_51(rangka([1] * 6))
        b = r[r.lajur == 'sue'].iloc[0]
        self.assertEqual(b.n_tahun, 6)
        self.assertEqual(b.konsisten, 6)          # konsisten 6/6
        self.assertFalse(b.boleh_dinilai)
        self.assertFalse(b.lulus_51)              # tetapi TIDAK lulus

    def test_rho_lemah_gagal_walaupun_konsisten(self):
        rng = np.random.default_rng(1)
        bhg = []
        for i in range(14):
            n = 4000                  # > AMBANG_TAHUN (§9.7)
            x = rng.normal(size=n)
            v = x * 0.002 + rng.normal(size=n)    # korelasi hampir sifar
            bhg.append(pd.DataFrame({'tahun': 2012 + i, 'sue': x, 'pul_henti2atr': v}))
        d = pd.concat(bhg, ignore_index=True)
        for k in T.LAJUR:
            if k not in d:
                d[k] = np.nan
        b = T.ujian_51(d)
        b = b[b.lajur == 'sue'].iloc[0]
        self.assertLess(b.rho_abs, 0.05)
        self.assertFalse(b.lulus_51)


class TestAmbangSetiapTahun(unittest.TestCase):
    def test_ambang_dikunci_3000(self):
        self.assertEqual(T.AMBANG_TAHUN, 3000)

    def test_tahun_bawah_ambang_dikecualikan(self):
        """§9.7: tahun di bawah 3,000 tidak dikira dalam pembilang MAHUPUN penyebut."""
        rng = np.random.default_rng(2)
        bhg = []
        for i in range(14):
            n = 500 if i < 3 else 4000          # 3 tahun pertama di bawah ambang
            x = rng.normal(size=n)
            v = x * 0.5 + rng.normal(size=n) * 0.1
            bhg.append(pd.DataFrame({'tahun': 2012 + i, 'sue': x, 'pul_henti2atr': v}))
        d = pd.concat(bhg, ignore_index=True)
        for k in T.LAJUR:
            if k not in d:
                d[k] = np.nan
        b = T.ujian_51(d)
        b = b[b.lajur == 'sue'].iloc[0]
        self.assertEqual(b.n_tahun, 11)                        # 14 - 3
        self.assertEqual(b.tahun_dikecualikan, '2012,2013,2014')
        self.assertTrue(b.boleh_dinilai)                       # 11 >= 10
        self.assertEqual(b.perlu_konsisten, int(np.ceil(0.71 * 11)))

    def test_kurang_10_tahun_layak_belum_boleh_dinilai(self):
        """Lima tahun di bawah ambang -> 9 layak -> BELUM BOLEH DINILAI, walaupun konsisten penuh."""
        rng = np.random.default_rng(3)
        bhg = []
        for i in range(14):
            n = 500 if i < 5 else 4000
            x = rng.normal(size=n)
            v = x * 0.5 + rng.normal(size=n) * 0.1
            bhg.append(pd.DataFrame({'tahun': 2012 + i, 'sue': x, 'pul_henti2atr': v}))
        d = pd.concat(bhg, ignore_index=True)
        for k in T.LAJUR:
            if k not in d:
                d[k] = np.nan
        b = T.ujian_51(d)
        b = b[b.lajur == 'sue'].iloc[0]
        self.assertEqual(b.n_tahun, 9)
        self.assertEqual(b.konsisten, 9)
        self.assertFalse(b.boleh_dinilai)
        self.assertFalse(b.lulus_51)


class TestSetSignalDikunci(unittest.TestCase):
    def test_20_ujian_seperti_dipradaftar(self):
        d = pd.DataFrame({'sue': [0.0, 1.0, 2.0], 'tumbuh_hasil': [0.0, 1.0, 2.0],
                          'pecutan_hasil': [0.0, 1.0, 2.0],
                          'hari_sejak_earnings': [1.0, 50.0, np.nan],
                          'hari_ke_earnings_jangka': [3.0, 40.0, np.nan]})
        batas = {k: dict(q1=0.5, q5=1.5) for k in T.LAJUR}
        S = T.signal_binari(d, batas)
        self.assertEqual(len(S), 20)              # §9.4: 6 kuintil + 2 tingkap + 12 silang
        self.assertEqual(sum(1 for n in S if '&' in n), 12)

    def test_tingkap_pead_ke_belakang(self):
        d = pd.DataFrame({'sue': [np.nan], 'tumbuh_hasil': [np.nan], 'pecutan_hasil': [np.nan],
                          'hari_sejak_earnings': [3.0], 'hari_ke_earnings_jangka': [np.nan]})
        S = T.signal_binari(d, {})
        self.assertTrue(S['sejak_earnings_le5'][0])
        self.assertFalse(S['jangka_earnings_le5'][0])

    def test_jangka_negatif_bukan_tingkap(self):
        """Jangkaan yang sudah lepas (negatif) bukan tingkap pra-earnings."""
        d = pd.DataFrame({'sue': [np.nan], 'tumbuh_hasil': [np.nan], 'pecutan_hasil': [np.nan],
                          'hari_sejak_earnings': [np.nan], 'hari_ke_earnings_jangka': [-4.0]})
        S = T.signal_binari(d, {})
        self.assertFalse(S['jangka_earnings_le5'][0])

    def test_keluarga_fdr_berasingan(self):
        self.assertEqual(T.KELUARGA, 'FASA2_SEC')

    def test_sasaran_dan_henti_sama_dengan_fasa1(self):
        self.assertEqual(T.UFUK, 63)
        self.assertEqual(T.HENTI_ATR, 2.0)
        self.assertEqual(T.LAJUR, ['sue', 'tumbuh_hasil', 'pecutan_hasil'])


class TestKebasian(unittest.TestCase):
    def test_ambang_sama_dengan_selang_maks_step10(self):
        """§9.6: satu ambang, bukan dua — sama dengan SELANG_MAKS jangkaan kitaran step10."""
        import step10_sec as T10
        self.assertEqual(T.BASI_MAKS, T10.SELANG_MAKS)
        self.assertEqual(T.BASI_MAKS, 120)

    def test_tingkap_pead_lebih_ketat_daripada_basi(self):
        self.assertLess(T.TINGKAP, T.BASI_MAKS)


if __name__ == '__main__':
    unittest.main()

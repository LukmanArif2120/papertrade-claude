"""Ujian unit bagi standard/kad_skor.py dan standard/portfolio_t4.py.

TestKunci ialah PRADAFTAR (standard/SPEC_KAD_SKOR.md, 6 Nov 2026). Ia sengaja menyalin setiap ambang
sebagai literal: melonggarkan gate selepas melihat data mesti menyentuh DUA fail dan satu spec
bertarikh, jadi ia kelihatan dalam semakan dan tidak boleh berlaku secara senyap.
"""
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'kod'))
import kad_skor as KS  # noqa: E402
import portfolio_t4 as T4  # noqa: E402
import lift_kaedah as LK  # noqa: E402


class TestKunci(unittest.TestCase):
    """Ambang dipradaftar 6 Nov 2026. JANGAN ubah tanpa keputusan pengguna + pradaftar baharu."""

    def test_ambang(self):
        self.assertEqual(KS.G1_HARI_BELI_MIN, 20)
        self.assertEqual(KS.G1_BEZA_MATA, 1.0)
        self.assertEqual(KS.G1_LIFT_MATA, 2.0)
        self.assertEqual((KS.Z_ALPHA, KS.Z_KUASA), (1.96, 0.84))
        self.assertEqual(KS.G2_ALPHA, 0.05)
        self.assertEqual(KS.G3_Q, 0.05)
        self.assertEqual(KS.G6_SESI, 126)
        self.assertEqual(KS.G6_PERSENTIL, 95)
        self.assertEqual(KS.G6_MDD, -26.82)
        self.assertEqual(KS.STATUS, ('NEGATIF', 'GAGAL', 'BELUM CUKUP', 'CALON', 'TERBUKTI'))

    def test_g3_sama_dengan_lift(self):
        """G3 menilai lulus BH-FDR yang lift_kaedah kira; q mesti sama atau gate itu bohong."""
        self.assertEqual(KS.G3_Q, LK.Q_FDR)

    def test_berat_t4(self):
        self.assertEqual(T4.BERAT, (0.8, 0.7, 0.5))
        self.assertEqual(T4.LORONG, {'L1': 'kaedah', 'L2': 'henti'})

    def test_spec_menyebut_ambang(self):
        with open(os.path.join(AKAR, 'BacktestShariah2', 'standard', 'SPEC_KAD_SKOR.md'), encoding='utf-8') as f:
            s = f.read()
        for t in ('G1_HARI_BELI_MIN = 20', 'G2_ALPHA = 0.05', 'G3_Q = 0.05', 'G6_SESI = 126',
                  'G6_PERSENTIL = 95', 'G6_MDD = -26.82', 'Dipradaftar 6 Nov 2026'):
            self.assertIn(t, s)


def baris(**k):
    r = dict(hari_beli=60, tutup=700, jangkaan=1.5, ci_bawah=0.3, lift=1.2, lift_lulus=True, hari0=0,
             pantau='OK', p_dd=5.0, p_dd_had=20.0, t4_sesi=130, t4_pul=30.0, t4_spus=10.0, t4_jalur_p95=20.0,
             t4_mdd=-12.0)
    r.update(k)
    return r


class TestGate(unittest.TestCase):

    def st(self, **k):
        return KS.tentukan(baris(**k), 610, 59)[0]

    def test_terbukti(self):
        self.assertEqual(self.st(), 'TERBUKTI')

    def test_g6_belum_jadi_calon(self):
        self.assertEqual(self.st(t4_sesi=125), 'CALON')
        self.assertEqual(self.st(t4_pul=9.0), 'CALON')          # kalah SPUS
        self.assertEqual(self.st(t4_pul=19.0), 'CALON')         # dalam jalur rawak
        self.assertEqual(self.st(t4_mdd=-27.0), 'CALON')

    def test_g1(self):
        self.assertEqual(self.st(hari_beli=19), 'BELUM CUKUP')
        self.assertEqual(self.st(hari_beli=30, tutup=100), 'BELUM CUKUP')   # tiada laluan n atau hari beli
        self.assertEqual(self.st(hari_beli=59, tutup=0), 'TERBUKTI')        # laluan hari beli
        self.assertEqual(self.st(hari_beli=20, tutup=610), 'TERBUKTI')      # laluan n

    def test_g2_had_bawah(self):
        self.assertEqual(self.st(ci_bawah=-0.01), 'GAGAL')
        self.assertEqual(self.st(jangkaan=-0.1, ci_bawah=-1.0), 'GAGAL')

    def test_g3(self):
        self.assertEqual(self.st(lift_lulus=False), 'GAGAL')

    def test_g4_hari0_tidak_dikecualikan(self):
        self.assertEqual(self.st(hari0=40), 'TERBUKTI')                     # jangkaan masih positif
        ok, sebab = KS.g4(dict(hari0=40, jangkaan=-0.2))
        self.assertFalse(ok)

    def test_g5(self):
        self.assertEqual(self.st(pantau='GANTUNG'), 'GAGAL')
        self.assertEqual(self.st(pantau='BERSARA', hari_beli=5), 'GAGAL')   # G5 sebelum G1
        self.assertEqual(self.st(p_dd=25.0), 'GAGAL')
        self.assertEqual(self.st(p_dd=25.0, p_dd_had=None), 'TERBUKTI')     # tiada had (Nxx)

    def test_negatif_mendahului(self):
        self.assertEqual(self.st(lift=-2.0, lift_lulus=True, hari_beli=3), 'NEGATIF')
        self.assertEqual(self.st(lift=-2.0, lift_lulus=False, hari_beli=3), 'BELUM CUKUP')

    def test_n_perlu(self):
        self.assertEqual(KS.n_perlu(3.95), 123)      # KAEDAH_TERBAIK.md §6: ~122 pada SD 3.95
        self.assertIsNone(KS.n_perlu(None))


class TestStatistik(unittest.TestCase):

    def test_semua_posisi_dan_hari0(self):
        g = pd.DataFrame(dict(
            pul=[10.0, -5.0, -5.0, 2.0, 4.0, -1.0],
            terbuka=[False, False, True, True, False, False],
            tarikh_beli=['2026-10-16', '2026-10-16', '2026-10-17', '2026-10-17', '2026-10-20', '2026-10-21'],
            tarikh_keluar=['2026-10-20', '2026-10-16', '', '', '2026-10-25', '2026-10-21'],
            sebab_keluar=['sasaran', 'henti', '', '', 'masa', 'henti']))
        d = KS.statistik(g)
        self.assertAlmostEqual(d['jangkaan'], 5.0 / 6)
        self.assertEqual(d['hari0'], 2)                  # dua henti pada hari beli, terbuka tidak dikira
        self.assertEqual(d['tutup'], 4)
        self.assertAlmostEqual(d['pul_buka'], -1.5)
        self.assertAlmostEqual(d['payoff'], (16 / 3) / (11 / 3))
        self.assertAlmostEqual(d['tanpa5'], np.mean([-5.0, -5.0, 2.0, 4.0, -1.0]))   # buang 1 terbaik
        self.assertLess(d['ci_bawah'], d['jangkaan'])


class TestJsonLajur(unittest.TestCase):

    def test_pergi_balik(self):
        rows = [dict(id='M01', n=3, lift=None, gate={g: g in ('G4', 'G5') for g in KS.KOL_GATE},
                     sebab={'G1': 'hari beli 3/20'})]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'k.json')
            KS.tulis_json(p, dict(tajuk='x'), rows)
            m, r = KS.baca_json(p)
        self.assertEqual(m['tajuk'], 'x')
        self.assertEqual(r[0]['gate'], rows[0]['gate'])
        self.assertEqual(r[0]['sebab'], rows[0]['sebab'])


class TestT4(unittest.TestCase):

    def test_campur_imbang_bulanan(self):
        idx = ['2026-10-30', '2026-11-02', '2026-11-03']
        L = pd.Series([1.10, 1.10, 1.21], index=idx)      # lorong +10%, rata, +10%
        S = pd.Series([1.00, 1.00, 1.00], index=idx)      # SPUS rata
        c = T4.campur(L, S, 0.5)
        self.assertAlmostEqual(c.iloc[0], 1.05)
        # imbang semula 2 Nov: 1.05 dibahagi 50/50, lorong +10% pada 3 Nov -> 1.05 x (0.5 + 0.55)
        self.assertAlmostEqual(c.iloc[2], 1.05 * 1.05)

    def test_asas_semula_jalur(self):
        s = pd.Series([1.0, 1.1, 1.21], index=['2026-10-16', '2026-10-17', '2026-10-20'])
        r = T4.asas_semula(s, '2026-10-17')
        self.assertAlmostEqual(r.iloc[0], 1.1)            # sesi pertama lorong diukur dari tutup semalam
        self.assertAlmostEqual(r.iloc[-1], 1.21)
        r2 = T4.asas_semula(s, '2026-10-20')
        self.assertAlmostEqual(r2.iloc[0], 1.1)

    def test_spus_asas_buka(self):
        S = pd.DataFrame(dict(buka=[100.0, 102.0], tutup=[101.0, 104.0]), index=['2026-10-16', '2026-10-17'])
        x = T4.siri_spus(S, ['2026-10-16', '2026-10-17'])
        self.assertAlmostEqual(x.iloc[0], 1.01)           # tutup / BUKA sesi pertama (BANDING_SPUS peraturan 1)
        self.assertAlmostEqual(x.iloc[1], 1.04)

    def test_lorong_satu_kaedah_ikut_rank(self):
        P = pd.DataFrame(dict(
            id_kaedah=['M01'] * 12 + ['M02'],
            saham=[f'S{i:02d}' for i in range(12)] + ['ZZ'],
            rank=list(range(12)) + [99],
            tarikh_beli=['2026-10-16'] * 13, harga_beli=[10.0] * 13, tarikh_isyarat=['2026-10-15'] * 13,
            keluar=[False] * 13, tarikh_keluar_henti=[''] * 13, harga_keluar_henti=[np.nan] * 13,
            keluar1=[False] * 13, tarikh_keluar=[''] * 13, harga_keluar1=[np.nan] * 13, rs=[np.nan] * 13))
        R, E = T4.lorong_kaedah(P, 'M01', 'kaedah', ['2026-10-16'], lambda s, d: 11.0)
        self.assertEqual(len(R), 10)                       # 10 slot
        self.assertNotIn('ZZ', set(R.saham))               # kaedah lain tidak masuk
        self.assertEqual(set(R.saham), {f'S{i:02d}' for i in range(2, 12)})   # rank tertinggi dahulu
        self.assertAlmostEqual(E.ekuiti.iloc[0], 1.1)       # 10 x 10% pada 10 -> tutup 11 (kos hanya pada realisasi)


if __name__ == '__main__':
    unittest.main()

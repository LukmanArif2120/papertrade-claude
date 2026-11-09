"""Ujian unit bagi standard/kad_skor.py dan standard/portfolio_t4.py.

TestKunci ialah PRADAFTAR (standard/SPEC_KAD_SKOR.md, 6 Nov 2026; pindaan 7 Nov 2026). Ia sengaja menyalin setiap ambang
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
    """Ambang dipradaftar 6 Nov 2026, dipinda 7 Nov 2026. JANGAN ubah tanpa keputusan pengguna + pradaftar baharu."""

    def test_ambang(self):
        self.assertEqual(KS.G1_HARI_BELI_MIN, 20)
        self.assertEqual(KS.G1_LIFT_MATA, 2.0)
        self.assertEqual(KS.G1_REJIM_MIN, 10)                 # pindaan 7 Nov
        self.assertEqual((KS.Z_ALPHA, KS.Z_KUASA), (1.96, 0.84))
        self.assertEqual(KS.G2_ALPHA, 0.05)
        self.assertEqual(KS.G2_NW_LAG, 5)                     # pindaan 7 Nov
        self.assertEqual(KS.G3_Q, 0.05)
        self.assertEqual(KS.G6_SESI, 126)
        self.assertEqual(KS.G6_MDD_HAD, -10.0)                # pindaan 7 Nov: toleransi pengguna
        self.assertEqual(KS.G4_HARI0_MAKS, 0)                 # pindaan 6 Nov 2026: ketat
        self.assertEqual(KS.STATUS, ('NEGATIF', 'GAGAL', 'BELUM CUKUP', 'CALON', 'TERBUKTI'))
        self.assertFalse(hasattr(KS, 'G6_MDD'))               # MDD SPUS -26.82% bukan lagi gate
        self.assertFalse(hasattr(KS, 'G6_PERSENTIL'))         # p95 daripada 20 cabutan = cabutan ke-2

    def test_lift_masuk_dikunci(self):
        """G3 = lift masuk yang lulus plasebo (laporan/PLASEBO_GATE.md); mengubah reka bentuk mesti lulus semula."""
        self.assertEqual(KS.G3_Q, LK.Q_FDR)
        self.assertEqual(LK.UFUK, 10)
        self.assertEqual(LK.MIN_N, 30)
        self.assertEqual(LK.MIN_MINGGU, 5)
        self.assertEqual(LK.TERCILE, 3)
        self.assertEqual(LK.MULA_LANGSUNG, {'M': '2026-10-15', 'N': '2026-11-03', 'GB': '2026-11-03'})

    def test_berat_t4(self):
        self.assertEqual(T4.BERAT, (0.8, 0.7, 0.5))
        self.assertIs(T4.LANGSUNG_SAHAJA, True)               # pindaan 9 Nov 2026: lorong LANGSUNG sahaja
        self.assertEqual(T4.LORONG, {'L1': 'kaedah', 'L2': 'henti'})
        self.assertAlmostEqual(T4.berat_mdd(-20.0), 0.5)      # sama dengan kad_skor.pada_mdd
        self.assertAlmostEqual(KS.pada_mdd(8.0, -20.0), 4.0)

    def test_spec_menyebut_ambang(self):
        with open(os.path.join(AKAR, 'BacktestShariah2', 'standard', 'SPEC_KAD_SKOR.md'), encoding='utf-8') as f:
            s = f.read()
        for t in ('G1_HARI_BELI_MIN = 20', 'G2_ALPHA = 0.05', 'G3_Q = 0.05', 'G6_SESI = 126',
                  'Dipradaftar 6 Nov 2026', 'G4_HARI0_MAKS = 0', 'Pindaan 6 Nov 2026',
                  'Pindaan 7 Nov 2026', 'Dipradaftar 7 Nov 2026', 'G1_REJIM_MIN = 10', 'G2_NW_LAG = 5',
                  'G3_UFUK = 10', 'G6_MDD_HAD = -10.0', 'N/GB: 2026-11-03',
                  'Pindaan 9 Nov 2026', 'LANGSUNG_SAHAJA = True'):
            self.assertIn(t, s)


def baris(**k):
    r = dict(hari_beli=60, hari_on=12, hari_off=12, buku_harian=0.05, buku_ci_bawah=0.01, lift=1.2,
             lift_lulus=True, hari0=0, pantau='OK', p_dd=5.0, p_dd_had=20.0, t4_sesi=130, t4_pul=30.0,
             t4_mdd=-12.0, t4_spus=10.0, t4_spus_mdd=-15.0, t4_jalur_nisbah_maks=1.5)
    r.update(k)
    return r


class TestGate(unittest.TestCase):

    def st(self, perlu=59, **k):
        return KS.tentukan(baris(**k), perlu)[0]

    def test_terbukti(self):
        self.assertEqual(self.st(), 'TERBUKTI')

    def test_g6_pada_mdd_pengguna(self):
        self.assertEqual(self.st(t4_sesi=125), 'CALON')
        self.assertEqual(self.st(t4_pul=-1.0), 'CALON')
        # pul 30 MDD -12 -> 25.0 pada MDD -10; SPUS 10 MDD -15 -> 6.67. Lorong MDD -40: 30 x 0.25 = 7.5 (masih menang)
        self.assertEqual(self.st(t4_mdd=-40.0, t4_jalur_nisbah_maks=0.5), 'TERBUKTI')
        # lorong MDD -50: 30 x 0.2 = 6.0 < SPUS 6.67 -> kalah SPUS pada MDD sama walaupun pulangan mentah 3x
        self.assertEqual(self.st(t4_mdd=-50.0, t4_jalur_nisbah_maks=0.5), 'CALON')
        # nisbah 30/12 = 2.5 tidak melepasi maksimum jalur 3.0
        self.assertEqual(self.st(t4_jalur_nisbah_maks=3.0), 'CALON')

    def test_g1_hari_langsung_dan_rejim(self):
        self.assertEqual(self.st(hari_beli=58), 'BELUM CUKUP')
        self.assertEqual(self.st(hari_on=9), 'BELUM CUKUP')      # satu fasa pasaran sahaja
        self.assertEqual(self.st(hari_off=9), 'BELUM CUKUP')
        self.assertEqual(self.st(perlu=None), 'BELUM CUKUP')    # kuasa belum boleh dianggar
        self.assertEqual(self.st(perlu=10, hari_beli=20), 'TERBUKTI')   # lantai 20
        self.assertEqual(self.st(perlu=10, hari_beli=19), 'BELUM CUKUP')

    def test_g2_buku(self):
        self.assertEqual(self.st(buku_ci_bawah=-0.01), 'GAGAL')
        self.assertEqual(self.st(buku_harian=-0.1, buku_ci_bawah=-0.3), 'GAGAL')
        self.assertEqual(self.st(buku_harian=None, buku_ci_bawah=None), 'GAGAL')

    def test_g3(self):
        self.assertEqual(self.st(lift_lulus=False), 'GAGAL')

    def test_g4_ketat(self):
        """Pindaan 6 Nov 2026: satu henti hari-0 sudah gagal, walaupun jangkaan positif."""
        self.assertEqual(self.st(hari0=1), 'GAGAL')
        self.assertEqual(self.st(hari0=40, hari_beli=5), 'BELUM CUKUP')    # G1 sebelum G4
        self.assertTrue(KS.g4(dict(hari0=0))[0])
        self.assertTrue(KS.g4(dict(hari0=None))[0])                         # Nxx: tiada henti

    def test_g5(self):
        self.assertEqual(self.st(pantau='GANTUNG'), 'GAGAL')
        self.assertEqual(self.st(pantau='BERSARA', hari_beli=5), 'GAGAL')   # G5 sebelum G1
        self.assertEqual(self.st(p_dd=25.0), 'GAGAL')
        self.assertEqual(self.st(p_dd=25.0, p_dd_had=None), 'TERBUKTI')     # tiada had (Nxx)

    def test_negatif_perlukan_g1(self):
        """Pindaan 7 Nov: NEGATIF tidak diberi pada data belum matang / satu fasa pasaran."""
        self.assertEqual(self.st(lift=-2.0, lift_lulus=True), 'NEGATIF')
        self.assertEqual(self.st(lift=-2.0, lift_lulus=True, hari_beli=3), 'BELUM CUKUP')
        self.assertEqual(self.st(lift=-2.0, lift_lulus=True, hari_on=1), 'BELUM CUKUP')
        self.assertEqual(self.st(lift=-2.0, lift_lulus=False), 'GAGAL')

    def test_n_perlu(self):
        self.assertEqual(KS.n_perlu(3.95), 123)      # maklumat sahaja sejak 7 Nov
        self.assertIsNone(KS.n_perlu(None))


class TestBuku(unittest.TestCase):
    """G2: buku berat sama, ditanda setiap hari, SE Newey-West."""

    def setUp(self):
        self.sesi = ['20261102', '20261103', '20261104']
        self.C = pd.DataFrame({'20261102': [110.0, 100.0], '20261103': [121.0, 90.0], '20261104': [121.0, 90.0]},
                              index=['AAA', 'BBB'])

    def test_buku_dua_posisi(self):
        P = pd.DataFrame(dict(id_kaedah=['M01', 'M01'], saham=['AAA', 'BBB'], tarikh_beli=['2026-11-02'] * 2,
                              harga_beli=[100.0, 100.0], tarikh_keluar=['', '2026-11-03'], untung_pct=[np.nan, -5.0]))
        r = KS.buku_harian(P, self.sesi, self.C, kos=0.0)['M01']
        # Hari 1: AAA 1.10, BBB 1.00 -> (0.10 + 0.0) / 2 = +5%.
        self.assertAlmostEqual(float(r.iloc[0]), 5.0)
        # Hari 2: AAA 1.10 -> 1.21 (+0.11); BBB keluar pada -5% (1.00 -> 0.95, -0.05) -> 0.06 / 2.10
        self.assertAlmostEqual(float(r.iloc[1]), 0.06 / 2.10 * 100)
        # Hari 3: hanya AAA, rata
        self.assertAlmostEqual(float(r.iloc[2]), 0.0)

    def test_kos_ditolak(self):
        P = pd.DataFrame(dict(id_kaedah=['M01'], saham=['AAA'], tarikh_beli=['2026-11-02'], harga_beli=[100.0],
                              tarikh_keluar=[''], untung_pct=[np.nan]))
        r = KS.buku_harian(P, self.sesi, self.C, kos=0.1)['M01']
        self.assertAlmostEqual(float(r.iloc[0]), 10.0 - 0.1)

    def test_nw_lebih_luas_bila_autokorelasi(self):
        x = np.repeat([1.0, -1.0], 30)                  # sangat berautokorelasi
        self.assertGreater(KS.nw_se(x, 5), x.std(ddof=0) / np.sqrt(len(x)))


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
        self.assertIsNone(d['ci_bawah'])                  # CI setiap-posisi dibuang 7 Nov (tanda dikongsi)


class TestSlip(unittest.TestCase):
    """Sensitiviti slippage henti (maklumat, 8 Nov 2026)."""

    def test_hanya_henti_intrahari_diisi_tepat(self):
        P = pd.DataFrame(dict(
            saham=['AAA', 'BBB', 'CCC', 'DDD'], terbuka=[False, False, False, True],
            sebab_keluar=['henti', 'henti', 'isyarat keluar', ''], harga_beli=[100.0] * 4,
            henti=[95.0, 95.0, 95.0, 95.0], harga_keluar=[95.0, 90.0, 95.0, np.nan],
            tarikh_keluar=['2026-11-05', '2026-11-05', '2026-11-05', ''], pul=[-5.2, -10.2, -5.2, 1.0]))
        rendah = {('AAA', '20261105'): 91.0, ('BBB', '20261105'): 89.0, ('CCC', '20261105'): 91.0}
        s = KS.pul_slip(P, rendah)
        self.assertAlmostEqual(s[0], -5.2 - 2.0)     # isian tengah (95+91)/2 = 93 -> rugi lebih 2 mata
        self.assertAlmostEqual(s[1], -10.2)           # jurang buka (diisi 90, bukan pada henti): tidak diubah
        self.assertAlmostEqual(s[2], -5.2)            # bukan keluar henti
        self.assertAlmostEqual(s[3], 1.0)             # masih terbuka


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

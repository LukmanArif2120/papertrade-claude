"""Ujian unit bagi standard/skor_kaedah.py.

TestKunci ialah PRADAFTAR (standard/SPEC_SKOR_KAEDAH.md, 9 Nov 2026). Ia sengaja menyalin setiap berat dan sauh
sebagai literal: mengubahnya selepas melihat data mesti menyentuh DUA fail dan satu spec bertarikh.
"""
import json
import os
import sys
import tempfile
import unittest

import numpy as np

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import skor_kaedah as SK  # noqa: E402


class TestKunci(unittest.TestCase):
    """Berat dan sauh dipradaftar 9 Nov 2026. JANGAN ubah tanpa keputusan pengguna + pradaftar baharu bertarikh."""

    def test_berat(self):
        self.assertEqual(SK.BERAT_TIANG, {'A': 0.35, 'B': 0.30, 'C': 0.25, 'D': 0.10})
        self.assertAlmostEqual(sum(SK.BERAT_TIANG.values()), 1.0)
        self.assertEqual(SK.BERAT_METRIK, {'A1': ('A', 20), 'A2': ('A', 10), 'A3': ('A', 5),
                                           'B1': ('B', 12), 'B2': ('B', 6), 'B3': ('B', 6), 'B4': ('B', 6),
                                           'C1': ('C', 12), 'C2': ('C', 8), 'C3': ('C', 5),
                                           'D1': ('D', 4), 'D2': ('D', 3), 'D3': ('D', 3)})
        self.assertEqual(sum(b for _, b in SK.BERAT_METRIK.values()), 100)
        for t, w in SK.BERAT_TIANG.items():      # berat metrik dalam tiang = berat tiang x 100
            self.assertEqual(sum(b for tt, b in SK.BERAT_METRIK.values() if tt == t), round(w * 100))

    def test_sauh(self):
        self.assertEqual(SK.SAUH, {'A1': (-2.0, 0.0, 2.0), 'A2': (-10.0, 0.0, 10.0), 'A3': (0.5, 1.0, 2.0),
                                   'B1': (-1.0, 0.0, 1.0), 'B2': (10.0, 5.0, 0.0), 'B3': (-24.0, -16.0, -8.0),
                                   'B4': (-2.0, 0.0, 2.0), 'D1': (-0.2, 0.0, 0.2), 'D3': (0.0, 0.5, 1.0)})
        self.assertEqual(SK.C1_T_MIN, 2.0)
        self.assertEqual(SK.C2_HARI_PENUH, 60)
        self.assertEqual(SK.C2_TUTUP_PENUH, 100)
        self.assertEqual(SK.C3_REJIM_PENUH, 10)
        self.assertEqual(SK.D2_LIFT_SKALA, 4.0)
        self.assertEqual(SK.KECUT_H, 20)
        self.assertEqual(SK.SILING, {'NEGATIF': 20.0, 'GANTUNG': 30.0, 'BERSARA': 30.0, 'GAGAL': 40.0})
        self.assertEqual(SK.LANTAI_GEO, 1.0)
        self.assertEqual(SK.SPEARMAN_HARI, 7)
        self.assertEqual(SK.NEUTRAL, 50.0)
        self.assertEqual(SK.PRADAFTAR, '2026-11-09')

    def test_spec_menyebut(self):
        with open(os.path.join(AKAR, 'BacktestShariah2', 'standard', 'SPEC_SKOR_KAEDAH.md'), encoding='utf-8') as f:
            s = f.read()
        for t in ('Dipradaftar 9 Nov 2026', 'Untung 0.35', 'Tahan 0.30', 'Bukti 0.25', 'Konsisten 0.10',
                  '`KECUT_H` = 20', '`C1_T_MIN` = 2.0', '`C2_HARI_PENUH` = 60', '`C2_TUTUP_PENUH` = 100',
                  '`C3_REJIM_PENUH` = 10', '`D2_LIFT_SKALA` (= 4)', 'NEGATIF ≤ 20', 'GAGAL ≤ 40',
                  '−2 · 0 · +2', '0.5 · 1.0 · 2.0', '−24 · −16 · −8', '−0.2 · 0 · +0.2', '0 · 0.5 · 1.0',
                  'BUKAN keputusan wang sebenar'):
            self.assertIn(t, s)


class TestPeta(unittest.TestCase):

    def test_naik(self):
        self.assertEqual(SK.peta(-2, SK.SAUH['A1']), 0)
        self.assertEqual(SK.peta(0, SK.SAUH['A1']), 50)
        self.assertEqual(SK.peta(2, SK.SAUH['A1']), 100)
        self.assertEqual(SK.peta(1, SK.SAUH['A1']), 75)
        self.assertEqual(SK.peta(9, SK.SAUH['A1']), 100)         # dipotong
        self.assertEqual(SK.peta(None, SK.SAUH['A1']), 50)       # tiada data = neutral
        self.assertEqual(SK.peta(float('nan'), SK.SAUH['A1']), 50)
        self.assertEqual(SK.peta(1.5, SK.SAUH['A3']), 75)        # sekeping tidak simetri

    def test_turun(self):
        self.assertEqual(SK.peta(10, SK.SAUH['B2']), 0)
        self.assertEqual(SK.peta(5, SK.SAUH['B2']), 50)
        self.assertEqual(SK.peta(0, SK.SAUH['B2']), 100)
        self.assertEqual(SK.peta(2.5, SK.SAUH['B2']), 75)
        self.assertEqual(SK.peta(20, SK.SAUH['B2']), 0)

    def test_e_maks(self):
        self.assertEqual(SK.e_maks(1), 0.0)
        self.assertAlmostEqual(SK.e_maks(223), 2.80, places=2)
        self.assertEqual(SK.t_sauh(5), 2.0)                     # N kecil: lantai 2.0
        self.assertGreater(SK.t_sauh(223), 2.0)

    def test_skala_log(self):
        self.assertEqual(SK.skala_log(0, 60), 0)
        self.assertEqual(SK.skala_log(60, 60), 100)
        self.assertEqual(SK.skala_log(600, 60), 100)
        self.assertAlmostEqual(SK.skala_log(16, 60), 100 * np.log1p(16) / np.log1p(60))

    def test_ulcer_kratio(self):
        self.assertIsNone(SK.ulcer([1.0]))
        self.assertAlmostEqual(SK.ulcer([1.0, 1.0, 1.0]), 0.0)
        self.assertAlmostEqual(SK.ulcer([0.9, 0.9]), 10.0)      # puncak termasuk asas 1.0
        naik = [1.0 * 1.001 ** i for i in range(1, 30)]
        self.assertGreater(SK.k_ratio(naik), 1.0)
        turun = [1.0 / 1.001 ** i for i in range(1, 30)]
        self.assertLess(SK.k_ratio(turun), -1.0)
        self.assertIsNone(SK.k_ratio([1.0, 1.1, 1.2]))           # n < 5

    def test_d2(self):
        self.assertEqual(SK.skor_d2({}), 50)
        self.assertEqual(SK.skor_d2(dict(lift=1.0, lift_lulus=True)), 100)
        self.assertEqual(SK.skor_d2(dict(lift=-1.0, lift_lulus=True)), 0)
        self.assertEqual(SK.skor_d2(dict(lift=2.0, lift_lulus=False)), 75)
        self.assertEqual(SK.skor_d2(dict(lift=-9.0, lift_lulus=False)), 0)

    def test_wfe(self):
        self.assertIsNone(SK.wfe(dict(buku_harian=0.1)))
        self.assertAlmostEqual(SK.wfe(dict(buku_harian=0.1, bt_purata=2.0, bt_hari=10)), 0.5)
        self.assertIsNone(SK.wfe(dict(buku_harian=0.1, bt_purata=-2.0, bt_hari=10)))


class TestLorongLangsung(unittest.TestCase):

    def setUp(self):
        import pandas as pd
        tarikh = [f'2026-10-{16+i:02d}' for i in range(6)] + ['2026-11-03', '2026-11-04']
        self.T4 = pd.DataFrame({'tarikh': tarikh, 'N1X1|L1': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.65, 1.5],
                                'M1|L1': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
                                'M2|L1': [np.nan] * 6 + [1.02, 1.03]}).set_index('tarikh')
        self.S = pd.DataFrame({'buka': [100.0] * 8, 'tutup': [100.0, 101, 102, 103, 104, 105, 106, 107]},
                              index=tarikh)

    def test_mxx_lorong_penuh(self):
        L = SK.lorong_langsung(self.T4, self.S, 'M1', '2026-10-15')
        self.assertEqual(L['sesi'], 8)
        self.assertAlmostEqual(L['pul'], 70.0)
        self.assertAlmostEqual(L['spus'], 7.0)
        self.assertAlmostEqual(L['lebih_spus'], 63.0)
        self.assertAlmostEqual(L['mdd'], 0.0)
        self.assertEqual(L['nisbah'], 10.0)                       # MDD sifar -> dipotong 10

    def test_nxx_dipotong_dan_diasas_semula(self):
        L = SK.lorong_langsung(self.T4, self.S, 'N1X1', '2026-11-03')
        self.assertEqual(L['sesi'], 2)
        self.assertAlmostEqual(L['ekuiti'][0], 1.65 / 1.5)        # asas = tutup sesi sebelum mula LANGSUNG
        self.assertAlmostEqual(L['pul'], 0.0)
        self.assertAlmostEqual(L['mdd'], (1.5 / 1.65 - 1) * 100)  # puncak 1.1 -> 1.0
        self.assertAlmostEqual(L['spus'], 7.0)                    # asas buka 2026-11-03 = 100, tutup 107
        self.assertAlmostEqual(L['lebih_spus'], -7.0)

    def test_lorong_mula_selepas_langsung(self):
        L = SK.lorong_langsung(self.T4, self.S, 'M2', '2026-11-03')
        self.assertEqual(L['sesi'], 2)
        self.assertAlmostEqual(L['ekuiti'][0], 1.02)              # tiada sesi sebelum: asas 1.0

    def test_tiada(self):
        self.assertIsNone(SK.lorong_langsung(self.T4, self.S, 'M9', '2026-10-15'))
        self.assertIsNone(SK.lorong_langsung(self.T4, self.S, 'M1', '2026-12-01'))
        self.assertIsNone(SK.lorong_langsung(None, self.S, 'M1', '2026-10-15'))
        L = SK.lorong_langsung(self.T4, None, 'M1', '2026-10-15')
        self.assertIsNone(L['lebih_spus'])


def baris(**k):
    r = dict(id='M999', nama='Ujian', keluarga='M', status='BELUM CUKUP', pantau='OK', hari_beli=20, n=50, tutup=30,
             jangkaan=1.0, payoff=1.5, cvar10=-12.0, tanpa5=0.5, hari_on=10, hari_off=10,
             buku_harian=0.10, buku_ci_bawah=-0.02, buku_ci_atas=0.22, buku_sesi=20,
             lift=None, lift_lulus=None, bt_purata=5.0, bt_hari=10.0, mula_langsung='2026-10-15')
    r.update(k)
    return r


class TestGabungan(unittest.TestCase):

    def test_tiang_geometri_kecut(self):
        T = {'A': 100, 'B': 100, 'C': 100, 'D': 100}
        self.assertAlmostEqual(SK.geometri(T), 100.0)
        T = {'A': 100, 'B': 0, 'C': 100, 'D': 100}
        self.assertLess(SK.geometri(T), 30)                      # satu tiang sifar menarik ke bawah
        T = {'A': 60, 'B': 60, 'C': 60, 'D': 60}
        self.assertAlmostEqual(SK.geometri(T), 60.0)
        s, w = SK.kecut(90, 20)
        self.assertAlmostEqual(w, 0.5)
        self.assertAlmostEqual(s, 70.0)
        s, w = SK.kecut(90, 0)
        self.assertAlmostEqual(s, 50.0)

    def test_siling(self):
        self.assertEqual(SK.siling(70, dict(status='NEGATIF')), 20)
        self.assertEqual(SK.siling(70, dict(status='BELUM CUKUP', pantau='GANTUNG')), 30)
        self.assertEqual(SK.siling(70, dict(status='GAGAL')), 40)
        self.assertEqual(SK.siling(70, dict(status='TERBUKTI', pantau='OK')), 70)
        self.assertEqual(SK.siling(15, dict(status='NEGATIF')), 15)

    def test_skor_baris(self):
        ek = [1.0 + 0.002 * i for i in range(1, 21)]
        L = {'M999': dict(sesi=20, pul=4.0, mdd=-1.0, nisbah=0.8, spus=1.0, lebih_spus=3.0, ekuiti=ek)}
        r = SK.skor_baris(baris(), L, 223)
        self.assertEqual(set(r['markah']), set(SK.BERAT_METRIK))
        self.assertTrue(0 <= r['skor'] <= 100)
        self.assertGreater(r['skor'], 50)                         # kaedah baik, 20 hari beli -> atas 50
        self.assertAlmostEqual(r['berat_data'], 0.5)
        self.assertEqual(r['markah']['C3'], 100)
        self.assertEqual(r['markah']['D2'], 50)
        self.assertEqual(r['markah']['D3'], 20)                   # WFE 0.1 / (5/10) = 0.2
        # tiada T4: Ulcer dan K-ratio neutral
        r2 = SK.skor_baris(baris(), {}, 223)
        self.assertEqual(r2['markah']['B2'], 50)
        self.assertEqual(r2['markah']['D1'], 50)
        # hari beli 1: skor hampir 50 walaupun metrik hebat
        r3 = SK.skor_baris(baris(hari_beli=1, jangkaan=10, payoff=5), L, 223)
        self.assertLess(abs(r3['skor'] - 50), 3)

    def test_wfe_markah(self):
        r = SK.skor_baris(baris(buku_harian=0.1, bt_purata=5.0, bt_hari=10.0), {}, 223)
        self.assertAlmostEqual(r['mentah']['D3'], 0.2)
        self.assertEqual(r['markah']['D3'], 20)

    def test_hujung_ke_hujung(self):
        import kad_skor as KS
        with tempfile.TemporaryDirectory() as d:
            rows = []
            for i in range(12):
                r = baris(id=f'M{i:03d}', jangkaan=1.0 - 0.2 * i, t4_pul=2.0 - 0.3 * i)
                r['gate'] = {g: False for g in KS.KOL_GATE}
                r['sebab'] = {}
                rows.append(r)
            kj = os.path.join(d, 'kad_skor.json')
            KS.tulis_json(kj, dict(kini='2026-11-09', harga_pada='2026-11-06', hari_beli=16, hari_on=1, hari_off=15), rows)
            import pandas as pd
            T = {'tarikh': [f'2026-10-{16+i:02d}' for i in range(10)]}
            for j in range(12):
                T[f'M{j:03d}|L1'] = [1 + (0.004 - 0.0005 * j) * i for i in range(10)]
                T[f'M{j:03d}|L2'] = [1.0] * 10
            pd.DataFrame(T).to_csv(os.path.join(d, 't4_siri.csv'), index=False)
            SK.KS_JSON, SK.T4_SIRI, SK.SPUS_HARIAN = kj, os.path.join(d, 't4_siri.csv'), os.path.join(d, 'tiada.csv')
            SK.JSN, SK.MD, SK.SEJARAH = (os.path.join(d, 'skor.json'), os.path.join(d, 'SKOR.md'),
                                         os.path.join(d, 'sejarah.csv'))
            self.assertEqual(SK.main(), 0)
            M, R = SK.baca_json(SK.JSN)
            self.assertEqual(len(R), 12)
            self.assertEqual([r['id'] for r in R][0], 'M000')     # jangkaan terbaik di atas
            self.assertTrue(all(R[i]['skor'] >= R[i + 1]['skor'] for i in range(11)))
            self.assertIsNone(M['spearman'])
            s = open(SK.MD, encoding='utf-8').read()
            self.assertIn('BUKAN keputusan', s)
            self.assertIn('Status keputusan', s)
            # larian kedua pada tarikh sama: tiada perubahan, sejarah tidak bertambah
            self.assertEqual(SK.main(), 0)
            self.assertEqual(len(pd.read_csv(SK.SEJARAH)), 12)
            # snapshot 8 hari lalu -> Spearman dikira
            S = pd.read_csv(SK.SEJARAH)
            S2 = S.copy(); S2['tarikh'] = '2026-10-29'; S2['skor'] = S2['skor'].to_numpy()[::-1]
            pd.concat([S2, S]).to_csv(SK.SEJARAH, index=False)
            sp = SK.spearman(pd.read_csv(SK.SEJARAH, dtype={'tarikh': str}), '2026-11-06', R, rows)
            self.assertEqual(sp['tarikh'], '2026-10-29')
            self.assertEqual(sp['n'], 12)


if __name__ == '__main__':
    unittest.main()

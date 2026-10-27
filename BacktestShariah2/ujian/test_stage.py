# Ujian standard/stage.py (Stage Analysis Weinstein mingguan, dashboard harian/stage).
import os, sys, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import stage as S  # noqa: E402

M = S.MINUS


def frame(c, v=None, mula='2025-01-06'):
    """Bar harian daripada senarai tutup (hari dagangan berturut-turut mulai Isnin)."""
    c = np.asarray(c, float)
    d = [int(x.strftime('%Y%m%d')) for x in pd.bdate_range(mula, periods=len(c))]
    return pd.DataFrame(dict(date=d, open=c, high=c * 1.01, low=c * 0.99, close=c,
                             volume=np.full(len(c), 1e6) if v is None else np.asarray(v, float)))


class Mingguan(unittest.TestCase):
    def test_kumpul_isnin_jumaat(self):
        a = S.mingguan(frame([1, 2, 3, 4, 5, 6, 7]))          # 5 hari + 2 hari
        self.assertEqual(len(a), 2)
        self.assertEqual(list(a.n), [5, 2])
        self.assertEqual(list(a.open), [1.0, 6.0])
        self.assertEqual(list(a.close), [5.0, 7.0])
        self.assertEqual(list(a.high.round(2)), [5.05, 7.07])
        self.assertEqual(list(a.volume), [5e6, 2e6])
        self.assertEqual(list(a.tarikh), [20250110, 20250114])


class Siri(unittest.TestCase):
    def test_peringkat(self):
        c = np.array([10.0, 11, 9, 9, 11])
        turun = np.array([np.nan, 10.2, 10.1, 10.0, 9.9])     # minggu 1 tiada cerun
        self.assertTrue(np.isnan(S.siri(c, turun)[1]))
        self.assertEqual(list(S.siri(c, turun)[2:]), [4.0, 4.0, 0.0])   # bawah MA30 menurun = 4; atas = 1/3
        naik = np.array([np.nan, 9.9, 10.0, 10.1, 10.2])
        self.assertEqual(list(S.siri(c, naik)[2:]), [0.0, 0.0, 2.0])    # bawah MA30 menaik = 1/3; atas = 2


class Jejak(unittest.TestCase):
    def test_surut_ke_neutral_tidak_set_semula(self):
        p = np.array([np.nan, 4, 4, 2, 2, 0, 2], float)       # 4 -> 2 (breakout) -> 1/3 -> 2 (sambungan)
        mula, dari, tepat, awal = S.jejak(p)
        self.assertEqual(list(awal), [False, False, False, True, False, False, False])
        self.assertEqual(mula[6], 3)                          # kitaran sama: kiraan minggu diteruskan
        self.assertEqual(dari[6], 4)
        self.assertTrue(tepat[6])

    def test_mula_liputan_tersensor(self):
        p = np.array([2, 2, 2], float)                        # sudah dalam Stage 2 pada minggu pertama
        mula, dari, tepat, awal = S.jejak(p)
        self.assertFalse(awal.any())                          # bukan breakout: hanya permulaan data
        self.assertFalse(tepat.any())
        self.assertEqual(list(mula), [0, 0, 0])

    def test_neutral_selepas_stage_2_ialah_kawasan_puncak(self):
        p = np.array([2, 2, 0, 0, 4], float)
        mula, dari, tepat, awal = S.jejak(p)
        self.assertEqual(dari[3], 2)                          # 1/3 selepas Stage 2 = Stage 3
        self.assertEqual(mula[3], 2)                          # minggu dikira dari mula larian 1/3
        self.assertTrue(awal[4])                              # 4A: breakdown pertama sejak Stage 2


class Label(unittest.TestCase):
    def test_sebelas_label(self):
        self.assertEqual(S.label(0, 5, False, None), '1/3')
        self.assertEqual(S.label(2, 1, True, True), '2A')     # minggu breakout: tiada varian MA10
        self.assertEqual(S.label(2, 5, False, False), '2')
        self.assertEqual(S.label(2, 5, False, True), '2' + M)
        self.assertEqual(S.label(2, S.LEWAT, False, False), '2B')
        self.assertEqual(S.label(2, S.LEWAT, False, True), '2B' + M)
        self.assertEqual(S.label(4, 1, True, False), '4A')
        self.assertEqual(S.label(4, 5, False, True), '4')     # Stage 4 bawah MA10 = normal
        self.assertEqual(S.label(4, 5, False, False), '4' + M)
        self.assertEqual(S.label(4, S.LEWAT, False, True), '4B')
        self.assertEqual(S.label(4, S.LEWAT, False, False), '4B' + M)


class Kualiti(unittest.TestCase):
    def test_rs_dan_volum(self):
        self.assertEqual(S.kualiti(5.0, 2.5), '+')
        self.assertEqual(S.kualiti(5.0, 1.2), '')             # RS baik tetapi volum mula lemah
        self.assertEqual(S.kualiti(5.0, None), '+')           # volum mula tidak diketahui -> RS sahaja
        self.assertEqual(S.kualiti(-1.0, 9.0), M)
        self.assertEqual(S.kualiti(None, 9.0), '')


class Kira(unittest.TestCase):
    def siri_turun_naik(self):
        """200 hari turun, kemudian 200 hari naik: Stage 4 -> 1/3 -> Stage 2."""
        return np.r_[np.linspace(200, 100, 200), np.linspace(100, 260, 200)]

    def test_hujung_stage_2(self):
        r = S.kira(frame(self.siri_turun_naik()))
        self.assertEqual(r['p'], 2)
        self.assertTrue(r['label'].startswith('2'))
        self.assertTrue(r['tepat'])
        self.assertEqual(r['dari'], 4)
        self.assertGreater(r['minggu'], 1)

    def test_breakout_2a_dengan_volum(self):
        c = self.siri_turun_naik()
        g = S.garis(frame(c))
        a2 = [x for x in g if x[4] == '2A']
        self.assertEqual(len(a2), 1)                          # satu sahaja minggu 2A dalam kitaran ini
        self.assertEqual([x[4] for x in g][0], '4')           # mula liputan: Stage 4 tanpa label A

    def test_sejarah_pendek(self):
        r = S.kira(frame(np.full(60, 10.0)))
        self.assertIsNone(r['p'])
        self.assertIn('minggu', r['sebab'])

    def test_mansfield_dan_dokumen(self):
        c = self.siri_turun_naik()
        H = {'AAA': frame(c), 'BBB': frame(np.full(400, 50.0))}
        spy = S.spy_mingguan({'SPY': frame(np.linspace(100, 120, 400))})
        d = S.dokumen(H, {'AAA', 'BBB', 'CCC'}, {'SPY': frame(np.linspace(100, 120, 400))})
        self.assertEqual(d['lajur'], S.LAJUR)
        self.assertEqual([r[0] for r in d['rows']], ['AAA', 'BBB', 'CCC'])
        self.assertTrue(all(v is None for v in d['rows'][2][1:]))     # CCC: tiada harga
        k = {x: i for i, x in enumerate(S.LAJUR)}
        self.assertIsNotNone(S.kira(frame(c), spy)['mansfield'])
        self.assertEqual(d['rows'][1][k['label']], '1/3')             # harga rata: MA30 mendatar
        self.assertEqual(sum(d['kiraan'].values()), 3)


if __name__ == '__main__':
    unittest.main()

"""Ujian unit bagi REVERSE/step15_setup.py (grid dikunci, jalur tengah, pulangan, aritmetik 70/30)."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from REVERSE import step15_setup as SU  # noqa: E402


def bar(n=400, mula='2014-01-02', naik=0.0, rendah_di=None, puncak_di=None):
    d = pd.bdate_range(mula, periods=n)
    c = 100.0 + naik * np.arange(n)
    if puncak_di is not None:
        c = c.copy()
        c[puncak_di:] = c[puncak_di]          # datar selepas puncak -> Chandelier tercetus
    lo = c - 1.0
    if rendah_di is not None:
        lo = lo.copy()
        lo[rendah_di] = c[rendah_di] - 50.0   # jurang dalam -> henti tercetus
    return pd.DataFrame({'ticker': 'T', 'date': d, 'open': c, 'high': c + 1.0, 'low': lo,
                         'close': c, 'volume': 1e8})


class TestGridDikunci(unittest.TestCase):
    """Spec §3 menetapkan grid; melebarkannya memerlukan pradaftar baharu."""

    def _d(self, n=50):
        rng = np.random.default_rng(1)
        k = {c: rng.normal(50, 10, n) for c in ('rsi14', 'stoch_k', 'bb_pctb', 'mfi14')}
        k.update({c: rng.integers(0, 2, n).astype(bool) for c in
                  ('macd_cross', 'rsi_lintas50', 'rsi_lintas60', 'ema_crossback', 'donchian20',
                   'pocket_pivot', 'gap_and_go', 'vcp', 'bb_squeeze', 'breakout_asas',
                   'supertrend')})
        k.update(hari_macd_cross=rng.integers(0, 30, n).astype(float),
                 hari_gc=rng.integers(0, 90, n).astype(float),
                 j_ma200=rng.normal(0, 10, n), cerun_ma50=rng.normal(0, 2, n),
                 vol_n50=rng.uniform(0.5, 2.0, n))
        return pd.DataFrame(k)

    def test_672_setup(self):
        S, nt, nj, npf = SU.grid(self._d())
        self.assertEqual((nt, nj, npf), (14, 8, 6))
        self.assertEqual(len(S), 672)

    def test_dua_pemicu_urutan_ada(self):
        T = SU.pemicu(self._d())
        self.assertIn('urutan:macd->gc', T)
        self.assertIn('urutan:gc->macd', T)

    def test_penapis_tiada_ialah_kawalan(self):
        P = SU.penapis(self._d(30))
        self.assertIn('tiada', P)
        self.assertTrue(P['tiada'].all())

    def test_supertrend_arah_bukan_kehadiran(self):
        """PEPIJAT 29 Okt 2026: supertrend ialah ARAH -1/+1, bukan bendera 0/1.

        `astype(bool)` memberi True untuk KEDUA-DUA -1 dan +1, jadi penapis itu menjadi no-op
        yang menduplikasi 'tiada' dan membazirkan slot tahan. Ujian ini mengunci pembetulan.
        """
        d = self._d(4)
        d['supertrend'] = [1.0, -1.0, 1.0, -1.0]
        P = SU.penapis(d)
        self.assertEqual(list(P['supertrend']), [True, False, True, False])
        self.assertFalse(bool(P['supertrend'].all()), 'supertrend tidak boleh no-op')

    def test_penapis_supertrend_bukan_salinan_tiada(self):
        d = self._d(200)
        d['supertrend'] = np.resize([1.0, -1.0], 200)
        P = SU.penapis(d)
        self.assertFalse(np.array_equal(P['supertrend'], P['tiada']))

    def test_jalur_ialah_julat_TENGAH_bukan_kuintil(self):
        # Inilah jurang yang spec §1 namakan: kuintil tidak boleh menyatakan julat tengah.
        d = pd.DataFrame({'rsi14': [30.0, 50.0, 80.0], 'stoch_k': [50.0] * 3,
                          'bb_pctb': [50.0] * 3, 'mfi14': [50.0] * 3})
        J = SU.jalur(d)
        m = J['rsi14[45,60]']
        self.assertFalse(bool(m[0]))   # 30 di bawah jalur
        self.assertTrue(bool(m[1]))    # 50 DALAM jalur
        self.assertFalse(bool(m[2]))   # 80 di atas jalur

    def test_jalur_mengecualikan_nan(self):
        d = pd.DataFrame({'rsi14': [np.nan, 50.0], 'stoch_k': [50.0] * 2,
                          'bb_pctb': [50.0] * 2, 'mfi14': [50.0] * 2})
        m = SU.jalur(d)['rsi14[45,60]']
        self.assertFalse(bool(m[0]))

    def test_pecahan_latih_tahan_tidak_bertindih(self):
        self.assertLess(SU.LATIH[1], SU.TAHAN[0])
        self.assertEqual(SU.LATIH, (2012, 2019))
        self.assertEqual(SU.TAHAN, (2020, 2025))


class TestPulangan(unittest.TestCase):
    def test_harga_tetap_memberi_kos_sahaja(self):
        R = SU.pul_satu_ticker(bar())
        v = R.E63.to_numpy()[:200]
        self.assertTrue(np.all(v[np.isfinite(v)] < 0))        # kos dua sisi
        self.assertTrue(np.all(v[np.isfinite(v)] > -0.02))

    def test_menaik_memberi_pulangan_positif(self):
        R = SU.pul_satu_ticker(bar(naik=0.5))
        self.assertGreater(float(np.nanmean(R.E63.to_numpy()[:200])), 0.10)

    def test_henti_mengurangkan_bila_jurang_dalam(self):
        tanpa = SU.pul_satu_ticker(bar(naik=0.2))
        dgn = SU.pul_satu_ticker(bar(naik=0.2, rendah_di=100))
        # Bar sebelum jurang mesti lebih buruk dengan henti daripada tanpa henti.
        a = float(np.nanmean(dgn.E63S.to_numpy()[60:99]))
        b = float(np.nanmean(tanpa.E63S.to_numpy()[60:99]))
        self.assertLess(a, b)

    def test_trail_keluar_lebih_awal_selepas_puncak(self):
        R = SU.pul_satu_ticker(bar(naik=0.5, puncak_di=120))
        self.assertTrue(np.isfinite(R.ETRAIL.to_numpy()[50]))

    def test_tiada_pandang_hadapan_pada_bar_awal(self):
        # Mengubah bar TERAKHIR tidak boleh menukar pulangan bar awal.
        g1 = bar(naik=0.2)
        g2 = g1.copy()
        g2.loc[g2.index[-1], ['open', 'high', 'low', 'close']] = 9999.0
        a = SU.pul_satu_ticker(g1).E63.to_numpy()[:200]
        b = SU.pul_satu_ticker(g2).E63.to_numpy()[:200]
        np.testing.assert_allclose(a, b, rtol=1e-9)


class TestMetrik(unittest.TestCase):
    def test_aritmetik_70_30_pengguna(self):
        """Premis pengguna: 70% menang, 30% rugi ditampung henti.

        70 dagangan +1% dan 30 dagangan -4% memberi kadar menang 70% TETAPI jangkaan -0.5%.
        Ujian ini mengkodkan sebab kadar menang bukan kriteria (spec §6).
        """
        pul = np.array([0.01] * 70 + [-0.04] * 30)
        m = SU.metrik_asas(pul)
        self.assertAlmostEqual(m['menang'], 70.0, places=6)
        self.assertAlmostEqual(m['untung'], 1.0, places=6)
        self.assertAlmostEqual(m['rugi'], -4.0, places=6)
        self.assertAlmostEqual(m['jangkaan'], -0.5, places=6)
        self.assertLess(m['jangkaan'], 0)

    def test_kadar_menang_rendah_boleh_positif(self):
        # Sebaliknya juga benar: 30% menang pada +10% dengan 70% rugi pada -2% = +1.6%.
        m = SU.metrik_asas(np.array([0.10] * 30 + [-0.02] * 70))
        self.assertAlmostEqual(m['menang'], 30.0, places=6)
        self.assertGreater(m['jangkaan'], 0)

    def test_tanpa5_membuang_pemenang_teratas(self):
        pul = np.concatenate([[5.0], np.full(99, 0.001)])
        m = SU.metrik_asas(pul)
        self.assertGreater(m['jangkaan'], m['tanpa5'])

    def test_kosong_memberi_n_sifar(self):
        self.assertEqual(SU.metrik_asas(np.array([np.nan, np.nan]))['n'], 0)


if __name__ == '__main__':
    unittest.main()

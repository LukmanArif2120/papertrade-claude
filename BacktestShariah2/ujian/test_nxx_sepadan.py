"""Kaedah Nxx produksi MESTI sepadan bit-untuk-bit dengan kajian REVERSE.

Kalau ujian ini gagal, jejak hadapan Papertrade C sedang menjejak peraturan yang BUKAN
peraturan yang `REVERSE/silang_akhir.csv` ukur, jadi kesemua nombor pradaftar
`REVERSE/SPEC_JEJAK_N.md` tidak lagi terpakai. Ia bukan ujian kosmetik.

Bahaya khusus yang ia jaga: `enjin.rsi` guna `ewm(alpha=1/n, adjust=False)` tanpa benih
purata-n dan `enjin.atr` guna `rolling(n).mean()`, sedangkan kajian guna pelicinan Wilder
dengan benih purata-n. Modul Nxx mesti memakai `kaedah/_nxx.py`, bukan pembantu enjin.
"""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
sys.path.insert(0, str(AKAR / 'BacktestShariah2' / 'kod'))
sys.path.insert(0, str(AKAR / 'BacktestShariah2' / 'kod' / 'kaedah'))

import kaedah._nxx as NX                       # noqa: E402
import REVERSE.teras.ind as IND                # noqa: E402

STOR = AKAR / 'BacktestShariah2' / 'data' / 'harga' / 'stor' / 'harga_A.csv'
N_TICKER = 25
MIN_BAR = 300


def _harga():
    H = pd.read_csv(STOR)
    H['date'] = pd.to_datetime(H.date.astype(str), format='%Y%m%d')
    out = []
    for t in sorted(H.ticker.unique()):
        g = (H[H.ticker == t].sort_values('date').set_index('date')
             [['open', 'high', 'low', 'close', 'volume']].astype('float64'))
        if len(g) >= MIN_BAR:
            out.append((t, g))
        if len(out) >= N_TICKER:
            break
    return out


class TestNxxSepadan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not STOR.exists():
            raise unittest.SkipTest(f'stor harga tiada: {STOR}')
        cls.H = _harga()
        if not cls.H:
            raise unittest.SkipTest('tiada ticker dengan bar cukup')

    def test_lajur_indikator_identik(self):
        """rsi14, adx14, bb_pctb, vol_n50 mesti identik dengan REVERSE/teras/ind.py."""
        for t, g in self.H:
            a, b = NX.indikator(g), IND.kira(g)
            for k in ('rsi14', 'adx14', 'bb_pctb', 'vol_n50'):
                ok = np.isfinite(a[k]) & np.isfinite(b[k])
                self.assertGreater(int(ok.sum()), 100, f'{t} {k}: terlalu sedikit nilai sah')
                d = float((a[k] - b[k]).abs()[ok].max())
                self.assertLess(d, 1e-9, f'{t} {k}: maks |delta| {d:.3e}')

    def test_ema20_dan_sentuh_identik(self):
        """ema20 + sentuh_ema20 mesti identik dengan step18_nxx.tambahan."""
        for t, g in self.H:
            a = NX.indikator(g)
            e20 = g.close.ewm(span=20, adjust=False, min_periods=20).mean()
            ok = np.isfinite(a.ema20) & np.isfinite(e20)
            self.assertLess(float((a.ema20 - e20).abs()[ok].max()), 1e-9, t)
            self.assertEqual(int((a.sentuh_ema20.astype(bool) != (g.low <= e20)).sum()), 0, t)

    def test_topeng_identik(self):
        """N19/N20/N37/N115/GB02/X13 mesti sifar bar berbeza, dan mesti ADA isyarat."""
        jum = {k: 0 for k in ('N19', 'N20', 'N37', 'N115', 'GB02', 'X13')}
        for t, g in self.H:
            a, b = NX.indikator(g), IND.kira(g)
            e20 = g.close.ewm(span=20, adjust=False, min_periods=20).mean()
            ref = {
                'N19': (b.bb_pctb < 0) & (b.rsi14 < 30),
                'N20': ((b.bb_pctb.shift(1) < 0) & (b.bb_pctb > 0)
                        & (b.rsi14 > 30) & (b.rsi14.shift(1) <= 30)),
                'N37': b['gap_and_go'] > 0,
                'N115': (b.adx14 > 30) & (g.low <= e20) & (g.close > g.high.shift(1)),
                'X13': b.rsi14 > 70,
            }
            ref['GB02'] = ref['N19'] | ref['N37'] | ref['N115']
            got = {'N19': NX.n19(a), 'N20': NX.n20(a), 'N37': NX.n37(a),
                   'N115': NX.n115(a, g), 'GB02': NX.gb02_atau3(a, g), 'X13': NX.x13(a)}
            for k, r in ref.items():
                x = got[k].fillna(False).astype(bool)
                y = r.fillna(False).astype(bool)
                self.assertEqual(int((x != y).sum()), 0, f'{t} {k}: topeng terpesong')
                jum[k] += int(y.sum())
        for k, n in jum.items():
            self.assertGreater(n, 0, f'{k}: SIFAR isyarat rujukan — ujian sia-sia')

    def test_kesatuan_betul(self):
        """GB02 mesti KESATUAN (>= setiap kaki), bukan persilangan."""
        for t, g in self.H:
            a = NX.indikator(g)
            u = NX.gb02_atau3(a, g).fillna(False)
            for nama, kaki in (('N19', NX.n19(a)), ('N37', NX.n37(a)),
                               ('N115', NX.n115(a, g))):
                k = kaki.fillna(False)
                self.assertTrue(bool((u | k).equals(u)), f'{t}: {nama} bukan subset GB02')
            self.assertGreaterEqual(int(u.sum()), int(NX.n19(a).fillna(False).sum()), t)

    def test_modul_tiada_henti_tiada_sasaran(self):
        """Setiap modul Nxx: ADA_HENTI False, stop/tgt NaN -> kecacatan hari-0 mustahil."""
        import importlib
        for mid in ('N19', 'N20', 'N37', 'N115', 'GB02'):
            m = importlib.import_module(f'kaedah.{mid}')
            self.assertFalse(m.ADA_HENTI, mid)
            self.assertEqual(m.TMAX, NX.IMBAS, f'{mid}: TMAX mesti = IMBAS kajian 126')
            fr = {t: g.copy() for t, g in self.H}
            m.sedia(fr, None)
            for t, g in fr.items():
                self.assertTrue(bool(g.stop.isna().all()), f'{mid} {t}: stop bukan NaN')
                self.assertTrue(bool(g.tgt.isna().all()), f'{mid} {t}: tgt bukan NaN')
                self.assertIn('exitc', g.columns, f'{mid} {t}')
            self.assertGreater(int(sum(g.sig.sum() for g in fr.values())), 0,
                               f'{mid}: tiada isyarat sama sekali')

    def test_tiada_henti_hari_0(self):
        """Lalu enjin produksi: sebab keluar 'henti' mesti SIFAR (KOLAM_EKOR.md §4a)."""
        import importlib

        import enjin
        m = importlib.import_module('kaedah.GB02')
        fr = {t: g.copy() for t, g in self.H}
        m.sedia(fr, None)
        T = enjin.trades(fr, tmax=m.TMAX, warm=m.WARM)
        self.assertGreater(len(T), 0, 'tiada dagangan — ujian sia-sia')
        self.assertEqual(int((T.why == 'henti').sum()), 0, 'henti muncul walaupun stop NaN')
        self.assertGreater(int((T.why == 'isyarat keluar').sum()), 0, 'X13 tidak pernah cetus')


if __name__ == '__main__':
    unittest.main()

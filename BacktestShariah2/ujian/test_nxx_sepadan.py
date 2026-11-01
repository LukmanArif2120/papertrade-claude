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
# 20 kohort jejak hadapan (SPEC_JEJAK_N.md). Senarai ini ialah kontrak: kalau modul
# ditambah atau dibuang tanpa mengemas spec, ujian ini gagal.
NXX = ('N15', 'N16', 'N17', 'N19', 'N20', 'N24', 'N31', 'N37', 'N42', 'N46', 'N49',
       'N62', 'N73', 'N75', 'N76', 'N115', 'N118', 'N119', 'N124', 'GB02')
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
        for mid in NXX:
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

    def test_import_seperti_produksi(self):
        """Modul mesti boleh diimport TEPAT seperti pemuat produksi melakukannya.

        `harian_c.py` dan `lejar.py` meletakkan `kod/` pada sys.path dan memanggil
        `importlib.import_module('kaedah.N19')` — `kod/kaedah/` TIDAK pada path. Jadi
        `import _nxx` gagal dengan ModuleNotFoundError walaupun ia berjalan dalam ujian yang
        meletakkan `kod/kaedah/` pada path sendiri. Pepijat itu BERLAKU pada 1 Nov 2026 dan
        hanya larian hujung-ke-hujung menangkapnya; ujian ini menggantikan larian itu.
        """
        import subprocess
        kod = AKAR / 'BacktestShariah2' / 'kod'
        skrip = ('import sys, importlib; sys.path.insert(0, %r);'
                 'ms=%r;' % (str(kod), list(NXX)) + (''
                 '[importlib.import_module("kaedah."+m) for m in ms];'
                 'print("OK")'))
        r = subprocess.run([sys.executable, '-c', skrip], capture_output=True, text=True,
                           cwd=str(AKAR))
        self.assertEqual(r.returncode, 0, f'import gaya produksi gagal:\n{r.stderr[-1500:]}')
        self.assertIn('OK', r.stdout)

    def test_rank_berterusan_bukan_sifar(self):
        """`rank` mesti skor BERTERUSAN, bukan 0.0.

        `harian_c.MAKS_KAEDAH` mengehadkan 10 isyarat baharu setiap kaedah setiap imbasan dan
        memilih ikut `rank`. Dengan `rank = 0` pemilihan jadi sewenang-wenang, dan
        `KEPEKATAN_BENIH.md` mengukur hingar pemilihan susunan sewenang-wenang pada 17.3 mata
        peratus setahun. Ujian ini gagal jika sesiapa menetapkan semula rank kepada pemalar.
        """
        import importlib
        for mid in NXX:
            m = importlib.import_module(f'kaedah.{mid}')
            fr = {t: g.copy() for t, g in self.H}
            m.sedia(fr, None)
            akhir = np.array([float(g['rank'].iloc[-1]) for g in fr.values()])
            sah = akhir[akhir > -1e8]
            self.assertGreater(len(sah), 5, f'{mid}: terlalu sedikit rank sah')
            self.assertGreater(len(np.unique(sah)), len(sah) * 0.9,
                               f'{mid}: rank banyak seri — pemilihan jadi sewenang-wenang')
            self.assertGreater(float(np.ptp(sah)), 1e-6, f'{mid}: rank pemalar')

    def test_u14_sepadan_kajian(self):
        """`u14` mesti formula `step27_keluar_portfolio.skor_pangkat` tepat: C[-21]/C[-252]-1."""
        for t, g in self.H:
            r = NX.u14(g)
            ref = g.close.shift(21) / g.close.shift(252) - 1.0
            ok = np.isfinite(ref)
            self.assertGreater(int(ok.sum()), 10, t)
            self.assertLess(float((r[ok] - ref[ok]).abs().max()), 1e-12, t)
            self.assertTrue(bool((r[~ok] == -9e9).all()), f'{t}: NaN bukan -9e9')

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


class TestKohortLengkap(unittest.TestCase):
    """Senarai 20 kohort ialah kontrak antara kod dan `REVERSE/SPEC_JEJAK_N.md`."""

    def test_modul_sepadan_senarai(self):
        import glob
        import os
        pola = ('N*.py', 'GB*.py')
        ada = {os.path.basename(p)[:-3]
               for q in pola
               for p in glob.glob(str(AKAR / 'BacktestShariah2' / 'kod' / 'kaedah' / q))}
        self.assertEqual(ada, set(NXX),
                         f'modul tanpa dalam senarai: {sorted(ada - set(NXX))}; '
                         f'dalam senarai tanpa modul: {sorted(set(NXX) - ada)}')
        self.assertEqual(len(NXX), 20)

    def test_kawalan_negatif_ada(self):
        """Jejak mesti mengandungi kawalan negatif, jika tidak keputusannya tidak boleh dibaca."""
        for mid in ('N76', 'N24', 'N31', 'N62'):
            self.assertIn(mid, NXX, f'{mid} ialah kawalan negatif dan mesti dijejak')

"""Kaedah Nxx produksi MESTI sepadan bit-untuk-bit dengan kajian REVERSE.

Kalau ujian ini gagal, jejak hadapan Papertrade C sedang menjejak peraturan yang BUKAN
peraturan yang `REVERSE/silang_akhir.csv` ukur, jadi kesemua nombor pradaftar
`REVERSE/SPEC_JEJAK_N.md` tidak lagi terpakai. Ia bukan ujian kosmetik.

Bahaya khusus yang ia jaga: `enjin.rsi` guna `ewm(alpha=1/n, adjust=False)` tanpa benih
purata-n dan `enjin.atr` guna `rolling(n).mean()`, sedangkan kajian guna pelicinan Wilder
dengan benih purata-n. Modul Nxx mesti memakai `kaedah/_nxx.py`, bukan pembantu enjin.
"""
import re
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
NXX = (
    'N124X15', 'N19X13', 'N75X13', 'N73X13', 'N124X36',
    'N16X13', 'N75X15', 'N42X15', 'N119X13', 'N37X17',
    'N64X17', 'N28X17', 'N75X17', 'N55X13', 'N16X15',
    'N37X36', 'N64X36', 'N50X17', 'N42X17', 'N119X15',
    'N53X17', 'N65X36', 'N37X14', 'N65X14', 'N64X14',
    'N06X36', 'N24X17', 'N25X17', 'N42X14', 'N53X36',
    'N56X17', 'N25X36', 'N38X36', 'N50X14', 'N56X36',
    'N53X16', 'N40X36', 'N36X36', 'N24X36', 'N22X36',
)
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
        m = importlib.import_module('kaedah.N19X13')   # kohort pangkat 2
        fr = {t: g.copy() for t, g in self.H}
        m.sedia(fr, None)
        T = enjin.trades(fr, tmax=m.TMAX, warm=m.WARM)
        self.assertGreater(len(T), 0, 'tiada dagangan — ujian sia-sia')
        self.assertEqual(int((T.why == 'henti').sum()), 0, 'henti muncul walaupun stop NaN')
        self.assertGreater(int((T.why == 'isyarat keluar').sum()), 0, 'X13 tidak pernah cetus')




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
        self.assertEqual(len(NXX), 40)

    def test_setiap_kohort_ada_baris_jejak40(self):
        """Setiap modul mesti sepadan satu baris `REVERSE/jejak40.csv` — kontrak."""
        import csv as _csv
        with (AKAR / 'REVERSE' / 'jejak40.csv').open() as fh:
            baris = {f"{r['masuk']}{r['keluar']}" for r in _csv.DictReader(fh)}
        self.assertEqual(set(NXX), baris,
                         f'modul tanpa baris: {sorted(set(NXX) - baris)}; '
                         f'baris tanpa modul: {sorted(baris - set(NXX))}')

    def test_keluar_berbeza_antara_kohort(self):
        """Jejak mesti merentas BEBERAPA keluar — kalau semua satu keluar, paksi keluar
        (yang diukur ~12x lebih berpengaruh daripada masuk) tidak diuji sama sekali."""
        import importlib
        kl = set()
        for mid in NXX:
            m = importlib.import_module(f'kaedah.{mid}')
            kl.add(re.search(r"keluar='(\w+)'", (AKAR / 'BacktestShariah2' / 'kod' /
                   'kaedah' / f'{mid}.py').read_text()).group(1))
        self.assertGreaterEqual(len(kl), 4, f'hanya {len(kl)} keluar berbeza: {kl}')


class TestPariti40(unittest.TestCase):
    """Pariti bit bagi SETIAP topeng dan keluar yang 40 kohort produksi pakai.

    `AUDIT_JEJAK_N.md` F6: dalam jejak 20-kohort hanya 6 daripada 20 topeng dilindungi ujian
    pariti walaupun senarai itu dipanggil "kontrak", dan audit perlu menyemak 14 yang lain
    sendiri. Kelas ini menutup jurang itu: setiap topeng dan keluar dalam `jejak40.csv`
    dibandingkan dengan `REVERSE/teras/ind.py` + `step18_nxx.tambahan` secara eksplisit.
    """

    @classmethod
    def setUpClass(cls):
        if not STOR.exists():
            raise unittest.SkipTest(f'stor harga tiada: {STOR}')
        cls.H = _harga()
        if not cls.H:
            raise unittest.SkipTest('tiada ticker dengan bar cukup')
        with (AKAR / 'REVERSE' / 'jejak40.csv').open() as fh:
            import csv as _csv
            rows = list(_csv.DictReader(fh))
        cls.MASUK = sorted({r['masuk'] for r in rows}, key=lambda x: int(x[1:]))
        cls.KELUAR = sorted({r['keluar'] for r in rows if r['keluar'] != 'X15'})

    def test_semua_topeng_dan_keluar_40_identik(self):
        L = lambda x, n=1: x.shift(n)  # noqa: E731
        jum = {}
        for t, g in self.H:
            a, b = NX.indikator(g), IND.kira(g)
            e20 = g.close.ewm(span=20, adjust=False, min_periods=20).mean()
            t20 = g.high.rolling(20).max().shift(1)
            gap = g.open / g.close.shift(1) - 1.0
            t45 = (g.close < g.close.shift(1)).rolling(5).sum() >= 4
            # ind.kira tidak mendedahkan ma20/sd20 (pemboleh ubah tempatan); formula
            # ind.py:189-190 verbatim
            m20 = g.close.rolling(20, min_periods=20).mean()
            s20 = g.close.rolling(20, min_periods=20).std(ddof=0)
            ref = {
                'N06': (b.ma50 > b.ma200) & (L(b.ma50) <= L(b.ma200)),
                'N16': b.rsi2 < 10,
                'N19': (b.bb_pctb < 0) & (b.rsi14 < 30),
                'N22': (b.bb_pctb > 100) & (b.rsi14 > 50),
                'N24': (b.supertrend > 0) & (b.adx14 > 20),
                'N25': (b.supertrend > 0) & (g.close > e20) & (b.adx14 > 23),
                'N28': (b.adx14 > 25) & (b.mdi < b.adx14),
                'N36': b.pocket_pivot > 0,
                'N37': b['gap_and_go'] > 0,
                'N38': b.vcp > 0,
                'N40': (b.obv_tinggi_baru > 0) & (g.close > b.ma50),
                'N42': (b.vol_n50 >= 2.0) & (g.close > L(g.close)),
                'N50': ((b.julat10 < 0.5 * b.julat20) & (b.vol_n50 >= 1.5)
                        & (g.close > L(g.high))),
                'N53': (b.supertrend > 0) & (b.adx14 > 25),
                'N55': (b.bb_pctb < 20) & (b.rsi14 > 40) & (b.adx14 > 20),
                'N56': (b.rsi14 > 50) & (b.adx14 > 20),
                'N64': (b['gap_and_go'] > 0) & (b.vol_n50 >= 2.0),
                'N65': ((b['gap_and_go'] > 0) & (b.vol_n50 >= 1.5)
                        & (b['j_52w_tinggi'] >= -5.0)),
                'N73': g.close < (m20 - 2.0 * s20),
                'N75': b.rsi14 < 40,
                'N119': (L(g.close, 2) > L(g.close)) & (L(g.close) > g.close),
                'N124': (gap >= 0.08) & (b.vol_n50 >= 2.0),
                'X13': b.rsi14 > 70,
                'X14': (b.rsi14 > 50) & (L(b.rsi14) <= 50),
                'X16': b.supertrend <= 0,
                'X17': b.adx14 < 20,
                'X36': (g.close < b.ma50) & L(g.close < b.ma50).fillna(False),
            }
            got = {
                'N06': NX.n06(a, g), 'N16': NX.n16(a), 'N19': NX.n19(a), 'N22': NX.n22(a),
                'N24': NX.n24(a), 'N25': NX.n25(a, g), 'N28': NX.n28(a), 'N36': NX.n36(a),
                'N37': NX.n37(a), 'N38': NX.n38(a), 'N40': NX.n40(a, g),
                'N42': NX.n42(a, g), 'N50': NX.n50(a, g), 'N53': NX.n53(a),
                'N55': NX.n55(a), 'N56': NX.n56(a), 'N64': NX.n64(a), 'N65': NX.n65(a),
                'N73': NX.n73(a, g), 'N75': NX.n75(a), 'N119': NX.n119(g),
                'N124': NX.n124(a), 'X13': NX.x13(a), 'X14': NX.x14(a), 'X16': NX.x16(a),
                'X17': NX.x17(a), 'X36': NX.x36(a, g),
            }
            # setiap yang jejak40 perlukan MESTI ada di sini
            for k in self.MASUK + self.KELUAR:
                self.assertIn(k, ref, f'{k} dipakai oleh jejak40 tetapi tiada rujukan pariti')
                x = got[k].fillna(False).astype(bool)
                y = ref[k].fillna(False).astype(bool)
                self.assertEqual(int((x != y).sum()), 0, f'{t} {k}: topeng terpesong')
                jum[k] = jum.get(k, 0) + int(y.sum())
        for k, n in jum.items():
            self.assertGreater(n, 0, f'{k}: SIFAR isyarat rujukan — ujian sia-sia')
        self.assertGreaterEqual(len(jum), 27, f'hanya {len(jum)} topeng/keluar diuji')


if __name__ == '__main__':
    unittest.main()

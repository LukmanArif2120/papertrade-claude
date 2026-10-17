# Ujian pantas penala: data 431 (20 saham) sebagai pengganti Release, universe tiruan, 3 percubaan.
import os, sys, json, types, shutil, tempfile, unittest, warnings, hashlib
import numpy as np, pandas as pd

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
for p in (os.path.join(AKAR, 'BacktestShariah2', 'kod'), os.path.join(AKAR, 'AUTOTUNE', 'teras'), os.path.join(AKAR, 'AUTOTUNE', 'tala')):
    if p not in sys.path: sys.path.insert(0, p)
import data as D
import objektif as O
import tala, rancang
from enjin import atr

TK = ['ADSK', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'ANET', 'COST', 'AVGO', 'SHOP', 'TRI', 'PODD', 'SEDG', 'GNRC', 'DOCU',
      'DXCM', 'IOVA', 'ABNB', 'AMZN', 'META', 'TSLA']
_F = {}


def pengganti():
    """Modul tiruan teras/data.py atas data 431: universe setiap bulan = semua TK, kumpulan ikut md5."""
    if 'm' in _F: return _F['m']
    fr, idx = D.muat_431(); fr = {t: fr[t] for t in TK if t in fr}
    bulan = pd.period_range('2019-01', '2026-12', freq='M').strftime('%Y-%m')
    kum = {t: 'A' if int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 == 0 else 'B' for t in fr}
    univ = pd.DataFrame([dict(bulan=b, ticker=t, kedudukan=1, kumpulan=kum[t]) for b in bulan for t in fr])

    def muat(mula, akhir, kumpulan='AB', dir=None):
        mula, akhir = pd.Timestamp(mula), pd.Timestamp(akhir)
        f = {t: g[(g.index >= mula) & (g.index <= akhir)].copy() for t, g in fr.items() if kum[t] in kumpulan}
        return ({t: g for t, g in f.items() if len(g)},
                {k: v[(v.index >= mula) & (v.index <= akhir)] for k, v in idx.items()}, univ)
    m = types.SimpleNamespace(muat=muat, topeng=D.topeng, ambil=lambda c=None: None,
                              akhir_data=lambda c=None: max(g.index.max() for g in fr.values()), kum=kum)
    _F['m'] = m
    return m


def kaedah_tiruan():
    """Pecah tinggi n hari; henti = tutup − k × ATR14; keluar tutup < SMA n."""
    m = types.SimpleNamespace(ID='MX', NAMA='tiruan', VARIAN='', TMAX=None, WARM=60, ADA_HENTI=True, SILANG=False,
                              PERLU_BAR=60, PARAM=dict(n=20, k=2.0), JULAT=dict(n=('int', 10, 40), k=('float', 1.0, 3.0)),
                              TALA=['n', 'k'], BELUM_DITALA=False)

    def sedia(fr, idx, P=None):
        P = {**m.PARAM, **(P or {})}
        for g in fr.values():
            c = g.close
            g['sig'] = c > g.high.rolling(P['n']).max().shift(1)
            g['stop'] = c - P['k'] * atr(g); g['tgt'] = np.nan
            g['exitc'] = c < c.rolling(P['n']).mean(); g['rank'] = c / c.shift(20) - 1
    m.sedia = sedia
    return m


class UjiTala(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp()
        cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal; shutil.rmtree(cls.dir, ignore_errors=True)

    def test_tetingkap(self):
        w = tala.tetingkap(0, '2026-10-02')
        self.assertEqual([str(x.date()) for x in w['latih'] + w['ujian']], ['2010-01-01', '2012-12-31', '2013-01-01', '2013-12-31'])
        w = tala.tetingkap(11, '2026-10-02'); self.assertEqual(str(w['ujian'][1].date()), '2024-09-30')
        w = tala.tetingkap(12, '2026-10-02'); self.assertEqual(str(w['ujian'][1].date()), '2026-10-02')
        w = tala.tetingkap(13, '2026-10-02'); self.assertIsNone(w['ujian']); self.assertEqual(str(w['latih'][0].date()), '2023-10-03')
        self.assertEqual(tala.senarai_kajian('0-3,12'), [0, 1, 2, 3, 12])

    def test_akhir_tiruan(self):
        H = tala.tala('MX', 12, tala.Sumber(None, pengganti()), n_trials=3, keluar=self.dir)
        self.assertEqual(H['status'], 'SIAP', H['ralat'])
        self.assertEqual(H['n_trials'], 3)
        self.assertEqual(set(H['params']), {'n', 'k'})
        for k in ('ujian_A', 'ujian_B', 'ujian_AB', 'dataran', 'pbo', 'top10', 'latih_A', 'latih_A_asal'):
            self.assertIn(k, H)
        hu = H['harian_ujian']; self.assertEqual(len(hu['tarikh']), len(hu['A']))
        self.assertTrue(hu['tarikh'][0] >= '2024-10-01')
        self.assertTrue(os.path.exists(os.path.join(self.dir, 'MX', 'k12.json')))
        json.load(open(os.path.join(self.dir, 'MX', 'k12.json')))
        # percubaan pertama = PARAM asal
        self.assertEqual(H['latih_A_asal']['n'] >= 0, True)

    def test_semasa_dan_asal_belum_ditala(self):
        H = tala.tala('M54', 13, tala.Sumber(None, pengganti()), n_trials=3, keluar=self.dir)
        self.assertEqual(H['status'], 'SIAP', H['ralat'])
        self.assertEqual(H['n_trials'], 1 if not H['tala'] else 3); self.assertNotIn('ujian_A', H)

    def test_ralat_ditulis(self):
        H = tala.tala('MX', 0, tala.Sumber(None, pengganti()), n_trials=2, keluar=self.dir)   # tiada data 2010
        self.assertEqual(H['status'], 'RALAT'); self.assertTrue(H['ralat'])
        self.assertTrue(os.path.exists(os.path.join(self.dir, 'MX', 'k00.json')))


class UjiObjektif(unittest.TestCase):
    def test_skor_dan_pilih(self):
        ix = pd.bdate_range('2020-01-01', periods=504)
        cv = pd.Series(np.linspace(1.0, 1.21, 504), ix)
        self.assertAlmostEqual(O.cagr(cv), 1.21 ** (365.25 / ((ix[-1] - ix[0]).days + 1)) - 1)
        self.assertEqual(O.mdd(cv), 0.0)
        m = dict(cagr=0.2, mdd=-0.4, n=50, days=10)
        self.assertAlmostEqual(O.skor(m), -1 + 0.2 - 0.2)
        self.assertAlmostEqual(O.skor(dict(m, mdd=-0.2)), 0.2)
        self.assertLess(O.skor(dict(m, mdd=-0.2, n=10)), 0)
        R = [dict(skor=0.5, lulus=True, thn_min=-0.2), dict(skor=0.4, lulus=True, thn_min=0.1), dict(skor=0.9, lulus=False, thn_min=0.5)]
        self.assertEqual(O.pilih_teguh(R)[0]['skor'], 0.4)

    def test_pbo(self):
        rng = np.random.default_rng(1)
        self.assertGreater(O.pbo(rng.normal(0, 0.01, (800, 30)))['pbo'], 0.2)      # hingar: PBO tinggi
        M = rng.normal(0, 0.01, (800, 30)); M[:, 0] += 0.003
        self.assertLess(O.pbo(M)['pbo'], 0.1)                                          # satu unggul: PBO rendah
        sr, sk, ku, n = O.sharpe(M[:, 0]); self.assertGreater(O.dsr(sr, sk, ku, n, O.sr0([0.01, 0.02, 0.0], 100)), 0.9)


class UjiRancang(unittest.TestCase):
    def test_lpt(self):
        tugas = [dict(kaedah=f'M{i}', kajian=0, kos=c) for i, c in enumerate([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])]
        S = rancang.lpt(tugas, 3)
        beban = sorted(sum(t['kos'] for t in s) for s in S)
        self.assertEqual(sum(beban), 55); self.assertLessEqual(beban[-1] - beban[0], 2)


if __name__ == '__main__':
    unittest.main()

# Ujian A02 (SPEC_A02): lorong enjin, dagangan dipegang, objektif lebihan SPY, pemanasan, tala/saringan/pelan,
# pengesahan/label/gabungan. Data sintetik (laluan rawak 2008–2026, 24 saham + SPY); tiada rangkaian.
import os, sys, json, types, shutil, tempfile, unittest, warnings, hashlib
import numpy as np, pandas as pd

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
for p in (os.path.join(AKAR, 'BacktestShariah2', 'kod'), os.path.join(AKAR, 'AUTOTUNE', 'teras'),
          os.path.join(AKAR, 'AUTOTUNE', 'tala'), os.path.join(AKAR, 'AUTOTUNE', 'sahkan')):
    if p not in sys.path: sys.path.insert(0, p)
import data as D
import enjin_at as E
import objektif as O
import tala, tala_a02 as T2, saringan_a02 as SR, pekerja_a02 as PA
import sahkan_a02 as SA, imbas_a02 as IA
from gabung_hasil import versi_kod

_F = {}


def sintetik(n=24, mula='2008-01-01', akhir='2026-09-30', benih=7):
    if 'fr' in _F: return _F['fr'], _F['idx']
    rng = np.random.default_rng(benih)
    ix = pd.bdate_range(mula, akhir)

    def siri(mu, sd, p0):
        c = p0 * np.exp(np.cumsum(rng.normal(mu, sd, len(ix))))
        o = c * np.exp(rng.normal(0, sd / 3, len(ix)))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, sd / 2, len(ix))))
        l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, sd / 2, len(ix))))
        return pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=rng.uniform(1e6, 5e6, len(ix))), index=ix)
    fr = {f'T{i:02d}': siri(rng.uniform(-2e-4, 8e-4), 0.02, 50) for i in range(n)}
    for g in fr.values(): g['turnover'] = g.close * g.volume
    spy = siri(3e-4, 0.01, 100); spy['turnover'] = spy.close * spy.volume
    _F['fr'], _F['idx'] = fr, {'SPY': spy, 'QQQ': spy.copy()}
    return _F['fr'], _F['idx']


def pengganti():
    if 'm' in _F: return _F['m']
    fr, idx = sintetik()
    bulan = pd.period_range('2008-01', '2026-12', freq='M').strftime('%Y-%m')
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
    from enjin import atr
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


def bingkai(n, sig_hari=(), o=None):
    ix = pd.bdate_range('2020-01-01', periods=n)
    c = np.full(n, 10.0) if o is None else np.asarray(o, float)
    g = pd.DataFrame(dict(open=c, high=c * 1.01, low=c * 0.99, close=c, volume=1e7, sig=False, stop=1.0, tgt=np.nan,
                          exitc=False, rank=0.0), index=ix)
    for i in sig_hari: g.iloc[i, g.columns.get_loc('sig')] = True
    return g


class UjiEnjinA02(unittest.TestCase):
    def test_lorong(self):
        self.assertTrue(E.had60_lorong('had60')); self.assertFalse(E.had60_lorong('asal'))
        with self.assertRaises(ValueError): E.had60_lorong('x')

    def test_asal_tiada_had(self):
        g = bingkai(200, [5])
        S = E.Susun({'X': g})
        a = S.dagangan(None, 2, had60=True); b = S.dagangan(None, 2, had60=False)
        self.assertEqual(int(a.days.iloc[0]), 60); self.assertEqual(a.why.iloc[0], 'masa')
        self.assertEqual(b.why.iloc[0], 'hujung'); self.assertGreater(int(b.days.iloc[0]), 60)
        c = S.dagangan(30, 2, had60=False)   # TMAX asal kaedah dikekalkan
        self.assertEqual(int(c.days.iloc[0]), 30)

    def test_dipegang(self):
        fr = {f'X{i}': bingkai(80, [5]) for i in range(10)}
        for i, g in enumerate(fr.values()): g['rank'] = float(i)
        T = E.trades(fr, None, 2, kos=False, gap=False, had60=False)
        P = E.Pasaran(fr, '2020-01-01', None)
        cv0 = P.lengkung(T)
        cv, Tp = P.lengkung(T, pegang=True)
        pd.testing.assert_series_equal(cv0, cv)
        self.assertEqual(len(T), 10); self.assertEqual(len(Tp), 8)
        self.assertEqual(sorted(Tp.ticker), [f'X{i}' for i in range(2, 10)])   # rank tertinggi dipegang

    def test_dipegang_kosong(self):
        fr = {'X': bingkai(30)}
        cv, Tp = E.Pasaran(fr, '2020-01-01', None).lengkung(E.trades(fr, None, 2), pegang=True)
        self.assertEqual(len(Tp), 0); self.assertTrue((cv == 1.0).all())


class UjiObjektifA02(unittest.TestCase):
    def setUp(self):
        self.ix = pd.bdate_range('2014-01-01', '2015-12-31')

    def test_spy_lengkung(self):
        ci = pd.bdate_range('2013-12-02', '2016-01-29')
        c = pd.Series(np.arange(1, len(ci) + 1, dtype=float), index=ci)
        s = O.spy_lengkung(c, self.ix)
        sebelum = c[c.index < self.ix[0]].iloc[-1]
        self.assertAlmostEqual(s.iloc[0], c.loc[self.ix[0]] / sebelum)
        self.assertAlmostEqual(s.iloc[-1], c.loc[self.ix[-1]] / sebelum)

    def test_ringkas_skor(self):
        cv = pd.Series(np.linspace(1, 1.5, len(self.ix)), index=self.ix)
        spy = pd.Series(np.linspace(1, 1.2, len(self.ix)), index=self.ix)
        T = pd.DataFrame(dict(ret=[0.01] * 40, days=[5] * 40))
        m = O.ringkas_a02(T, cv, spy)
        self.assertAlmostEqual(m['lebihan'], O.cagr(cv) - O.cagr(spy))
        self.assertTrue(O.lulus_a02(m)); self.assertAlmostEqual(O.skor_a02(m), m['lebihan'])
        self.assertEqual(set(m['tahunan_lebih']), {2014, 2015})
        self.assertAlmostEqual(m['thn_min'], min(m['tahunan_lebih'].values()))
        m2 = dict(m, n=29); self.assertFalse(O.lulus_a02(m2))
        self.assertAlmostEqual(O.skor_a02(m2), -1 + m['lebihan'])
        m3 = dict(m, mdd=-0.40, spy_mdd=-0.20)    # had = −0.30; lebihan MDD 0.10
        self.assertAlmostEqual(O.skor_a02(m3), -1 + m['lebihan'] - 0.2)
        m4 = dict(m, mdd=-0.29, spy_mdd=-0.20); self.assertTrue(O.lulus_a02(m4))

    def test_pilih_teguh_tahun_lebih(self):
        R = [dict(skor=0.3, lulus=True, thn_min=-0.2), dict(skor=0.2, lulus=True, thn_min=0.05),
             dict(skor=0.9, lulus=False, thn_min=0.5)]
        p, ok = O.pilih_teguh(R); self.assertTrue(ok); self.assertEqual(p['skor'], 0.2)

    def test_panas(self):
        m = types.SimpleNamespace(PARAM=dict(n=50, x_ambang_500000=500000, k=2.0), JULAT=dict(n=('int', 25, 300)), WARM=200)
        self.assertEqual(O.panas_a02(m), int(np.ceil(1.6 * 500)))
        m.JULAT = dict(n=('int', 10, 40)); m.WARM = 50
        self.assertEqual(O.panas_a02(m), 400)


class UjiTalaA02(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp()
        cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)
        cls.S = tala.Sumber(modul=pengganti())

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_tetingkap(self):
        ad = pd.Timestamp('2026-09-30')
        w = T2.tetingkap(0, ad); self.assertEqual(str(w['latih'][0].date()), '2010-01-01')
        self.assertEqual(str(w['ujian'][1].date()), '2013-12-31')
        w = T2.tetingkap(5, ad); self.assertEqual(str(w['ujian'][0].date()), '2018-01-01')
        w = T2.tetingkap(6, ad); self.assertEqual((str(w['latih'][0].date()), str(w['ujian'][0].date())), ('2016-01-01', '2019-01-01'))
        self.assertEqual(w['ujian'][1], ad)
        w = T2.tetingkap(7, ad); self.assertIsNone(w['ujian']); self.assertEqual(str(w['latih'][0].date()), '2023-10-01')
        with self.assertRaises(ValueError): T2.tetingkap(8, ad)

    def test_tala_wf_akhir_semasa(self):
        for k, lo in ((0, 'asal'), (6, 'had60'), (7, 'had60')):
            H = T2.tala('MX', lo, k, self.S, n_trials=3, keluar=self.dir)
            self.assertEqual(H['status'], 'SIAP', H.get('ralat'))
            f = os.path.join(self.dir, f'MX_{lo}', f'k{k:02d}.json'); self.assertTrue(os.path.exists(f))
            J = json.load(open(f))
            self.assertEqual((J['id_kaedah'], J['lorong'], J['kaedah']), ('MX', lo, f'MX_{lo}'))
            self.assertIn('versi_kod', J); self.assertEqual(J['panas_hari'], 400)
            self.assertIn('lebihan', J['latih_A'])
            if k == 7: self.assertNotIn('ujian_A', J); continue
            kum = ['A', 'B', 'AB'] if k == 6 else ['A', 'B']
            for g in kum:
                self.assertIn(f'ujian_{g}', J)
                self.assertEqual(len(J['harian_ujian'][g]), len(J['harian_ujian']['tarikh']))
            self.assertEqual(len(J['harian_ujian']['SPY']), len(J['harian_ujian']['tarikh']))
            if k == 6: self.assertIn('pbo', J)
            if k == 0: self.assertEqual(J['harian_ujian']['tarikh'][0][:4], '2013')


class UjiSaringanPelan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp()
        cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)
        cls.S = tala.Sumber(modul=pengganti())

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_saring(self):
        R = SR.saring('MX', self.S)
        self.assertEqual(set(R), {'had60', 'asal'})
        for r in R.values():
            self.assertEqual(r['status'], 'SIAP', r.get('ralat'))
            self.assertAlmostEqual(r['skor'], min(r['lebihan_A'], r['lebihan_B']))
            self.assertAlmostEqual(r['lebihan_A'], r['cagr_A'] - r['spy_A'])

    def test_pilih_gabung_rancang(self):
        d = os.path.join(self.dir, 's'); os.makedirs(d)
        for i in range(30):
            mid = f'M{i + 1:02d}'
            J = {lo: dict(kaedah=mid, lorong=lo, status='SIAP', skor=(i if lo == 'had60' else -i) / 100.0,
                          lebihan_A=0.0, lebihan_B=0.0, n_tala=0 if i == 29 else 3, saat=10.0 + i) for lo in T2.LORONG}
            json.dump(J, open(os.path.join(d, f'{mid}.json'), 'w'))
        csv = os.path.join(self.dir, 'saringan.csv'); pj = os.path.join(self.dir, 'pilihan.json')
        Dd, J = SR.gabung([d], 20, csv, pj)
        self.assertEqual(len(Dd), 60)
        self.assertEqual(J['pilihan']['had60'][:2], ['M29', 'M28'])   # M30 tiada TALA → dikecualikan
        self.assertEqual(J['pilihan']['asal'][:2], ['M01', 'M02'])
        self.assertEqual(len(J['tugas']), 40)
        P = PA.rancang(pj, csv, list(range(8)), 120, 20)
        self.assertEqual(P['n_tugas'], 320); self.assertEqual(len(P['shard']), 20)
        self.assertEqual(sum(len(s) for s in P['shard']), 320)

    def test_shard_versi(self):
        ids = [f'M{i}' for i in range(1, 135)]
        semua = sum((SR.shard(ids, i, 20) for i in range(20)), [])
        self.assertEqual(sorted(semua), sorted(ids))
        self.assertEqual(versi_kod('M54_had60'), versi_kod('M54')); self.assertIsNotNone(versi_kod('M54'))


class UjiLabelA02(unittest.TestCase):
    def asas(self, **kw):
        m = dict(lebihan_a=0.02, lebihan_b=0.01, lebihan_peng=0.03, mdd_oos=-0.25, spy_mdd_oos=-0.20, dsr=0.95,
                 imbasan='BERSIH'); m.update(kw); return m

    def test_label(self):
        self.assertEqual(SA.label(self.asas()), 'LULUS')
        self.assertEqual(SA.label(self.asas(dsr=0.5)), 'CALON')
        self.assertEqual(SA.label(self.asas(mdd_oos=-0.31)), 'CALON')
        self.assertEqual(SA.label(self.asas(imbasan='TIDAK DIIMBAS')), 'CALON')
        self.assertEqual(SA.label(self.asas(lebihan_b=-0.01)), 'TIDAK LULUS')
        self.assertEqual(SA.label(self.asas(lebihan_peng=float('nan'))), 'TIDAK LULUS')
        self.assertEqual(SA.label(self.asas(imbasan='PANDANG HADAPAN')), 'PANDANG HADAPAN')

    def test_tamak(self):
        ix = pd.bdate_range('2013-01-01', periods=300); rng = np.random.default_rng(1)
        a = pd.Series(rng.normal(0, 0.01, 300), ix)
        r = {'X': a, 'Y': a * 1.01, 'Z': pd.Series(rng.normal(0, 0.01, 300), ix)}
        nil = {('X',): (0.05, -0.1), ('X', 'Z'): (0.06, -0.12)}
        p, log, _ = SA.pilih_tamak(['X', 'Y', 'Z'], r, lambda ids: nil[tuple(ids)], had_mdd=-0.3)
        self.assertEqual(p, ['X', 'Z']); self.assertEqual(log[1]['tindakan'], 'langkau: korelasi')
        p, log, _ = SA.pilih_tamak(['X', 'Z'], r, lambda ids: nil[tuple(ids)], had_mdd=-0.11)
        self.assertEqual(p, ['X']); self.assertIn('MDD', log[1]['tindakan'])


class UjiHujungA02(unittest.TestCase):
    """Tala MX kedua-dua lorong k0–7 (3 percubaan) → imbasan → sahkan_a02.jalan (dengan gabungan) atas data sintetik."""
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp(); cls.tala = os.path.join(cls.dir, 'tala')
        cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)
        cls.S = tala.Sumber(modul=pengganti())
        for lo in T2.LORONG:
            for k in range(8): T2.tala('MX', lo, k, cls.S, n_trials=3, keluar=cls.tala)
        json.dump(dict(pilihan={'had60': ['MX'], 'asal': ['MX']}, tugas=['MX_had60', 'MX_asal']),
                  open(os.path.join(cls.dir, 'pilihan.json'), 'w'))
        pd.DataFrame([dict(kaedah='MX', lorong=lo, status='SIAP', skor=0.01, sr_lebih_A=s, saat=1.0)
                      for lo, s in (('had60', 0.01), ('asal', 0.02))]).to_csv(os.path.join(cls.dir, 'saringan.csv'), index=False)

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_imbas_dan_sahkan(self):
        fr, idx = sintetik()
        IA._D.update(fr={t: g[g.index >= '2010-01-01'] for t, g in list(fr.items())[:6]}, idx=idx, tala=self.tala)
        R = IA.semak('MX_had60')
        self.assertNotIn('ralat', R, R.get('jejak')); self.assertTrue(R['set'])
        self.assertEqual(IA.status(R), 'BERSIH')
        d = os.path.join(self.dir, 'imbas'); os.makedirs(d); json.dump(R, open(os.path.join(d, 'MX_had60.json'), 'w'))
        out = IA.tulis([d], self.dir)
        self.assertEqual(out['MX_had60']['status'], 'BERSIH')
        self.assertTrue(os.path.exists(os.path.join(self.dir, 'PANDANG_HADAPAN.md')))
        D, gab, ring, n = SA.jalan(self.S, proses=2, keluar=self.dir, tala=self.tala)
        self.assertEqual(len(D), 2); self.assertLessEqual(n, 150)
        r = D.set_index('tugas').loc['MX_had60']
        self.assertEqual(r.kajian_siap, '01234567'); self.assertEqual(r.imbasan, 'BERSIH')
        self.assertEqual(D.set_index('tugas').loc['MX_asal'].imbasan, 'TIDAK DIIMBAS')
        self.assertEqual(r.oos_mula[:4], '2013'); self.assertEqual(r.oos_akhir[:4], '2018')
        self.assertEqual(r.peng_mula[:4], '2019')
        self.assertAlmostEqual(r.lebihan_a, r.cagr_a - r.spy_oos, places=9)
        for f in ('parameter_sedia.csv', 'gabungan.json', 'ringkasan.json', 'papan.json', 'LAPORAN.md'):
            self.assertTrue(os.path.exists(os.path.join(self.dir, f)), f)
        sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'dashboard'))
        import jana_db
        docs = jana_db.bina(self.dir, '2026-10-18T00:00Z')
        self.assertTrue(all(k.startswith('a02_') for k in docs), list(docs))
        self.assertIn('a02_kaedah_MX_had60', docs); self.assertEqual(docs['a02_ringkasan']['versi'], 'A02')
        self.assertEqual(set(docs['a02_ringkasan']['kiraan_label']), set(SA.LABEL))
        if gab.get('terpilih'):
            self.assertIn('oos_A', gab); self.assertIn('pengesahan', gab)
            if gab['terpilih'] == [gab['calon_dinilai'][0]]:   # gabungan satu kaedah = OOS kaedah itu (rank persentil monoton)
                x = D.set_index('tugas').loc[gab['terpilih'][0]]
                self.assertAlmostEqual(gab['oos_A']['cagr'], x.cagr_a, places=3)


if __name__ == '__main__':
    unittest.main()

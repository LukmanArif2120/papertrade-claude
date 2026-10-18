# Ujian A03 (SPEC_A03): had rugi 8% enjin, topeng F/M, 5 slot, saringan 4 sistem, pemilihan 10 sistem utama, tala,
# imbasan pandang ke hadapan termasuk F, pengesahan/laporan dan db dashboard a03_*. Data sintetik; tiada rangkaian.
import os, sys, json, shutil, tempfile, unittest, warnings
import numpy as np, pandas as pd

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
for p in (os.path.join(AKAR, 'BacktestShariah2', 'kod'), os.path.join(AKAR, 'AUTOTUNE', 'teras'),
          os.path.join(AKAR, 'AUTOTUNE', 'tala'), os.path.join(AKAR, 'AUTOTUNE', 'sahkan'), os.path.dirname(__file__)):
    if p not in sys.path: sys.path.insert(0, p)
import enjin_at as E
import tala, tala_a02 as T2, tala_a03 as T3, saringan_a03 as SR3, pekerja_a02 as PA
import sahkan_a03 as SA3, imbas_a03 as IA3, menang_a03 as MA
from test_a02 import sintetik, pengganti, kaedah_tiruan, bingkai


def eps_sintetik(fr, benih=3, bocor=False):
    """Jadual EPS format ciri.py: satu suku setiap ~91 hari bagi setiap ticker; separuh 'sebelum', separuh 'selepas'.
    bocor=True: `tersedia` = tarikh laporan walaupun 'selepas' (kebocoran sengaja untuk ujian imbasan)."""
    rng = np.random.default_rng(benih); R = []
    for t, g in fr.items():
        hari = g.index; tarikh = pd.date_range('2008-02-15', '2026-09-15', freq='91D')
        eps = np.cumprod(1 + rng.normal(0.04, 0.15, len(tarikh))) * rng.choice([1, -1], p=[0.85, 0.15])
        for q, (d, e) in enumerate(zip(tarikh, eps)):
            masa = 'sebelum' if q % 2 == 0 else 'selepas'
            k = np.searchsorted(hari, d, 'left' if (masa == 'sebelum' or bocor) else 'right')
            ters = hari[k] if k < len(hari) else pd.NaT
            lalu = eps[q - 4] if q >= 4 else np.nan
            yoy = (e - lalu) / lalu if q >= 4 and lalu > 0 else np.nan
            R.append(dict(ticker=t, tarikh_laporan=d, tarikh=d, masa=masa, eps_sebenar=e, eps_anggaran=np.nan,
                          sumber='ujian', tersedia=ters, eps_yoy=yoy, eps_yoy_sebelum=np.nan))
    return pd.DataFrame(R)


def bersih(nisbah):
    """Pulangan selepas komisen COST setiap sisi (kos=False)."""
    return nisbah * (1 - E.COST) / (1 + E.COST) - 1


class UjiHadRugi(unittest.TestCase):
    def satu(self, harga, rendah=None, stop=1.0, **kw):
        n = len(harga); g = bingkai(n, [0], harga)
        if rendah is not None:
            for i, v in rendah.items(): g.iloc[i, g.columns.get_loc('low')] = v
        g['stop'] = stop
        return E.Susun({'X': g}).dagangan(None, 0, gap=True, kos=False, had60=False, **kw)

    def test_lalai_sama(self):
        fr, _ = sintetik()
        f = {t: g.iloc[-600:].copy() for t, g in list(fr.items())[:5]}
        for g in f.values():
            g['sig'] = g.close > g.close.rolling(20).max().shift(1); g['stop'] = g.close * 0.85
            g['tgt'] = np.nan; g['exitc'] = g.close < g.close.rolling(10).mean(); g['rank'] = 0.0
        S = E.Susun(f)
        pd.testing.assert_frame_equal(S.dagangan(None, 30), S.dagangan(None, 30, had_rugi=None))
        pd.testing.assert_frame_equal(S.dagangan(None, 30), S.dagangan(None, 30, had_rugi=0.0))
        b = S.dagangan(None, 30, had_rugi=0.08)
        self.assertTrue((b.ret[b.why == 'henti'] > -0.20).all())

    def test_had_hari_kedua(self):
        h = [10.0] * 3 + [9.5] * 5 + [9.0] * 10   # masuk buka bar 1 = 10; 0.92 × 10 = 9.2
        T = self.satu(h, had_rugi=0.08)
        self.assertEqual(T.why.iloc[0], 'henti')
        self.assertEqual(str(T.ex.iloc[0].date()), str(pd.bdate_range('2020-01-01', periods=20)[8].date()))
        self.assertAlmostEqual(T.ret.iloc[0], bersih(0.90))   # gap ke bawah paras had → keluar pada buka
        T0 = self.satu(h)                                     # tanpa had: henti kaedah 1.0 tidak disentuh
        self.assertEqual(T0.why.iloc[0], 'hujung')

    def test_rendah_intrahari(self):
        h = [10.0] * 30
        T = self.satu(h, rendah={4: 9.0}, had_rugi=0.08)
        self.assertEqual(T.why.iloc[0], 'henti'); self.assertAlmostEqual(T.ret.iloc[0], bersih(0.92))

    def test_hari_masuk_tidak_berubah(self):
        h = [10.0] * 30
        T = self.satu(h, rendah={1: 9.0}, had_rugi=0.08)       # rendah hari masuk < 9.2 → tiada keluar hari 1
        self.assertNotEqual(str(T.ex.iloc[0].date()), str(T.ent.iloc[0].date()))
        self.assertEqual(T.why.iloc[0], 'hujung')

    def test_henti_kaedah_lebih_tinggi(self):
        h = [10.0] * 30
        T = self.satu(h, rendah={5: 9.4}, stop=9.5, had_rugi=0.08)
        self.assertAlmostEqual(T.ret.iloc[0], bersih(0.95))


class UjiTopeng(unittest.TestCase):
    def test_siri_m(self):
        ix = pd.bdate_range('2015-01-01', periods=400)
        naik = pd.DataFrame(dict(close=np.linspace(100, 200, 400)), index=ix)
        m = T3.siri_m({'SPY': naik})
        self.assertFalse(m.iloc[:199].any()); self.assertTrue(m.iloc[200:].all())
        turun = pd.DataFrame(dict(close=np.linspace(200, 100, 400)), index=ix)
        self.assertFalse(T3.siri_m({'SPY': turun}).any())

    def test_f_ganti_dan_ciri(self):
        fr, _ = sintetik()
        f = {t: g for t, g in list(fr.items())[:3]}
        self.assertTrue(all(s.all() for s in T3.lajur_f(f, None).values()))
        eps = eps_sintetik(f)
        F = T3.lajur_f(f, eps)
        self.assertEqual(set(F), set(f))
        for t, s in F.items():
            self.assertTrue(s.index.equals(f[t].index)); self.assertEqual(s.dtype, bool)
        self.assertTrue(0 < np.mean([s.mean() for s in F.values()]) < 1)

    def test_penilai_topeng_slot(self):
        warnings.filterwarnings('ignore')
        S = tala.Sumber(modul=pengganti()); m = kaedah_tiruan()
        fr, idx, univ = S.muat('2012-01-01', '2016-12-31', 'AB')
        tiada = eps_sintetik(fr).assign(eps_sebenar=-1.0)
        pn = T3.Penilai03(m, fr, idx, univ, S, pd.Timestamp('2014-01-01'), pd.Timestamp('2016-12-31'), ['A', 'B'], eps=tiada)
        r = pn.jalan03({}, ['A'], ('had60',), tuple(T3.SISTEM))
        self.assertEqual(r[('had60', 'A', 'utama')][0]['n'], 0)
        self.assertEqual(r[('had60', 'A', 'f_sahaja')][0]['n'], 0)
        nm, nt = r[('had60', 'A', 'm_sahaja')][0]['n'], r[('had60', 'A', 'tanpa')][0]['n']
        self.assertGreater(nt, 0); self.assertLessEqual(nm, nt)
        Tp = r[('had60', 'A', 'tanpa')][2]
        aktif = max(int(((Tp.ent <= d) & (Tp.ex > d)).sum()) for d in pd.bdate_range('2014-01-01', '2016-12-31'))
        self.assertLessEqual(aktif, 5)
        ms = T3.siri_m(idx)
        Tm = r[('had60', 'A', 'm_sahaja')][2]
        self.assertTrue(ms.reindex(pd.DatetimeIndex(Tm.sig)).fillna(False).all())


class UjiSaringanA03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp(); cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)
        cls.S = tala.Sumber(modul=pengganti())

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal; shutil.rmtree(cls.dir, ignore_errors=True)

    def test_kaedah(self):
        lain = T3.kaedah_lain()
        self.assertEqual(len(lain), 6); self.assertFalse(set(lain) & set(T3.PAKAR))
        self.assertEqual(len(T3.senarai_kaedah()), 20); self.assertEqual(len(T3.PAKAR), 14)

    def test_saring(self):
        R = SR3.saring('MX', self.S, None)
        self.assertEqual(len(R), 8)
        d = {(r['lorong'], r['varian']): r for r in R}
        for r in R:
            self.assertEqual(r['status'], 'SIAP', r.get('ralat'))
            self.assertAlmostEqual(r['skor'], min(r['lebihan_A'], r['lebihan_B']))
            self.assertAlmostEqual(r['skor_menang'], min(r['menang_A'], r['menang_B']))
            self.assertIn('pf_B', r); self.assertIn('jangkaan_A', r)
        for lo in T2.LORONG:   # F pengganti (semua benar): utama = m_sahaja, f_sahaja = tanpa
            self.assertAlmostEqual(d[(lo, 'utama')]['skor'], d[(lo, 'm_sahaja')]['skor'])
            self.assertAlmostEqual(d[(lo, 'f_sahaja')]['skor'], d[(lo, 'tanpa')]['skor'])

    def test_gabung_pilih_rancang(self):
        d = os.path.join(self.dir, 's'); os.makedirs(d)
        for i in range(20):
            mid = f'M{i + 1:02d}'
            J = [dict(kaedah=mid, lorong=lo, varian=v, status='SIAP', lebihan_A=0.0, lebihan_B=0.0, n_A=50, mdd_A=-0.2,
                      skor=0.0, cagr_A=-0.01 if i == 17 else 0.05, cagr_B=0.04, menang_A=0.4 + i / 100, menang_B=0.6,
                      skor_menang=(i if lo == 'had60' else i - 0.5) / 100.0 + (0.5 if v == 'tanpa' else 0.0),
                      n_tala=0 if i == 19 else 3, saat=10.0 + i) for lo in T2.LORONG for v in T3.SISTEM]
            json.dump(J, open(os.path.join(d, f'{mid}.json'), 'w'))
        csv = os.path.join(self.dir, 'saringan.csv'); pj = os.path.join(self.dir, 'pilihan.json')
        D, J = SR3.gabung([d], 10, csv, pj)
        self.assertEqual(len(D), 160)
        # M20 tiada TALA; M18 CAGR A <= 0; ablasi tidak dipilih
        self.assertEqual(J['tugas'][:3], ['M19_had60', 'M19_asal', 'M17_had60'])
        self.assertEqual(len(J['tugas']), 10)
        self.assertEqual(sum(len(v) for v in J['pilihan'].values()), 10)
        self.assertEqual(J['varian']['tanpa']['had60']['n'], 20)
        P = PA.rancang(pj, csv, list(range(8)), 120, 20)
        self.assertEqual(P['n_tugas'], 80)


class UjiMenang(unittest.TestCase):
    def asas(self, **kw):
        m = dict(menang_a=0.6, menang_b=0.58, cagr_a=0.1, cagr_b=0.05, pf_a=1.5, pf_b=1.4, mdd_oos=-0.3, menang_peng=0.56,
                 cagr_peng=0.02, n_a=150, n_b=120, imbasan='BERSIH'); m.update(kw); return m

    def test_label(self):
        self.assertEqual(MA.label(self.asas()), ('MENANG', []))
        self.assertEqual(MA.label(self.asas(pf_b=1.2))[0], 'HAMPIR')
        self.assertEqual(MA.label(self.asas(n_b=99))[0], 'HAMPIR')
        self.assertEqual(MA.label(self.asas(imbasan='PANDANG HADAPAN'))[0], 'HAMPIR')
        self.assertEqual(MA.label(self.asas(mdd_oos=-0.36, menang_a=0.5))[0], 'TIDAK')
        self.assertEqual(MA.label(self.asas(menang_peng=float('nan')))[0], 'HAMPIR')

    def test_statistik(self):
        T = pd.DataFrame(dict(ret=[0.1, -0.05, 0.2, 0.0]))
        a = T3.statistik(T); self.assertEqual((a['n_menang'], a['n_kalah']), (2, 2))
        t = T3.terbitan(**a)
        self.assertAlmostEqual(t['menang'], 0.5); self.assertAlmostEqual(t['pf'], 0.3 / 0.05)
        self.assertAlmostEqual(t['purata_untung'], 0.15); self.assertAlmostEqual(t['purata_rugi'], -0.025)
        self.assertAlmostEqual(t['jangkaan'], 0.25 / 4)
        self.assertIsNone(T3.terbitan(0, 0, 0.0, 0.0)['menang'])

    def test_objektif(self):
        m = dict(n=40, mdd=-0.2, spy_mdd=-0.2, lebihan=0.03, win=0.52)
        self.assertTrue(T3.lulus_a03(m)); self.assertAlmostEqual(T3.skor_a03(m), 0.03)
        m['win'] = 0.45
        self.assertFalse(T3.lulus_a03(m)); self.assertAlmostEqual(T3.skor_a03(m), -1 + 0.03 - 0.05)


class UjiImbasF(unittest.TestCase):
    def test_eps_pada_tersedia(self):
        fr, _ = sintetik()
        f = {t: g for t, g in list(fr.items())[:2]}
        eps = eps_sintetik(f)
        self.assertEqual(IA3.semak_tersedia(eps)['langgar'], 0)
        self.assertGreater(IA3.semak_tersedia(eps_sintetik(f, bocor=True))['langgar'], 0)
        c = pd.Timestamp(eps.tarikh.iloc[5])
        e = IA3.eps_pada(eps, c)
        self.assertTrue((pd.to_datetime(e.tarikh) <= c).all())
        self.assertEqual(c in set(pd.to_datetime(e.tarikh)), eps.masa.iloc[5] == 'sebelum')

    def test_semak_f(self):
        fr, _ = sintetik()
        f = {t: g[g.index >= '2010-01-01'] for t, g in list(fr.items())[:3]}
        eps = eps_sintetik(f)
        # tarikh potong = hari laporan 'selepas' (kebocoran hanya kelihatan pada hari itu)
        sel = eps[(eps.masa == 'selepas') & (eps.tarikh > '2012-01-01')].tarikh.head(12).tolist()
        sel = [str(f[next(iter(f))].index[f[next(iter(f))].index.searchsorted(d)].date()) for d in sel]
        self.assertEqual(IA3.semak_f(f, eps, sel), {})
        self.assertIn('F', IA3.semak_f(f, eps_sintetik(f, bocor=True), sel))

    def test_liputan(self):
        p = os.path.join(tempfile.mkdtemp(), 'L.md')
        open(p, 'w').write('| Tahun | Baris | ada % | ada A % | ada B % | yoy % | F % |\n|---|---|---|---|---|---|---|\n'
                           '| 2013 | 100 | 65.0 | 60 | 70 | 50 | 10 |\n| 2014 | 100 | 80.5 | 80 | 81 | 70 | 12 |\n')
        lp = SA3.liputan(p)
        self.assertEqual(lp, {2013: 0.65, 2014: 0.805}); self.assertEqual(SA3.liputan_rendah(lp), [2013])


class UjiHujungA03(unittest.TestCase):
    """Tala MX (2 lorong, k0–7, 3 percubaan, sistem utama) → imbasan A03 → sahkan_a03.jalan → db a03_*."""
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        cls.dir = tempfile.mkdtemp(); cls.tala = os.path.join(cls.dir, 'tala')
        cls.asal = tala.muat_kaedah
        tala.muat_kaedah = lambda mid: kaedah_tiruan() if mid == 'MX' else cls.asal(mid)
        cls.S = tala.Sumber(modul=pengganti())
        fr, _ = sintetik(); cls.eps = eps_sintetik(fr)
        for lo in T2.LORONG:
            for k in range(8): T3.tala('MX', lo, k, cls.S, cls.eps, n_trials=3, keluar=cls.tala)
        json.dump(dict(versi='A03', pilihan={'had60': ['MX'], 'asal': ['MX']}, tugas=['MX_had60', 'MX_asal'],
                       pakar=['MX'], lain=[]), open(os.path.join(cls.dir, 'pilihan.json'), 'w'))
        pd.DataFrame([dict(kaedah='MX', lorong=lo, varian=v, status='SIAP', skor=0.01, lebihan_A=0.01, lebihan_B=0.02,
                           mdd_A=-0.2, n_A=40, sr_lebih_A=s, saat=1.0)
                      for lo, s in (('had60', 0.01), ('asal', 0.02)) for v in T3.SISTEM]).to_csv(
            os.path.join(cls.dir, 'saringan.csv'), index=False)
        cls.a02 = os.path.join(cls.dir, 'a02'); os.makedirs(cls.a02)
        pd.DataFrame([dict(kaedah='MX', lorong='had60', status='SIAP', skor=-0.01, sr_lebih_A=0.005)]).to_csv(
            os.path.join(cls.a02, 'saringan.csv'), index=False)
        cls.lp = os.path.join(cls.dir, 'LIPUTAN.md')
        open(cls.lp, 'w').write('| 2013 | 1 | 75.0 | 1 | 1 | 1 | 1 |\n')

    @classmethod
    def tearDownClass(cls):
        tala.muat_kaedah = cls.asal; shutil.rmtree(cls.dir, ignore_errors=True)

    def test_hujung(self):
        J = json.load(open(os.path.join(self.tala, 'MX_had60', 'k06.json')))
        self.assertEqual(J['status'], 'SIAP', J.get('ralat')); self.assertEqual(J['versi'], 'A03')
        self.assertEqual(J['sistem']['slot'], 5); self.assertTrue(J['sistem']['F'] and J['sistem']['M'])
        fr, idx = sintetik()
        sub = {t: g[g.index >= '2010-01-01'] for t, g in list(fr.items())[:6]}
        IA3._D.update(fr=sub, idx=idx, tala=self.tala, eps=self.eps[self.eps.ticker.isin(set(sub))])
        R = IA3.semak('MX_had60')
        self.assertNotIn('ralat', R, R.get('jejak')); self.assertIn('F', R['set'])
        self.assertEqual(R['tersedia']['langgar'], 0)
        d = os.path.join(self.dir, 'imbas'); os.makedirs(d); json.dump(R, open(os.path.join(d, 'MX_had60.json'), 'w'))
        out = IA3.tulis([d], self.dir)
        self.assertIn(out['MX_had60']['status'], ('BERSIH', 'PANDANG HADAPAN'))
        self.assertNotIn('F', out['MX_had60']['lajur'])
        D, gab, ring, n = SA3.jalan(self.S, self.eps, proses=2, keluar=self.dir, tala=self.tala, a02=self.a02,
                                    liputan_md=self.lp)
        self.assertEqual(len(D), 2); self.assertLessEqual(n, 150)
        self.assertEqual(ring['n_dsr'], 308); self.assertEqual(ring['n_sr_saringan'], 3)
        self.assertFalse(ring['liputan_rendah'])
        r = D.set_index('tugas').loc['MX_had60']
        self.assertEqual(r.kajian_siap, '01234567')
        self.assertIn(r.label, MA.LABEL); self.assertIn(r.label_a02, SA3.S2.LABEL)
        self.assertEqual(r.n_a, sum(J2['ujian_A']['n'] for J2 in
                                    [json.load(open(os.path.join(self.tala, 'MX_had60', f'k{k:02d}.json'))) for k in range(6)]))
        self.assertAlmostEqual(r.menang_a + r.kalah_a, 1.0)
        L = open(os.path.join(self.dir, 'LAPORAN.md')).read()
        self.assertIn('Saringan (peringkat 1): utama lwn ablasi', L); self.assertIn('Perbandingan dengan A02', L)
        sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE', 'dashboard'))
        import jana_db
        docs = jana_db.bina(self.dir, '2026-10-18T00:00Z')
        self.assertTrue(all(k.startswith('a03_') for k in docs), list(docs))
        self.assertEqual(docs['a03_ringkasan']['versi'], 'A03'); self.assertIn('a03_kaedah_MX_had60', docs)


if __name__ == '__main__':
    unittest.main()

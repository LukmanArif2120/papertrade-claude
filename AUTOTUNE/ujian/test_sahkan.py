# Ujian F6 (AUTOTUNE/sahkan): label SPEC §5, sambungan OOS, DSR dan N, pemilihan tamak, laporan.
# Fikstur JSON sintetik sahaja; tiada data harga, tiada rangkaian.
import json, math, os, shutil, sys, tempfile, unittest
import numpy as np, pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, 'sahkan'))
import umum as U
import pengesahan as P
import gabungan as G
import laporan as L

UJI = [(f'{2013 + k}-01-01', f'{2013 + k}-12-31') for k in range(11)] + [('2024-01-01', '2024-09-30')]


def hari(a, b): return pd.bdate_range(a, b)


def siri_json(t, r): return dict(tarikh=[d.strftime('%Y-%m-%d') for d in t], r=[float(x) for x in r])


def buat_kaedah(akar, kid, mu_a, mu_b, mu_k, sd=0.01, hari_pegang=10, pbo=0.1, dataran=0.8, ncuba=120,
                benih=0, langkau=(), ralat=()):
    rng = np.random.default_rng(benih)
    d = os.path.join(akar, kid); os.makedirs(d, exist_ok=True)
    for k in range(14):
        if k in langkau: continue
        j = dict(kaedah=kid, kajian=k, param={'n': 10 + k}, n_cubaan=ncuba, ralat=None)
        if k in ralat: j = dict(kaedah=kid, kajian=k, ralat='gagal', n_cubaan=0)
        elif k <= 11:
            t = hari(*UJI[k])
            j['ujian'] = dict(mula=UJI[k][0], akhir=UJI[k][1])
            j['pulangan_ujian'] = dict(A=siri_json(t, rng.normal(mu_a, sd, len(t))),
                                       B=siri_json(t, rng.normal(mu_b, sd, len(t))))
            j['metrik_ujian'] = dict(A=dict(n=20, hari=hari_pegang, menang=0.5), B=dict(n=10, hari=hari_pegang, menang=0.6))
            if k == 0:
                tb = hari('2013-01-01', '2018-12-31')
                j['bersih'] = dict(pulangan=siri_json(tb, rng.normal(mu_a, sd, len(tb))))
        elif k == 12:
            t = hari('2024-10-01', '2026-09-30')
            j['pulangan_ujian'] = dict(AB=siri_json(t, rng.normal(mu_k, sd, len(t))))
            j['pbo'] = pbo; j['dataran'] = dataran
        with open(os.path.join(d, f'k{k:02d}.json'), 'w') as f: json.dump(j, f)


def buat_modul(akar, kid, belum=False):
    os.makedirs(akar, exist_ok=True)
    with open(os.path.join(akar, f'{kid}.py'), 'w') as f:
        f.write(f"ID = '{kid}'\nNAMA = 'Ujian {kid}'\n" + ('BELUM_DITALA = True\n' if belum else ''))


def spy_palsu(mu=0.0004):
    t = hari('2009-01-01', '2026-10-16')
    return pd.Series(100 * np.cumprod(1 + np.full(len(t), mu)), index=t)


ASAS = dict(cagr_a=0.20, cagr_b=0.15, mdd_a=-0.20, hari_a=10, spy_a=0.12, spy_b=0.12,
            cagr_kunci=0.20, spy_kunci=0.10, dsr=0.97, pbo=0.2)


class TestLabel(unittest.TestCase):
    def m(self, **kw): x = dict(ASAS); x.update(kw); return x

    def test_tinggi_dan_sempadan(self):
        self.assertEqual(U.label(self.m()), 'TINGGI')
        self.assertEqual(U.label(self.m(dsr=0.95, pbo=0.30, mdd_a=-0.30)), 'TINGGI')   # sempadan termasuk
        self.assertEqual(U.label(self.m(dsr=0.9499)), 'SEDERHANA')
        self.assertEqual(U.label(self.m(pbo=0.3001)), 'SEDERHANA')
        self.assertEqual(U.label(self.m(cagr_kunci=0.10)), 'SEDERHANA')                 # kunci = SPY bukan >
        self.assertEqual(U.label(self.m(pbo=float('nan'))), 'SEDERHANA')

    def test_sederhana_rendah_gagal(self):
        self.assertEqual(U.label(self.m(cagr_b=0.12)), 'RENDAH')                         # B = SPY bukan >
        self.assertEqual(U.label(self.m(mdd_a=-0.3001)), 'RENDAH')
        self.assertEqual(U.label(self.m(cagr_a=0.11)), 'RENDAH')
        self.assertEqual(U.label(self.m(cagr_a=0.0)), 'GAGAL')
        self.assertEqual(U.label(self.m(cagr_a=-0.05)), 'GAGAL')
        self.assertEqual(U.label(self.m(cagr_a=float('nan'))), 'GAGAL')

    def test_bukan_swing_dan_belum(self):
        self.assertEqual(U.label(self.m(hari_a=1.99)), 'BUKAN SWING')
        self.assertEqual(U.label(self.m(hari_a=60.01)), 'BUKAN SWING')
        self.assertEqual(U.label(self.m(hari_a=2.0)), 'TINGGI')
        self.assertEqual(U.label(self.m(hari_a=60.0)), 'TINGGI')
        self.assertEqual(U.label(self.m(hari_a=1.0), belum=True), 'BELUM DITALA')


class TestMetrik(unittest.TestCase):
    def test_sambung(self):
        a = pd.Series([0.01, 0.02], index=pd.to_datetime(['2013-01-02', '2013-01-03']))
        b = pd.Series([-0.01], index=pd.to_datetime(['2014-01-02']))
        r = U.sambung([b, a])
        self.assertEqual(list(r.values), [0.01, 0.02, -0.01])
        with self.assertRaises(ValueError): U.sambung([a, a])

    def test_cagr_mdd(self):
        r = pd.Series([0.1, -0.5, 0.2], index=hari('2020-01-01', '2020-01-03'))
        self.assertAlmostEqual(U.mdd(r), -0.5)
        self.assertAlmostEqual(U.cagr(pd.Series(np.full(252, 0.001))), 1.001 ** 252 - 1)
        self.assertAlmostEqual(U.mdd(pd.Series([-0.1, 0.0])), -0.1)                       # modal awal 1.0 dikira

    def test_siri_format(self):
        t = ['2020-01-02', '2020-01-03']
        for o in (dict(tarikh=t, r=[0.1, 0.2]), {t[0]: 0.1, t[1]: 0.2}, [[t[0], 0.1], [t[1], 0.2]]):
            s = U.siri(o)
            self.assertEqual(list(s.values), [0.1, 0.2]); self.assertEqual(s.index[0], pd.Timestamp(t[0]))

    def test_dsr(self):
        rng = np.random.default_rng(1)
        r = pd.Series(rng.normal(0.002, 0.01, 2500))
        d1, d2, d3 = U.dsr(r, 1), U.dsr(r, 1000), U.dsr(r, 300000)
        self.assertGreater(d1, d2); self.assertGreater(d2, d3)
        self.assertGreater(d1, 0.99)
        self.assertTrue(math.isnan(U.dsr(r, 0)))
        self.assertLess(U.dsr(pd.Series(rng.normal(0, 0.01, 2500)), 300000), 0.5)

    def test_spy_tarikh_sama(self):
        spy = spy_palsu(0.001)
        t = hari('2015-01-01', '2015-12-31')
        self.assertAlmostEqual(P.spy_cagr(spy, t), 1.001 ** 252 - 1, places=9)


class TestPengesahan(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.tala = os.path.join(self.d, 'tala'); self.kd = os.path.join(self.d, 'kaedah')
        self.out = os.path.join(self.d, 'hasil')
        buat_kaedah(self.tala, 'M01', 0.0012, 0.0012, 0.0012, sd=0.004, benih=1)                  # kuat
        buat_kaedah(self.tala, 'M02', 0.0003, -0.0002, 0.0002, sd=0.004, benih=2)                   # lemah
        buat_kaedah(self.tala, 'M03', 0.0012, 0.0012, 0.0012, sd=0.004, benih=3, langkau=(5,))    # k05 tiada
        buat_kaedah(self.tala, 'M04', 0.0012, 0.0012, 0.0012, sd=0.004, benih=4)                  # modul belum
        buat_kaedah(self.tala, 'M05', 0.0012, 0.0012, 0.0012, sd=0.004, benih=5, hari_pegang=1.5)
        buat_kaedah(self.tala, 'M06', 0.0012, 0.0012, 0.0012, sd=0.004, benih=6, ralat=(12,))     # k12 ralat
        for k in ('M01', 'M02', 'M03', 'M05', 'M06'): buat_modul(self.kd, k)
        buat_modul(self.kd, 'M04', belum=True)
        self.df, self.ring = P.jalan(self.tala, self.out, spy=spy_palsu(), kaedah_dir=self.kd,
                                     kaedah=['M01', 'M02', 'M03', 'M04', 'M05', 'M06'])
        self.r = self.df.set_index('kaedah')

    def tearDown(self): shutil.rmtree(self.d)

    def test_label(self):
        self.assertIn(self.r.loc['M01', 'label'], ('TINGGI', 'SEDERHANA'))
        self.assertEqual(self.r.loc['M02', 'label'], 'RENDAH')
        self.assertEqual(self.r.loc['M03', 'label'], 'BELUM DITALA')
        self.assertIn('k05', self.r.loc['M03', 'catatan'])
        self.assertEqual(self.r.loc['M04', 'label'], 'BELUM DITALA')
        self.assertEqual(self.r.loc['M05', 'label'], 'BUKAN SWING')
        self.assertEqual(self.r.loc['M06', 'label'], 'BELUM DITALA')

    def test_sambungan_dan_n(self):
        n_hari = sum(len(hari(*u)) for u in UJI)
        kaj = U.baca_kajian('M01', os.path.join(self.tala, 'M01'))
        self.assertEqual(len(P.oos(kaj, 'A')), n_hari)
        self.assertEqual(self.r.loc['M01', 'n_a'], 20 * 12)
        self.assertEqual(self.r.loc['M01', 'n_b'], 10 * 12)
        self.assertAlmostEqual(self.r.loc['M01', 'menang_b'], 0.6)
        self.assertEqual(self.r.loc['M01', 'oos_mula'], '2013-01-01')
        self.assertEqual(self.r.loc['M01', 'oos_akhir'], '2024-09-30')
        # N DSR = jumlah percubaan semua kaedah (M03 13 kajian, M06 k12 ralat → 0)
        self.assertEqual(self.ring['n_cubaan_jumlah'], 120 * (14 * 4 + 13 + 13))
        dsr = U.dsr(P.oos(kaj, 'A'), self.ring['n_cubaan_jumlah'])
        self.assertAlmostEqual(self.r.loc['M01', 'dsr'], dsr, places=5)
        self.assertEqual(json.loads(self.r.loc['M01', 'param_semasa']), {'n': 23})
        self.assertEqual(json.loads(self.r.loc['M01', 'param_akhir']), {'n': 22})
        self.assertAlmostEqual(self.r.loc['M01', 'pbo'], 0.1)
        self.assertEqual(self.r.loc['M01', 'kunci_mula'], '2024-10-01')

    def test_ringkasan_dan_laporan(self):
        self.assertEqual(sum(self.ring['kiraan_label'].values()), 6)
        self.assertEqual(self.ring['top20_cagr_a'][0]['kaedah'] in ('M01', 'M05'), True)
        h = G.jalan(keluar=self.out, tala=self.tala, spy=spy_palsu(), penjana=object()) \
            if not (self.df.label.isin(['TINGGI', 'SEDERHANA'])).any() else None
        # tiada gabungan sebenar (perlu data) — tulis gabungan kosong untuk laporan
        if h is None:
            U.tulis_json(os.path.join(self.out, 'gabungan.json'), dict(terpilih=[], penjelasan='ujian', terbaik3_oos_a=[]))
        baris, papan = L.jana(self.out)
        self.assertLessEqual(len(baris), 150)
        self.assertEqual(len(papan), 6)
        for p in papan: self.assertLessEqual(len(json.dumps(p, ensure_ascii=False, separators=(',', ':')).encode()), 2048)
        with open(os.path.join(self.out, 'LAPORAN.md'), encoding='utf-8') as f: teks = f.read()
        self.assertIn('BELUM DITALA (3)', teks)
        with open(os.path.join(self.out, 'papan.json')) as f: json.load(f)


class TestGabungan(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(7); t = hari('2013-01-01', '2016-12-31'); n = len(t)
        asas = rng.normal(0, 0.01, n)
        self.r = {
            'X1': pd.Series(0.0010 + asas, t),                              # terbaik
            'X2': pd.Series(0.0009 + 0.9 * asas + rng.normal(0, 0.004, n), t),  # korelasi tinggi dengan X1
            'X3': pd.Series(0.0008 + rng.normal(0, 0.01, n), t),            # bebas → menambah
            'X4': pd.Series(-0.0020 + rng.normal(0, 0.01, n), t),           # menurunkan CAGR
            'X5': pd.Series(0.0007 + rng.normal(0, 0.01, n), t),
            'X6': pd.Series(0.0007 + rng.normal(0, 0.01, n), t),
            'X7': pd.Series(0.0007 + rng.normal(0, 0.01, n), t),
            'X8': pd.Series(0.0007 + rng.normal(0, 0.01, n), t),
            'X9': pd.Series(0.0007 + rng.normal(0, 0.01, n), t),
        }
        self.panggil = []

        def nilai(ids):
            self.panggil.append(tuple(ids))
            g = pd.concat([self.r[i] for i in ids], axis=1).mean(axis=1)     # campuran sama berat (palsu)
            return U.cagr(g), U.mdd(g)
        self.nilai = nilai

    def test_tamak(self):
        calon = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9']
        pilih, log, (c, d) = G.pilih_tamak(calon, self.r, self.nilai, maks=6)
        self.assertEqual(pilih[0], 'X1')
        self.assertNotIn('X2', pilih); self.assertNotIn('X4', pilih)
        self.assertIn('X3', pilih)
        self.assertLessEqual(len(pilih), 6)
        t = {s['kaedah']: s['tindakan'] for s in log}
        self.assertTrue(t['X2'].startswith('langkau'))
        self.assertTrue(t['X4'].startswith('tolak'))
        self.assertNotIn(('X1', 'X2'), self.panggil)                    # korelasi disemak sebelum nilai
        # CAGR naik setiap kali tambah
        cg = [s['cagr'] for s in log if s['tindakan'] in ('mula', 'tambah')]
        self.assertEqual(cg, sorted(cg))
        self.assertAlmostEqual(c, cg[-1])

    def test_maks_dan_mdd(self):
        pilih, log, _ = G.pilih_tamak(['X1', 'X3', 'X5'], self.r, self.nilai, maks=1)
        self.assertEqual(pilih, ['X1']); self.assertEqual(len(log), 1)
        pilih, log, _ = G.pilih_tamak(['X1', 'X3'], self.r, lambda ids: (len(ids) * 0.1, -0.31 if len(ids) > 1 else -0.1))
        self.assertEqual(pilih, ['X1']); self.assertIn('MDD', log[-1]['tindakan'])
        self.assertEqual(G.pilih_tamak([], self.r, self.nilai)[0], [])

    def test_persentil_kongsi(self):
        e = pd.to_datetime(['2020-01-02'] * 3 + ['2020-01-03'])
        T = pd.DataFrame(dict(ticker=['a', 'b', 'c', 'd'], ent=e, ex=e, ret=0.0, days=1, rank=[5.0, -1.0, 2.0, -100.0]))
        p = G.persentil(T)
        self.assertEqual(list(p['rank']), [1.0, 1 / 3, 2 / 3, 1.0])
        T2 = p.assign(ticker=['x', 'y', 'z', 'w'])
        k = G.kongsi([p, T2])
        self.assertEqual(list(k.ticker[:2]), ['a', 'x'])                  # seri → urutan kaedah dikekalkan

    def test_tiada_calon(self):
        d = tempfile.mkdtemp()
        try:
            pd.DataFrame([dict(kaedah='M01', label='RENDAH', cagr_a=0.05, mdd_a=-0.2, cagr_b=0.04, cagr_kunci=0.01,
                               param_semasa='{}')]).to_csv(os.path.join(d, 'parameter_sedia.csv'), index=False)
            h = G.jalan(keluar=d, tala=d, spy=spy_palsu(), penjana=object())
            self.assertEqual(h['terpilih'], [])
            self.assertEqual(h['terbaik3_oos_a'][0]['kaedah'], 'M01')
            with open(os.path.join(d, 'gabungan.json')) as f: self.assertIn('Tiada', json.load(f)['penjelasan'])
        finally:
            shutil.rmtree(d)

    def test_tetingkap(self):
        self.assertEqual(G.tetingkap_kajian({}, 0), ('2010-01-01', '2013-01-01', '2013-12-31'))
        self.assertEqual(G.tetingkap_kajian({}, 11), ('2021-01-01', '2024-01-01', '2024-09-30'))
        self.assertEqual(G.tetingkap_kajian({}, 12), ('2021-10-01', '2024-10-01', None))


if __name__ == '__main__':
    unittest.main()

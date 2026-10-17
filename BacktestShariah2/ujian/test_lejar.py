# Ujian Lejar Penuh (standard/lejar.py): dagangan lejar sesi demi sesi = enjin.trades v1.2 atas data sama.
import os, sys, types, tempfile, unittest, argparse
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import lejar, enjin

MULA = pd.Timestamp('2025-06-02')


def _sedia(fr, idx, buka_esok=True):
    for t, g in fr.items():
        c, o = g.close, g.open
        ma = c.rolling(10).mean()
        asas = (c > ma) & (c.shift() <= ma.shift())
        stop = g.low.rolling(5).min() * 0.98
        sig = asas & ~(o.shift(-1) <= stop) if buka_esok else asas      # peraturan buka esok (seperti M14)
        sig[g.index < MULA] = False
        g['sig'] = sig.fillna(False); g['stop'] = stop; g['tgt'] = c * 1.08
        g['exitc'] = c < ma * 0.97; g['rank'] = c / c.shift(20) - 1


def modul(nama, buka_esok=True):
    m = types.ModuleType(f'kaedah.{nama}')
    m.ID = nama; m.NAMA = 'Ujian'; m.VARIAN = 'x'; m.TMAX = 15; m.WARM = 30; m.PERLU_BAR = 60; m.SILANG = False
    m.sedia = lambda fr, idx: _sedia(fr, idx, buka_esok)
    sys.modules[f'kaedah.{nama}'] = m
    return m


def data(n=320, saham=('AAA', 'BBB', 'CCC', 'DDD'), benih=7):
    rng = np.random.default_rng(benih)
    ix = pd.bdate_range('2024-09-02', periods=n)
    fr = {}
    for t in saham:
        r = rng.normal(0.0008, 0.025, n)
        c = 50 * np.exp(np.cumsum(r)); o = c * np.exp(rng.normal(0, 0.012, n))
        h = np.maximum(o, c) * (1 + rng.uniform(0, 0.02, n)); l = np.minimum(o, c) * (1 - rng.uniform(0, 0.02, n))
        fr[t] = pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=1e6), index=ix)
    spy = pd.DataFrame(dict(open=1.0, high=1.0, low=1.0, close=1.0, volume=1.0), index=ix)
    return fr, {'SPY': spy, 'QQQ': spy.copy()}


def jalan_lejar(mid, fr, idx, langkau_sesi=()):
    lejar.FR, lejar.IDX = fr, idx
    T, W, tutup, langkau = [], [], [], []
    bil = {}
    for S in [x for x in idx['SPY'].index if x >= MULA]:
        if S in langkau_sesi: continue          # larian kaedah gagal / terlepas pada sesi ini
        h = lejar.kerja((mid, S, T, W, None, set(), bil))
        assert h['ralat'] is None, h['ralat']
        T, W = h['terbuka'], h['tunggu']; tutup += h['tutup']; langkau += h['langkau']
        for p in h['beli']: bil[p['saham']] = p['belian_ke']
    return T, W, tutup, langkau


def enjin_trades(m, fr, idx):
    f = {t: g.copy() for t, g in fr.items()}
    m.sedia(f, idx)
    return enjin.trades(f, m.TMAX, m.WARM)


class UjiLejar(unittest.TestCase):
    # Kesetaraan enjin diuji dengan TIGA_LORONG=False (posisi tutup apabila lorong 1 keluar, seperti enjin.trades).
    # Dengan tiga lorong, lorong 1 setiap posisi tetap = enjin, tetapi belian semula disekat sehingga semua lorong keluar.
    def setUp(self):
        self._tiga = lejar.TIGA_LORONG; lejar.TIGA_LORONG = False

    def tearDown(self):
        lejar.TIGA_LORONG = self._tiga

    def test_sama_dengan_enjin(self):
        m = modul('M9001'); fr, idx = data()
        E = enjin_trades(m, fr, idx)
        T, W, tutup, langkau = jalan_lejar('M9001', fr, idx)
        self.assertGreater(len(E), 10)
        tutup_e = E[E.why != 'hujung']
        L = pd.DataFrame(tutup)
        self.assertEqual(len(L), len(tutup_e))
        a = L.sort_values(['saham', 'tarikh_isyarat']).reset_index(drop=True)
        b = tutup_e.sort_values(['ticker', 'sig']).reset_index(drop=True)
        self.assertEqual(list(a.saham), list(b.ticker))
        self.assertEqual(list(a.tarikh_isyarat), [str(x.date()) for x in b.sig])
        self.assertEqual(list(a.tarikh_beli), [str(x.date()) for x in b.ent])
        self.assertEqual(list(a.tarikh_keluar), [str(x.date()) for x in b.ex])
        self.assertEqual(list(a.sebab_keluar), list(b.why))
        self.assertEqual(list(a.hari), list(b.days))
        np.testing.assert_allclose(a.pulangan.astype(float), b.ret, atol=2e-5)
        np.testing.assert_allclose(a.mfe_pct.astype(float) / 100, b.mfe, atol=2e-5)
        # posisi terbuka lejar = dagangan 'hujung' enjin
        terbuka_e = E[E.why == 'hujung']
        self.assertEqual(sorted((p['saham'], p['tarikh_isyarat']) for p in T),
                         sorted((t, str(s.date())) for t, s in zip(terbuka_e.ticker, terbuka_e.sig)))
        self.assertFalse(any(x['sebab'] == 'buka <= henti' for x in langkau))

    def test_tampung_sesi_terlepas(self):
        # sesi tanpa isyarat baharu boleh terlepas; keluar dinilai bar demi bar apabila larian disambung
        m = modul('M9002'); fr, idx = data(benih=11)
        f = {t: g.copy() for t, g in fr.items()}; m.sedia(f, idx)
        ada_sig = set().union(*[set(g.index[g.sig]) for g in f.values()])
        sesi = [x for x in idx['SPY'].index if x >= MULA]
        terlepas = [s for s in sesi[5:] if s not in ada_sig and (s - pd.Timedelta(days=1)) not in ada_sig][:25]
        _, _, penuh, _ = jalan_lejar('M9002', fr, idx)
        _, _, separa, _ = jalan_lejar('M9002', fr, idx, langkau_sesi=set(terlepas))
        k = lambda L: sorted((r['saham'], r['tarikh_isyarat'], r['tarikh_keluar'], r['harga_keluar']) for r in L)
        self.assertGreater(len(terlepas), 10)
        self.assertEqual(k(penuh), k(separa))

    def test_buka_bawah_henti_dilangkau(self):
        modul('M9003', buka_esok=False); fr, idx = data(benih=3)
        g = fr['AAA']; f = {'AAA': g.copy()}; sys.modules['kaedah.M9003'].sedia(f, idx)
        i = int(np.flatnonzero(f['AAA'].sig.values)[0])
        g.iloc[i + 1, g.columns.get_loc('open')] = float(f['AAA'].stop.iloc[i]) * 0.99   # buka esok jurang bawah henti
        g.iloc[i + 1, g.columns.get_loc('low')] = min(g.low.iloc[i + 1], g.open.iloc[i + 1])
        _, _, tutup, langkau = jalan_lejar('M9003', {'AAA': g}, idx)
        sbb = {(x['saham'], x['tarikh_isyarat']): x['sebab'] for x in langkau}
        self.assertEqual(sbb.get(('AAA', str(g.index[i].date()))), 'buka <= henti')
        self.assertNotIn(str(g.index[i].date()), [r['tarikh_isyarat'] for r in tutup])

    def test_larian_penuh_fail(self):
        # stor -> jalan (dua kali, kedua tiada sesi baharu) -> semak -> ringkas
        modul('M9001'); fr, idx = data(n=300)
        with tempfile.TemporaryDirectory() as d:
            stor = os.path.join(d, 'stor'); os.makedirs(stor)
            rows = [g.assign(ticker=t, date=g.index.strftime('%Y%m%d').astype(int)) for t, g in fr.items()]
            pd.concat(rows)[lejar.LAJ].to_csv(os.path.join(stor, 'harga_A.csv'), index=False)
            pd.concat([g.assign(ticker=t, date=g.index.strftime('%Y%m%d').astype(int)) for t, g in idx.items()])[lejar.LAJ] \
                .to_csv(os.path.join(stor, 'harga_idx.csv'), index=False)
            lama = lejar.STOR, lejar.LEJAR
            lejar.STOR, lejar.LEJAR = stor, os.path.join(d, 'lejar')
            os.environ['LEJAR_UNIV'] = os.path.join(d, 'tiada.txt')
            try:
                a = argparse.Namespace(mula=str(MULA.date()), hingga=None, proses=2, hanya='M9001')
                lejar.cmd_jalan(a); lejar.cmd_jalan(a)
                T, O = lejar.semua_posisi()
                E = enjin_trades(sys.modules['kaedah.M9001'], fr, idx)
                self.assertEqual(len(T), int((E.why != 'hujung').sum())); self.assertEqual(len(O), int((E.why == 'hujung').sum()))
                with self.assertRaises(SystemExit) as cm:
                    lejar.cmd_semak(argparse.Namespace())
                self.assertEqual(cm.exception.code, 0)
                self.assertTrue(os.path.exists(os.path.join(d, 'lejar', 'isyarat', f"{idx['SPY'].index[-1].strftime('%Y%m%d')}.csv.gz")))
            finally:
                lejar.STOR, lejar.LEJAR = lama; os.environ.pop('LEJAR_UNIV', None)


class UjiTigaLorong(unittest.TestCase):
    def setUp(self):
        self._tiga = lejar.TIGA_LORONG; lejar.TIGA_LORONG = True

    def tearDown(self):
        lejar.TIGA_LORONG = self._tiga

    def test_lorong1_sama_enjin_dan_belian_semula_disekat(self):
        m = modul('M9004'); fr, idx = data(benih=5)
        T, W, tutup, langkau = jalan_lejar('M9004', fr, idx)
        semua = tutup + T
        self.assertGreater(len(semua), 5); self.assertGreater(len(tutup), 1)
        # setiap posisi tutup: ketiga-tiga lorong keluar, tarikh lorong >= tarikh beli
        for r in tutup:
            self.assertTrue(r['tutup_semua'])
            for c in ('tarikh_keluar', 'tarikh_keluar_henti', 'tarikh_keluar_10'):
                self.assertGreaterEqual(r[c], r['tarikh_beli'])
        # tiada dua posisi kaedah+saham bertindih: belian baharu hanya selepas tarikh tutup sepenuhnya posisi sebelumnya
        by = {}
        for r in semua: by.setdefault(r['saham'], []).append(r)
        for t, a in by.items():
            a.sort(key=lambda r: r['tarikh_beli'])
            for x, y in zip(a, a[1:]):
                self.assertTrue(lejar.tarikh_tutup(x), f'{t}: posisi terbuka diikuti belian baharu')
                self.assertGreater(y['tarikh_isyarat'], lejar.tarikh_tutup(x))
        # lorong 1 setiap posisi = enjin bagi isyarat yang sama (keluar ditentukan oleh bar, bukan oleh lorong lain)
        f = {t: g.copy() for t, g in fr.items()}; m.sedia(f, idx)
        for r in [r for r in semua if r.get('tarikh_keluar')]:
            g = f[r['saham']]; i = g.index.get_loc(pd.Timestamp(r['tarikh_isyarat']))
            E = enjin.trades({r['saham']: g.iloc[:].assign(sig=[k == i for k in range(len(g))])}, m.TMAX, 0)
            self.assertEqual(str(E.ex.iloc[0].date()), r['tarikh_keluar'])


if __name__ == '__main__':
    unittest.main()

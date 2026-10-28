# Ujian Lejar Penuh (standard/lejar.py): dagangan lejar sesi demi sesi = enjin.trades v1.2 atas data sama.
import os, sys, types, tempfile, unittest, argparse, json
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import lejar, enjin

MULA = pd.Timestamp('2025-06-02')


def _sedia(fr, idx, buka_esok=True, exit_perlu_esok=False):
    for t, g in fr.items():
        c, o = g.close, g.open
        ma = c.rolling(10).mean()
        asas = (c > ma) & (c.shift() <= ma.shift())
        stop = g.low.rolling(5).min() * 0.98
        sig = asas & ~(o.shift(-1) <= stop) if buka_esok else asas      # peraturan buka esok (seperti M14)
        sig[g.index < MULA] = False
        g['sig'] = sig.fillna(False); g['stop'] = stop; g['tgt'] = c * 1.08
        g['exitc'] = c < ma * 0.97; g['rank'] = c / c.shift(20) - 1
        if exit_perlu_esok:   # seperti modul `_exitc_*` (M76, M82 …): bendera bar j hanya jika bar j+1 wujud
            g['exitc'] = g['exitc'] & c.shift(-1).notna()


def modul(nama, buka_esok=True, exit_perlu_esok=False):
    m = types.ModuleType(f'kaedah.{nama}')
    m.ID = nama; m.NAMA = 'Ujian'; m.VARIAN = 'x'; m.TMAX = 15; m.WARM = 30; m.PERLU_BAR = 60; m.SILANG = False
    m.sedia = lambda fr, idx: _sedia(fr, idx, buka_esok, exit_perlu_esok)
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


def jalan_lejar(mid, fr, idx, langkau_sesi=(), aa=None):
    lejar.FR, lejar.IDX = fr, idx
    T, W, tutup, langkau = [], [], [], []
    bil = {}
    for S in [x for x in idx['SPY'].index if x >= MULA]:
        if S in langkau_sesi: continue          # larian kaedah gagal / terlepas pada sesi ini
        h = lejar.kerja((mid, S, T, W, None, set(), bil, aa or {}))
        assert h['ralat'] is None, h['ralat']
        T, W = h['terbuka'], h['tunggu']; tutup += h['tutup']; langkau += h['langkau']
        for p in h['beli']: bil[p['saham']] = p['belian_ke']
    return T, W, tutup, langkau


def enjin_trades(m, fr, idx):
    f = {t: g.copy() for t, g in fr.items()}
    m.sedia(f, idx)
    return enjin.trades(f, m.TMAX, m.WARM)


class UjiLejar(unittest.TestCase):
    # Kesetaraan enjin diuji dengan DUA_LORONG=False (posisi tutup apabila lorong 1 keluar, seperti enjin.trades).
    # Dengan dua lorong (UjiDuaLorong), lorong 1 tetap = enjin kerana hanya lorong 1 menyekat belian semula (sejak 19 Okt 2026).
    def setUp(self):
        self._dua = lejar.DUA_LORONG; lejar.DUA_LORONG = False

    def tearDown(self):
        lejar.DUA_LORONG = self._dua

    def test_saham_diambil_alih_tidak_dibeli(self):
        # sejak 21 Okt 2026: saham dalam set ambil alih sesi S tidak masuk menunggu dan tidak dibeli
        modul('M9006'); fr, idx = data()
        T0, _, tutup0, _ = jalan_lejar('M9006', fr, idx)
        self.assertTrue(any(p['saham'] == 'AAA' for p in T0 + tutup0))
        T, W, tutup, langkau = jalan_lejar('M9006', fr, idx, aa={'AAA': 'ambil alih'})
        self.assertFalse(any(p['saham'] == 'AAA' for p in T + W + tutup))
        self.assertEqual(sorted({p['saham'] for p in T + tutup}), sorted({p['saham'] for p in T0 + tutup0} - {'AAA'}))

    def test_posisi_saham_delist_ditutup(self):
        # saham tanpa bar >= DELIST_SESI sesi: posisi terbuka ditutup pada tutup bar terakhir (lorong 1 'delist' + lorong 2)
        modul('M9007'); fr, idx = data()
        akhir = fr['AAA'].index[-30]; fr['AAA'] = fr['AAA'][fr['AAA'].index <= akhir]
        lejar.DUA_LORONG = True
        T, W, tutup, langkau = jalan_lejar('M9007', fr, idx)
        self.assertFalse(any(p['saham'] == 'AAA' for p in T))
        dl = [p for p in tutup if p.get('sebab_keluar') == 'delist']
        self.assertTrue(dl)
        for p in dl:
            self.assertEqual((p['tarikh_keluar'], p['tarikh_keluar_henti'], p['tutup_semua']), (lejar.tkh(akhir), lejar.tkh(akhir), True))
            self.assertAlmostEqual(float(p['harga_keluar']), float(fr['AAA'].close.iloc[-1]), places=3)

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

    def test_exitc_perlu_bar_esok_sama_dengan_enjin(self):
        # 22 Okt 2026 (R2): exitc bar terakhir belum diketahui pada sesi itu; lejar mesti tetap keluar seperti enjin
        m = modul('M9008', exit_perlu_esok=True); fr, idx = data(benih=11)
        E = enjin_trades(m, fr, idx); E = E[E.why != 'hujung']
        T, W, tutup, langkau = jalan_lejar('M9008', fr, idx)
        self.assertGreater((E.why == 'exit').sum() if 'exit' in set(E.why) else len(E), 3)
        a = sorted((p['saham'], p['tarikh_isyarat'], p['tarikh_keluar'], p['sebab_keluar']) for p in tutup)
        b = sorted((t, str(s.date()), str(x.date()), w) for t, s, x, w in zip(E.ticker, E.sig, E.ex, E.why))
        self.assertEqual(a, b)

    def test_tampal_moomoo_hanya_buka_rasmi(self):
        # 22 Okt 2026 (R1): nota "buka sementara … (sahkan kline …)" tidak diterima; nilai disahkan terkini menang
        with tempfile.TemporaryDirectory() as d:
            stor = os.path.join(d, 'stor'); pt = os.path.join(d, 'papertrade'); lj = os.path.join(d, 'lejar')
            for x in (stor, pt, lj): os.makedirs(x)
            pd.DataFrame(dict(ticker=['AAA'], date=[20261020], open=[9.0])).to_csv(os.path.join(stor, 'buka_moomoo.csv'), index=False)
            json.dump({'sesi_terakhir': '2026-10-19'}, open(os.path.join(lj, 'status.json'), 'w'))
            pd.DataFrame(dict(tarikh_beli=['2026-10-20', '2026-10-20', '2026-10-21'], saham=['AAA', 'BBB', 'CCC'], harga_beli=['10.5', '20', '30'],
                              tidak_dibeli=['', '', ''], nota=['buka rasmi kline 20 Okt (disahkan 6:02 MYT)',
                                                               'buka sementara quote 9:37 NY (sahkan kline selepas 10:00)',
                                                               'belian ke-2; buka rasmi kline 21 Okt (disahkan 6:02 MYT)'])) \
                .to_csv(os.path.join(pt, 'claude.csv'), index=False)
            S = {'harga_A.csv': pd.DataFrame(dict(ticker=['AAA', 'BBB', 'CCC'], date=[20261020, 20261020, 20261021], open=[10.0, 21.0, 31.0],
                                                  high=[11.0, 22.0, 32.0], low=[9.5, 19.0, 29.0], close=[10.8, 20.5, 30.5], volume=[1e6] * 3))}
            lama = lejar.STOR, lejar.LEJAR, lejar.BS2
            lejar.STOR, lejar.LEJAR, lejar.BS2 = stor, lj, d
            try:
                lejar.tampal_moomoo(S)
            finally:
                lejar.STOR, lejar.LEJAR, lejar.BS2 = lama
            self.assertEqual(list(S['harga_A.csv'].open), [10.5, 21.0, 30.0])
            M = pd.read_csv(os.path.join(stor, 'buka_moomoo.csv')).set_index('ticker').open.to_dict()
            self.assertEqual(M, {'AAA': 10.5, 'CCC': 30.0})

    def test_tampal_moomoo_langkau_skala_tidak_sepadan(self):
        # 28 Okt 2026 (ralat BUUU): buka sebelum pecahan dalam buka_moomoo.csv tidak boleh menimpa bar stor yang
        # sudah dilaras — beza > TOL_SKALA dilangkau dan dilaporkan, bar stor kekal.
        with tempfile.TemporaryDirectory() as d:
            stor = os.path.join(d, 'stor'); pt = os.path.join(d, 'papertrade'); lj = os.path.join(d, 'lejar')
            for x in (stor, pt, lj): os.makedirs(x)
            pd.DataFrame(dict(ticker=['AAA'], date=[20261019], open=[42.67])).to_csv(os.path.join(stor, 'buka_moomoo.csv'), index=False)
            json.dump({'sesi_terakhir': '2026-10-19'}, open(os.path.join(lj, 'status.json'), 'w'))
            S = {'harga_A.csv': pd.DataFrame(dict(ticker=['AAA'], date=[20261019], open=[4.267], high=[4.349],
                                                  low=[4.083], close=[4.328], volume=[1e6]))}
            lama = lejar.STOR, lejar.LEJAR, lejar.BS2
            lejar.STOR, lejar.LEJAR, lejar.BS2 = stor, lj, d
            try:
                hasil = lejar.tampal_moomoo(S)
            finally:
                lejar.STOR, lejar.LEJAR, lejar.BS2 = lama
            self.assertEqual(list(S['harga_A.csv'].open), [4.267])
            self.assertEqual(list(S['harga_A.csv'].high), [4.349])
            self.assertEqual(hasil['ditampal'], 0)
            self.assertEqual(len(hasil['langkau_skala']), 1)

    def test_modul_replika_keluar_dagangan_sendiri(self):
        # 22 Okt 2026 (R10): exitc modul replika = bendera dagangan replika (bermula WARM). Lejar bermula di tengah: posisi yang
        # isyaratnya jatuh semasa replika memegang dagangan lain mesti keluar ikut dagangan SENDIRI (kod/dagangan.py)
        import dagangan
        m = types.ModuleType('kaedah.M9009'); m.ID = 'M9009'; m.NAMA = 'Ujian'; m.VARIAN = 'x'; m.TMAX = 15; m.PERLU_BAR = 60
        m.SILANG = False; m.WARM = 30

        def _replika(g, warm):
            o, c, sig = g.open.values, g.close.values, g.sig.values; n = len(g); ex = np.zeros(n, bool); i = warm
            while i < n - 1:
                if not sig[i]: i += 1; continue
                e = o[i + 1]; j = i + 1; k = n - 1
                while j < n:
                    if c[j] < e * 0.97 and j + 1 < n: ex[j] = True; k = j + 1; break
                    if j - i >= m.TMAX: k = j; break
                    j += 1
                i = k + 1
            return ex

        def sedia(fr, idx):
            for g in fr.values():
                c = g.close; ma = c.rolling(5).mean()
                g['sig'] = (c > ma).fillna(False)            # isyarat berterusan (seperti M81/M82)
                g['stop'] = np.nan; g['tgt'] = np.nan; g['rank'] = 0.0
                g['exitc'] = _replika(g, m.WARM)
        m.sedia = sedia; sys.modules['kaedah.M9009'] = m
        fr, idx = data(benih=5)
        dagangan.REPLIKA.add('M9009')
        try:
            T, W, tutup, langkau = jalan_lejar('M9009', fr, idx)
        finally:
            dagangan.REPLIKA.discard('M9009')
        self.assertGreater(len(tutup), 5)
        for p in tutup:
            g = fr[p['saham']]; i = g.index.get_loc(pd.Timestamp(p['tarikh_isyarat'])); e = float(g.open.iloc[i + 1])
            c = g.close.values; o = g.open.values; jangka = None
            for j in range(i + 1, len(g)):
                if c[j] < e * 0.97 and j + 1 < len(g): jangka = (str(g.index[j + 1].date()), o[j + 1], 'isyarat keluar'); break
                if j - i >= m.TMAX: jangka = (str(g.index[j].date()), c[j], 'masa'); break
            self.assertEqual((p['tarikh_keluar'], p['sebab_keluar']), (jangka[0], jangka[2]), p['saham'] + ' ' + p['tarikh_isyarat'])
            self.assertAlmostEqual(float(p['harga_keluar']), float(jangka[1]), places=3)

    def test_univ_sesi_arkib(self):
        # 22 Okt 2026 (R8): universe sesi terkini diarkib; bina semula memakai arkib, bukan universe semasa
        with tempfile.TemporaryDirectory() as d:
            lama = lejar.UNIV_ARKIB; lejar.UNIV_ARKIB = d
            try:
                self.assertEqual(lejar.univ_sesi('2026-10-20', {'AAA', 'BBB'}, False), {'AAA', 'BBB'})
                self.assertFalse(os.listdir(d))                                   # sesi lama: tidak diarkib
                lejar.univ_sesi('2026-10-21', {'AAA', 'BBB'}, True)
                self.assertEqual(lejar.univ_sesi('2026-10-21', {'CCC'}, True), {'AAA', 'BBB'})
                self.assertIsNone(lejar.univ_sesi('2026-10-22', None, True))
            finally:
                lejar.UNIV_ARKIB = lama

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


class UjiDuaLorong(unittest.TestCase):
    def setUp(self):
        self._dua = lejar.DUA_LORONG; lejar.DUA_LORONG = True

    def tearDown(self):
        lejar.DUA_LORONG = self._dua

    def test_lorong1_sama_enjin_dan_lorong2_tidak_menyekat(self):
        # sejak 19 Okt 2026 hanya lorong 1 menyekat isyarat baharu kaedah+saham sama, jadi dagangan lorong 1 lejar = enjin.trades
        # walaupun posisi kekal terbuka dalam lorong 2
        m = modul('M9004'); fr, idx = data(benih=5)
        E = enjin_trades(m, fr, idx)
        T, W, tutup, langkau = jalan_lejar('M9004', fr, idx)
        semua = tutup + T
        self.assertGreater(len(semua), 5)
        # setiap posisi tutup: kedua-dua lorong keluar, tarikh lorong >= tarikh beli
        for r in tutup:
            self.assertTrue(r['tutup_semua'])
            for c in ('tarikh_keluar', 'tarikh_keluar_henti'):
                self.assertGreaterEqual(r[c], r['tarikh_beli'])
        L = sorted((r['saham'], r['tarikh_isyarat'], r['tarikh_beli'], r.get('tarikh_keluar') or '') for r in semua)
        J = sorted((t, str(s.date()), str(e.date()), '' if w == 'hujung' else str(x.date()))
                   for t, s, e, x, w in zip(E.ticker, E.sig, E.ent, E.ex, E.why))
        self.assertEqual(L, J)
        # lorong 1 tidak bertindih: belian baharu hanya selepas hari lorong 1 posisi sebelumnya keluar
        by = {}
        for r in semua: by.setdefault(r['saham'], []).append(r)
        bertindih = 0
        for t, a in by.items():
            a.sort(key=lambda r: r['tarikh_beli'])
            for x, y in zip(a, a[1:]):
                self.assertTrue(x.get('tarikh_keluar')); self.assertGreater(y['tarikh_isyarat'], x['tarikh_keluar'])
                bertindih += not lejar.tarikh_tutup(x) or lejar.tarikh_tutup(x) >= y['tarikh_isyarat']
        self.assertGreater(bertindih, 0)        # posisi lorong 2 lama masih terbuka ketika belian baharu

    def test_bina_semula_apabila_peraturan_lorong2_berubah(self):
        # keluar_lorong.VERSI lain daripada status.json `lorong2` -> lejar dikosongkan dan diproses semula dari sesi mula
        modul('M9005'); fr, idx = data(n=300, benih=9)
        with tempfile.TemporaryDirectory() as d:
            stor = os.path.join(d, 'stor'); os.makedirs(stor)
            for nama, x in (('harga_A.csv', fr), ('harga_idx.csv', idx)):
                pd.concat([g.assign(ticker=t, date=g.index.strftime('%Y%m%d').astype(int)) for t, g in x.items()])[lejar.LAJ] \
                    .to_csv(os.path.join(stor, nama), index=False)
            lama = lejar.STOR, lejar.LEJAR
            lejar.STOR, lejar.LEJAR = stor, os.path.join(d, 'lejar')
            os.environ['LEJAR_UNIV'] = os.path.join(d, 'tiada.txt')
            try:
                a = argparse.Namespace(mula=str(MULA.date()), hingga=None, proses=1, hanya='M9005', paksa=False)
                lejar.cmd_jalan(a)
                kunci = lambda: sorted(map(tuple, pd.concat(lejar.semua_posisi())[
                    ['saham', 'tarikh_beli', 'tarikh_keluar', 'keluar_henti', 'tarikh_keluar_henti']].astype(str).values))
                asal = kunci(); self.assertGreater(len(asal), 5)
                p = os.path.join(d, 'lejar', 'status.json'); st = json.load(open(p))
                self.assertEqual(st['lorong2'], lejar.keluar_lorong.VERSI)
                # keadaan peraturan lama: versi lain dan satu posisi terbuka hilang (tanpa bina semula, tiada sesi baharu diproses)
                st['lorong2'] = 'lama'; json.dump(st, open(p, 'w'))
                f = os.path.join(d, 'lejar', 'terbuka.csv'); O = pd.read_csv(f, dtype=str, keep_default_na=False)
                O.iloc[1:].to_csv(f, index=False)
                lejar.cmd_jalan(argparse.Namespace(mula=None, hingga=None, proses=1, hanya='M9005', paksa=False))
                st = json.load(open(p))
                self.assertEqual((st['lorong2'], st['bina_semula'][-1]['dari'], st['mula']),
                                 (lejar.keluar_lorong.VERSI, 'lama', str(MULA.date())))
                self.assertEqual(kunci(), asal)
                with self.assertRaises(SystemExit) as cm:
                    lejar.cmd_semak(argparse.Namespace())
                self.assertEqual(cm.exception.code, 0)
            finally:
                lejar.STOR, lejar.LEJAR = lama; os.environ.pop('LEJAR_UNIV', None)


if __name__ == '__main__':
    unittest.main()


class UjiLiputan(unittest.TestCase):
    def test_sesi_data_tidak_lengkap_ditangguh(self):
        modul('M9001'); fr, idx = data(n=300)
        akhir = idx['SPY'].index[-1]
        fr['AAA'] = fr['AAA'][fr['AAA'].index < akhir]          # 1/4 saham tiada bar sesi terakhir
        with tempfile.TemporaryDirectory() as d:
            stor = os.path.join(d, 'stor'); os.makedirs(stor)
            pd.concat([g.assign(ticker=t, date=g.index.strftime('%Y%m%d').astype(int)) for t, g in fr.items()])[lejar.LAJ] \
                .to_csv(os.path.join(stor, 'harga_A.csv'), index=False)
            pd.concat([g.assign(ticker=t, date=g.index.strftime('%Y%m%d').astype(int)) for t, g in idx.items()])[lejar.LAJ] \
                .to_csv(os.path.join(stor, 'harga_idx.csv'), index=False)
            lama = lejar.STOR, lejar.LEJAR
            lejar.STOR, lejar.LEJAR = stor, os.path.join(d, 'lejar')
            os.environ['LEJAR_UNIV'] = os.path.join(d, 'tiada.txt')
            try:
                a = argparse.Namespace(mula=str(MULA.date()), hingga=None, proses=1, hanya='M9001', paksa=False)
                lejar.cmd_jalan(a)
                st = json.load(open(os.path.join(d, 'lejar', 'status.json')))
                self.assertLess(pd.Timestamp(st['sesi_terakhir']), akhir)
                a.paksa = True; lejar.cmd_jalan(a)
                st = json.load(open(os.path.join(d, 'lejar', 'status.json')))
                self.assertEqual(pd.Timestamp(st['sesi_terakhir']), akhir)
            finally:
                lejar.STOR, lejar.LEJAR = lama; os.environ.pop('LEJAR_UNIV', None)

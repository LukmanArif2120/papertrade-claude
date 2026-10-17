# Ujian standard/harian_c.py (Papertrade C harian tanpa LLM): gelung keluar = enjin.trades v1.2; peraturan imbasan
# (had 10 sekaedah, calon watchlist di luar had, isyarat mingguan, posisi terbuka dikecualikan); peraturan langkau beli.
import csv, os, sys, tempfile, types, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import harian_c as H, enjin, sahkan as SH


def data(n=300, saham=('AAA', 'BBB', 'CCC'), benih=3):
    rng = np.random.default_rng(benih); ix = pd.bdate_range('2025-01-02', periods=n); fr = {}
    for t in saham:
        c = 40 * np.exp(np.cumsum(rng.normal(0.0005, 0.02, n))); o = c * np.exp(rng.normal(0, 0.01, n))
        h = np.maximum(o, c) * (1 + rng.uniform(0, 0.02, n)); l = np.minimum(o, c) * (1 - rng.uniform(0, 0.02, n))
        fr[t] = pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=1e6), index=ix)
    return fr


def sedia_uji(fr, idx):
    for g in fr.values():
        c = g.close; ma = c.rolling(10).mean()
        g['sig'] = ((c > ma) & (c.shift() <= ma.shift())).fillna(False)
        g['stop'] = g.low.rolling(5).min() * 0.97; g['tgt'] = c * 1.06; g['exitc'] = (c < ma * 0.98).fillna(False)
        g['rank'] = c / c.shift(20) - 1


class TestKeluar(unittest.TestCase):
    def test_sama_dengan_enjin(self):
        """Setiap dagangan enjin.trades (tmax 12): nilai_keluar dari bar isyarat memberi tarikh & harga keluar yang sama."""
        fr = data(); sedia_uji(fr, {})
        T = enjin.trades({t: g.copy() for t, g in fr.items()}, tmax=12, warm=30)
        self.assertGreater(len(T), 20)
        n = 0
        for _, d in T.iterrows():
            g = fr[d.ticker]; i = g.index.get_loc(d.sig)
            x = H.nilai_keluar(g, i, 12)
            if d.ex == g.index[-1] and d.why == 'hujung':
                continue
            self.assertIsNotNone(x); self.assertIn('t', x, d)
            self.assertEqual(x['t'], str(d.ex.date()), d)
            e = g.open.iloc[i + 1]
            self.assertAlmostEqual(x['p'] / e * (1 - enjin.COST) / (1 + enjin.COST) - 1, d.ret, places=9)
            n += 1
        self.assertGreater(n, 15)

    def test_menunggu(self):
        fr = data(n=80); g = fr['AAA']; sedia_uji(fr, {})
        g['stop'] = 0.0; g['tgt'] = np.nan; g['exitc'] = False; g.iloc[-1, g.columns.get_loc('exitc')] = True
        self.assertEqual(H.nilai_keluar(g, 40, 0), {'menunggu': str(g.index[-1].date())})


class TestImbas(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        ix = pd.bdate_range('2026-09-01', '2026-10-15')
        H.FR = {}; H.IDX = {'SPY': pd.DataFrame(dict(open=1.0, high=1.0, low=1.0, close=1.0, volume=1.0), index=ix)}
        with open(os.path.join(self.d, 'claude.csv'), 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'keluar', 'tutup_semua', 'tidak_dibeli', 'tidak_sah'])
            w.writerow(['2026-10-01', 'T00', 'M01', '10', 'False', 'False', '', ''])      # terbuka -> dikecualikan
            w.writerow(['2026-09-01', 'T01', 'M01', '10', 'True', 'True', '', ''])        # tutup -> belian ke-2
        with open(os.path.join(self.d, 'watchlist.csv'), 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['Saham', 'Kaedah', 'Tarikh masuk watchlist']); w.writerow(['T14', 'M01', '2026-10-13'])

    def hasil(self, mid, n):
        return {mid: dict(isyarat=[dict(saham=f'T{k:02d}', rank=float(n - k), henti=9.0, sasaran=12.0, tutup=10.0,
                                        sumber='lain', buka_maks=None) for k in range(n)], hampir=[])}

    def test_had_dan_watchlist(self):
        rk = {}
        H.imbas(self.d, '2026-10-15', self.hasil('M01', 15), pd.Timestamp('2026-10-15 20:00', tz='Asia/Kuala_Lumpur'), rk, None)
        _, rows = SH.baca(os.path.join(self.d, 'senarai_beli.csv'))
        t = {r['saham']: r for r in rows}
        self.assertNotIn('T00', t)                                   # posisi terbuka kaedah sama
        self.assertEqual(sum(r['asal'] == 'isyarat' for r in rows), 10)   # T01–T10 (rank tertinggi)
        self.assertEqual(t['T14']['asal'], 'watchlist')              # calon watchlist yang lengkap, di luar 10 teratas
        self.assertEqual(len(rows), 11)
        self.assertEqual(t['T01']['belian_ke'], '2')
        self.assertEqual(rk['ditolak'], {'dipegang': 1, 'had': 3})

    def test_watchlist_dalam_had(self):
        """Calon watchlist dalam 10 teratas dikira dalam had (tidak menambah baris)."""
        with open(os.path.join(self.d, 'watchlist.csv'), 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['Saham', 'Kaedah', 'Tarikh masuk watchlist']); w.writerow(['T02', 'M01', '2026-10-13'])
        rk = {}
        H.imbas(self.d, '2026-10-15', self.hasil('M01', 15), pd.Timestamp('2026-10-15 20:00', tz='Asia/Kuala_Lumpur'), rk, None)
        _, rows = SH.baca(os.path.join(self.d, 'senarai_beli.csv'))
        self.assertEqual(len(rows), 10); self.assertEqual({r['saham']: r['asal'] for r in rows}['T02'], 'watchlist')

    def test_mingguan(self):
        rk = {}   # 15 Okt 2026 = Khamis: isyarat mingguan ditolak
        H.imbas(self.d, '2026-10-15', self.hasil('M52', 3), pd.Timestamp('2026-10-15 20:00', tz='Asia/Kuala_Lumpur'), rk, None)
        self.assertEqual(rk['senarai_beli'], 0); self.assertEqual(rk['ditolak'].get('mingguan'), 3)
        self.assertFalse(H.akhir_minggu('2026-10-15')); self.assertTrue(H.akhir_minggu('2026-10-16'))


class TestBeli(unittest.TestCase):
    def test_langkau_dan_rekod(self):
        d = tempfile.mkdtemp(); stor = os.path.join(d, 'stor'); os.makedirs(stor)
        ix = pd.bdate_range('2026-08-03', '2026-10-15')
        rows = [(t, int(x.strftime('%Y%m%d')), 10, 10.5, 9.5, 10, 1e6) for t in ('AAA', 'BBB', 'CCC') for x in ix]
        pd.DataFrame(rows, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']).to_csv(os.path.join(stor, 'harga_B.csv'), index=False)
        pd.DataFrame([('SPY',) + r[1:] for r in rows if r[0] == 'AAA'], columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']).to_csv(
            os.path.join(stor, 'harga_idx.csv'), index=False)
        lajur = H.SENARAI_LAJUR
        with open(os.path.join(d, 'senarai_beli.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
            for t, henti, bmax in (('AAA', 9.0, ''), ('BBB', 10.6, ''), ('CCC', 9.0, 10.2)):
                w.writerow(dict(saham=t, kaedah='M99X', sektor='S', industri='I', pct_dipenuhi=100, harga_rujukan=10, henti=henti,
                                buka_maks=bmax, sasaran='', tarikh_isyarat='2026-10-15', tarikh_imbasan='2026-10-16', belian_ke=1))
        with open(os.path.join(d, 'claude.csv'), 'w', newline='') as f:
            csv.writer(f).writerow(SH.POSISI)
        buka = os.path.join(d, 'buka.csv')
        pd.DataFrame(dict(ticker=['AAA', 'BBB', 'CCC'], open=[10.4, 10.4, 10.4], volume=[1e5] * 3)).to_csv(buka, index=False)
        H.main(['beli', '--folder', d, '--stor', stor, '--tarikh', '2026-10-16', '--buka', buka, '--masa', '2026-10-16 21:40'])
        _, r = SH.baca(os.path.join(d, 'claude.csv'))
        self.assertEqual([x['saham'] for x in r], ['AAA'])           # BBB: buka <= henti; CCC: buka > buka_maks
        self.assertEqual(r[0]['harga_beli'], '10.4'); self.assertEqual(r[0]['sumber'], 'harian_c')
        st = H.status_baca(d)['beli']; self.assertEqual((st['direkod'], st['dilangkau']), (1, 2))
        # larian kedua hari sama: dilangkau (idempoten)
        H.main(['beli', '--folder', d, '--stor', stor, '--tarikh', '2026-10-16', '--buka', buka])
        self.assertEqual(len(SH.baca(os.path.join(d, 'claude.csv'))[1]), 1)


if __name__ == '__main__':
    unittest.main()

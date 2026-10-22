# Ujian kod/dagangan.py (22 Okt 2026, R10): lajur kaedah replika bagi dagangan sendiri — sama dengan enjin bagi dagangan replika,
# bendera dagangan sendiri bagi isyarat yang jatuh semasa replika memegang dagangan lain, dan pembetulan posisi Papertrade C.
import csv, os, sys, tempfile, types, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import dagangan as D  # noqa: E402
import enjin  # noqa: E402
import harian_c as H  # noqa: E402

IX = pd.bdate_range('2025-01-02', periods=160)


def modul(nama):
    """Isyarat berterusan (tutup > MA5); keluar replika: tutup < 0.97 x buka masuk (perlu bar esok) atau had masa 15."""
    m = types.ModuleType(f'kaedah.{nama}'); m.ID = nama; m.NAMA = 'Ujian'; m.VARIAN = 'x'; m.TMAX = 15; m.PERLU_BAR = 60
    m.SILANG = False; m.WARM = 30

    def _replika(g, warm=m.WARM):
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
    m._replika = _replika

    def sedia(fr, idx):
        for g in fr.values():
            c = g.close
            g['sig'] = (c > c.rolling(5).mean()).fillna(False); g['stop'] = np.nan; g['tgt'] = np.nan; g['rank'] = 0.0
            g['exitc'] = _replika(g)          # lalai `warm` (diikat semasa def) — sedia_dagangan menukarnya juga
    m.sedia = sedia
    sys.modules[f'kaedah.{nama}'] = m
    return m


def harga(benih=4, n=160):
    r = np.random.default_rng(benih); c = 50 * np.exp(np.cumsum(r.normal(0.001, 0.02, n))); o = c * np.exp(r.normal(0, 0.01, n))
    return pd.DataFrame(dict(open=o, high=np.maximum(o, c) * 1.01, low=np.minimum(o, c) * 0.99, close=c, volume=1e6), index=IX[:n])


def jangka(g, i, tmax=15):
    e = g.open.iloc[i + 1]
    for j in range(i + 1, len(g)):
        if g.close.iloc[j] < e * 0.97 and j + 1 < len(g): return str(g.index[j + 1].date())
        if j - i >= tmax: return str(g.index[j].date())
    return None


class TestDagangan(unittest.TestCase):
    def setUp(self):
        self.m = modul('M9010'); D.REPLIKA.add('M9010')
        self.idx = {'SPY': harga(1)}

    def tearDown(self):
        D.REPLIKA.discard('M9010')

    def test_sama_enjin_dan_dagangan_sendiri(self):
        g = harga()
        f = {'X': g.copy()}; self.m.sedia(f, self.idx); f['X'] = enjin.siap(f['X'])
        E = enjin.trades({'X': f['X'].copy()}, self.m.TMAX, self.m.WARM)
        mula = {str(s.date()) for s in E.sig}
        self.assertGreater(len(E), 3)
        for s, x in zip(E.sig, E.ex):          # dagangan replika: sama dengan enjin
            gd = D.sedia_dagangan(self.m, 'X', g, self.idx, s)
            r = H.nilai_keluar(gd, gd.index.get_loc(s), self.m.TMAX)
            if r and r.get('t'):
                self.assertEqual(r['t'], str(x.date()))
        sig = f['X'].sig.values; n_luar = 0
        for i in np.flatnonzero(sig):           # isyarat semasa replika memegang dagangan lain: keluar dagangan sendiri
            if i < self.m.WARM or i + 1 >= len(g) or str(g.index[i].date()) in mula:
                continue
            gd = D.sedia_dagangan(self.m, 'X', g, self.idx, g.index[i])
            r = H.nilai_keluar(gd, i, self.m.TMAX)
            self.assertEqual((r or {}).get('t'), jangka(g, i)); n_luar += 1
        self.assertGreater(n_luar, 5)
        self.assertEqual(self.m.WARM, 30)        # dipulihkan
        self.assertEqual(self.m._replika.__defaults__, (30,))

    def test_bar_akhir_bendera_keluar(self):
        g = harga()
        for k in range(60, 150):
            gs = g.iloc[:k]
            f = {'X': gs.copy()}; self.m.sedia(f, self.idx); s = f['X'].sig.values
            i = int(np.flatnonzero(s[:k - 2])[-1]) if s[:k - 2].any() else None
            if i is None or i < self.m.WARM: continue
            gd = D.sedia_dagangan(self.m, 'X', gs, self.idx, gs.index[i])
            e = gs.open.iloc[i + 1]
            if gs.close.iloc[-1] < e * 0.97 and not (gs.close.iloc[i + 1:-1] < e * 0.97).any() and k - 1 - i < self.m.TMAX:
                self.assertTrue(bool(gd.exitc.iloc[-1]))   # bendera bar akhir diketahui (bar sementara)
                return
        self.skipTest('tiada kes bar akhir')

    def test_betul_c(self):
        g = harga()
        f = {'X': g.copy()}; self.m.sedia(f, self.idx)
        E = enjin.trades({'X': enjin.siap(f['X']).copy()}, self.m.TMAX, self.m.WARM)
        mula = {str(s.date()) for s in E.sig}
        i = next(i for i in np.flatnonzero(f['X'].sig.values) if i >= self.m.WARM and str(g.index[i].date()) not in mula
                 and i + 20 < len(g) and jangka(g, i))
        betul = jangka(g, i)
        salah = str(g.index[i + 2].date()) if str(g.index[i + 2].date()) != betul else str(g.index[i + 3].date())
        lajur = ['tarikh_beli', 'saham', 'kaedah', 'id_kaedah', 'harga_beli', 'harga_terkini', 'untung_pct', 'hari', 'henti', 'sasaran',
                 'isyarat_keluar', 'keluar', 'tarikh_keluar', 'harga_keluar', 'untung_akhir_pct', 'sumber', 'tarikh_isyarat', 'nota',
                 'tidak_sah', 'tidak_dibeli', 'keluar_henti', 'tutup_semua']
        r0 = dict(tarikh_beli=str(g.index[i + 1].date()), saham='X', kaedah='M9010', id_kaedah='M9010', harga_beli=f'{g.open.iloc[i + 1]:.4f}',
                  keluar='True', tarikh_keluar=salah, harga_keluar='1', untung_akhir_pct='-1', sumber='harian_c',
                  tarikh_isyarat=str(g.index[i].date()), keluar_henti='True', tutup_semua='True', nota='buka rasmi')
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_5.csv')
            with open(p, 'w', newline='') as fh:
                w = csv.DictWriter(fh, lajur); w.writeheader(); w.writerow({k: r0.get(k, '') for k in lajur})
            x = D.betul_c(d, {'X': g}, self.idx)
            self.assertEqual([(y[4], y[5]) for y in x], [(salah, betul)])
            with open(p) as fh:
                r = list(csv.DictReader(fh))[0]
            self.assertEqual((r['keluar'], r['tarikh_keluar'], r['tutup_semua']), ('True', betul, 'True'))
            self.assertIn('dagangan sendiri', r['nota'])
            self.assertEqual(D.betul_c(d, {'X': g}, self.idx), [])


if __name__ == '__main__':
    unittest.main()

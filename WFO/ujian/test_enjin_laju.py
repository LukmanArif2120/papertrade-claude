# Ujian kesetaraan enjin_laju lawan enjin v1.2 (subset kecil saham supaya pantas).
# Pengesahan penuh semua kaedah: WFO/kod/sahkan_enjin.py → WFO/laporan/ENJIN_LAJU_SAHKAN.md
import os, sys, random, unittest, warnings, importlib
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'BacktestShariah2', 'kod'))
import wfo, enjin, enjin_laju as L
from sahkan_enjin import sama_T, sama_cv

TK = ['ADSK', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'ANET', 'COST', 'AVGO', 'SHOP', 'TRI', 'PODD', 'SEDG', 'GNRC', 'DOCU', 'DXCM', 'IOVA']


class UjiEnjinLaju(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore')
        fr, cls.idx, _ = wfo.muat_data()
        cls.fr = {t: fr[t] for t in TK if t in fr}

    def _banding(self, mid, cfgs):
        m = importlib.import_module(mid)
        f = wfo.salin(self.fr); m.sedia(f, self.idx); f = {t: enjin.siap(g) for t, g in f.items()}
        for s, e, x in cfgs:
            h = f if s == 'ASAL' and e == 'ASAL' else {
                t: g.assign(stop=wfo.lajur_stop(g, s, g.stop), exitc=wfo.lajur_exit(g, e, g.exitc, g.tgt)[0],
                            tgt=wfo.lajur_exit(g, e, g.exitc, g.tgt)[1]) for t, g in f.items()}
            A = enjin.trades(h, x or None, m.WARM); B = L.trades_laju(h, x or None, m.WARM)
            ok, why = sama_T(A, B); self.assertTrue(ok, f'{mid} {s}/{e}/{x}: {why}')
            if len(A): self.assertTrue(sama_cv(enjin.portfolio(A, f), L.portfolio_laju(B, f)), f'{mid} {s}/{e}/{x} portfolio')

    def test_M96_merentas_saham(self):
        self._banding('M96', [('ASAL', 'ASAL', 0), ('ASAL', 'SMA50', 10), ('ATR1.5', 'CHAN3', 63)])

    def test_M37(self):
        self._banding('M37', [('ASAL', 'ASAL', 0), ('PCT8', 'CHAN3', 42), ('LOW5', 'TIADA', 21)])

    def test_jumlah_seperti_sum_python(self):
        rng = random.Random(7)
        for _ in range(3000):
            n = rng.randint(0, 8); v = []; isn = []
            for _ in range(n):
                x = rng.uniform(-1, 1) * 10 ** rng.randint(-3, 16); k = rng.random() < 0.4
                v.append(np.float64(x) if k else float(x)); isn.append(k)
            py = sum(v); nb, nbn = L._jumlah_py(np.array(v, float), np.array(isn, bool), n)
            self.assertEqual(py, nb)
            if n: self.assertEqual(type(py) is np.float64, nbn)


if __name__ == '__main__':
    unittest.main()

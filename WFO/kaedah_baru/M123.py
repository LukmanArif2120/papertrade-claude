from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M123'
NAMA = 'CCI Correction (Lambert, ChartSchool)'
VARIAN = 'V0 Katalog K156 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 200
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K156. Bias mingguan dikira atas minggu LENGKAP sebelumnya (CCI20 mingguan > +100 hidupkan, < −100 matikan). Isyarat: CCI20 harian pernah < −100 sejak kali terakhir di atas 0, kemudian silang atas 0. Exit asal (andaian katalog): CCI harian silang bawah +100. Tiada henti asal.

def sedia(fr, idx):
    for g in fr.values():
        wk = g.index.to_period('W-FRI')
        w = g.groupby(wk).agg(high=('high', 'max'), low=('low', 'min'), close=('close', 'last'))
        cw = cci(w.high, w.low, w.close, 20).values; b = np.zeros(len(cw), bool); st = False
        for j, v in enumerate(cw):
            if v > 100: st = True
            elif v < -100: st = False
            b[j] = st
        bias_w = pd.Series(b, w.index)
        bias = pd.Series(wk.map(lambda p: bias_w.get(p - 1, False)), g.index).astype(bool)
        cd = cci(g.high, g.low, g.close, 20).values; n = len(g); turun = False; sg = np.zeros(n, bool)
        for i in range(1, n):
            if cd[i] < -100: turun = True
            if turun and cd[i] > 0 and cd[i - 1] <= 0:
                sg[i] = True; turun = False
            elif cd[i] > 0: turun = False
        cds = pd.Series(cd, g.index)
        siap_lajur(g, pd.Series(sg, g.index) & bias, pd.Series(np.nan, g.index), exitc=(cds < 100) & (cds.shift() >= 100))

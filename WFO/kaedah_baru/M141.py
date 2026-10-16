from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M141'
NAMA = "First Thrust (Landry)"
VARIAN = 'V0 Katalog K256 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K256. KABUR ("utama"/"tajam" tidak ditakrif). Andaian: low utama = low terendah 60 hari, berlaku dalam 15 bar lepas; rali tajam = high sejak low >= low + 3 x ATR14; undur pertama = bar pertama high < high semalam selepas low; pencetus esok tutup > high bar undur. Henti low bar undur.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; a = atr(g).values; n = len(g)
        lo60 = g.low.rolling(60).min().values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); t = -1; dipakai = -1
        for i in range(61, n):
            if l[i] <= lo60[i]: t = i
            if t < 0 or i - t > 15: continue
            k = i - 1                                    # bar undur calon
            if k <= t + 1 or t == dipakai: continue
            pertama = h[k] < h[k - 1] and all(h[j] >= h[j - 1] for j in range(t + 1, k))
            if pertama and h[t:k].max() >= l[t] + 3 * a[k] and c[i] > h[k]:
                sig[i] = True; stop[i] = l[k]; dipakai = t
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)

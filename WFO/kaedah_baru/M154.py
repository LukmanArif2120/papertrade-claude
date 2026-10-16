from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M154'
NAMA = "HOLP (High of Low Period)"
VARIAN = 'V0 Katalog K305 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K305. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. Pembetulan 20 bar: bar low terendah 20 bar (k); pencetus tutup pertama > high bar k (tiada tutup > high k antara k dan semalam). Henti = low bar k.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(21, n):
            if not naik[i]: continue
            k = i - 20 + int(np.argmin(l[i - 20:i]))
            if c[i] > h[k] and (k + 1 > i - 1 or c[k + 1:i].max() <= h[k]):
                sig[i] = True; stop[i] = l[k]
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)

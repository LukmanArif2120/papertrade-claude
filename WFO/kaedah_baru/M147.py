from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M147'
NAMA = "Improved Three-Bar Pullback"
VARIAN = 'V0 Katalog K288 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K288. TRIX(9) > isyarat EMA3 pada bar ke-3; 3 tutup menurun berturut; pencetus esok tutup > high bar ke-3. Henti low bar ke-3 (andaian).

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        t = trix(c, 9); s = ema(t, 3)
        tiga = (c < c.shift()) & (c.shift() < c.shift(2)) & (c.shift(2) < c.shift(3)) & (t > s)
        stop = l.shift(1)
        sig = tiga.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

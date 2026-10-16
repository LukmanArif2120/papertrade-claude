from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M158'
NAMA = "Doubly Adaptive Profit Targets"
VARIAN = 'V0 Katalog K379 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K379. Hari A: tutup > SMA50 dan ADX14 naik. Hari B: buka > high A dan low <= high A (beli had di high A terisi). Isyarat pada tutup B, masuk buka esok (proksi). Henti = tutup − 4 x ATR20. Sasaran ATR tidak dimodelkan. Exit asal: tutup < SMA50.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); ax = adx(g, 14)
        A = (c > s50) & (ax > ax.shift())
        sig = A.shift(1, fill_value=False) & (o > h.shift(1)) & (l <= h.shift(1))
        stop = c - 4 * atr(g, 20)
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < s50)

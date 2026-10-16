from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M127'
NAMA = "Slingshot Bullish"
VARIAN = 'V0 Katalog K177 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K177. 2 bulan = 42 hari. Hari A: high 42 hari; hari B: low < low hari A; pencetus hari C tutup > high hari A. Henti "2 mata" ditukar kepada low hari B (andaian). Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        A = h >= h.rolling(42).max()
        sig = A.shift(2, fill_value=False) & (l.shift(1) < l.shift(2)) & (c > h.shift(2))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop)

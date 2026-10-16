from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M125'
NAMA = "2-Bar Breakout"
VARIAN = 'V0 Katalog K163 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 30
ADA_HENTI = True
SILANG = False
PERLU_BAR = 30
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K163. Henti = low semalam (katalog). Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        sig = (h.shift(1) > pd.concat([h.shift(2), h.shift(3)], axis=1).max(axis=1)) & (c > c.shift(1))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop)

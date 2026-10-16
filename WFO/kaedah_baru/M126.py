from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M126'
NAMA = "Hidden Smash Day (beli, Larry Williams)"
VARIAN = 'V0 Katalog K164 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K164. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. "High baharu" = high tertinggi 20 hari (andaian). Hari smash: tutup dalam 25% bawah julat. Pencetus esok tutup > high hari smash; henti low hari smash.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20))
        pos = ((c - l) / (h - l)).where(h > l)
        smash = naik & (h >= h.rolling(20).max()) & (pos <= 0.25)
        stop = l.shift(1)
        sig = smash.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

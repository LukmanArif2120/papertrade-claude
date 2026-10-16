from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M119'
NAMA = '180 Bullish (Cooper)'
VARIAN = 'V0 Katalog K151 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K151. Henti "1 mata" ditukar kepada low bar persediaan (andaian). Pencetus esok tutup > high bar persediaan. Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        pos = ((c - l) / (h - l)).where(h > l)
        persediaan = (pos.shift() <= 0.25) & (pos >= 0.75) & (c > sma(c, 10)) & (c > sma(c, 50))
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

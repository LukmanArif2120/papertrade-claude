from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M120'
NAMA = 'Reversal New Highs'
VARIAN = 'V0 Katalog K152 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 70
ADA_HENTI = True
SILANG = False
PERLU_BAR = 70
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K152. Henti "1 mata" ditukar kepada low hari luar (andaian). Pencetus esok tutup > high hari luar. Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        rng = h - l
        luar = (l < l.shift()) & (h > h.shift())
        persediaan = (c > 30) & luar & (rng >= rng.rolling(5).max()) & (h >= h.rolling(60).max())
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

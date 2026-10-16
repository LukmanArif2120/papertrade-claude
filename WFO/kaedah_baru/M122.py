from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M122'
NAMA = 'Moving Momentum (ChartSchool)'
VARIAN = 'V0 Katalog K155 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 170
ADA_HENTI = False
SILANG = False
PERLU_BAR = 170
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K155. Andaian: Stokastik perlahan (14,3) < 20 dalam 10 hari terakhir, kemudian histogram MACD(12,26,9) silang atas 0; SMA20 > SMA150. Exit asal (andaian katalog): SMA20 < SMA150 atau histogram < 0. Tiada henti asal.

def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        k = stoch_k(g, 14, 3); hist = macd_hist(c)
        os_ = (k < 20).astype(float).rolling(10).max() > 0
        tren = sma(c, 20) > sma(c, 150)
        sig = tren & os_ & (hist > 0) & (hist.shift() <= 0)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(~tren) | (hist < 0))

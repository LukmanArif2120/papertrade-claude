from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M134'
NAMA = "First Kiss After Daylight (Landry)"
VARIAN = 'V0 Katalog K200 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K200. Andaian: "low utama baharu" = low terendah 60 hari dalam 60 bar lepas; "daylight" = >= 5 bar berturut low > SMA10; ciuman pertama = bar pertama low <= SMA10 selepas daylight; pencetus tutup > high bar ciuman (katalog: andaian atas high sebelumnya). Henti low bar ciuman. Keluar Landry tidak dimodelkan (WFO).

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        s10 = sma(c, 10)
        atas = l > s10
        run = atas.groupby((~atas).cumsum()).cumsum()
        cium = (l <= s10) & (run.shift(1) >= 5)
        lowu = (l <= l.rolling(60).min()).astype(float).rolling(60).max() > 0
        stop = l.shift(1)
        sig = (cium & lowu).shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

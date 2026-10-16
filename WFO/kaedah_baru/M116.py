from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M116'
NAMA = '2/20 EMA Breakout (Landry)'
VARIAN = 'V0 Katalog K146 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K146. Henti mengekor EMA20 dimodelkan sebagai henti awal = EMA20 hari isyarat + exit tutup < EMA20.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        e20 = ema(c, 20)
        dua = (l > e20) & (l.shift() > e20.shift())
        sig = dua.shift(1, fill_value=False) & (c > pd.concat([h.shift(1), h.shift(2)], axis=1).max(axis=1))
        siap_lajur(g, sig & ~langkau(g, e20), e20, exitc=c < e20)

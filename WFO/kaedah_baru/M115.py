from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M115'
NAMA = 'Bow Tie (Landry)'
VARIAN = 'V0 Katalog K145 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K145. Andaian: "berkipas dalam 3–5 bar" = susunan SMA10>EMA20>EMA30 baru bermula 3–5 bar sebelum bar undur; undur = tutup & high < semalam; pencetus tutup > high bar undur.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        susun = (sma(c, 10) > ema(c, 20)) & (ema(c, 20) > ema(c, 30))
        run = susun.groupby((~susun).cumsum()).cumsum()           # bar berturut tersusun
        naik = c > c.shift()
        undur = (c < c.shift()) & (h < h.shift())
        persediaan = susun & undur & naik.shift(1, fill_value=False) & naik.shift(2, fill_value=False) & run.shift(1).between(3, 5)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1)) & susun
        siap_lajur(g, sig & ~langkau(g, stop), stop)

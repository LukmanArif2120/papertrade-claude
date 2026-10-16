from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M139'
NAMA = "均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik)"
VARIAN = 'V0 Katalog K225 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K225. Himpun = (maks - min SMA5/10/20) <= 0.5 x ATR14 pada bar sebelumnya; "kali pertama" (andaian) = tiada himpun dalam 20 bar sebelum itu; pencetus tutup > MA tertinggi. Saiz kecil jika MA60 menurun — tidak dimodelkan. Henti = low bar pencetus (andaian).

def sedia(fr, idx):
    for g in fr.values():
        c, l = g.close, g.low
        m = pd.concat([sma(c, 5), sma(c, 10), sma(c, 20)], axis=1)
        himpun = (m.max(axis=1) - m.min(axis=1)) <= 0.5 * atr(g)
        pertama = himpun.shift(1, fill_value=False) & (himpun.shift(2).astype(float).rolling(20).max() == 0)
        sig = pertama & (c > m.max(axis=1))
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop)

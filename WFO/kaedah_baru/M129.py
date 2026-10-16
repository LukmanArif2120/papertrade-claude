from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M129'
NAMA = "Wick Play"
VARIAN = 'V0 Katalog K180 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K180. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. "Saham kuat" = aliran naik. Hari 1: sumbu atas >= 40% julat (andaian). Hari 2: buka dalam sumbu (atas badan, bawah high hari 1) dan low >= atas badan hari 1. Hari 3: tutup > high hari 2 (andaian "atas high"). Henti low hari 2 (andaian). KABUR: ambang sumbu tidak dinyatakan sumber.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20))
        atas = pd.concat([o, c], axis=1).max(axis=1); r = (h - l).where(h > l)
        hari1 = naik & ((h - atas) / r >= 0.40)
        hari2 = hari1.shift(1, fill_value=False) & (o > atas.shift(1)) & (o < h.shift(1)) & (l >= atas.shift(1))
        stop = l.shift(1)
        sig = hari2.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

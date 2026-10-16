from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M133'
NAMA = "Bull Hook (Crabel)"
VARIAN = 'V0 Katalog K196 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K196. Hari hook: buka > high semalam, tutup < tutup semalam, julat < julat semalam. Pencetus esok: tutup > buka esok + Stretch (Stretch = 2 x SMA10 min(H-O, O-L)) — proksi tutup untuk beli henti. Henti = tutup - 6 x ATR20 (katalog: entry - 6 ATR20; tutup sebagai proksi entry). Keluar masa hari ke-n ditala WFO (tmax).

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        r = h - l
        hook = (o > h.shift()) & (c < c.shift()) & (r < r.shift())
        stretch = 2 * sma(pd.concat([h - o, o - l], axis=1).min(axis=1), 10)
        sig = hook.shift(1, fill_value=False) & (c > o + stretch.shift(1))
        stop = c - 6 * atr(g, 20)
        siap_lajur(g, sig & ~langkau(g, stop), stop)

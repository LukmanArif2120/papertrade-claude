from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M153'
NAMA = "Range Leader"
VARIAN = 'V0 Katalog K304 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 30
ADA_HENTI = True
SILANG = False
PERLU_BAR = 30
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K304. Julat > julat semalam dan titik tengah > high semalam; beli buka esok; langkau jika buka esok < titik tengah. Henti low bar. Sasaran 2R / pulang modal tidak dimodelkan.

def sedia(fr, idx):
    for g in fr.values():
        h, l = g.high, g.low
        mid = (h + l) / 2
        sig = ((h - l) > (h - l).shift()) & (mid > h.shift())
        lk = (g.open.shift(-1) < mid).fillna(False)
        siap_lajur(g, sig & ~lk & ~langkau(g, l), l)

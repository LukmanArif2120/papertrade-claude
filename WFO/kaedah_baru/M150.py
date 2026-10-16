from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M150'
NAMA = "Trend Bar Failure (Brooks)"
VARIAN = 'V0 Katalog K297 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K297. EMA20 naik. Bar A: bar aliran turun (tutup < buka, badan > 50% julat). Bar B: low < low A. Pencetus bar selepas B (sah 1 bar): tutup > high A. Henti low B (andaian).

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e = ema(c, 20); r = h - l
        A = (c < o) & ((o - c) > 0.5 * r) & (e > e.shift())
        B = A.shift(1, fill_value=False) & (l < l.shift(1))
        stop = l.shift(1)
        sig = B.shift(1, fill_value=False) & (c > h.shift(2))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

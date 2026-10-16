from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M128'
NAMA = "Inventory Retracement Bar (IRB, Rob Hoffman)"
VARIAN = 'V0 Katalog K179 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K179. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. IRB: buka dan tutup kedua-duanya >= 45% julat di bawah high. Pencetus esok tutup > high IRB; henti low IRB (andaian; katalog tiada henti).

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20)); r = (h - l).where(h > l)
        irb = naik & ((h - o) / r >= 0.45) & ((h - c) / r >= 0.45)
        stop = l.shift(1)
        sig = irb.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

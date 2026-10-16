from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M130'
NAMA = "多方炮 (dua lilin hijau mengapit satu merah)"
VARIAN = 'V0 Katalog K189 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K189. KABUR: sumber tiada ambang angka. Andaian: lilin 1 hijau, badan >= 1.5 x purata badan 20 hari; lilin 2 merah, badan < 0.5 x badan 1, volum < volum 1, low > buka lilin 1; lilin 3 hijau, volum > volum 2, buka <= tutup 2 dan tutup >= buka 2; SMA5 > SMA10 > SMA20. Isyarat pada tutup lilin 3; henti low terendah 3 lilin.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        b = (c - o).abs(); pb = b.rolling(20).mean()
        L1 = (c > o) & (b >= 1.5 * pb)
        L2 = (c < o) & (b < 0.5 * b.shift(1)) & (v < v.shift(1)) & (l > o.shift(1))
        L3 = (c > o) & (v > v.shift(1)) & (o <= c.shift(1)) & (c >= o.shift(1))
        susun = (sma(c, 5) > sma(c, 10)) & (sma(c, 10) > sma(c, 20))
        sig = L1.shift(2, fill_value=False) & L2.shift(1, fill_value=False) & L3 & susun
        stop = l.rolling(3).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop)

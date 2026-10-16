from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M151'
NAMA = "Outside Bar Failure"
VARIAN = 'V0 Katalog K298 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = False
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K298. SMA20 naik. Bar luar bearish O (high > high semalam, low < low semalam, tutup < buka). Selepas low O ditembus, bar bullish pertama U (tutup > buka); pencetus tutup > high U. Batal jika ada bar dengan high < low O, atau selepas 10 bar (andaian). Tiada henti (katalog).

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        s20 = sma(g.close, 20).values
        sig = np.zeros(n, bool); t = -1; lo = np.nan; tembus = False; u = np.nan
        for i in range(21, n):
            if h[i] > h[i - 1] and l[i] < l[i - 1] and c[i] < o[i] and s20[i] > s20[i - 1]:
                t = i; lo = l[i]; tembus = False; u = np.nan; continue
            if t < 0: continue
            if i - t > 10 or h[i] < lo: t = -1; continue
            if not tembus:
                if l[i] < lo: tembus = True
                continue
            if not np.isnan(u) and c[i] > u: sig[i] = True; t = -1; continue
            if c[i] > o[i]: u = h[i]
        siap_lajur(g, pd.Series(sig, g.index), pd.Series(np.nan, g.index))

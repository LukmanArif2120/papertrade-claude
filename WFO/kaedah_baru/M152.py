from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M152'
NAMA = "Spike & Ledge"
VARIAN = 'V0 Katalog K303 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K303. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. Hari lonjakan S: low < low terendah 5 bar sebelumnya ("menduga low") dan tutup dalam 25% atas julat. Para: 4–10 bar selepas S dengan semua low > low S. Pencetus: tutup > tutup tertinggi para. Henti = low terendah para.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        pos = ((g.close - g.low) / (g.high - g.low)).where(g.high > g.low).values
        l5 = g.low.shift(1).rolling(5).min().values
        S = naik & (l < l5) & (pos >= 0.75)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(12, n):
            for k in range(5, 12):
                s = i - k
                if not S[s]: continue
                para = slice(s + 1, i)
                if l[para].min() > l[s] and c[i] > c[para].max():
                    sig[i] = True; stop[i] = l[para].min(); break
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)

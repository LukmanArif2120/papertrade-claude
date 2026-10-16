from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M159'
NAMA = "Heikin-Ashi Trend"
VARIAN = 'V0 Katalog K381 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = False
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K381. Bar HA bullish (tutup HA > buka HA) dengan bayang bawah <= 10% julat HA (andaian "kecil") dan tutup > tutup 5 hari lepas (n=5 andaian); beli buka esok. Exit asal: bar HA bearish pertama. Tiada henti.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        hc = (o + h + l + c) / 4; ho = np.empty(n); ho[0] = (o[0] + c[0]) / 2
        for i in range(1, n): ho[i] = (ho[i - 1] + hc[i - 1]) / 2
        hh = np.maximum(h, np.maximum(ho, hc)); hl = np.minimum(l, np.minimum(ho, hc))
        hcs, hos = pd.Series(hc, g.index), pd.Series(ho, g.index)
        bull = hcs > hos
        bayang = (np.minimum(ho, hc) - hl) <= 0.1 * (hh - hl)
        sig = bull & pd.Series(bayang, g.index) & (g.close > g.close.shift(5))
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=hcs < hos)

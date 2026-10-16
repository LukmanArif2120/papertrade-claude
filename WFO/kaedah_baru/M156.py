from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M156'
NAMA = "Single Penetration (DiNapoli)"
VARIAN = 'V0 Katalog K346 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K346. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. (penapis DMA asal tidak diberi). Tujahan: H = high tertinggi 20 hari (baru dicapai dalam 10 bar), L = low terendah 20 bar sebelum H. Masuk pada sentuhan pertama paras 38.2% (low <= H − 0.382(H−L), tutup > paras 61.8%). Henti = H − 0.618(H−L). Sasaran COP/XOP tidak dimodelkan.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); guna = -1
        for i in range(41, n):
            if not naik[i]: continue
            k = i - 10 + int(np.argmax(h[i - 10:i]))
            if h[k] < h[k - 20:k].max(initial=-np.inf) or k == guna: continue
            L = l[k - 20:k].min(); H = h[k]
            p38, p62 = H - 0.382 * (H - L), H - 0.618 * (H - L)
            if l[k + 1:i].min(initial=np.inf) <= p38: continue        # bukan sentuhan pertama
            if l[i] <= p38 and c[i] > p62:
                sig[i] = True; stop[i] = p62; guna = k
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)

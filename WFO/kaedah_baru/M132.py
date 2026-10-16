from _alat import sma, ema, stoch_k, macd_hist, cci, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M132'
NAMA = "Ascending Scallop (Bulkowski)"
VARIAN = 'V0 Katalog K193 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 120
ADA_HENTI = True
SILANG = False
PERLU_BAR = 120
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K193. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. KABUR: bentuk J dikesan secara angka (andaian): puncak kiri = high tertinggi 60 hari sebelum lembah; lembah = low terendah 40 hari, 5–40 bar selepas puncak; kedalaman 8–35%; pencetus tutup > puncak kiri (puncak kanan lebih tinggi). Henti bawah lembah. Sasaran 62% tidak dimodelkan.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        s50 = sma(g.close, 50); naik = ((g.close > s50) & (s50 > s50.shift(20))).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(100, n):
            if not naik[i]: continue
            w = slice(i - 40, i); t = i - 40 + int(np.argmin(l[w])); lv = l[t]
            if i - t < 3: continue
            a0 = max(0, t - 60); a1 = t - 5
            if a1 <= a0: continue
            pk = a0 + int(np.argmax(h[a0:a1])); pv = h[pk]
            if t - pk > 40: continue
            dalam = (pv - lv) / pv
            if not (0.08 <= dalam <= 0.35): continue
            if c[i] > pv and c[i - 1] <= pv and h[t:i].max() <= pv * 1.02:
                sig[i] = True; stop[i] = lv
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)

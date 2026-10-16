from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M148'
NAMA = "Natural Number Method"
VARIAN = 'V0 Katalog K289 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 200
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K289. Bar persediaan = tutup pertama silang atas WMA180. Nombor bulat (andaian): langkah 1 (<$20), 5 (<$100), 10 (<$500), 50 (selainnya). Paras = nombor bulat seterusnya di atas high bar persediaan; pencetus tutup > paras dalam 20 bar selagi tutup > WMA180. Henti = paras − 1 langkah. Exit asal: tutup < WMA180.

def langkah(p):
    return 1.0 if p < 20 else 5.0 if p < 100 else 10.0 if p < 500 else 50.0

def sedia(fr, idx):
    for g in fr.values():
        h, c = g.high.values, g.close.values; w = wma(g.close, 180).values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); b = -1; lv = st = np.nan
        for i in range(1, n):
            if np.isnan(w[i]) or np.isnan(w[i - 1]): continue
            if c[i] > w[i] and c[i - 1] <= w[i - 1]:
                k = langkah(h[i]); lv = (np.floor(h[i] / k) + 1) * k; st = lv - k; b = i; continue
            if b >= 0:
                if c[i] <= w[i] or i - b > 20: b = -1; continue
                if c[i] > lv: sig[i] = True; stop[i] = st; b = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, exitc=g.close < pd.Series(w, g.index))

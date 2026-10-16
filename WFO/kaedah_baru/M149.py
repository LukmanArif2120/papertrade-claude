from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M149'
NAMA = "3-Step Pullback"
VARIAN = 'V0 Katalog K290 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K290. Keltner: EMA15 ± 2 x ATR15. Tutup > saluran atas; kemudian undur 3–15 bar; dalam undur, susutan dari high tertinggi sejak itu ke low = 20–80% lebar saluran; pencetus bar momentum naik (tutup > buka dan tutup > high semalam; pin bar tidak dimodelkan). Henti = tutup − 2.5 x ATR15. Sasaran 1:1 tidak dimodelkan.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        e = ema(g.close, 15).values; a = atr(g, 15).values
        sig = np.zeros(n, bool); t0 = -1; mx = -np.inf
        for i in range(1, n):
            if np.isnan(a[i]): continue
            if c[i] > e[i] + 2 * a[i]: t0 = i; mx = h[i]; continue
            if t0 < 0: continue
            mx = max(mx, h[i]); k = i - t0
            if k > 15: t0 = -1; continue
            lebar = 4 * a[i]; susut = (mx - min(l[t0 + 1:i + 1])) / lebar
            if k >= 3 and 0.2 <= susut <= 0.8 and c[i] > o[i] and c[i] > h[i - 1]:
                sig[i] = True; t0 = -1
        stop = g.close - 2.5 * atr(g, 15)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop)

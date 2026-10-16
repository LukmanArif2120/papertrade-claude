from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M160'
NAMA = "Measured Move Up"
VARIAN = 'V0 Katalog K395 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K395. KABUR (perlu pengesanan ayunan). Andaian: zigzag 3 x ATR14; kaki pertama A(low)→B(high) disahkan; pembetulan dari B, retracement 30–70% kaki AB, low pembetulan > A; pencetus pusingan naik: tutup > high semalam. Henti low pembetulan. Sasaran kaki kedua tidak dimodelkan.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; a = atr(g).values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        arah = 0; ext = np.nan; A = B = np.nan; lo = np.inf; aktif = False
        for i in range(1, n):
            if np.isnan(a[i]): continue
            if arah >= 0:
                if np.isnan(ext) or h[i] > ext: ext = h[i]
                if ext - l[i] >= 3 * a[i]:
                    B = ext; arah = -1; ext = l[i]; aktif = not np.isnan(A); lo = l[i]
            else:
                if l[i] < ext: ext = l[i]
                if h[i] - ext >= 3 * a[i]: A = ext; arah = 1; ext = h[i]; aktif = False
            if aktif:
                lo = min(lo, l[i]); rt = (B - lo) / (B - A) if B > A else np.nan
                if lo <= A: aktif = False; continue
                if 0.3 <= rt <= 0.7 and c[i] > h[i - 1]:
                    sig[i] = True; stop[i] = lo; aktif = False
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)

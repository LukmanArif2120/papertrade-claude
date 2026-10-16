from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M117'
NAMA = 'Landry Pullback (high 2 bulan)'
VARIAN = 'V0 Katalog K147 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K147. Andaian: 2 bulan = 42 hari; pencetus tutup > high semalam selepas 2–7 bar high menurun dari high 42 hari; henti = low bar pencetus; langkau jika risiko > 4%. Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        hh = h >= h.rolling(42).max()
        lh = h < h.shift()
        L = lh.groupby((~lh).cumsum()).cumsum().astype(int)       # panjang larian high menurun
        Lp = L.shift(1).fillna(0).astype(int).values
        hhv = hh.values; n = len(g); puncak = np.zeros(n, bool)
        for i in range(n):
            p = i - 1 - Lp[i]
            if 2 <= Lp[i] <= 7 and p >= 0: puncak[i] = hhv[p]
        stop = l
        sig = pd.Series(puncak, g.index) & (c > h.shift(1)) & ((c - l) / c <= 0.04)
        siap_lajur(g, sig & ~langkau(g, stop), stop)

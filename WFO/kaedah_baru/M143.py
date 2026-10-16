from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M143'
NAMA = "장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang)"
VARIAN = 'V0 Katalog K266 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K266. Diuji tanpa pemangkin berita (saringan). Andaian: mendatar = julat 20 hari sebelumnya <= 15%; lilin naik panjang = tutup >= 7% atas tutup semalam, tutup > buka, volum >= 2 x purata 20 hari. Beli pada sentuhan pertama MA5 dalam 10 bar (low <= SMA5 dan tutup >= SMA5). Tambah posisi tidak dimodelkan. Henti low hari sentuhan; exit asal tutup < MA5.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open.values, g.high.values, g.low.values, g.close.values, g.volume.values; n = len(g)
        s5 = sma(g.close, 5).values; v20 = g.volume.rolling(20).mean().shift(1).values
        hh = g.high.rolling(20).max().shift(1).values; ll = g.low.rolling(20).min().shift(1).values
        sig = np.zeros(n, bool); b = -1
        for i in range(1, n):
            if (hh[i] - ll[i]) / ll[i] <= 0.15 and c[i] >= 1.07 * c[i - 1] and c[i] > o[i] and v[i] >= 2 * v20[i]:
                b = i; continue
            if b >= 0 and i - b <= 10:
                if l[i] <= s5[i] and c[i] >= s5[i]: sig[i] = True; b = -1
            elif b >= 0: b = -1
        stop = g.low
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop, exitc=g.close < sma(g.close, 5))

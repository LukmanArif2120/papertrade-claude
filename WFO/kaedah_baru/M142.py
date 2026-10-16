from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M142'
NAMA = "Pecahan volum dari dasar (底部放量)"
VARIAN = 'V0 Katalog K264 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 270
ADA_HENTI = True
SILANG = False
PERLU_BAR = 270
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K264. Hari pecah: volum >= 2 x purata 20 hari; tutup > 1.03 x high tertinggi 20 hari sebelumnya ("high sebelumnya", andaian); tutup > MA250 dan MA250 naik (> 20 hari lepas). Penapis kadar pusing ganti diabaikan (tiada data). Pencetus: dalam 10 bar, bar undur pertama (tutup < tutup semalam) dengan low >= paras pecah. Henti = low hari pecah. Sasaran +15–20% tidak dimodelkan (WFO).

def sedia(fr, idx):
    for g in fr.values():
        h, l, c, v = g.high.values, g.low.values, g.close.values, g.volume.values; n = len(g)
        m250 = sma(g.close, 250).values; m250l = pd.Series(m250).shift(20).values
        v20 = g.volume.rolling(20).mean().shift(1).values; h20 = g.high.rolling(20).max().shift(1).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); b = -1; lv = sl = np.nan
        for i in range(1, n):
            if v[i] >= 2 * v20[i] and c[i] > 1.03 * h20[i] and c[i] > m250[i] and m250[i] > m250l[i]:
                b = i; lv = h20[i]; sl = l[i]; continue
            if b >= 0 and i - b <= 10:
                if l[i] < lv: b = -1; continue
                if c[i] < c[i - 1]: sig[i] = True; stop[i] = sl; b = -1
            elif b >= 0: b = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)

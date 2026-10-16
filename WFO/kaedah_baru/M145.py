from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M145'
NAMA = "Yum-Yum Continuation"
VARIAN = 'V0 Katalog K285 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K285. Aliran = tutup > EMA20 dan EMA20 naik. Bar Yum-Yum: julat > purata julat 10 bar sebelumnya, tutup > high tertinggi 20 bar sebelumnya ("swing high tertinggi", andaian), tutup dalam 25% atas julat dan > buka. Pencetus dalam 1–3 bar: tutup > high bar itu. Henti low bar itu.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e = ema(c, 20); r = h - l; pos = ((c - l) / r).where(r > 0)
        yy = (c > e) & (e > e.shift()) & (r > r.shift(1).rolling(10).mean()) & (c > h.shift(1).rolling(20).max()) & (pos >= 0.75) & (c > o)
        tahap = h.where(yy).ffill(limit=3).shift(1); lw = l.where(yy).ffill(limit=3).shift(1)
        sig = tahap.notna() & (c > tahap) & ~yy.shift(1, fill_value=False).rolling(3).max().isna()
        sig = sig & ~(c.shift() > tahap)                 # pencetus pertama sahaja
        siap_lajur(g, sig & ~langkau(g, lw), lw)

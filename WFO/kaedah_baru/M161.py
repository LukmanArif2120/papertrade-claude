from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M161'
NAMA = "EMA 10/21 + Supertrend (10,3)"
VARIAN = 'V0 Katalog K397 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K397. Penapis: EMA10 > EMA21 dan Supertrend(10,3) hijau. (A) undur: low <= EMA10 dan lilin pengesahan (tutup > buka dan tutup > EMA10); ATAU (B) pecah julat sempit 5 hari (julat 5 hari <= 1.5 x ATR14, andaian): tutup > high tertinggi 5 hari sebelumnya. Henti = low terendah 10 bar (swing low, andaian). Jual berperingkat dan tambah semula tidak dimodelkan; exit asal: 2 tutup berturut < EMA21.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e10, e21 = ema(c, 10), ema(c, 21); st = supertrend_hijau(g, 10, 3.0)
        A = (l <= e10) & (c > o) & (c > e10)
        rng5 = h.shift(1).rolling(5).max() - l.shift(1).rolling(5).min()
        B = (rng5 <= 1.5 * atr(g)) & (c > h.shift(1).rolling(5).max())
        sig = (e10 > e21) & st & (A | B)
        stop = l.rolling(10).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=(c < e21) & (c.shift() < e21.shift()))

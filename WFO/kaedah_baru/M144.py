from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M144'
NAMA = "Screw Bar"
VARIAN = 'V0 Katalog K274 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K274. Semalam tutup di low (dalam 10% bawah julat); hari ini buka > high semalam dan tutup > high semalam; senarai semak: (tutup - SMA50) < 4 x ATR14, ADR 20 hari >= 4%. Masuk intrahari diganti buka esok (proksi). Henti = low hari ini (andaian). Exit asal: tutup < SMA20 (andaian "ekor MA10/MA20").

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        pos = ((c - l) / (h - l)).where(h > l)
        adr = ((h - l) / c).rolling(20).mean()
        sig = (pos.shift() <= 0.10) & (o > h.shift()) & (c > h.shift()) & ((c - sma(c, 50)) < 4 * atr(g)) & (adr >= 0.04)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < sma(c, 20))

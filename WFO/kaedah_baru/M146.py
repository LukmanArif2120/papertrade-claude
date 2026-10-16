from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M146'
NAMA = "3-Bar Momentum Pattern"
VARIAN = 'V0 Katalog K286 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K286. 3 bar: TR, tutup, low dan high masing-masing naik; semua tutup > buka; pecutan: kenaikan tutup bar 3 > bar 2 dan kenaikan high bar 3 > bar 2; penapis high > high tertinggi 20 bar sebelumnya (N=20 andaian). Beli buka esok. Henti low bar pertama corak. Keluar masa ditala WFO.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
        naik = lambda s: (s > s.shift(1)) & (s.shift(1) > s.shift(2))
        hijau = (c > o) & (c.shift() > o.shift()) & (c.shift(2) > o.shift(2))
        pecut = (c - c.shift() > c.shift() - c.shift(2)) & (h - h.shift() > h.shift() - h.shift(2))
        sig = naik(tr) & naik(c) & naik(l) & naik(h) & hijau & pecut & (h > h.shift(3).rolling(20).max())
        stop = l.shift(2)
        siap_lajur(g, sig & ~langkau(g, stop), stop)

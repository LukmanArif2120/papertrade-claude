from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M118'
NAMA = 'Expansion Pivot (Cooper)'
VARIAN = 'V0 Katalog K150 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K150. Andaian: "harga ≤SMA50 semalam/hari ini dan pecah naik" = low semalam atau hari ini ≤ SMA50, tutup > SMA50, bar naik; pencetus esok tutup > high bar itu. Tiada exit asal.

def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); rng = h - l
        luas = rng > rng.shift(1).rolling(9).max()
        dekat = pd.concat([l, l.shift()], axis=1).min(axis=1) <= s50
        persediaan = luas & dekat & (c > s50) & (c > o)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)

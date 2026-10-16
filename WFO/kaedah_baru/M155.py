from _alat import sma, ema, wma, trix, adx, supertrend_hijau, naik_aliran, stoch_k, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M155'
NAMA = "Market Cycle Strategy"
VARIAN = 'V0 Katalog K331 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 80
ADA_HENTI = False
SILANG = False
PERLU_BAR = 80
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K331. S1 = Stoch perlahan (13,8), S2 = (21,13), S3 = (34,21) (%K dilicinkan; andaian tafsiran). Syarat: S1 > S2 > S3; (S1 − S3)/S3 > 10%; (S1 dan S2 naik ATAU volum/purata 21 > 1.2); isyarat pada hari pertama syarat benar. Exit asal: susunan hilang atau S1 berpusing turun. Tiada henti.

def sedia(fr, idx):
    for g in fr.values():
        v = g.volume
        s1, s2, s3 = stoch_k(g, 13, 8), stoch_k(g, 21, 13), stoch_k(g, 34, 21)
        susun = (s1 > s2) & (s2 > s3)
        ok = susun & ((s1 - s3) / s3 > 0.10) & (((s1 > s1.shift()) & (s2 > s2.shift())) | (v / v.rolling(21).mean() > 1.2))
        sig = ok & ~ok.shift(1, fill_value=False)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(~susun) | (s1 < s1.shift()))

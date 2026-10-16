from _alat import sma, ema, stoch_k, macd_hist, cci, cci_mingguan_lalu, mingguan_lalu, langkau, siap_lajur
import numpy as np, pandas as pd

ID = 'M124'
NAMA = "'Last' Stochastic Technique (ChartSchool)"
VARIAN = 'V0 Katalog K157 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 60
ADA_HENTI = False
SILANG = False
PERLU_BAR = 60
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K157. Minggu lepas = minggu kalendar lengkap sebelumnya. Exit asal (andaian katalog): %K < 50 dan tutup < tutup terendah minggu lepas. Tiada henti asal.

def sedia(fr, idx):
    for g in fr.values():
        c = g.close; k = stoch_k(g, 39, 3)
        tinggi = mingguan_lalu(g, lambda gb: gb.close.max())
        rendah = mingguan_lalu(g, lambda gb: gb.close.min())
        sig = (k > 50) & (k.shift() <= 50) & (c > tinggi)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(k < 50) & (c < rendah))

from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M138'
NAMA = "直升机空中加油 (Helikopter isi minyak di udara)"
VARIAN = 'V0 Katalog K224 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 40
ADA_HENTI = False
SILANG = False
PERLU_BAR = 40
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K224. Andaian: >= 5 lilin naik berturut (tutup > tutup semalam) dengan volum purata larian > purata 20 hari sebelumnya; kemudian lilin turun kecil (tutup < buka, badan < 0.5 x purata badan larian) dengan volum < 0.5 x purata volum larian; isyarat pada tutup lilin turun. Exit asal: volum > 3 x purata 20 hari (andaian "sangat besar"). Untung >10% tidak dimodelkan (WFO).

def sedia(fr, idx):
    for g in fr.values():
        o, c, v = g.open, g.close, g.volume
        naik = c > c.shift()
        run = naik.groupby((~naik).cumsum()).cumsum()
        r = run.shift(1).fillna(0)
        vrun = v.shift(1).rolling(5).mean(); brun = (c - o).abs().shift(1).rolling(5).mean()
        v20 = v.shift(6).rolling(20).mean()
        turun = (c < o) & ((o - c) < 0.5 * brun) & (v < 0.5 * vrun)
        sig = (r >= 5) & (vrun > v20) & turun
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=v > 3 * v.rolling(20).mean().shift(1))

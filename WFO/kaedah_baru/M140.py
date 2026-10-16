from _alat import sma, ema, langkau, siap_lajur
from enjin import atr
import numpy as np, pandas as pd

ID = 'M140'
NAMA = "猎豹出击 (Serangan Cheetah)"
VARIAN = 'V0 Katalog K229 (entry sahaja; stop/exit/tempoh ditala WFO)'
TMAX = None
WARM = 120
ADA_HENTI = True
SILANG = False
PERLU_BAR = 120
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K229. KABUR. Andaian: "kejatuhan panjang" = tutup < MA60 pada >= 40 daripada 60 hari sebelumnya dan tutup semalam <= 85% high 120 hari; "volum kering" = purata volum 20 hari < purata 60 hari. Isyarat: tutup silang atas MA60 dan naik > 4.5% berbanding tutup semalam. Henti = low hari isyarat (andaian).

def sedia(fr, idx):
    for g in fr.values():
        h, l, c, v = g.high, g.low, g.close, g.volume
        m60 = sma(c, 60)
        jatuh = ((c < m60).shift(1).astype(float).rolling(60).sum() >= 40) & (c.shift() <= 0.85 * h.rolling(120).max().shift())
        kering = v.rolling(20).mean().shift(1) < v.rolling(60).mean().shift(1)
        sig = jatuh & kering & (c > m60) & (c.shift() <= m60.shift()) & (c / c.shift() - 1 > 0.045)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop)

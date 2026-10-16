try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M134'
NAMA = "First Kiss After Daylight (Landry)"
VARIAN = 'V1 WFO beku: henti ATR2, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M134.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K200. Andaian: "low utama baharu" = low terendah 60 hari dalam 60 bar lepas; "daylight" = >= 5 bar berturut low > SMA10; ciuman pertama = bar pertama low <= SMA10 selepas daylight; pencetus tutup > high bar ciuman (katalog: andaian atas high sebelumnya). Henti low bar ciuman. Keluar Landry tidak dimodelkan (WFO).

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        s10 = sma(c, 10)
        atas = l > s10
        run = atas.groupby((~atas).cumsum()).cumsum()
        cium = (l <= s10) & (run.shift(1) >= 5)
        lowu = (l <= l.rolling(60).min()).astype(float).rolling(60).max() > 0
        stop = l.shift(1)
        sig = (cium & lowu).shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR2'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

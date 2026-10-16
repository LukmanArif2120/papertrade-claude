try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M125'
NAMA = "2-Bar Breakout"
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax tiada'
TMAX = None
WARM = 30
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 30
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M125.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K163. Henti = low semalam (katalog). Tiada exit asal.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        sig = (h.shift(1) > pd.concat([h.shift(2), h.shift(3)], axis=1).max(axis=1)) & (c > c.shift(1))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

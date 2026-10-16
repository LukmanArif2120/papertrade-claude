try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M158'
NAMA = "Doubly Adaptive Profit Targets"
VARIAN = 'V1 WFO beku: henti PCT12, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M158.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K379. Hari A: tutup > SMA50 dan ADX14 naik. Hari B: buka > high A dan low <= high A (beli had di high A terisi). Isyarat pada tutup B, masuk buka esok (proksi). Henti = tutup − 4 x ATR20. Sasaran ATR tidak dimodelkan. Exit asal: tutup < SMA50.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); ax = adx(g, 14)
        A = (c > s50) & (ax > ax.shift())
        sig = A.shift(1, fill_value=False) & (o > h.shift(1)) & (l <= h.shift(1))
        stop = c - 4 * atr(g, 20)
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < s50)


HENTI_KOD = 'PCT12'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

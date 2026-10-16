try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M127'
NAMA = "Slingshot Bullish"
VARIAN = 'V1 WFO beku: henti LOW1, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M127.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K177. 2 bulan = 42 hari. Hari A: high 42 hari; hari B: low < low hari A; pencetus hari C tutup > high hari A. Henti "2 mata" ditukar kepada low hari B (andaian). Tiada exit asal.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        A = h >= h.rolling(42).max()
        sig = A.shift(2, fill_value=False) & (l.shift(1) < l.shift(2)) & (c > h.shift(2))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'LOW1'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

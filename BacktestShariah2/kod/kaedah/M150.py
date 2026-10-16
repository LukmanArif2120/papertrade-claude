try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M150'
NAMA = "Trend Bar Failure (Brooks)"
VARIAN = 'V1 WFO beku: henti PCT12, keluar SMA20, tmax 21'
TMAX = 21
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M150.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K297. EMA20 naik. Bar A: bar aliran turun (tutup < buka, badan > 50% julat). Bar B: low < low A. Pencetus bar selepas B (sah 1 bar): tutup > high A. Henti low B (andaian).

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e = ema(c, 20); r = h - l
        A = (c < o) & ((o - c) > 0.5 * r) & (e > e.shift())
        B = A.shift(1, fill_value=False) & (l < l.shift(1))
        stop = l.shift(1)
        sig = B.shift(1, fill_value=False) & (c > h.shift(2))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT12'
KELUAR_KOD = 'SMA20'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

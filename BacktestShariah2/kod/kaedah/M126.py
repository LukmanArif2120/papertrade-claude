try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M126'
NAMA = "Hidden Smash Day (beli, Larry Williams)"
VARIAN = 'V1 WFO beku: henti ATR3, keluar SMA50, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M126.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K164. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. "High baharu" = high tertinggi 20 hari (andaian). Hari smash: tutup dalam 25% bawah julat. Pencetus esok tutup > high hari smash; henti low hari smash.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20))
        pos = ((c - l) / (h - l)).where(h > l)
        smash = naik & (h >= h.rolling(20).max()) & (pos <= 0.25)
        stop = l.shift(1)
        sig = smash.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR3'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

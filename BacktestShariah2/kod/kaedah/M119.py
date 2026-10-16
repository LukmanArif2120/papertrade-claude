try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M119'
NAMA = '180 Bullish (Cooper)'
VARIAN = 'V1 WFO beku: henti ASAL, keluar CHAN4, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M119.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K151. Henti "1 mata" ditukar kepada low bar persediaan (andaian). Pencetus esok tutup > high bar persediaan. Tiada exit asal.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        pos = ((c - l) / (h - l)).where(h > l)
        persediaan = (pos.shift() <= 0.25) & (pos >= 0.75) & (c > sma(c, 10)) & (c > sma(c, 50))
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ASAL'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

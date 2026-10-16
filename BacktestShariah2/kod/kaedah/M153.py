try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M153'
NAMA = "Range Leader"
VARIAN = 'V1 WFO beku: henti PCT12, keluar CHAN2, tmax 10'
TMAX = 10
WARM = 30
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 30
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M153.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K304. Julat > julat semalam dan titik tengah > high semalam; beli buka esok; langkau jika buka esok < titik tengah. Henti low bar. Sasaran 2R / pulang modal tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        h, l = g.high, g.low
        mid = (h + l) / 2
        sig = ((h - l) > (h - l).shift()) & (mid > h.shift())
        lk = (g.open.shift(-1) < mid).fillna(False)
        siap_lajur(g, sig & ~lk & ~langkau(g, l), l)


HENTI_KOD = 'PCT12'
KELUAR_KOD = 'CHAN2'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

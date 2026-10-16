try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M147'
NAMA = "Improved Three-Bar Pullback"
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M147.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K288. TRIX(9) > isyarat EMA3 pada bar ke-3; 3 tutup menurun berturut; pencetus esok tutup > high bar ke-3. Henti low bar ke-3 (andaian).

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        t = trix(c, 9); s = ema(t, 3)
        tiga = (c < c.shift()) & (c.shift() < c.shift(2)) & (c.shift(2) < c.shift(3)) & (t > s)
        stop = l.shift(1)
        sig = tiga.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT15'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M128'
NAMA = "Inventory Retracement Bar (IRB, Rob Hoffman)"
VARIAN = 'V1 WFO beku: henti PCT10, keluar SMA20, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M128.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K179. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. IRB: buka dan tutup kedua-duanya >= 45% julat di bawah high. Pencetus esok tutup > high IRB; henti low IRB (andaian; katalog tiada henti).

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20)); r = (h - l).where(h > l)
        irb = naik & ((h - o) / r >= 0.45) & ((h - c) / r >= 0.45)
        stop = l.shift(1)
        sig = irb.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT10'
KELUAR_KOD = 'SMA20'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M133'
NAMA = "Bull Hook (Crabel)"
VARIAN = 'V1 WFO beku: henti ATR2, keluar SMA50, tmax 21'
TMAX = 21
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M133.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K196. Hari hook: buka > high semalam, tutup < tutup semalam, julat < julat semalam. Pencetus esok: tutup > buka esok + Stretch (Stretch = 2 x SMA10 min(H-O, O-L)) — proksi tutup untuk beli henti. Henti = tutup - 6 x ATR20 (katalog: entry - 6 ATR20; tutup sebagai proksi entry). Keluar masa hari ke-n ditala WFO (tmax).

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        r = h - l
        hook = (o > h.shift()) & (c < c.shift()) & (r < r.shift())
        stretch = 2 * sma(pd.concat([h - o, o - l], axis=1).min(axis=1), 10)
        sig = hook.shift(1, fill_value=False) & (c > o + stretch.shift(1))
        stop = c - 6 * atr(g, 20)
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR2'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

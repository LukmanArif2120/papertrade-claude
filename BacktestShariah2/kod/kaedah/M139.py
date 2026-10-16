try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M139'
NAMA = "均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik)"
VARIAN = 'V1 WFO beku: henti PCT15, keluar TIADA, tmax 21'
TMAX = 21
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M139.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K225. Himpun = (maks - min SMA5/10/20) <= 0.5 x ATR14 pada bar sebelumnya; "kali pertama" (andaian) = tiada himpun dalam 20 bar sebelum itu; pencetus tutup > MA tertinggi. Saiz kecil jika MA60 menurun — tidak dimodelkan. Henti = low bar pencetus (andaian).

def _entri(fr, idx):
    for g in fr.values():
        c, l = g.close, g.low
        m = pd.concat([sma(c, 5), sma(c, 10), sma(c, 20)], axis=1)
        himpun = (m.max(axis=1) - m.min(axis=1)) <= 0.5 * atr(g)
        pertama = himpun.shift(1, fill_value=False) & (himpun.shift(2).astype(float).rolling(20).max() == 0)
        sig = pertama & (c > m.max(axis=1))
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT15'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

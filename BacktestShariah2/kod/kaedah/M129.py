try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M129'
NAMA = "Wick Play"
VARIAN = 'V1 WFO beku: henti LOW10, keluar TIADA, tmax 63'
TMAX = 63
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M129.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K180. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. "Saham kuat" = aliran naik. Hari 1: sumbu atas >= 40% julat (andaian). Hari 2: buka dalam sumbu (atas badan, bawah high hari 1) dan low >= atas badan hari 1. Hari 3: tutup > high hari 2 (andaian "atas high"). Henti low hari 2 (andaian). KABUR: ambang sumbu tidak dinyatakan sumber.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); naik = (c > s50) & (s50 > s50.shift(20))
        atas = pd.concat([o, c], axis=1).max(axis=1); r = (h - l).where(h > l)
        hari1 = naik & ((h - atas) / r >= 0.40)
        hari2 = hari1.shift(1, fill_value=False) & (o > atas.shift(1)) & (o < h.shift(1)) & (l >= atas.shift(1))
        stop = l.shift(1)
        sig = hari2.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'LOW10'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

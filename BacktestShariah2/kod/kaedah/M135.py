try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M135'
NAMA = "3rd Watch"
VARIAN = 'V1 WFO beku: henti LOW10, keluar SMA50, tmax 63'
TMAX = 63
WARM = 150
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 150
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M135.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K202. KABUR. Andaian: paras = high tertinggi 126 hari sebelum 20 hari terakhir; tiada high melebihi paras dalam 20 hari lepas; >= 2 pivot high (fraktal 2 bar) dalam 3% bawah paras dalam 126 hari; bar pecahan tutup > paras dengan volum >= 1.5 x purata 20 hari; masuk pada tutup bar pecahan (bukan bar sempit/undur). Henti low bar pecahan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c, v = g.high, g.low, g.close, g.volume
        paras = h.shift(21).rolling(106).max()
        senyap = h.shift(1).rolling(20).max() <= paras
        piv = (h.shift(2) > pd.concat([h.shift(4), h.shift(3), h.shift(1), h], axis=1).max(axis=1))
        dekat = piv & (h.shift(2) >= 0.97 * paras) & (h.shift(2) <= paras)
        sentuh = dekat.astype(float).rolling(126).sum() >= 2
        sig = senyap & sentuh & (c > paras) & (v >= 1.5 * v.rolling(20).mean().shift(1))
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'LOW10'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

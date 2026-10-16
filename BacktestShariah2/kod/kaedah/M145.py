try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M145'
NAMA = "Yum-Yum Continuation"
VARIAN = 'V1 WFO beku: henti LOW10, keluar ASAL, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M145.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K285. Aliran = tutup > EMA20 dan EMA20 naik. Bar Yum-Yum: julat > purata julat 10 bar sebelumnya, tutup > high tertinggi 20 bar sebelumnya ("swing high tertinggi", andaian), tutup dalam 25% atas julat dan > buka. Pencetus dalam 1–3 bar: tutup > high bar itu. Henti low bar itu.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e = ema(c, 20); r = h - l; pos = ((c - l) / r).where(r > 0)
        yy = (c > e) & (e > e.shift()) & (r > r.shift(1).rolling(10).mean()) & (c > h.shift(1).rolling(20).max()) & (pos >= 0.75) & (c > o)
        tahap = h.where(yy).ffill(limit=3).shift(1); lw = l.where(yy).ffill(limit=3).shift(1)
        sig = tahap.notna() & (c > tahap) & ~yy.shift(1, fill_value=False).rolling(3).max().isna()
        sig = sig & ~(c.shift() > tahap)                 # pencetus pertama sahaja
        siap_lajur(g, sig & ~langkau(g, lw), lw)


HENTI_KOD = 'LOW10'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

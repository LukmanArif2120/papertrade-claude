try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M157'
NAMA = "Consolidation Pivot Breakout (versi angka)"
VARIAN = 'V1 WFO beku: henti PCT6, keluar ASAL, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M157.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K358. Syarat katalog: naik >15% dalam 20 hari ATAU >25% dalam 40 hari; tutup dalam 15% dari high 50 hari ("high", andaian); tutup > EMA10 & EMA21; EMA10 > EMA21; EMA21 > EMA21 5 hari lepas; ADR 5 hari < 3%; julat hari ini < 2%; purata volum 5 hari < 80% purata 50 hari. Pusingan-U intrahari diganti: esok tutup > high hari persediaan. Henti low hari persediaan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c, v = g.high, g.low, g.close, g.volume
        e10, e21 = ema(c, 10), ema(c, 21)
        adr5 = ((h - l) / c).rolling(5).mean()
        ok = (((c / c.shift(20) - 1) > 0.15) | ((c / c.shift(40) - 1) > 0.25)) & (c >= 0.85 * h.rolling(50).max()) \
             & (c > e10) & (c > e21) & (e10 > e21) & (e21 > e21.shift(5)) & (adr5 < 0.03) & ((h - l) / c < 0.02) \
             & (v.rolling(5).mean() < 0.8 * v.rolling(50).mean())
        stop = l.shift(1)
        sig = ok.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT6'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M161'
NAMA = "EMA 10/21 + Supertrend (10,3)"
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M161.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K397. Penapis: EMA10 > EMA21 dan Supertrend(10,3) hijau. (A) undur: low <= EMA10 dan lilin pengesahan (tutup > buka dan tutup > EMA10); ATAU (B) pecah julat sempit 5 hari (julat 5 hari <= 1.5 x ATR14, andaian): tutup > high tertinggi 5 hari sebelumnya. Henti = low terendah 10 bar (swing low, andaian). Jual berperingkat dan tambah semula tidak dimodelkan; exit asal: 2 tutup berturut < EMA21.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        e10, e21 = ema(c, 10), ema(c, 21); st = supertrend_hijau(g, 10, 3.0)
        A = (l <= e10) & (c > o) & (c > e10)
        rng5 = h.shift(1).rolling(5).max() - l.shift(1).rolling(5).min()
        B = (rng5 <= 1.5 * atr(g)) & (c > h.shift(1).rolling(5).max())
        sig = (e10 > e21) & st & (A | B)
        stop = l.rolling(10).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=(c < e21) & (c.shift() < e21.shift()))


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

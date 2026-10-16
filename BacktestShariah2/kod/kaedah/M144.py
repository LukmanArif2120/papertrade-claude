try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M144'
NAMA = "Screw Bar"
VARIAN = 'V1 WFO beku: henti ATR4, keluar SMA50, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M144.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K274. Semalam tutup di low (dalam 10% bawah julat); hari ini buka > high semalam dan tutup > high semalam; senarai semak: (tutup - SMA50) < 4 x ATR14, ADR 20 hari >= 4%. Masuk intrahari diganti buka esok (proksi). Henti = low hari ini (andaian). Exit asal: tutup < SMA20 (andaian "ekor MA10/MA20").

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        pos = ((c - l) / (h - l)).where(h > l)
        adr = ((h - l) / c).rolling(20).mean()
        sig = (pos.shift() <= 0.10) & (o > h.shift()) & (c > h.shift()) & ((c - sma(c, 50)) < 4 * atr(g)) & (adr >= 0.04)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < sma(c, 20))


HENTI_KOD = 'ATR4'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

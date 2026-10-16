try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M146'
NAMA = "3-Bar Momentum Pattern"
VARIAN = 'V1 WFO beku: henti PCT6, keluar SMA50, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M146.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K286. 3 bar: TR, tutup, low dan high masing-masing naik; semua tutup > buka; pecutan: kenaikan tutup bar 3 > bar 2 dan kenaikan high bar 3 > bar 2; penapis high > high tertinggi 20 bar sebelumnya (N=20 andaian). Beli buka esok. Henti low bar pertama corak. Keluar masa ditala WFO.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
        naik = lambda s: (s > s.shift(1)) & (s.shift(1) > s.shift(2))
        hijau = (c > o) & (c.shift() > o.shift()) & (c.shift(2) > o.shift(2))
        pecut = (c - c.shift() > c.shift() - c.shift(2)) & (h - h.shift() > h.shift() - h.shift(2))
        sig = naik(tr) & naik(c) & naik(l) & naik(h) & hijau & pecut & (h > h.shift(3).rolling(20).max())
        stop = l.shift(2)
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'PCT6'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

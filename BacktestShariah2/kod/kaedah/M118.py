try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M118'
NAMA = 'Expansion Pivot (Cooper)'
VARIAN = 'V1 WFO beku: henti LOW5, keluar SMA50, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M118.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K150. Andaian: "harga ≤SMA50 semalam/hari ini dan pecah naik" = low semalam atau hari ini ≤ SMA50, tutup > SMA50, bar naik; pencetus esok tutup > high bar itu. Tiada exit asal.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        s50 = sma(c, 50); rng = h - l
        luas = rng > rng.shift(1).rolling(9).max()
        dekat = pd.concat([l, l.shift()], axis=1).min(axis=1) <= s50
        persediaan = luas & dekat & (c > s50) & (c > o)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'LOW5'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

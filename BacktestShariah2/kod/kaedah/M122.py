try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M122'
NAMA = 'Moving Momentum (ChartSchool)'
VARIAN = 'V1 WFO beku: henti LOW5, keluar TIADA, tmax 42'
TMAX = 42
WARM = 170
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 170
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M122.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K155. Andaian: Stokastik perlahan (14,3) < 20 dalam 10 hari terakhir, kemudian histogram MACD(12,26,9) silang atas 0; SMA20 > SMA150. Exit asal (andaian katalog): SMA20 < SMA150 atau histogram < 0. Tiada henti asal.

def _entri(fr, idx):
    for g in fr.values():
        c = g.close
        k = stoch_k(g, 14, 3); hist = macd_hist(c)
        os_ = (k < 20).astype(float).rolling(10).max() > 0
        tren = sma(c, 20) > sma(c, 150)
        sig = tren & os_ & (hist > 0) & (hist.shift() <= 0)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(~tren) | (hist < 0))


HENTI_KOD = 'LOW5'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

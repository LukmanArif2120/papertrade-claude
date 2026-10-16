try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M151'
NAMA = "Outside Bar Failure"
VARIAN = 'V1 WFO beku: henti ATR1.5, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M151.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K298. SMA20 naik. Bar luar bearish O (high > high semalam, low < low semalam, tutup < buka). Selepas low O ditembus, bar bullish pertama U (tutup > buka); pencetus tutup > high U. Batal jika ada bar dengan high < low O, atau selepas 10 bar (andaian). Tiada henti (katalog).

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        s20 = sma(g.close, 20).values
        sig = np.zeros(n, bool); t = -1; lo = np.nan; tembus = False; u = np.nan
        for i in range(21, n):
            if h[i] > h[i - 1] and l[i] < l[i - 1] and c[i] < o[i] and s20[i] > s20[i - 1]:
                t = i; lo = l[i]; tembus = False; u = np.nan; continue
            if t < 0: continue
            if i - t > 10 or h[i] < lo: t = -1; continue
            if not tembus:
                if l[i] < lo: tembus = True
                continue
            if not np.isnan(u) and c[i] > u: sig[i] = True; t = -1; continue
            if c[i] > o[i]: u = h[i]
        siap_lajur(g, pd.Series(sig, g.index), pd.Series(np.nan, g.index))


HENTI_KOD = 'ATR1.5'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

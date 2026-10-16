try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M141'
NAMA = "First Thrust (Landry)"
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 63'
TMAX = 63
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M141.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K256. KABUR ("utama"/"tajam" tidak ditakrif). Andaian: low utama = low terendah 60 hari, berlaku dalam 15 bar lepas; rali tajam = high sejak low >= low + 3 x ATR14; undur pertama = bar pertama high < high semalam selepas low; pencetus esok tutup > high bar undur. Henti low bar undur.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; a = atr(g).values; n = len(g)
        lo60 = g.low.rolling(60).min().values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); t = -1; dipakai = -1
        for i in range(61, n):
            if l[i] <= lo60[i]: t = i
            if t < 0 or i - t > 15: continue
            k = i - 1                                    # bar undur calon
            if k <= t + 1 or t == dipakai: continue
            pertama = h[k] < h[k - 1] and all(h[j] >= h[j - 1] for j in range(t + 1, k))
            if pertama and h[t:k].max() >= l[t] + 3 * a[k] and c[i] > h[k]:
                sig[i] = True; stop[i] = l[k]; dipakai = t
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)


HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M152'
NAMA = "Spike & Ledge"
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M152.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K303. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. Hari lonjakan S: low < low terendah 5 bar sebelumnya ("menduga low") dan tutup dalam 25% atas julat. Para: 4–10 bar selepas S dengan semua low > low S. Pencetus: tutup > tutup tertinggi para. Henti = low terendah para.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        pos = ((g.close - g.low) / (g.high - g.low)).where(g.high > g.low).values
        l5 = g.low.shift(1).rolling(5).min().values
        S = naik & (l < l5) & (pos >= 0.75)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(12, n):
            for k in range(5, 12):
                s = i - k
                if not S[s]: continue
                para = slice(s + 1, i)
                if l[para].min() > l[s] and c[i] > c[para].max():
                    sig[i] = True; stop[i] = l[para].min(); break
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)


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

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M154'
NAMA = "HOLP (High of Low Period)"
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M154.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K305. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. Pembetulan 20 bar: bar low terendah 20 bar (k); pencetus tutup pertama > high bar k (tiada tutup > high k antara k dan semalam). Henti = low bar k.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(21, n):
            if not naik[i]: continue
            k = i - 20 + int(np.argmin(l[i - 20:i]))
            if c[i] > h[k] and (k + 1 > i - 1 or c[k + 1:i].max() <= h[k]):
                sig[i] = True; stop[i] = l[k]
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)


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

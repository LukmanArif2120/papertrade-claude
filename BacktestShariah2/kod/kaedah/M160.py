try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M160'
NAMA = "Measured Move Up"
VARIAN = 'V1 WFO beku: henti LOW10, keluar EMA21, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M160.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K395. KABUR (perlu pengesanan ayunan). Andaian: zigzag 3 x ATR14; kaki pertama A(low)→B(high) disahkan; pembetulan dari B, retracement 30–70% kaki AB, low pembetulan > A; pencetus pusingan naik: tutup > high semalam. Henti low pembetulan. Sasaran kaki kedua tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; a = atr(g).values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        arah = 0; ext = np.nan; A = B = np.nan; lo = np.inf; aktif = False
        for i in range(1, n):
            if np.isnan(a[i]): continue
            if arah >= 0:
                if np.isnan(ext) or h[i] > ext: ext = h[i]
                if ext - l[i] >= 3 * a[i]:
                    B = ext; arah = -1; ext = l[i]; aktif = not np.isnan(A); lo = l[i]
            else:
                if l[i] < ext: ext = l[i]
                if h[i] - ext >= 3 * a[i]: A = ext; arah = 1; ext = h[i]; aktif = False
            if aktif:
                lo = min(lo, l[i]); rt = (B - lo) / (B - A) if B > A else np.nan
                if lo <= A: aktif = False; continue
                if 0.3 <= rt <= 0.7 and c[i] > h[i - 1]:
                    sig[i] = True; stop[i] = lo; aktif = False
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)


HENTI_KOD = 'LOW10'
KELUAR_KOD = 'EMA21'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

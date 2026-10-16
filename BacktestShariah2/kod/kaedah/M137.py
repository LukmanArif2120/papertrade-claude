try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M137'
NAMA = "Livermore System"
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M137.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K212. Pivot = ayunan >= 4 x ATR14 (zigzag; pivot disahkan apabila harga berbalik 4 ATR). Isyarat: tutup > kedua-dua pivot bekalan (swing high) terkini; masuk buka esok. Henti = tutup - 6 x ATR20 (proksi entry). Exit asal: tutup < pivot permintaan (swing low) terkini.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; a = atr(g).values; n = len(g)
        sig = np.zeros(n, bool); dem = np.full(n, np.nan)
        arah = 0; ext = np.nan; sup = []; lo = np.nan
        for i in range(n):
            if np.isnan(a[i]): continue
            if arah >= 0:
                if np.isnan(ext) or h[i] > ext: ext = h[i]
                if ext - l[i] >= 4 * a[i]: sup.append(ext); arah = -1; ext = l[i]
            else:
                if l[i] < ext: ext = l[i]
                if h[i] - ext >= 4 * a[i]: lo = ext; arah = 1; ext = h[i]
            dem[i] = lo
            if len(sup) >= 2 and c[i] > max(sup[-1], sup[-2]) and (i == 0 or c[i - 1] <= max(sup[-1], sup[-2])): sig[i] = True
        stop = g.close - 6 * atr(g, 20)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop, exitc=g.close < pd.Series(dem, g.index))


HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

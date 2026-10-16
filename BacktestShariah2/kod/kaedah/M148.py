try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M148'
NAMA = "Natural Number Method"
VARIAN = 'V1 WFO beku: henti PCT6, keluar EMA10, tmax 42'
TMAX = 42
WARM = 200
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 200
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M148.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K289. Bar persediaan = tutup pertama silang atas WMA180. Nombor bulat (andaian): langkah 1 (<$20), 5 (<$100), 10 (<$500), 50 (selainnya). Paras = nombor bulat seterusnya di atas high bar persediaan; pencetus tutup > paras dalam 20 bar selagi tutup > WMA180. Henti = paras − 1 langkah. Exit asal: tutup < WMA180.

def langkah(p):
    return 1.0 if p < 20 else 5.0 if p < 100 else 10.0 if p < 500 else 50.0

def _entri(fr, idx):
    for g in fr.values():
        h, c = g.high.values, g.close.values; w = wma(g.close, 180).values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); b = -1; lv = st = np.nan
        for i in range(1, n):
            if np.isnan(w[i]) or np.isnan(w[i - 1]): continue
            if c[i] > w[i] and c[i - 1] <= w[i - 1]:
                k = langkah(h[i]); lv = (np.floor(h[i] / k) + 1) * k; st = lv - k; b = i; continue
            if b >= 0:
                if c[i] <= w[i] or i - b > 20: b = -1; continue
                if c[i] > lv: sig[i] = True; stop[i] = st; b = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, exitc=g.close < pd.Series(w, g.index))


HENTI_KOD = 'PCT6'
KELUAR_KOD = 'EMA10'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

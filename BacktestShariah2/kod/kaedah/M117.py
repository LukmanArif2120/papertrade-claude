try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M117'
NAMA = 'Landry Pullback (high 2 bulan)'
VARIAN = 'V1 WFO beku: henti ATR3, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M117.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K147. Andaian: 2 bulan = 42 hari; pencetus tutup > high semalam selepas 2–7 bar high menurun dari high 42 hari; henti = low bar pencetus; langkau jika risiko > 4%. Tiada exit asal.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        hh = h >= h.rolling(42).max()
        lh = h < h.shift()
        L = lh.groupby((~lh).cumsum()).cumsum().astype(int)       # panjang larian high menurun
        Lp = L.shift(1).fillna(0).astype(int).values
        hhv = hh.values; n = len(g); puncak = np.zeros(n, bool)
        for i in range(n):
            p = i - 1 - Lp[i]
            if 2 <= Lp[i] <= 7 and p >= 0: puncak[i] = hhv[p]
        stop = l
        sig = pd.Series(puncak, g.index) & (c > h.shift(1)) & ((c - l) / c <= 0.04)
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR3'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

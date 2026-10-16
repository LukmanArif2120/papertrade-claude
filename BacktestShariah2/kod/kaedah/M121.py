try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M121'
NAMA = 'High 2 bull flag (Brooks)'
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M121.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K153. Andaian kiraan: undur bermula bila high < high semalam selepas swing high; H-n = bar dengan high > high semalam selepas bar turun; H2 = kali kedua dalam undur yang sama. Bar isyarat tutup dalam 25% atas julat; EMA20 naik & tutup > EMA20. Pencetus esok tutup > high bar H2; henti low bar H2. Sasaran 2R tidak dimodelkan (harga masuk belum diketahui).

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values
        e20 = ema(g.close, 20); tren = ((g.close > e20) & (e20 > e20.shift())).values
        pos = ((g.close - g.low) / (g.high - g.low)).where(g.high > g.low).values
        n = len(g); h2 = np.zeros(n, bool); sw = -np.inf; dalam = False; kira = 0
        for i in range(2, n):
            if h[i] > sw and not dalam:
                sw = h[i]; continue
            if h[i] > sw and dalam:                     # undur tamat, swing high baharu
                sw = h[i]; dalam = False; kira = 0; continue
            if not dalam and h[i] < h[i - 1]:
                dalam = True; kira = 0; continue
            if dalam and h[i] > h[i - 1] and h[i - 1] < h[i - 2]:
                kira += 1
                if kira == 2 and tren[i] and pos[i] >= 0.75: h2[i] = True
        H2 = pd.Series(h2, g.index)
        stop = g.low.shift(1)
        sig = H2.shift(1, fill_value=False) & (g.close > g.high.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop)


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

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M131'
NAMA = "Ross Hook (Joe Ross)"
VARIAN = 'V1 WFO beku: henti ATR2, keluar TIADA, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M131.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K192. KABUR: pivot perlu ditakrif. Andaian: pivot = fraktal 2 bar (disahkan 2 bar kemudian, tiada pandang ke hadapan). 1-2-3 naik: pivot low 1, pivot high 2, pivot low 3 > low 1. Selepas tutup > titik 2, cangkuk = high tertinggi sebelum bar pertama yang gagal buat high baharu; pencetus tutup > cangkuk. Henti = low titik 3.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        p_low = []; p_high = []                      # (indeks, nilai) pivot yang sudah disahkan
        tahap = 0; t2 = t3 = cg = np.nan; mx = -np.inf; guna = -1   # guna: pivot low 3 terakhir yang sudah dipakai
        for i in range(4, n):
            k = i - 2                                # pivot di k disahkan pada i
            if l[k] < min(l[k-2], l[k-1], l[k+1], l[k+2]): p_low.append((k, l[k]))
            if h[k] > max(h[k-2], h[k-1], h[k+1], h[k+2]): p_high.append((k, h[k]))
            if tahap == 0 and len(p_low) >= 2 and p_high:
                (a, la), (b, lb) = p_low[-2], p_low[-1]
                hh = [x for x in p_high if a < x[0] < b]
                if hh and lb > la and b != guna: tahap = 1; t2 = max(x[1] for x in hh); t3 = lb; guna = b
            if tahap == 1:
                if l[i] < t3: tahap = 0; continue
                if c[i] > t2: tahap = 2; mx = h[i]; continue
            if tahap == 2:
                if l[i] < t3: tahap = 0; continue
                if h[i] > mx: mx = h[i]
                elif h[i] < h[i-1]: tahap = 3; cg = mx
                continue
            if tahap == 3:
                if l[i] < t3: tahap = 0; continue
                if c[i] > cg: sig[i] = True; stop[i] = t3; tahap = 0
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)


HENTI_KOD = 'ATR2'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

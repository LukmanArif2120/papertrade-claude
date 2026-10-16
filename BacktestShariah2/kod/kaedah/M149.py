try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M149'
NAMA = "3-Step Pullback"
VARIAN = 'V1 WFO beku: henti ASAL, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M149.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K290. Keltner: EMA15 ± 2 x ATR15. Tutup > saluran atas; kemudian undur 3–15 bar; dalam undur, susutan dari high tertinggi sejak itu ke low = 20–80% lebar saluran; pencetus bar momentum naik (tutup > buka dan tutup > high semalam; pin bar tidak dimodelkan). Henti = tutup − 2.5 x ATR15. Sasaran 1:1 tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        e = ema(g.close, 15).values; a = atr(g, 15).values
        sig = np.zeros(n, bool); t0 = -1; mx = -np.inf
        for i in range(1, n):
            if np.isnan(a[i]): continue
            if c[i] > e[i] + 2 * a[i]: t0 = i; mx = h[i]; continue
            if t0 < 0: continue
            mx = max(mx, h[i]); k = i - t0
            if k > 15: t0 = -1; continue
            lebar = 4 * a[i]; susut = (mx - min(l[t0 + 1:i + 1])) / lebar
            if k >= 3 and 0.2 <= susut <= 0.8 and c[i] > o[i] and c[i] > h[i - 1]:
                sig[i] = True; t0 = -1
        stop = g.close - 2.5 * atr(g, 15)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop)


HENTI_KOD = 'ASAL'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

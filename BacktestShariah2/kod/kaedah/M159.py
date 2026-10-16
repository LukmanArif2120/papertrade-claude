try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M159'
NAMA = "Heikin-Ashi Trend"
VARIAN = 'V1 WFO beku: henti PCT15, keluar SMA20, tmax 10'
TMAX = 10
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M159.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K381. Bar HA bullish (tutup HA > buka HA) dengan bayang bawah <= 10% julat HA (andaian "kecil") dan tutup > tutup 5 hari lepas (n=5 andaian); beli buka esok. Exit asal: bar HA bearish pertama. Tiada henti.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values; n = len(g)
        hc = (o + h + l + c) / 4; ho = np.empty(n); ho[0] = (o[0] + c[0]) / 2
        for i in range(1, n): ho[i] = (ho[i - 1] + hc[i - 1]) / 2
        hh = np.maximum(h, np.maximum(ho, hc)); hl = np.minimum(l, np.minimum(ho, hc))
        hcs, hos = pd.Series(hc, g.index), pd.Series(ho, g.index)
        bull = hcs > hos
        bayang = (np.minimum(ho, hc) - hl) <= 0.1 * (hh - hl)
        sig = bull & pd.Series(bayang, g.index) & (g.close > g.close.shift(5))
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=hcs < hos)


HENTI_KOD = 'PCT15'
KELUAR_KOD = 'SMA20'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

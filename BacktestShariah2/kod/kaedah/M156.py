try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M156'
NAMA = "Single Penetration (DiNapoli)"
VARIAN = 'V1 WFO beku: henti ATR3, keluar TIADA, tmax 10'
TMAX = 10
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M156.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K346. Aliran naik (andaian) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. (penapis DMA asal tidak diberi). Tujahan: H = high tertinggi 20 hari (baru dicapai dalam 10 bar), L = low terendah 20 bar sebelum H. Masuk pada sentuhan pertama paras 38.2% (low <= H − 0.382(H−L), tutup > paras 61.8%). Henti = H − 0.618(H−L). Sasaran COP/XOP tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        naik = naik_aliran(g.close).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); guna = -1
        for i in range(41, n):
            if not naik[i]: continue
            k = i - 10 + int(np.argmax(h[i - 10:i]))
            if h[k] < h[k - 20:k].max(initial=-np.inf) or k == guna: continue
            L = l[k - 20:k].min(); H = h[k]
            p38, p62 = H - 0.382 * (H - L), H - 0.618 * (H - L)
            if l[k + 1:i].min(initial=np.inf) <= p38: continue        # bukan sentuhan pertama
            if l[i] <= p38 and c[i] > p62:
                sig[i] = True; stop[i] = p62; guna = k
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st)


HENTI_KOD = 'ATR3'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

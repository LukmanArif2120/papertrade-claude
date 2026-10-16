try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M136'
NAMA = "Short/Intermediate-term Low (Larry Williams)"
VARIAN = 'V1 WFO beku: henti PCT10, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M136.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K204. Low jangka pendek (LJP) = low < low bar sebelum & selepas (disahkan bar berikut). Low pertengahan = LJP yang lebih rendah daripada LJP sebelum & selepasnya (disahkan apabila LJP berikutnya terbentuk). Selepas pengesahan, pencetus pertama dalam 10 bar: tutup > high semalam. Henti = LJP terkini. Sasaran tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); ljp = []; bersedia = -1
        for i in range(2, n):
            k = i - 1
            if l[k] < l[k - 1] and l[k] < l[i]:
                ljp.append(l[k])
                if len(ljp) >= 3 and ljp[-2] < ljp[-3] and ljp[-2] < ljp[-1]: bersedia = i
            if bersedia >= 0 and i - bersedia <= 10 and c[i] > h[i - 1]:
                sig[i] = True; stop[i] = ljp[-1]; bersedia = -1
            elif bersedia >= 0 and i - bersedia > 10: bersedia = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)


HENTI_KOD = 'PCT10'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

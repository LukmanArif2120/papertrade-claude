try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M130'
NAMA = "多方炮 (dua lilin hijau mengapit satu merah)"
VARIAN = 'V1 WFO beku: henti ATR3.5, keluar ASAL, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M130.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K189. KABUR: sumber tiada ambang angka. Andaian: lilin 1 hijau, badan >= 1.5 x purata badan 20 hari; lilin 2 merah, badan < 0.5 x badan 1, volum < volum 1, low > buka lilin 1; lilin 3 hijau, volum > volum 2, buka <= tutup 2 dan tutup >= buka 2; SMA5 > SMA10 > SMA20. Isyarat pada tutup lilin 3; henti low terendah 3 lilin.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        b = (c - o).abs(); pb = b.rolling(20).mean()
        L1 = (c > o) & (b >= 1.5 * pb)
        L2 = (c < o) & (b < 0.5 * b.shift(1)) & (v < v.shift(1)) & (l > o.shift(1))
        L3 = (c > o) & (v > v.shift(1)) & (o <= c.shift(1)) & (c >= o.shift(1))
        susun = (sma(c, 5) > sma(c, 10)) & (sma(c, 10) > sma(c, 20))
        sig = L1.shift(2, fill_value=False) & L2.shift(1, fill_value=False) & L3 & susun
        stop = l.rolling(3).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR3.5'
KELUAR_KOD = 'ASAL'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M140'
NAMA = "猎豹出击 (Serangan Cheetah)"
VARIAN = 'V1 WFO beku: henti ATR3, keluar SMA50, tmax 63'
TMAX = 63
WARM = 120
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 120
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M140.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K229. KABUR. Andaian: "kejatuhan panjang" = tutup < MA60 pada >= 40 daripada 60 hari sebelumnya dan tutup semalam <= 85% high 120 hari; "volum kering" = purata volum 20 hari < purata 60 hari. Isyarat: tutup silang atas MA60 dan naik > 4.5% berbanding tutup semalam. Henti = low hari isyarat (andaian).

def _entri(fr, idx):
    for g in fr.values():
        h, l, c, v = g.high, g.low, g.close, g.volume
        m60 = sma(c, 60)
        jatuh = ((c < m60).shift(1).astype(float).rolling(60).sum() >= 40) & (c.shift() <= 0.85 * h.rolling(120).max().shift())
        kering = v.rolling(20).mean().shift(1) < v.rolling(60).mean().shift(1)
        sig = jatuh & kering & (c > m60) & (c.shift() <= m60.shift()) & (c / c.shift() - 1 > 0.045)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop)


HENTI_KOD = 'ATR3'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

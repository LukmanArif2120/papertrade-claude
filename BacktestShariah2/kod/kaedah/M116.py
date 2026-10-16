try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M116'
NAMA = '2/20 EMA Breakout (Landry)'
VARIAN = 'V1 WFO beku: henti PCT10, keluar TIADA, tmax 10'
TMAX = 10
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M116.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K146. Henti mengekor EMA20 dimodelkan sebagai henti awal = EMA20 hari isyarat + exit tutup < EMA20.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high, g.low, g.close
        e20 = ema(c, 20)
        dua = (l > e20) & (l.shift() > e20.shift())
        sig = dua.shift(1, fill_value=False) & (c > pd.concat([h.shift(1), h.shift(2)], axis=1).max(axis=1))
        siap_lajur(g, sig & ~langkau(g, e20), e20, exitc=c < e20)


HENTI_KOD = 'PCT10'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M155'
NAMA = "Market Cycle Strategy"
VARIAN = 'V1 WFO beku: henti ATR3, keluar TIADA, tmax 21'
TMAX = 21
WARM = 80
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 80
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M155.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K331. S1 = Stoch perlahan (13,8), S2 = (21,13), S3 = (34,21) (%K dilicinkan; andaian tafsiran). Syarat: S1 > S2 > S3; (S1 − S3)/S3 > 10%; (S1 dan S2 naik ATAU volum/purata 21 > 1.2); isyarat pada hari pertama syarat benar. Exit asal: susunan hilang atau S1 berpusing turun. Tiada henti.

def _entri(fr, idx):
    for g in fr.values():
        v = g.volume
        s1, s2, s3 = stoch_k(g, 13, 8), stoch_k(g, 21, 13), stoch_k(g, 34, 21)
        susun = (s1 > s2) & (s2 > s3)
        ok = susun & ((s1 - s3) / s3 > 0.10) & (((s1 > s1.shift()) & (s2 > s2.shift())) | (v / v.rolling(21).mean() > 1.2))
        sig = ok & ~ok.shift(1, fill_value=False)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(~susun) | (s1 < s1.shift()))


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

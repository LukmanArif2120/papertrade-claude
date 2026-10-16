try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M124'
NAMA = "'Last' Stochastic Technique (ChartSchool)"
VARIAN = 'V1 WFO beku: henti ATR2, keluar CHAN3, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M124.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K157. Minggu lepas = minggu kalendar lengkap sebelumnya. Exit asal (andaian katalog): %K < 50 dan tutup < tutup terendah minggu lepas. Tiada henti asal.

def _entri(fr, idx):
    for g in fr.values():
        c = g.close; k = stoch_k(g, 39, 3)
        tinggi = mingguan_lalu(g, lambda gb: gb.close.max())
        rendah = mingguan_lalu(g, lambda gb: gb.close.min())
        sig = (k > 50) & (k.shift() <= 50) & (c > tinggi)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(k < 50) & (c < rendah))


HENTI_KOD = 'ATR2'
KELUAR_KOD = 'CHAN3'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

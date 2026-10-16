try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M115'
NAMA = 'Bow Tie (Landry)'
VARIAN = 'V1 WFO beku: henti ASAL, keluar ASAL, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 60
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M115.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K145. Andaian: "berkipas dalam 3–5 bar" = susunan SMA10>EMA20>EMA30 baru bermula 3–5 bar sebelum bar undur; undur = tutup & high < semalam; pencetus tutup > high bar undur.

def _entri(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        susun = (sma(c, 10) > ema(c, 20)) & (ema(c, 20) > ema(c, 30))
        run = susun.groupby((~susun).cumsum()).cumsum()           # bar berturut tersusun
        naik = c > c.shift()
        undur = (c < c.shift()) & (h < h.shift())
        persediaan = susun & undur & naik.shift(1, fill_value=False) & naik.shift(2, fill_value=False) & run.shift(1).between(3, 5)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1)) & susun
        siap_lajur(g, sig & ~langkau(g, stop), stop)


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

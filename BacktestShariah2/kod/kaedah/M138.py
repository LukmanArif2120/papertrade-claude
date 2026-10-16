try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M138'
NAMA = "直升机空中加油 (Helikopter isi minyak di udara)"
VARIAN = 'V1 WFO beku: henti ATR4, keluar TIADA, tmax 63'
TMAX = 63
WARM = 40
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 40
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M138.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K224. Andaian: >= 5 lilin naik berturut (tutup > tutup semalam) dengan volum purata larian > purata 20 hari sebelumnya; kemudian lilin turun kecil (tutup < buka, badan < 0.5 x purata badan larian) dengan volum < 0.5 x purata volum larian; isyarat pada tutup lilin turun. Exit asal: volum > 3 x purata 20 hari (andaian "sangat besar"). Untung >10% tidak dimodelkan (WFO).

def _entri(fr, idx):
    for g in fr.values():
        o, c, v = g.open, g.close, g.volume
        naik = c > c.shift()
        run = naik.groupby((~naik).cumsum()).cumsum()
        r = run.shift(1).fillna(0)
        vrun = v.shift(1).rolling(5).mean(); brun = (c - o).abs().shift(1).rolling(5).mean()
        v20 = v.shift(6).rolling(20).mean()
        turun = (c < o) & ((o - c) < 0.5 * brun) & (v < 0.5 * vrun)
        sig = (r >= 5) & (vrun > v20) & turun
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=v > 3 * v.rolling(20).mean().shift(1))


HENTI_KOD = 'ATR4'
KELUAR_KOD = 'TIADA'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

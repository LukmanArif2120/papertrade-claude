try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
from enjin import atr
import numpy as np, pandas as pd

ID = 'M132'
NAMA = "Ascending Scallop (Bulkowski)"
VARIAN = 'V1 WFO beku: henti ATR4, keluar CHAN4, tmax 42'
TMAX = 42
WARM = 120
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 120
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M132.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K193. Aliran naik (andaian, sama bagi modul ini) = tutup > SMA50 dan SMA50 > SMA50 20 hari lepas. KABUR: bentuk J dikesan secara angka (andaian): puncak kiri = high tertinggi 60 hari sebelum lembah; lembah = low terendah 40 hari, 5–40 bar selepas puncak; kedalaman 8–35%; pencetus tutup > puncak kiri (puncak kanan lebih tinggi). Henti bawah lembah. Sasaran 62% tidak dimodelkan.

def _entri(fr, idx):
    for g in fr.values():
        h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
        s50 = sma(g.close, 50); naik = ((g.close > s50) & (s50 > s50.shift(20))).values
        sig = np.zeros(n, bool); stop = np.full(n, np.nan)
        for i in range(100, n):
            if not naik[i]: continue
            w = slice(i - 40, i); t = i - 40 + int(np.argmin(l[w])); lv = l[t]
            if i - t < 3: continue
            a0 = max(0, t - 60); a1 = t - 5
            if a1 <= a0: continue
            pk = a0 + int(np.argmax(h[a0:a1])); pv = h[pk]
            if t - pk > 40: continue
            dalam = (pv - lv) / pv
            if not (0.08 <= dalam <= 0.35): continue
            if c[i] > pv and c[i - 1] <= pv and h[t:i].max() <= pv * 1.02:
                sig[i] = True; stop[i] = lv
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s)


HENTI_KOD = 'ATR4'
KELUAR_KOD = 'CHAN4'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

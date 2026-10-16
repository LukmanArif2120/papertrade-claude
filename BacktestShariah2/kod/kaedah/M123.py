try:
    from kaedah._k145 import *
except ImportError:
    from _k145 import *
import numpy as np, pandas as pd

ID = 'M123'
NAMA = 'CCI Correction (Lambert, ChartSchool)'
VARIAN = 'V1 WFO beku: henti LOW1, keluar SMA50, tmax tiada'
TMAX = None
WARM = 200
ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang
SILANG = False
PERLU_BAR = 200
# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/M123.py.
# Sumber: BacktestShariah2/spec/KATALOG_K145.md baris K156. Bias mingguan dikira atas minggu LENGKAP sebelumnya (CCI20 mingguan > +100 hidupkan, < −100 matikan). Isyarat: CCI20 harian pernah < −100 sejak kali terakhir di atas 0, kemudian silang atas 0. Exit asal (andaian katalog): CCI harian silang bawah +100. Tiada henti asal.

def _entri(fr, idx):
    for g in fr.values():
        wk = g.index.to_period('W-FRI')
        w = g.groupby(wk).agg(high=('high', 'max'), low=('low', 'min'), close=('close', 'last'))
        cw = cci(w.high, w.low, w.close, 20).values; b = np.zeros(len(cw), bool); st = False
        for j, v in enumerate(cw):
            if v > 100: st = True
            elif v < -100: st = False
            b[j] = st
        bias_w = pd.Series(b, w.index)
        bias = pd.Series(wk.map(lambda p: bias_w.get(p - 1, False)), g.index).astype(bool)
        cd = cci(g.high, g.low, g.close, 20).values; n = len(g); turun = False; sg = np.zeros(n, bool)
        for i in range(1, n):
            if cd[i] < -100: turun = True
            if turun and cd[i] > 0 and cd[i - 1] <= 0:
                sg[i] = True; turun = False
            elif cd[i] > 0: turun = False
        cds = pd.Series(cd, g.index)
        siap_lajur(g, pd.Series(sg, g.index) & bias, pd.Series(np.nan, g.index), exitc=(cds < 100) & (cds.shift() >= 100))


HENTI_KOD = 'LOW1'
KELUAR_KOD = 'SMA50'
# Gabungan stop/exit/tmax: pilihan WFO suku 2026Q4 (latih 2023-10-01..2026-09-30). Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M137.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'atr_kali_6': 6,
    'atr_14': 14,
    'len_ambang_2': 2,
    'atr_20': 20,
    'a_kali_4': 4,
    'nilai_2': 2,
    'rank_shift_63': 63,
    'henti_atr': 2.5,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
}
ID = 'M137'
NAMA = 'Livermore System'
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_atr_kali_6 = P['atr_kali_6']
    _p_atr_14 = P['atr_14']
    _p_len_ambang_2 = P['len_ambang_2']
    _p_atr_20 = P['atr_20']
    _p_a_kali_4 = P['a_kali_4']
    _p_nilai_2 = P['nilai_2']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        a = atr(g, n=_p_atr_14).values
        n = len(g)
        sig = np.zeros(n, bool)
        dem = np.full(n, np.nan)
        arah = 0
        ext = np.nan
        sup = []
        lo = np.nan
        for i in range(n):
            if np.isnan(a[i]):
                continue
            if arah >= 0:
                if np.isnan(ext) or h[i] > ext:
                    ext = h[i]
                if ext - l[i] >= _p_a_kali_4 * a[i]:
                    sup.append(ext)
                    arah = -1
                    ext = l[i]
            else:
                if l[i] < ext:
                    ext = l[i]
                if h[i] - ext >= _p_a_kali_4 * a[i]:
                    lo = ext
                    arah = 1
                    ext = h[i]
            dem[i] = lo
            if len(sup) >= _p_len_ambang_2 and c[i] > max(sup[-1], sup[-_p_nilai_2]) and (i == 0 or c[i - 1] <= max(sup[-1], sup[-_p_nilai_2])):
                sig[i] = True
        stop = g.close - _p_atr_kali_6 * atr(g, _p_atr_20)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop, exitc=g.close < pd.Series(dem, g.index), P=P)
HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'atr_kali_6': ('float', 3.0, 9.0),
    'atr_14': ('int', 7, 28),
    'atr_20': ('int', 10, 40),
    'a_kali_4': ('float', 2.0, 6.0),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.25, 3.75),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_chan': ('float', 2.0, 6.0),
    'keluar_chan_tinggi': ('int', 11, 44),
    'keluar_chan_atr': ('int', 11, 44),
}
TALA = ['henti_atr', 'keluar_chan', 'keluar_chan_tinggi', 'keluar_chan_atr', 'a_kali_4', 'atr_kali_6']

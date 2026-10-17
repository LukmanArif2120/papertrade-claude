# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M141.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_61': 61,
    'atr_14': 14,
    'i_ambang_15': 15,
    'rolling_60': 60,
    'a_kali_3': 3,
    'rank_shift_63': 63,
    'henti_atr': 2.5,
    'had_henti': 0.85,
    'tmax': 63,
}
ID = 'M141'
NAMA = 'First Thrust (Landry)'
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 63'
TMAX = 63
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_range_61 = P['range_61']
    _p_atr_14 = P['atr_14']
    _p_i_ambang_15 = P['i_ambang_15']
    _p_rolling_60 = P['rolling_60']
    _p_a_kali_3 = P['a_kali_3']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        a = atr(g, n=_p_atr_14).values
        n = len(g)
        lo60 = g.low.rolling(_p_rolling_60).min().values
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        t = -1
        dipakai = -1
        for i in range(_p_range_61, n):
            if l[i] <= lo60[i]:
                t = i
            if t < 0 or i - t > _p_i_ambang_15:
                continue
            k = i - 1
            if k <= t + 1 or t == dipakai:
                continue
            pertama = h[k] < h[k - 1] and all((h[j] >= h[j - 1] for j in range(t + 1, k)))
            if pertama and h[t:k].max() >= l[t] + _p_a_kali_3 * a[k] and (c[i] > h[k]):
                sig[i] = True
                stop[i] = l[k]
                dipakai = t
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, P=P)
HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

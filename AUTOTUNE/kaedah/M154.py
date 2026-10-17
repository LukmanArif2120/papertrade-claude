# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M154.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_21': 21,
    'i_tolak_20': 20,
    'naik_aliran_sma_50': 50,
    'naik_aliran_shift_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 2.5,
    'had_henti': 0.85,
    'tmax': 42,
}
ID = 'M154'
NAMA = 'HOLP (High of Low Period)'
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_range_21 = P['range_21']
    _p_i_tolak_20 = P['i_tolak_20']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        naik = naik_aliran(g.close, P=P).values
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        for i in range(_p_range_21, n):
            if not naik[i]:
                continue
            k = i - _p_i_tolak_20 + int(np.argmin(l[i - _p_i_tolak_20:i]))
            if c[i] > h[k] and (k + 1 > i - 1 or c[k + 1:i].max() <= h[k]):
                sig[i] = True
                stop[i] = l[k]
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st, P=P)
HENTI_KOD = 'ATR2.5'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'naik_aliran_sma_50': ('int', 25, 100),
    'naik_aliran_shift_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.25, 3.75),
    'had_henti': ('float', 0.425, 0.99),
    'tmax': ('int', 21, 60),
}
TALA = ['tmax', 'henti_atr', 'had_henti']

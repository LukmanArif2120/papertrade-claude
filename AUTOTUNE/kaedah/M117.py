# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M117.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'c_ambang_0_04': 0.04,
    'lp_ambang_2': 2,
    'p_lp_ambang_2_ambang_7': 7,
    'rolling_42': 42,
    'rank_shift_63': 63,
    'henti_atr': 3.0,
    'had_henti': 0.85,
}
ID = 'M117'
NAMA = 'Landry Pullback (high 2 bulan)'
VARIAN = 'V1 WFO beku: henti ATR3, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_c_ambang_0_04 = P['c_ambang_0_04']
    _p_lp_ambang_2 = P['lp_ambang_2']
    _p_p_lp_ambang_2_ambang_7 = P['p_lp_ambang_2_ambang_7']
    _p_rolling_42 = P['rolling_42']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        hh = h >= h.rolling(_p_rolling_42).max()
        lh = h < h.shift()
        L = lh.groupby((~lh).cumsum()).cumsum().astype(int)
        Lp = L.shift(1).fillna(0).astype(int).values
        hhv = hh.values
        n = len(g)
        puncak = np.zeros(n, bool)
        for i in range(n):
            p = i - 1 - Lp[i]
            if _p_lp_ambang_2 <= Lp[i] <= _p_p_lp_ambang_2_ambang_7 and p >= 0:
                puncak[i] = hhv[p]
        stop = l
        sig = pd.Series(puncak, g.index) & (c > h.shift(1)) & ((c - l) / c <= _p_c_ambang_0_04)
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR3'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

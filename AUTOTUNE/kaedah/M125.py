# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M125.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'shift_2': 2,
    'shift_3': 3,
    'rank_shift_63': 63,
    'henti_atr': 2.5,
    'had_henti': 0.85,
}
ID = 'M125'
NAMA = '2-Bar Breakout'
VARIAN = 'V1 WFO beku: henti ATR2.5, keluar ASAL, tmax tiada'
TMAX = None
WARM = 30
ADA_HENTI = True
SILANG = False
PERLU_BAR = 30

def _entri(fr, idx, *, P=PARAM):
    _p_shift_2 = P['shift_2']
    _p_shift_3 = P['shift_3']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        sig = (h.shift(1) > pd.concat([h.shift(_p_shift_2), h.shift(_p_shift_3)], axis=1).max(axis=1)) & (c > c.shift(1))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
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

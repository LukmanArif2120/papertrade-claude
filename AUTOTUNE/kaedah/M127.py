# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M127.py
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
    'rolling_42': 42,
    'rank_shift_63': 63,
    'henti_low': 1,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
}
ID = 'M127'
NAMA = 'Slingshot Bullish'
VARIAN = 'V1 WFO beku: henti LOW1, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_shift_2 = P['shift_2']
    _p_rolling_42 = P['rolling_42']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        A = h >= h.rolling(_p_rolling_42).max()
        sig = A.shift(_p_shift_2, fill_value=False) & (l.shift(1) < l.shift(_p_shift_2)) & (c > h.shift(_p_shift_2))
        stop = l.shift(1)
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'LOW1'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

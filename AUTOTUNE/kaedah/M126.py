# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M126.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_50': 50,
    'pos_ambang_0_25': 0.25,
    'shift_20': 20,
    'rolling_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 3.0,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M126'
NAMA = 'Hidden Smash Day (beli, Larry Williams)'
VARIAN = 'V1 WFO beku: henti ATR3, keluar SMA50, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_pos_ambang_0_25 = P['pos_ambang_0_25']
    _p_shift_20 = P['shift_20']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        s50 = sma(c, _p_sma_50)
        naik = (c > s50) & (s50 > s50.shift(_p_shift_20))
        pos = ((c - l) / (h - l)).where(h > l)
        smash = naik & (h >= h.rolling(_p_rolling_20).max()) & (pos <= _p_pos_ambang_0_25)
        stop = l.shift(1)
        sig = smash.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR3'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

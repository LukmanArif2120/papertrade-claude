# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M146.py
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
    'rolling_20': 20,
    'shift_3': 3,
    'rank_shift_63': 63,
    'henti_pct': 6,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M146'
NAMA = '3-Bar Momentum Pattern'
VARIAN = 'V1 WFO beku: henti PCT6, keluar SMA50, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_shift_2 = P['shift_2']
    _p_rolling_20 = P['rolling_20']
    _p_shift_3 = P['shift_3']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
        naik = lambda s: (s > s.shift(1)) & (s.shift(1) > s.shift(_p_shift_2))
        hijau = (c > o) & (c.shift() > o.shift()) & (c.shift(_p_shift_2) > o.shift(_p_shift_2))
        pecut = (c - c.shift() > c.shift() - c.shift(_p_shift_2)) & (h - h.shift() > h.shift() - h.shift(_p_shift_2))
        sig = naik(tr) & naik(c) & naik(l) & naik(h) & hijau & pecut & (h > h.shift(_p_shift_3).rolling(_p_rolling_20).max())
        stop = l.shift(_p_shift_2)
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT6'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M153.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'h_bahagi_2': 2,
    'rank_shift_63': 63,
    'henti_pct': 12,
    'had_henti': 0.85,
    'keluar_chan': 2,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
    'tmax': 10,
}
ID = 'M153'
NAMA = 'Range Leader'
VARIAN = 'V1 WFO beku: henti PCT12, keluar CHAN2, tmax 10'
TMAX = 10
WARM = 30
ADA_HENTI = True
SILANG = False
PERLU_BAR = 30

def _entri(fr, idx, *, P=PARAM):
    _p_h_bahagi_2 = P['h_bahagi_2']
    for g in fr.values():
        h, l = (g.high, g.low)
        mid = (h + l) / _p_h_bahagi_2
        sig = (h - l > (h - l).shift()) & (mid > h.shift())
        lk = (g.open.shift(-1) < mid).fillna(False)
        siap_lajur(g, sig & ~lk & ~langkau(g, l), l, P=P)
HENTI_KOD = 'PCT12'
KELUAR_KOD = 'CHAN2'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

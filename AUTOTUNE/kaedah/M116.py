# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M116.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'ema_20': 20,
    'shift_2': 2,
    'rank_shift_63': 63,
    'henti_pct': 10,
    'had_henti': 0.85,
    'tmax': 10,
}
ID = 'M116'
NAMA = '2/20 EMA Breakout (Landry)'
VARIAN = 'V1 WFO beku: henti PCT10, keluar TIADA, tmax 10'
TMAX = 10
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_ema_20 = P['ema_20']
    _p_shift_2 = P['shift_2']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        e20 = ema(c, _p_ema_20)
        dua = (l > e20) & (l.shift() > e20.shift())
        sig = dua.shift(1, fill_value=False) & (c > pd.concat([h.shift(1), h.shift(_p_shift_2)], axis=1).max(axis=1))
        siap_lajur(g, sig & ~langkau(g, e20), e20, exitc=c < e20, P=P)
HENTI_KOD = 'PCT10'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'ema_20': ('int', 10, 40),
    'shift_2': ('int', 2, 4),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 5.0, 15.0),
    'had_henti': ('float', 0.425, 0.99),
    'tmax': ('int', 5, 20),
}
TALA = ['tmax', 'henti_pct', 'had_henti', 'ema_20', 'shift_2']

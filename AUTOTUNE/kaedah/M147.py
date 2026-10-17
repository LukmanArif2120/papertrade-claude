# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M147.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'trix_9': 9,
    'ema_3': 3,
    'shift_2': 2,
    'shift_3': 3,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
}
ID = 'M147'
NAMA = 'Improved Three-Bar Pullback'
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_trix_9 = P['trix_9']
    _p_ema_3 = P['ema_3']
    _p_shift_2 = P['shift_2']
    _p_shift_3 = P['shift_3']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        t = trix(c, _p_trix_9)
        s = ema(t, _p_ema_3)
        tiga = (c < c.shift()) & (c.shift() < c.shift(_p_shift_2)) & (c.shift(_p_shift_2) < c.shift(_p_shift_3)) & (t > s)
        stop = l.shift(1)
        sig = tiga.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'trix_9': ('int', 4, 18),
    'ema_3': ('int', 2, 6),
    'shift_2': ('int', 2, 4),
    'shift_3': ('int', 2, 6),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 7.5, 22.5),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['henti_pct', 'had_henti', 'trix_9', 'ema_3', 'shift_2', 'shift_3']

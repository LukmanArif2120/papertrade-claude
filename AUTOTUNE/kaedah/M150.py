# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M150.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'ema_20': 20,
    'shift_2': 2,
    'r_kali_0_5': 0.5,
    'rank_shift_63': 63,
    'henti_pct': 12,
    'had_henti': 0.85,
    'keluar_sma': 20,
    'tmax': 21,
}
ID = 'M150'
NAMA = 'Trend Bar Failure (Brooks)'
VARIAN = 'V1 WFO beku: henti PCT12, keluar SMA20, tmax 21'
TMAX = 21
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_ema_20 = P['ema_20']
    _p_shift_2 = P['shift_2']
    _p_r_kali_0_5 = P['r_kali_0_5']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        e = ema(c, _p_ema_20)
        r = h - l
        A = (c < o) & (o - c > _p_r_kali_0_5 * r) & (e > e.shift())
        B = A.shift(1, fill_value=False) & (l < l.shift(1))
        stop = l.shift(1)
        sig = B.shift(1, fill_value=False) & (c > h.shift(_p_shift_2))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT12'
KELUAR_KOD = 'SMA20'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

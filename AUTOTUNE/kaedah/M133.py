# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M133.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_kali_2': 2,
    'sma_10': 10,
    'atr_kali_6': 6,
    'atr_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 2.0,
    'had_henti': 0.85,
    'keluar_sma': 50,
    'tmax': 21,
}
ID = 'M133'
NAMA = 'Bull Hook (Crabel)'
VARIAN = 'V1 WFO beku: henti ATR2, keluar SMA50, tmax 21'
TMAX = 21
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_sma_kali_2 = P['sma_kali_2']
    _p_sma_10 = P['sma_10']
    _p_atr_kali_6 = P['atr_kali_6']
    _p_atr_20 = P['atr_20']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        r = h - l
        hook = (o > h.shift()) & (c < c.shift()) & (r < r.shift())
        stretch = _p_sma_kali_2 * sma(pd.concat([h - o, o - l], axis=1).min(axis=1), _p_sma_10)
        sig = hook.shift(1, fill_value=False) & (c > o + stretch.shift(1))
        stop = c - _p_atr_kali_6 * atr(g, _p_atr_20)
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR2'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

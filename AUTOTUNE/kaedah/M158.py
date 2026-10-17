# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M158.py
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
    'adx_14': 14,
    'atr_kali_4': 4,
    'atr_20': 20,
    'rank_shift_63': 63,
    'henti_pct': 12,
    'had_henti': 0.85,
}
ID = 'M158'
NAMA = 'Doubly Adaptive Profit Targets'
VARIAN = 'V1 WFO beku: henti PCT12, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_adx_14 = P['adx_14']
    _p_atr_kali_4 = P['atr_kali_4']
    _p_atr_20 = P['atr_20']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        s50 = sma(c, _p_sma_50)
        ax = adx(g, _p_adx_14)
        A = (c > s50) & (ax > ax.shift())
        sig = A.shift(1, fill_value=False) & (o > h.shift(1)) & (l <= h.shift(1))
        stop = c - _p_atr_kali_4 * atr(g, _p_atr_20)
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < s50, P=P)
HENTI_KOD = 'PCT12'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

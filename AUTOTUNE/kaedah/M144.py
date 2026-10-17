# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M144.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'adr_ambang_0_04': 0.04,
    'rolling_20': 20,
    'atr_kali_4': 4,
    'sma_20': 20,
    'pos_ambang_0_1': 0.1,
    'sma_50': 50,
    'atr_14': 14,
    'rank_shift_63': 63,
    'henti_atr': 4.0,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M144'
NAMA = 'Screw Bar'
VARIAN = 'V1 WFO beku: henti ATR4, keluar SMA50, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_adr_ambang_0_04 = P['adr_ambang_0_04']
    _p_rolling_20 = P['rolling_20']
    _p_atr_kali_4 = P['atr_kali_4']
    _p_sma_20 = P['sma_20']
    _p_pos_ambang_0_1 = P['pos_ambang_0_1']
    _p_sma_50 = P['sma_50']
    _p_atr_14 = P['atr_14']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        pos = ((c - l) / (h - l)).where(h > l)
        adr = ((h - l) / c).rolling(_p_rolling_20).mean()
        sig = (pos.shift() <= _p_pos_ambang_0_1) & (o > h.shift()) & (c > h.shift()) & (c - sma(c, _p_sma_50) < _p_atr_kali_4 * atr(g, n=_p_atr_14)) & (adr >= _p_adr_ambang_0_04)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=c < sma(c, _p_sma_20), P=P)
HENTI_KOD = 'ATR4'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

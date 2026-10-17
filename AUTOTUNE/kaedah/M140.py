# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M140.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_60': 60,
    'float_ambang_40': 40,
    'c_ambang_0_045': 0.045,
    'h_kali_0_85': 0.85,
    'rolling_60': 60,
    'rolling_20': 20,
    'rolling_120': 120,
    'rank_shift_63': 63,
    'henti_atr': 3.0,
    'had_henti': 0.85,
    'keluar_sma': 50,
    'tmax': 63,
}
ID = 'M140'
NAMA = '猎豹出击 (Serangan Cheetah)'
VARIAN = 'V1 WFO beku: henti ATR3, keluar SMA50, tmax 63'
TMAX = 63
WARM = 120
ADA_HENTI = True
SILANG = False
PERLU_BAR = 120

def _entri(fr, idx, *, P=PARAM):
    _p_sma_60 = P['sma_60']
    _p_float_ambang_40 = P['float_ambang_40']
    _p_c_ambang_0_045 = P['c_ambang_0_045']
    _p_h_kali_0_85 = P['h_kali_0_85']
    _p_rolling_60 = P['rolling_60']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_120 = P['rolling_120']
    for g in fr.values():
        h, l, c, v = (g.high, g.low, g.close, g.volume)
        m60 = sma(c, _p_sma_60)
        jatuh = ((c < m60).shift(1).astype(float).rolling(_p_rolling_60).sum() >= _p_float_ambang_40) & (c.shift() <= _p_h_kali_0_85 * h.rolling(_p_rolling_120).max().shift())
        kering = v.rolling(_p_rolling_20).mean().shift(1) < v.rolling(_p_rolling_60).mean().shift(1)
        sig = jatuh & kering & (c > m60) & (c.shift() <= m60.shift()) & (c / c.shift() - 1 > _p_c_ambang_0_045)
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR3'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'sma_60': ('int', 30, 120),
    'float_ambang_40': ('int', 20, 60),
    'c_ambang_0_045': ('float', 0.0225, 0.0675),
    'h_kali_0_85': ('float', 0.425, 0.99),
    'rolling_60': ('int', 30, 120),
    'rolling_20': ('int', 10, 40),
    'rolling_120': ('int', 60, 240),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.5, 4.5),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_sma': ('int', 25, 100),
}
TALA = ['henti_atr', 'keluar_sma', 'had_henti', 'rolling_60', 'sma_60', 'float_ambang_40']

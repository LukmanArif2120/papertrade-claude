# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M155.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'stoch_k_13': 13,
    'stoch_k_d_8': 8,
    'stoch_k_21': 21,
    'stoch_k_d_13': 13,
    'stoch_k_34': 34,
    'stoch_k_d_21': 21,
    's1_ambang_0_1': 0.1,
    'v_ambang_1_2': 1.2,
    'rolling_21': 21,
    'rank_shift_63': 63,
    'henti_atr': 3.0,
    'had_henti': 0.85,
    'tmax': 21,
}
ID = 'M155'
NAMA = 'Market Cycle Strategy'
VARIAN = 'V1 WFO beku: henti ATR3, keluar TIADA, tmax 21'
TMAX = 21
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_stoch_k_13 = P['stoch_k_13']
    _p_stoch_k_d_8 = P['stoch_k_d_8']
    _p_stoch_k_21 = P['stoch_k_21']
    _p_stoch_k_d_13 = P['stoch_k_d_13']
    _p_stoch_k_34 = P['stoch_k_34']
    _p_stoch_k_d_21 = P['stoch_k_d_21']
    _p_s1_ambang_0_1 = P['s1_ambang_0_1']
    _p_v_ambang_1_2 = P['v_ambang_1_2']
    _p_rolling_21 = P['rolling_21']
    for g in fr.values():
        v = g.volume
        s1, s2, s3 = (stoch_k(g, _p_stoch_k_13, _p_stoch_k_d_8), stoch_k(g, _p_stoch_k_21, _p_stoch_k_d_13), stoch_k(g, _p_stoch_k_34, _p_stoch_k_d_21))
        susun = (s1 > s2) & (s2 > s3)
        ok = susun & ((s1 - s3) / s3 > _p_s1_ambang_0_1) & ((s1 > s1.shift()) & (s2 > s2.shift()) | (v / v.rolling(_p_rolling_21).mean() > _p_v_ambang_1_2))
        sig = ok & ~ok.shift(1, fill_value=False)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=~susun | (s1 < s1.shift()), P=P)
HENTI_KOD = 'ATR3'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

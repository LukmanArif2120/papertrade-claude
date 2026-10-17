# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M122.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'stoch_k_14': 14,
    'stoch_k_d_3': 3,
    'macd_hist_a_12': 12,
    'macd_hist_b_26': 26,
    'macd_hist_s_9': 9,
    'sma_20': 20,
    'sma_150': 150,
    'rolling_10': 10,
    'k_ambang_20': 20,
    'rank_shift_63': 63,
    'henti_low': 5,
    'had_henti': 0.85,
    'tmax': 42,
}
ID = 'M122'
NAMA = 'Moving Momentum (ChartSchool)'
VARIAN = 'V1 WFO beku: henti LOW5, keluar TIADA, tmax 42'
TMAX = 42
WARM = 170
ADA_HENTI = True
SILANG = False
PERLU_BAR = 170

def _entri(fr, idx, *, P=PARAM):
    _p_stoch_k_14 = P['stoch_k_14']
    _p_stoch_k_d_3 = P['stoch_k_d_3']
    _p_macd_hist_a_12 = P['macd_hist_a_12']
    _p_macd_hist_b_26 = P['macd_hist_b_26']
    _p_macd_hist_s_9 = P['macd_hist_s_9']
    _p_sma_20 = P['sma_20']
    _p_sma_150 = P['sma_150']
    _p_rolling_10 = P['rolling_10']
    _p_k_ambang_20 = P['k_ambang_20']
    for g in fr.values():
        c = g.close
        k = stoch_k(g, _p_stoch_k_14, _p_stoch_k_d_3)
        hist = macd_hist(c, a=_p_macd_hist_a_12, b=_p_macd_hist_b_26, s=_p_macd_hist_s_9)
        os_ = (k < _p_k_ambang_20).astype(float).rolling(_p_rolling_10).max() > 0
        tren = sma(c, _p_sma_20) > sma(c, _p_sma_150)
        sig = tren & os_ & (hist > 0) & (hist.shift() <= 0)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=~tren | (hist < 0), P=P)
HENTI_KOD = 'LOW5'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

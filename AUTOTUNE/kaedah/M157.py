# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M157.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'ema_10': 10,
    'ema_21': 21,
    'rolling_5': 5,
    'h_ambang_0_02': 0.02,
    'v_kali_0_8': 0.8,
    'adr5_ambang_0_03': 0.03,
    'shift_5': 5,
    'rolling_50': 50,
    'c_ambang_0_15': 0.15,
    'c_ambang_0_25': 0.25,
    'h_kali_0_85': 0.85,
    'shift_20': 20,
    'shift_40': 40,
    'rank_shift_63': 63,
    'henti_pct': 6,
    'had_henti': 0.85,
}
ID = 'M157'
NAMA = 'Consolidation Pivot Breakout (versi angka)'
VARIAN = 'V1 WFO beku: henti PCT6, keluar ASAL, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_ema_10 = P['ema_10']
    _p_ema_21 = P['ema_21']
    _p_rolling_5 = P['rolling_5']
    _p_h_ambang_0_02 = P['h_ambang_0_02']
    _p_v_kali_0_8 = P['v_kali_0_8']
    _p_adr5_ambang_0_03 = P['adr5_ambang_0_03']
    _p_shift_5 = P['shift_5']
    _p_rolling_50 = P['rolling_50']
    _p_c_ambang_0_15 = P['c_ambang_0_15']
    _p_c_ambang_0_25 = P['c_ambang_0_25']
    _p_h_kali_0_85 = P['h_kali_0_85']
    _p_shift_20 = P['shift_20']
    _p_shift_40 = P['shift_40']
    for g in fr.values():
        h, l, c, v = (g.high, g.low, g.close, g.volume)
        e10, e21 = (ema(c, _p_ema_10), ema(c, _p_ema_21))
        adr5 = ((h - l) / c).rolling(_p_rolling_5).mean()
        ok = ((c / c.shift(_p_shift_20) - 1 > _p_c_ambang_0_15) | (c / c.shift(_p_shift_40) - 1 > _p_c_ambang_0_25)) & (c >= _p_h_kali_0_85 * h.rolling(_p_rolling_50).max()) & (c > e10) & (c > e21) & (e10 > e21) & (e21 > e21.shift(_p_shift_5)) & (adr5 < _p_adr5_ambang_0_03) & ((h - l) / c < _p_h_ambang_0_02) & (v.rolling(_p_rolling_5).mean() < _p_v_kali_0_8 * v.rolling(_p_rolling_50).mean())
        stop = l.shift(1)
        sig = ok.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT6'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

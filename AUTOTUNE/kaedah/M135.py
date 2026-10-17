# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M135.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'dekat_ambang_2': 2,
    'shift_2': 2,
    'rolling_106': 106,
    'v_kali_1_5': 1.5,
    'rolling_20': 20,
    'paras_kali_0_97': 0.97,
    'rolling_126': 126,
    'shift_21': 21,
    'shift_4': 4,
    'shift_3': 3,
    'rank_shift_63': 63,
    'henti_low': 10,
    'had_henti': 0.85,
    'keluar_sma': 50,
    'tmax': 63,
}
ID = 'M135'
NAMA = '3rd Watch'
VARIAN = 'V1 WFO beku: henti LOW10, keluar SMA50, tmax 63'
TMAX = 63
WARM = 150
ADA_HENTI = True
SILANG = False
PERLU_BAR = 150

def _entri(fr, idx, *, P=PARAM):
    _p_dekat_ambang_2 = P['dekat_ambang_2']
    _p_shift_2 = P['shift_2']
    _p_rolling_106 = P['rolling_106']
    _p_v_kali_1_5 = P['v_kali_1_5']
    _p_rolling_20 = P['rolling_20']
    _p_paras_kali_0_97 = P['paras_kali_0_97']
    _p_rolling_126 = P['rolling_126']
    _p_shift_21 = P['shift_21']
    _p_shift_4 = P['shift_4']
    _p_shift_3 = P['shift_3']
    for g in fr.values():
        h, l, c, v = (g.high, g.low, g.close, g.volume)
        paras = h.shift(_p_shift_21).rolling(_p_rolling_106).max()
        senyap = h.shift(1).rolling(_p_rolling_20).max() <= paras
        piv = h.shift(_p_shift_2) > pd.concat([h.shift(_p_shift_4), h.shift(_p_shift_3), h.shift(1), h], axis=1).max(axis=1)
        dekat = piv & (h.shift(_p_shift_2) >= _p_paras_kali_0_97 * paras) & (h.shift(_p_shift_2) <= paras)
        sentuh = dekat.astype(float).rolling(_p_rolling_126).sum() >= _p_dekat_ambang_2
        sig = senyap & sentuh & (c > paras) & (v >= _p_v_kali_1_5 * v.rolling(_p_rolling_20).mean().shift(1))
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'LOW10'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'dekat_ambang_2': ('int', 1, 3),
    'shift_2': ('int', 2, 4),
    'rolling_106': ('int', 53, 212),
    'v_kali_1_5': ('float', 0.75, 2.25),
    'rolling_20': ('int', 10, 40),
    'paras_kali_0_97': ('float', 0.485, 0.99),
    'rolling_126': ('int', 63, 252),
    'shift_21': ('int', 10, 42),
    'shift_4': ('int', 2, 8),
    'shift_3': ('int', 2, 6),
    'rank_shift_63': ('int', 32, 126),
    'henti_low': ('int', 5, 20),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_sma': ('int', 25, 100),
}
TALA = ['henti_low', 'keluar_sma', 'had_henti', 'rolling_20', 'dekat_ambang_2', 'rolling_106']

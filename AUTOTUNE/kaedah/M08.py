# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M08.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_20': 20,
    'shift_5': 5,
    'rolling_10': 10,
    'l_kali_0_99': 0.99,
    's20_kali_1_05': 1.05,
    'rolling_6': 6,
    'sl20_ambang_0_01': 0.01,
    's20_kali_1_01': 1.01,
}
ID = 'M08'
NAMA = 'SMA20 + SMA200'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 220
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _asas(g, *, P=PARAM):
    c, h, l, o = (g.close, g.high, g.low, g.open)
    s20 = c.rolling(P['rolling_20']).mean()
    sl20 = s20 / s20.shift(P['shift_5']) - 1
    lonjak = h.shift(1).rolling(P['rolling_10']).max()
    return (s20, sl20, lonjak)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_s20_kali_1_05 = P['s20_kali_1_05']
    _p_rolling_6 = P['rolling_6']
    _p_sl20_ambang_0_01 = P['sl20_ambang_0_01']
    _p_s20_kali_1_01 = P['s20_kali_1_01']
    for g in fr.values():
        c, h, l, o = (g.close, g.high, g.low, g.open)
        s20, sl20, lonjak = _asas(g, P=P)
        stop = _p_l_kali_0_99 * l.rolling(_p_rolling_6).min()
        asas = (sl20 >= _p_sl20_ambang_0_01) & (l <= _p_s20_kali_1_01 * s20) & (c > s20) & (c > o) & (lonjak >= _p_s20_kali_1_05 * s20)
        bn = o.shift(-1)
        langkau = (bn <= stop) | (bn > _p_s20_kali_1_05 * s20)
        g['_s20'] = s20
        g['_sl20'] = sl20
        g['_lonjak'] = lonjak
        g['sig'] = (asas & ~langkau).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (s20 < s20.shift()).fillna(False)
        g['rank'] = sl20
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_20': ('int', 10, 40),
    'shift_5': ('int', 2, 10),
    'rolling_10': ('int', 5, 20),
    'l_kali_0_99': ('float', 0.495, 0.99),
    's20_kali_1_05': ('float', 0.525, 1.575),
    'rolling_6': ('int', 3, 12),
    'sl20_ambang_0_01': ('float', 0.01, 0.015),
    's20_kali_1_01': ('float', 0.505, 1.515),
}
TALA = ['rolling_20', 'l_kali_0_99', 'rolling_6', 's20_kali_1_05', 'rolling_10', 'sl20_ambang_0_01']

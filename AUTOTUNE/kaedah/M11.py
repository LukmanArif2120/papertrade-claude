# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M11.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_7': 7,
    'l_kali_0_99': 0.99,
    'rolling_20': 20,
    'shift_63': 63,
    'rolling_11': 11,
    'rolling_50': 50,
}
ID = 'M11'
NAMA = 'NR7 Breakout + Volume'
VARIAN = 'V3 V1+NR7 hari dalam (NR7-ID)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _nr7id(g, *, P=PARAM):
    R = g.high - g.low
    nr7 = R <= R.rolling(P['rolling_7']).min()
    dalam = (g.high <= g.high.shift(1)) & (g.low >= g.low.shift(1))
    return nr7 & dalam

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_rolling_20 = P['rolling_20']
    _p_shift_63 = P['shift_63']
    _p_rolling_11 = P['rolling_11']
    _p_rolling_50 = P['rolling_50']
    for g in fr.values():
        c, h, l, o, v = (g.close, g.high, g.low, g.open, g.volume)
        k = _nr7id(g, P=P)
        vs20 = v.rolling(_p_rolling_20).mean()
        stop = _p_l_kali_0_99 * l.rolling(_p_rolling_11).min()
        asas = k.shift(1).fillna(False).astype(bool) & (c > h.shift(1)) & (v > vs20)
        sig = asas & ~(o.shift(-1) <= stop)
        g['_k'] = k
        g['_vs20'] = vs20
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < c.rolling(_p_rolling_50).mean()).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

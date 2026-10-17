# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M35.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_10': 10,
    's10_kali_1_02': 1.02,
    'shift_63': 63,
    'rolling_50': 50,
    'rolling_200': 200,
}
ID = 'M35'
NAMA = 'Pocket Pivot Morales & Kacher'
VARIAN = 'V3 V1 DEKAT10 sahaja'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _vt10(c, v, *, P=PARAM):
    turun = c < c.shift()
    vt = v.where(turun, 0.0)
    return vt.shift(1).rolling(P['rolling_10'], min_periods=1).max().fillna(0.0)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_s10_kali_1_02 = P['s10_kali_1_02']
    _p_shift_63 = P['shift_63']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_200 = P['rolling_200']
    for g in fr.values():
        c, l, v = (g.close, g.low, g.volume)
        s10, s50, s200 = (c.rolling(_p_rolling_10).mean(), c.rolling(_p_rolling_50).mean(), c.rolling(_p_rolling_200).mean())
        vt10 = _vt10(c, v, P=P)
        pp = (c > c.shift()) & (v > vt10)
        dekat10 = (l <= _p_s10_kali_1_02 * s10) & (c > s10)
        sig = pp & (c > s50) & (c > s200) & dekat10
        bk = g.open.shift(-1)
        sig = sig & ((bk > l) | bk.isna())
        g['_s10'] = s10
        g['_s50'] = s50
        g['_s200'] = s200
        g['_vt10'] = vt10
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = l
        g['tgt'] = np.nan
        g['exitc'] = ((c.shift() < s10.shift()) & (l < l.shift())).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

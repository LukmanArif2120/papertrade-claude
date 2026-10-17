# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M28.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'ambang': 3.0,
    'h_bahagi_3': 3,
    'l_kali_0_99': 0.99,
    'atrw_14': 14,
    'l_kali_1_01': 1.01,
    'c_kali_2': 2,
    'h_kali_0_6': 0.6,
    'o_bahagi_2': 2,
    'rolling_20': 20,
    'tmax': 10,
}
ID = 'M28'
NAMA = 'VWAP Separator + Kiss Pivot'
VARIAN = 'V2 Pemisahan ≥3 ATR'
TMAX = 10
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
AMBANG = 3.0

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_ambang = P['ambang']
    _p_h_bahagi_3 = P['h_bahagi_3']
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_atrw_14 = P['atrw_14']
    _p_l_kali_1_01 = P['l_kali_1_01']
    _p_c_kali_2 = P['c_kali_2']
    _p_h_kali_0_6 = P['h_kali_0_6']
    _p_o_bahagi_2 = P['o_bahagi_2']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        tp = (h + l + c) / _p_h_bahagi_3
        vw = (tp * v).rolling(_p_rolling_20).sum() / v.rolling(_p_rolling_20).sum()
        a = _atrw(g, n=_p_atrw_14, P=P)
        sepdn = (vw - l) / a
        lvl = l <= _p_l_kali_1_01 * l.shift(1).rolling(_p_rolling_20).min()
        jw = (np.minimum(o, c) - l >= _p_c_kali_2 * (c - o).abs()) & (c - l >= _p_h_kali_0_6 * (h - l))
        eg = (c > o) & (c.shift() < o.shift()) & (c >= o.shift()) & (o <= c.shift())
        pt = (o.shift() - c.shift() >= a.shift()) & (c >= (o.shift() + c.shift()) / _p_o_bahagi_2)
        rev = jw | eg | pt
        stop = _p_l_kali_0_99 * l
        on = o.shift(-1)
        sig = (sepdn >= _p_ambang) & lvl & rev & (c < vw)
        sig = sig & ~(on <= stop) & ~(on >= vw)
        g['_sepdn'] = sepdn
        g['_lvl'] = lvl.fillna(False)
        g['_vw'] = vw
        g['_rev'] = rev.fillna(False)
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = vw
        g['exitc'] = False
        g['rank'] = sepdn
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

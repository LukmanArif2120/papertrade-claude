# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M70.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_50': 50,
    'rolling_200': 200,
    'shift_63': 63,
    'ewm_span_10': 10,
    'ewm_span_21': 21,
}
ID = 'M70'
NAMA = 'Pecahan Hari Dalam'
VARIAN = 'V5 V1 masuk awal tanpa pengesahan'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_50 = P['rolling_50']
    _p_rolling_200 = P['rolling_200']
    _p_shift_63 = P['shift_63']
    _p_ewm_span_10 = P['ewm_span_10']
    _p_ewm_span_21 = P['ewm_span_21']
    for g in fr.values():
        c = g.close
        e10 = c.ewm(span=_p_ewm_span_10, adjust=False).mean()
        e21 = c.ewm(span=_p_ewm_span_21, adjust=False).mean()
        s50 = c.rolling(_p_rolling_50).mean()
        s200 = c.rolling(_p_rolling_200).mean()
        dalam = (g.high < g.high.shift()) & (g.low > g.low.shift()) & (g.high > g.low)
        atasma = (c > e10) & (c > e21) & (c > s50) & (c > s200)
        stop = g.low.copy()
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_dalam'] = dalam
        g['_atasma'] = atasma
        g['_e10'] = e10
        g['_e21'] = e21
        g['_s50'] = s50
        g['_s200'] = s200
        g['sig'] = dalam & atasma & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_50': ('int', 25, 100),
    'rolling_200': ('int', 100, 400),
    'shift_63': ('int', 32, 126),
    'ewm_span_10': ('int', 5, 20),
    'ewm_span_21': ('int', 10, 42),
}
TALA = ['rolling_50', 'rolling_200', 'ewm_span_10', 'ewm_span_21']

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M14.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'shift_2': 2,
    'rolling_50': 50,
}
ID = 'M14'
NAMA = 'Walking with the Whales'
VARIAN = 'V3 V1 pegang ikut SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_2 = P['shift_2']
    _p_rolling_50 = P['rolling_50']
    for g in fr.values():
        c, h, l, o = (g.close, g.high, g.low, g.open)
        s50 = c.rolling(_p_rolling_50).mean()
        Lhi = np.maximum(l.shift(1), l.shift(_p_shift_2))
        Llo = np.minimum(l.shift(1), l.shift(_p_shift_2))
        Hhi = np.maximum(h.shift(1), h.shift(_p_shift_2))
        stop = np.minimum(l, Llo)
        asas = (l <= Lhi) & (c > Llo) & (c > s50)
        sig = asas & ~(o.shift(-1) <= stop)
        g['_s50'] = s50
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = (Hhi - c) / (c - stop)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M23.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_126': 126,
    'rolling_50': 50,
    'vs50_kali_1_5': 1.5,
    'rolling_20': 20,
}
ID = 'M23'
NAMA = 'Breitstein Kapitulasi + Kesinambungan'
VARIAN = 'V5 V4 keluar close<SMA20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_126 = P['rolling_126']
    _p_rolling_50 = P['rolling_50']
    _p_vs50_kali_1_5 = P['vs50_kali_1_5']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        o, h, c, v = (g.open, g.high, g.close, g.volume)
        R = h.shift(1).rolling(_p_rolling_126).max()
        VS50 = v.rolling(_p_rolling_50).mean()
        sig = (c > R) & (c.shift() <= R.shift()) & (v >= _p_vs50_kali_1_5 * VS50)
        lk = (o.shift(-1) <= R).fillna(False)
        g['_R'] = R
        g['_VS50'] = VS50
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = R
        g['tgt'] = np.nan
        g['exitc'] = c < c.rolling(_p_rolling_20).mean()
        g['rank'] = v / VS50
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_126': ('int', 63, 252),
    'rolling_50': ('int', 25, 100),
    'vs50_kali_1_5': ('float', 0.75, 2.25),
    'rolling_20': ('int', 10, 40),
}
TALA = ['rolling_20', 'rolling_126', 'rolling_50', 'vs50_kali_1_5']

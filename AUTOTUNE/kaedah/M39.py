# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M39.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_100': 100,
    'sd_kali_2': 2,
    'c_kali_0_85': 0.85,
    'shift_63': 63,
}
ID = 'M39'
NAMA = 'Radge Pecahan Bollinger 100 hari'
VARIAN = 'V4 V1 jalur atas 2 SD'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 205

def _jalur(g, *, P=PARAM):
    c = g.close
    m = c.rolling(P['rolling_100']).mean()
    sd = c.rolling(P['rolling_100']).std(ddof=0)
    return (m, sd)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_sd_kali_2 = P['sd_kali_2']
    _p_c_kali_0_85 = P['c_kali_0_85']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c = g.close
        m, sd = _jalur(g, P=P)
        atas2 = m + _p_sd_kali_2 * sd
        bawah = m - sd
        lintas = (c > atas2) & (c.shift() <= atas2.shift())
        g['_atas2'] = atas2
        g['_bawah'] = bawah
        stop = np.maximum(bawah, _p_c_kali_0_85 * c)
        g['sig'] = lintas & ~(g.open.shift(-1) <= stop)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < bawah
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

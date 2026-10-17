# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M46.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'atr_40': 40,
    'rolling_200': 200,
    'rolling_50': 50,
    'shift_31': 31,
    'vol50_kali_1_5': 1.5,
    'a40_kali_0_75': 0.75,
    'shift_63': 63,
}
ID = 'M46'
NAMA = 'Jurang Naik Boleh Beli (Buyable Gap Up)'
VARIAN = 'V2 V1 dengan jurang ketat (low>high semalam+0.75xATR40)'
TMAX = None
WARM = 231
ADA_HENTI = True
SILANG = False
PERLU_BAR = 240

def _asas(g, *, P=PARAM):
    c = g.close
    a40 = atr(g, P['atr_40'])
    vol50 = g.volume.rolling(P['rolling_50']).mean().shift(1)
    s200 = c.rolling(P['rolling_200']).mean()
    s50 = c.rolling(P['rolling_50']).mean()
    aliran = (c.shift() > s200.shift()) & (s200.shift() > s200.shift(P['shift_31']))
    return (a40, vol50, s50, aliran)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_vol50_kali_1_5 = P['vol50_kali_1_5']
    _p_a40_kali_0_75 = P['a40_kali_0_75']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c = g.close
        a40, vol50, s50, aliran = _asas(g, P=P)
        ketat = g.low > g.high.shift() + _p_a40_kali_0_75 * a40.shift()
        taktutup = g.low > c.shift()
        volum = g.volume >= _p_vol50_kali_1_5 * vol50
        sig = ketat & taktutup & volum & aliran & (c > s50)
        stop = g.low
        g['sig'] = sig & ~(g.open.shift(-1) <= stop)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_a40'] = a40
        g['_vol50'] = vol50
        g['_s50'] = s50
        g['_aliran'] = aliran
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'atr_40': ('int', 20, 80),
    'rolling_200': ('int', 100, 400),
    'rolling_50': ('int', 25, 100),
    'shift_31': ('int', 16, 62),
    'vol50_kali_1_5': ('float', 0.75, 2.25),
    'a40_kali_0_75': ('float', 0.375, 0.99),
    'shift_63': ('int', 32, 126),
}
TALA = ['rolling_50', 'atr_40', 'rolling_200', 'vol50_kali_1_5', 'a40_kali_0_75', 'shift_31']

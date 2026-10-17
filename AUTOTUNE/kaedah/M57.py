# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M57.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'c_ambang_0_15': 0.15,
    'shift_10': 10,
    'rolling_10': 10,
    'rolling_63': 63,
    'shift_63': 63,
    'aliran_lag_2': 2,
    'rolling_50': 50,
    'shift_2': 2,
}
ID = 'M57'
NAMA = 'Landry Trend Knockout (TKO)'
VARIAN = 'V1 Dikunci (keluar tutup<SMA50)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _aliran(g, s50, lag, *, P=PARAM):
    c, h = (g.close, g.high)
    a = (c > s50) & (s50 > s50.shift(P['shift_10'])) & (c / c.shift(P['shift_63']) - 1 >= P['c_ambang_0_15']) & (h.rolling(P['rolling_10']).max() >= h.rolling(P['rolling_63']).max())
    return a.shift(lag).fillna(False).astype(bool)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_aliran_lag_2 = P['aliran_lag_2']
    _p_rolling_50 = P['rolling_50']
    _p_shift_2 = P['shift_2']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        s50 = g.close.rolling(_p_rolling_50).mean()
        lo = g.low
        ko = lo < np.minimum(lo.shift(1), lo.shift(_p_shift_2))
        ko1 = ko.shift(1).fillna(False).astype(bool)
        aliran = _aliran(g, s50, _p_aliran_lag_2, P=P)
        sah = ko1 & (g.high > g.high.shift(1))
        stop = np.minimum(lo.shift(1), lo)
        sig = aliran & sah & (g.close > s50)
        langkau = g.open.shift(-1) <= stop
        g['_aliran1'] = _aliran(g, s50, 1, P=P)
        g['_ko'] = ko & (g.close > s50)
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'c_ambang_0_15': ('float', 0.075, 0.225),
    'shift_10': ('int', 5, 20),
    'rolling_10': ('int', 5, 20),
    'rolling_63': ('int', 32, 126),
    'shift_63': ('int', 32, 126),
    'aliran_lag_2': ('int', 2, 4),
    'rolling_50': ('int', 25, 100),
    'shift_2': ('int', 2, 4),
}
TALA = ['rolling_50', 'c_ambang_0_15', 'rolling_10', 'rolling_63', 'aliran_lag_2', 'shift_63']

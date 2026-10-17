# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M102.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_3': 3,
    'rolling_50': 50,
    'rolling_7': 7,
    'rolling_65': 65,
    'r_ambang_0_02': 0.02,
    'fillna_1000000000_0': 1000000000.0,
    'shift_63': 63,
    'ti65_ambang_1_05': 1.05,
    'minv_ambang_100000': 100000,
    'c_ambang_3': 3,
}
ID = 'M102'
NAMA = 'Stockbee SLTB'
VARIAN = 'V5 V1 + volum hari ini > semalam'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _asas(g, *, P=PARAM):
    c = g.close
    R = c / c.shift(1) - 1
    ti65 = c.rolling(P['rolling_7']).mean() / c.rolling(P['rolling_65']).mean()
    minv = g.volume.shift(1).rolling(P['rolling_3']).min()
    s50 = c.rolling(P['rolling_50']).mean()
    return (R, ti65, minv, s50)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_r_ambang_0_02 = P['r_ambang_0_02']
    _p_fillna_1000000000_0 = P['fillna_1000000000_0']
    _p_shift_63 = P['shift_63']
    _p_ti65_ambang_1_05 = P['ti65_ambang_1_05']
    _p_minv_ambang_100000 = P['minv_ambang_100000']
    _p_c_ambang_3 = P['c_ambang_3']
    for g in fr.values():
        R, ti65, minv, s50 = _asas(g, P=P)
        c = g.close
        sltb = (minv >= _p_minv_ambang_100000) & (c >= _p_c_ambang_3) & (ti65 >= _p_ti65_ambang_1_05) & (c > g.open) & (c > c.shift(1)) & (R > R.shift(1)) & (R.shift(1) < _p_r_ambang_0_02)
        sig = sltb & (c > s50) & (g.volume > g.volume.shift(1))
        stop = g.low.copy()
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_ti65'] = ti65
        g['_minv'] = minv
        g['_s50'] = s50
        g['_R'] = R
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = (c / c.shift(_p_shift_63) - 1).fillna(-_p_fillna_1000000000_0)

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_3': ('int', 2, 6),
    'rolling_50': ('int', 25, 100),
    'rolling_7': ('int', 4, 14),
    'rolling_65': ('int', 32, 130),
    'r_ambang_0_02': ('float', 0.01, 0.03),
    'shift_63': ('int', 32, 126),
    'ti65_ambang_1_05': ('float', 0.525, 1.575),
    'minv_ambang_100000': ('int', 50000, 150000),
    'c_ambang_3': ('int', 2, 4),
}
TALA = ['rolling_50', 'rolling_3', 'rolling_7', 'rolling_65', 'r_ambang_0_02', 'ti65_ambang_1_05']

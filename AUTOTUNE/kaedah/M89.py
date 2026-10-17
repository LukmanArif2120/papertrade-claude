# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M89.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'shift_10': 10,
    'rma_atr_kali_2': 2,
    'rolling_65': 65,
    'shift_2': 2,
    'shift_3': 3,
    'shift_63': 63,
    'rma_atr_14': 14,
    'rolling_14': 14,
}
ID = 'M89'
NAMA = 'Chande 65sma-3cc'
VARIAN = 'V5 V1+SMA65 naik (>SMA65 10h lalu)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 220

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_10 = P['shift_10']
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_rolling_65 = P['rolling_65']
    _p_shift_2 = P['shift_2']
    _p_shift_3 = P['shift_3']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_rolling_14 = P['rolling_14']
    for g in fr.values():
        c = g.close
        s65 = c.rolling(_p_rolling_65).mean()
        atas = c > s65
        tiga = atas & atas.shift(1, fill_value=False) & atas.shift(_p_shift_2, fill_value=False) & (c.shift(_p_shift_3) <= s65.shift(_p_shift_3))
        naik = s65 > s65.shift(_p_shift_10)
        g['_s65'] = s65
        g['_naik'] = naik
        g['sig'] = tiga & naik
        g['stop'] = c - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = c < g.low.rolling(_p_rolling_14).min().shift(1)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

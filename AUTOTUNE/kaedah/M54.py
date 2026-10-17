# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M54.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_10': 10,
    'rolling_5': 5,
    'shift_5': 5,
    'rolling_50': 50,
    'ewm_span_21': 21,
    'rma_atr_kali_2': 2,
    'shift_63': 63,
    'rma_atr_14': 14,
    'rolling_20': 20,
}
ID = 'M54'
NAMA = 'IBD Power Trend'
VARIAN = 'V4 V1 sig=PT benar & tutup>high 20 hari'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _pt(g, *, P=PARAM):
    e21 = g.close.ewm(span=P['ewm_span_21'], adjust=False).mean()
    s50 = g.close.rolling(P['rolling_50']).mean()
    k1 = (g.low > e21).astype(int).rolling(P['rolling_10']).sum() == P['rolling_10']
    k2 = (e21 > s50).astype(int).rolling(P['rolling_5']).sum() == P['rolling_5']
    k3 = s50 > s50.shift(P['shift_5'])
    k4 = g.close > g.close.shift()
    mula_ok = (k1 & k2 & k3 & k4).values
    tamat = (e21 < s50).values
    pt = np.zeros(len(g), bool)
    for i in range(1, len(g)):
        if not pt[i - 1] and mula_ok[i]:
            pt[i] = True
        elif tamat[i]:
            pt[i] = False
        else:
            pt[i] = pt[i - 1]
    return (pd.Series(pt, g.index), e21, s50)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        pt, e21, s50 = _pt(g, P=P)
        hh20 = g.high.rolling(_p_rolling_20).max().shift(1)
        g['_pt'] = pt
        g['_hh20'] = hh20
        g['sig'] = pt & (g.close > hh20)
        g['stop'] = g.close - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = e21 < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_10': ('int', 5, 20),
    'rolling_5': ('int', 2, 10),
    'shift_5': ('int', 2, 10),
    'rolling_50': ('int', 25, 100),
    'ewm_span_21': ('int', 10, 42),
    'rma_atr_kali_2': ('float', 1.0, 3.0),
    'shift_63': ('int', 32, 126),
    'rma_atr_14': ('int', 7, 28),
    'rolling_20': ('int', 10, 40),
}
TALA = ['rma_atr_kali_2', 'rma_atr_14', 'rolling_50', 'ewm_span_21', 'rolling_10', 'rolling_5']

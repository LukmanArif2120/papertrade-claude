# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M74.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_50': 50,
    'rolling_150': 150,
    'rolling_200': 200,
    'rolling_252': 252,
    'shift_21': 21,
    'l252_kali_1_3': 1.3,
    'h252_kali_0_75': 0.75,
    'rma_atr_kali_1_5': 1.5,
    'shift_63': 63,
    'rma_atr_14': 14,
    'rolling_20': 20,
}
ID = 'M74'
NAMA = 'Lulus Baharu Trend Template Minervini'
VARIAN = 'V2 V1 tanpa S8 (7 syarat harga)'
TMAX = None
WARM = 275
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _syarat(g, *, P=PARAM):
    c = g.close
    s50 = c.rolling(P['rolling_50']).mean()
    s150 = c.rolling(P['rolling_150']).mean()
    s200 = c.rolling(P['rolling_200']).mean()
    h252 = g.high.rolling(P['rolling_252']).max()
    l252 = g.low.rolling(P['rolling_252']).min()
    S = pd.DataFrame({'S1': (c > s150) & (c > s200), 'S2': s150 > s200, 'S3': s200 > s200.shift(P['shift_21']), 'S4': (s50 > s150) & (s50 > s200), 'S5': c > s50, 'S6': c >= P['l252_kali_1_3'] * l252, 'S7': c >= P['h252_kali_0_75'] * h252}, index=g.index)
    return (S, s50, s150, s200, h252, l252)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_kali_1_5 = P['rma_atr_kali_1_5']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        S, s50, s150, s200, h252, l252 = _syarat(g, P=P)
        lulus = S.all(axis=1)
        sebelum = lulus.astype(int).shift(1).rolling(_p_rolling_20, min_periods=1).sum().fillna(0) > 0
        baharu = lulus & ~sebelum
        stop = np.maximum(g.close - _p_rma_atr_kali_1_5 * _rma_atr(g, n=_p_rma_atr_14, P=P), s50)
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_bil'] = S.sum(axis=1)
        g['_lulus'] = lulus
        g['_sebelum'] = sebelum
        g['_s50'] = s50
        g['_s150'] = s150
        g['_s200'] = s200
        g['_h252'] = h252
        g['_l252'] = l252
        g['sig'] = baharu & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

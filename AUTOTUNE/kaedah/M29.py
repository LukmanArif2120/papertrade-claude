# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M29.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'p1': 50,
    'p2': 110,
    'p3': 250,
    'rsi_75': 75,
    'c_kali_100': 100,
    'rolling_3': 3,
    'shift_5': 5,
    'rolling_14': 14,
    'rolling_6': 6,
    'k_ambang_20': 20,
    'z_kali_0_99': 0.99,
    'r75_ambang_50': 50,
}
ID = 'M29'
NAMA = 'EMA3 + RSI75 + Stokastik'
VARIAN = 'V4 V1 EMA 50/110/250'
TMAX = None
WARM = 300
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320
P1, P2, P3 = (50, 110, 250)

def _komponen(g, *, P=PARAM):
    _p_rolling_6 = P['rolling_6']
    c, h, l = (g.close, g.high, g.low)
    ema = lambda k: c.ewm(span=k, adjust=False).mean()
    e1, e2, e3 = (ema(P['p1']), ema(P['p2']), ema(P['p3']))
    r75 = rsi(c, P['rsi_75'])
    fk = P['c_kali_100'] * (c - l.rolling(P['rolling_14']).min()) / (h.rolling(P['rolling_14']).max() - l.rolling(P['rolling_14']).min())
    K = fk.rolling(P['rolling_3']).mean()
    D = K.rolling(P['rolling_3']).mean()
    z = pd.Series(np.nan, g.index)
    for ee in (e1, e2, e3):
        sentuh = (l - ee).rolling(_p_rolling_6).min() <= 0
        z = z.where(~sentuh, ee)
    susun = (e1 > e2) & (e2 > e3) & (e1 > e1.shift(P['shift_5'])) & (e2 > e2.shift(P['shift_5'])) & (e3 > e3.shift(P['shift_5']))
    return (e1, e2, e3, r75, K, D, z, susun)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_k_ambang_20 = P['k_ambang_20']
    _p_z_kali_0_99 = P['z_kali_0_99']
    _p_rolling_6 = P['rolling_6']
    _p_r75_ambang_50 = P['r75_ambang_50']
    for g in fr.values():
        o, c = (g.open, g.close)
        e1, e2, e3, r75, K, D, z, susun = _komponen(g, P=P)
        silang = (K.shift() <= D.shift()) & (K > D)
        k20 = K.rolling(_p_rolling_6).min() < _p_k_ambang_20
        sig = susun & (r75 > _p_r75_ambang_50) & z.notna() & (c > e3) & k20 & silang
        stop = _p_z_kali_0_99 * z
        sig = sig & ~(o.shift(-1) <= stop)
        g['_pers'] = (susun & (r75 > _p_r75_ambang_50) & z.notna() & (c > e3)).fillna(False)
        g['_e1'] = e1
        g['_e2'] = e2
        g['_e3'] = e3
        g['_k20'] = k20.fillna(False)
        g['_K'] = K
        g['_D'] = D
        g['_z'] = z
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ((c < e3) | (r75 < _p_r75_ambang_50)).fillna(False)
        g['rank'] = r75
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

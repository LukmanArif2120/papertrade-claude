# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M32.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'r_ambang_0_02': 0.02,
    'r_ambang_0_04': 0.04,
    'rolling_50': 50,
    'h_kali_0_8': 0.8,
    'rolling_20': 20,
    'shift_2': 2,
    'shift_6': 6,
    'rolling_3': 3,
    'shift_64': 64,
    'shift_3': 3,
    'clv_ambang_0_75': 0.75,
    'shift_63': 63,
}
ID = 'M32'
NAMA = 'Momentum Burst'
VARIAN = 'V2 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _komponen(g, *, P=PARAM):
    o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
    R = c / c.shift() - 1
    adr = (h / l).rolling(P['rolling_20']).mean() - 1
    rng = h - l
    clv = ((c - l) / rng).where(rng > 0, 0.0)
    s50 = c.rolling(P['rolling_50']).mean()
    burst = (R >= P['r_ambang_0_04']) & (v > v.shift())
    sempit = R.shift(1) < P['r_ambang_0_02']
    bukan3 = ~((R.shift(1) > 0) & (R.shift(P['shift_2']) > 0))
    a1 = adr.shift(1)
    rehat = (R.shift(1).abs() < a1) & (R.shift(P['shift_2']).abs() < a1) & (R.shift(P['shift_3']).abs() < a1) & (l.shift(1).rolling(P['rolling_3']).min() >= P['h_kali_0_8'] * h.shift(1).rolling(P['rolling_20']).max())
    aliran = (c.shift(1) > s50.shift(1)) & (s50.shift(1) > s50.shift(P['shift_6'])) & (c.shift(1) / c.shift(P['shift_64']) - 1 > 0)
    return dict(R=R, clv=clv, s50=s50, burst=burst, sempit=sempit, bukan3=bukan3, rehat=rehat, aliran=aliran)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_clv_ambang_0_75 = P['clv_ambang_0_75']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        k = _komponen(g, P=P)
        sig = k['burst'] & k['sempit'] & k['bukan3'] & k['rehat'] & k['aliran'] & (k['clv'] >= _p_clv_ambang_0_75) & (g.close > k['s50'])
        stop = g.low
        bk = g.open.shift(-1)
        sig = sig & ((bk > stop) | bk.isna())
        for nm in ('sempit', 'bukan3', 'rehat', 'aliran'):
            g['_' + nm] = k[nm]
        g['_s50'] = k['s50']
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < k['s50']).fillna(False)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

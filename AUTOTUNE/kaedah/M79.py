# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M79.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'a': 0.15,
    'shift_63': 63,
}
ID = 'M79'
NAMA = 'Radge: 20% Flipper'
VARIAN = 'V3 V1 dengan A=0.15 (masuk/keluar/henti 15%)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
A = 0.15

def _zigzag(c, *, P=PARAM):
    _p_a = P['a']
    c = c.values.astype(float)
    n = len(c)
    flip = np.zeros(n, bool)
    jatuh = np.zeros(n, bool)
    naik = np.zeros(n, bool)
    LT = np.full(n, np.nan)
    HT = np.full(n, np.nan)
    if n == 0:
        return (flip, jatuh, naik, LT, HT)
    st = False
    lt = c[0]
    ht = np.nan
    for i in range(n):
        if not st:
            if i > 0:
                lt = min(lt, c[i])
            if c[i] >= (1 + _p_a) * lt:
                st = True
                ht = c[i]
                flip[i] = True
        else:
            ht = max(ht, c[i])
            if c[i] <= (1 - _p_a) * ht:
                st = False
                lt = c[i]
                jatuh[i] = True
        naik[i] = st
        LT[i] = lt
        HT[i] = ht
    return (flip, jatuh, naik, LT, HT)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_a = P['a']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        flip, jatuh, naik, LT, HT = _zigzag(g.close, P=P)
        g['_naik'] = naik
        g['_LT'] = LT
        g['_HT'] = HT
        g['sig'] = flip
        g['stop'] = (1 - _p_a) * g.close
        g['tgt'] = np.nan
        g['exitc'] = jatuh
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'a': ('float', 0.075, 0.225),
    'shift_63': ('int', 32, 126),
}
TALA = ['a']

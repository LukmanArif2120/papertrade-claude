# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M33.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'h_bahagi_2': 2,
    'high_ambang_0_25': 0.25,
    'supertrend_10': 10,
    'supertrend_k_3_0': 3.0,
    'rolling_20': 20,
    'shift_63': 63,
}
ID = 'M33'
NAMA = 'Supertrend + SMA10'
VARIAN = 'V5 V1 + volum>VOL20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _atr_wilder(g, n=10, *, P=PARAM):
    c = g.close.values
    h = g.high.values
    l = g.low.values
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    a = np.full(len(c), np.nan)
    if len(c) <= n:
        return a
    a[n - 1] = tr[:n].mean()
    for i in range(n, len(c)):
        a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a

def _supertrend(g, n=10, k=3.0, *, P=PARAM):
    h = g.high.values
    l = g.low.values
    c = g.close.values
    N = len(c)
    a = _atr_wilder(g, n, P=P)
    hl2 = (h + l) / P['h_bahagi_2']
    ba = hl2 + k * a
    bb = hl2 - k * a
    GA = np.full(N, np.nan)
    GB = np.full(N, np.nan)
    up = np.zeros(N, bool)
    s = n - 1
    if N <= s:
        return (GA, GB, up, np.full(N, np.nan))
    GA[s] = ba[s]
    GB[s] = bb[s]
    up[s] = False
    for i in range(s + 1, N):
        GB[i] = bb[i] if bb[i] > GB[i - 1] or c[i - 1] < GB[i - 1] else GB[i - 1]
        GA[i] = ba[i] if ba[i] < GA[i - 1] or c[i - 1] > GA[i - 1] else GA[i - 1]
        if c[i] > GA[i - 1]:
            up[i] = True
        elif c[i] < GB[i - 1]:
            up[i] = False
        else:
            up[i] = up[i - 1]
    st = np.where(up, GB, GA)
    return (GA, GB, up, st)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_high_ambang_0_25 = P['high_ambang_0_25']
    _p_supertrend_10 = P['supertrend_10']
    _p_supertrend_k_3_0 = P['supertrend_k_3_0']
    _p_rolling_20 = P['rolling_20']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        GA, GB, up, st = _supertrend(g, n=_p_supertrend_10, k=_p_supertrend_k_3_0, P=P)
        upS = pd.Series(up, g.index)
        stS = pd.Series(st, g.index)
        pecah = upS & ~upS.shift(1, fill_value=True)
        tapak = g.high.shift(1).rolling(_p_rolling_20).max() / g.low.shift(1).rolling(_p_rolling_20).min() - 1 <= _p_high_ambang_0_25
        vol20 = g.volume.shift(1).rolling(_p_rolling_20).mean()
        sig = pecah & tapak & (g.volume > vol20)
        bk = g.open.shift(-1)
        sig = sig & ((bk > stS) | bk.isna())
        g['_up'] = upS
        g['_GA'] = pd.Series(GA, g.index)
        g['_vol20'] = vol20
        g['_tapak'] = tapak
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stS.where(upS)
        g['tgt'] = np.nan
        g['exitc'] = ~upS
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

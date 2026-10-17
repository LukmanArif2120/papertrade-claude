# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M36.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'out_bahagi_20': 20,
    'out_kali_19': 19,
    'n_20': 20,
    'n_kali_2': 2,
    'rolling_55': 55,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M36'
NAMA = 'Turtle 55/20'
VARIAN = 'V2 V1 keluar tutup<SMA50 + sig tutup>SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _N(g, n=20, *, P=PARAM):
    _p_out_bahagi_20 = P['out_bahagi_20']
    _p_out_kali_19 = P['out_kali_19']
    h, l, c = (g.high.values, g.low.values, g.close.values)
    pc = np.r_[np.nan, c[:-1]]
    js = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    out = np.full(len(c), np.nan)
    if len(c) < n:
        return pd.Series(out, g.index)
    out[n - 1] = js[:n].mean()
    for i in range(n, len(c)):
        out[i] = (_p_out_kali_19 * out[i - 1] + js[i]) / _p_out_bahagi_20
    return pd.Series(out, g.index)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_n_20 = P['n_20']
    _p_n_kali_2 = P['n_kali_2']
    _p_rolling_55 = P['rolling_55']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c, h = (g.close, g.high)
        h55 = h.shift(1).rolling(_p_rolling_55).max()
        s50 = c.rolling(_p_rolling_50).mean()
        N = _N(g, n=_p_n_20, P=P)
        pecah = (c > h55) & (c.shift() <= h55.shift())
        g['_h55'] = h55
        g['_s50'] = s50
        g['_N'] = N
        g['sig'] = (pecah & (c > s50)).fillna(False).astype(bool)
        g['stop'] = g.open.shift(-1) - _p_n_kali_2 * N
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

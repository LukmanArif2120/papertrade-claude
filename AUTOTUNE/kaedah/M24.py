# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M24.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'k': 2,
    'shift_252': 252,
    'rolling_200': 200,
}
ID = 'M24'
NAMA = 'Rotasi Momentum ROC12 + SMA200'
VARIAN = 'V0 Sumber tulen (K=2, tiada henti)'
TMAX = None
WARM = 260
ADA_HENTI = False
SILANG = True
PERLU_BAR = 260
K = 2

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_k = P['k']
    cl = pd.DataFrame({t: g.close for t, g in fr.items()}).sort_index()
    dts = cl.index
    nxt = pd.Series(dts, index=dts).shift(-1)
    me = pd.Series([pd.notna(nxt.iloc[k]) and dts[k].month != nxt.iloc[k].month for k in range(len(dts))], index=dts)
    if len(dts):
        last = dts[-1]
        me.iloc[-1] = (last + pd.offsets.BDay(1)).month != last.month
    roc12 = pd.DataFrame({t: g.close / g.close.shift(P['shift_252']) - 1 for t, g in fr.items()}).reindex(dts)
    s200 = pd.DataFrame({t: g.close.rolling(P['rolling_200']).mean() for t, g in fr.items()}).reindex(dts)
    atas = cl > s200
    lay = atas & roc12.notna() & pd.DataFrame({t: me for t in cl.columns})
    rk = roc12.where(lay).rank(axis=1, ascending=False)
    rk_hari = roc12.where(atas & roc12.notna()).rank(axis=1, ascending=False)
    for t, g in fr.items():
        L = lay[t].reindex(g.index).fillna(False).astype(bool)
        top = (rk[t].reindex(g.index) <= _p_k).fillna(False)
        m = me.reindex(g.index).fillna(False).astype(bool)
        g['sig'] = L & top
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = m & (~L | ~top)
        g['rank'] = roc12[t].reindex(g.index)
        g['_rkh'] = rk_hari[t].reindex(g.index)
        g['_me'] = m
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'k': ('int', 2, 4),
    'rolling_200': ('int', 100, 400),
}
TALA = ['k', 'rolling_200']

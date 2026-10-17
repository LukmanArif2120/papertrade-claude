# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M03.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_31': 31,
    'sd_kali_2': 2,
    'rsi_14': 14,
    'rolling_20': 20,
    'i_tolak_5': 5,
    'l_kali_0_99': 0.99,
    'i_tolak_30': 30,
}
ID = 'M03'
NAMA = 'BB Break + Divergence RSI'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 240

def _kira(g, *, P=PARAM):
    _p_range_31 = P['range_31']
    _p_i_tolak_5 = P['i_tolak_5']
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_i_tolak_30 = P['i_tolak_30']
    o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
    n = len(g)
    bm = g.close.rolling(P['rolling_20']).mean()
    sd = g.close.rolling(P['rolling_20']).std(ddof=0)
    BBL = (bm - P['sd_kali_2'] * sd).values
    BBU = bm + P['sd_kali_2'] * sd
    RS = rsi(g.close, P['rsi_14']).values
    sg = np.zeros(n, bool)
    st = np.full(n, np.nan)
    rk = np.zeros(n)
    setup = np.zeros(n, bool)
    L2v = np.full(n, np.nan)
    for i in range(_p_range_31, n):
        L2 = i - _p_i_tolak_5 + int(np.argmin(l[i - _p_i_tolak_5:i + 1]))
        K = [k for k in range(i - _p_i_tolak_30, i - _p_i_tolak_5) if c[k] < BBL[k]]
        if not K:
            continue
        L1 = K[int(np.argmin([l[k] for k in K]))]
        if any((c[q] > BBL[q] for q in range(L1 + 1, L2))) and l[L2] < l[L1] and (RS[L2] > RS[L1]):
            setup[i] = True
            L2v[i] = l[L2]
            if c[i] > h[i - 1] and c[i] > o[i]:
                sg[i] = True
                st[i] = _p_l_kali_0_99 * l[L2]
                rk[i] = RS[L2] - RS[L1]
    return (sg, st, rk, BBU, setup, L2v)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    for g in fr.values():
        sg, st, rk, BBU, setup, L2v = _kira(g, P=P)
        stop = pd.Series(st, g.index)
        bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())
        g['_setup'] = setup
        g['_l2'] = L2v
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = BBU
        g['exitc'] = False
        g['rank'] = rk

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

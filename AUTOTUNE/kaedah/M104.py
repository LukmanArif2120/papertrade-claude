# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M104.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_41': 41,
    'i_tolak_30': 30,
    'p_tolak_40': 40,
    'l_max': 30,
    'tiang_min': 0.5,
    'l_min': 10,
    'dalam_ambang_0_2': 0.2,
    'rr_kali_0_99': 0.99,
    'close_kali_0_88': 0.88,
    'fillna_1000000000_0': 1000000000.0,
    'rolling_50': 50,
    'vol50_kali_1_5': 1.5,
}
ID = 'M104'
NAMA = 'High Tight Flag / Power Play'
VARIAN = 'V2 V1 + tiang >=50%'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
TIANG_MIN = 0.5
L_MIN, L_MAX = (10, 30)

def _bendera(g, *, P=PARAM):
    """Per hari i: PUNCAK, L, TIANG, RENDAH_REHAT, DALAM, sah_dasar (Kad + laporan Andaian #2)."""
    _p_range_41 = P['range_41']
    _p_i_tolak_30 = P['i_tolak_30']
    _p_p_tolak_40 = P['p_tolak_40']
    h = g.high.values.astype(float)
    l = g.low.values.astype(float)
    n = len(g)
    pk = np.full(n, np.nan)
    L = np.zeros(n, int)
    tiang = np.full(n, np.nan)
    rr = np.full(n, np.nan)
    dalam = np.full(n, np.nan)
    for i in range(_p_range_41, n):
        a = max(0, i - _p_i_tolak_30)
        w = h[a:i]
        p = a + (len(w) - 1 - int(np.argmax(w[::-1])))
        if p - _p_p_tolak_40 < 0:
            continue
        das = l[p - _p_p_tolak_40:p].min()
        if not das <= l[p]:
            continue
        pk[i] = h[p]
        L[i] = i - p
        tiang[i] = h[p] / das - 1
        if i - 1 >= p + 1:
            rr[i] = l[p + 1:i].min()
            dalam[i] = 1 - rr[i] / h[p]
    idx = g.index
    return (pd.Series(pk, idx), pd.Series(L, idx), pd.Series(tiang, idx), pd.Series(rr, idx), pd.Series(dalam, idx))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_max = P['l_max']
    _p_tiang_min = P['tiang_min']
    _p_l_min = P['l_min']
    _p_dalam_ambang_0_2 = P['dalam_ambang_0_2']
    _p_rr_kali_0_99 = P['rr_kali_0_99']
    _p_close_kali_0_88 = P['close_kali_0_88']
    _p_fillna_1000000000_0 = P['fillna_1000000000_0']
    _p_rolling_50 = P['rolling_50']
    _p_vol50_kali_1_5 = P['vol50_kali_1_5']
    for g in fr.values():
        pk, L, tiang, rr, dalam = _bendera(g, P=P)
        vol50 = g.volume.rolling(_p_rolling_50).mean().shift(1)
        s50 = g.close.rolling(_p_rolling_50).mean()
        sd = (tiang >= _p_tiang_min) & (L >= _p_l_min) & (L <= _p_l_max) & (dalam <= _p_dalam_ambang_0_2)
        sig = sd & (g.close > pk) & (g.volume >= _p_vol50_kali_1_5 * vol50)
        g['_sd'] = sd
        g['_pk'] = pk
        g['_L'] = L
        g['_tiang'] = tiang
        g['_rr'] = rr
        g['_dalam'] = dalam
        g['_vol50'] = vol50
        g['sig'] = sig
        g['stop'] = np.maximum(rr * _p_rr_kali_0_99, g.close * _p_close_kali_0_88)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = tiang.fillna(-_p_fillna_1000000000_0)

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'l_max': ('int', 15, 60),
    'tiang_min': ('float', 0.25, 0.75),
    'l_min': ('int', 5, 20),
    'dalam_ambang_0_2': ('float', 0.1, 0.3),
    'rr_kali_0_99': ('float', 0.495, 0.99),
    'close_kali_0_88': ('float', 0.44, 0.99),
    'rolling_50': ('int', 25, 100),
    'vol50_kali_1_5': ('float', 0.75, 2.25),
}
TALA = ['rr_kali_0_99', 'close_kali_0_88', 'rolling_50', 'l_max', 'tiang_min', 'l_min']

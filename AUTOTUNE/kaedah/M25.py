# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M25.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_2': 2,
    'a_tolak_2': 2,
    'high_bahagi_3': 3,
    'tp_kuasa_2': 2,
    'n': 20,
    'range_12': 12,
    'low_kali_0_99': 0.99,
    'max_a1_11': 11,
    'i_tolak_11': 11,
    'n_tolak_2': 2,
    'i_tolak_10': 10,
    'shift_63': 63,
    'rolling_20': 20,
    'vs20_kali_0_7': 0.7,
    'tmax': 20,
}
ID = 'M25'
NAMA = 'VWAP Wave (proksi harian)'
VARIAN = 'V2 V1 tanpa sasaran'
TMAX = 20
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
N = 20

def _vw(g, n=N, *, P=PARAM):
    _p_tp_kuasa_2 = P['tp_kuasa_2']
    tp = (g.high + g.low + g.close) / P['high_bahagi_3']
    v = g.volume
    vw = (tp * v).rolling(n).sum() / v.rolling(n).sum()
    TP, V, VW = (tp.values, v.values.astype(float), vw.values)
    sd = np.full(len(g), np.nan)
    for i in range(n - 1, len(g)):
        w = V[i - n + 1:i + 1]
        if w.sum() > 0:
            sd[i] = np.sqrt((w * (TP[i - n + 1:i + 1] - VW[i]) ** _p_tp_kuasa_2).sum() / w.sum())
    return (vw, pd.Series(vw.values + sd, g.index))

def _penerimaan(C, UB, *, P=PARAM):
    """Untuk setiap i: indeks A terkini dalam [i-10, i-1] (hari penerimaan) dengan DISC & FIRST masih sah, atau -1."""
    _p_range_2 = P['range_2']
    _p_a_tolak_2 = P['a_tolak_2']
    n = len(C)
    out = np.full(n, -1)
    acc = np.zeros(n, bool)
    for a in range(_p_range_2, n):
        acc[a] = C[a] > UB[a] and C[a - 1] > UB[a - 1] and (C[a - _p_a_tolak_2] <= UB[a - _p_a_tolak_2])
    return acc

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_n = P['n']
    _p_range_12 = P['range_12']
    _p_low_kali_0_99 = P['low_kali_0_99']
    _p_max_a1_11 = P['max_a1_11']
    _p_i_tolak_11 = P['i_tolak_11']
    _p_n_tolak_2 = P['n_tolak_2']
    _p_i_tolak_10 = P['i_tolak_10']
    _p_shift_63 = P['shift_63']
    _p_rolling_20 = P['rolling_20']
    _p_vs20_kali_0_7 = P['vs20_kali_0_7']
    for g in fr.values():
        O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
        vw, ub = _vw(g, n=_p_n, P=P)
        UB = ub.values
        VW = vw.values
        vs20 = g.volume.rolling(_p_rolling_20).mean().values
        acc = _penerimaan(C, UB, P=P)
        n = len(g)
        sg = np.zeros(n, bool)
        pers = np.zeros(n, bool)
        for i in range(_p_range_12, n):
            for A in range(i - 1, i - _p_i_tolak_11, -1):
                if acc[A]:
                    ok = all((C[t] > UB[t] for t in range(A, i))) and all((L[t] > UB[t] for t in range(A + 1, i)))
                    pers[i] = ok
                    sg[i] = ok and L[i] <= UB[i] and (C[i] > UB[i]) and (C[i] > O[i]) and (V[i] >= _p_vs20_kali_0_7 * vs20[i])
                    break
        pe = np.zeros(n, bool)
        for i in range(n - 1, max(n - _p_n_tolak_2, _p_max_a1_11), -1):
            for A in range(i, i - _p_i_tolak_10, -1):
                if acc[A]:
                    pe[i] = all((C[t] > UB[t] for t in range(A, i + 1))) and all((L[t] > UB[t] for t in range(A + 1, i + 1)))
                    break
        stop = _p_low_kali_0_99 * g.low
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)
        g['_pers'] = pe
        g['_ub'] = UB
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(C < VW, g.index)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

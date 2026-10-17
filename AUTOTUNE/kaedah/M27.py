# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M27.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'pivot_k_3': 3,
    'atr_14': 14,
    'b_tolak_250': 250,
    'b_tolak_4': 4,
    'np_ambang_2': 2,
    'a14_kali_0_5': 0.5,
    'range_5': 5,
    'eq_4': 4,
    'i_tolak_14': 14,
    'shift_63': 63,
    'i_tolak_15': 15,
    'rolling_20': 20,
    'rolling_50': 50,
    'i_tolak_4': 4,
    'rolling_4': 4,
}
ID = 'M27'
NAMA = 'Price Action 4 Tiang'
VARIAN = 'V2 Persediaan A sahaja (flip & hold)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 270

def _pivot(a, k, fn, *, P=PARAM):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]):
            p[t] = True
    return np.where(p)[0]

def _flip(g, *, P=PARAM):
    """Untuk setiap hari b: senarai paras L (harga PH dalam P(b), TOUCH>=2) dengan close[b-1] <= L < close[b]."""
    _p_b_tolak_250 = P['b_tolak_250']
    _p_b_tolak_4 = P['b_tolak_4']
    _p_np_ambang_2 = P['np_ambang_2']
    _p_a14_kali_0_5 = P['a14_kali_0_5']
    H, L, C = [g[k].values.astype(float) for k in ['high', 'low', 'close']]
    n = len(g)
    a14 = atr(g, P['atr_14']).values
    ph = _pivot(H, P['pivot_k_3'], np.max, P=P)
    pl = _pivot(L, P['pivot_k_3'], np.min, P=P)
    pt = np.r_[ph, pl]
    pp = np.r_[H[ph], L[pl]]
    isph = np.r_[np.ones(len(ph), bool), np.zeros(len(pl), bool)]
    o = np.argsort(pt, kind='stable')
    pt, pp, isph = (pt[o], pp[o], isph[o])
    fl = {}
    for b in range(1, n):
        if np.isnan(a14[b]):
            continue
        lo, hi = (C[b - 1], C[b])
        if not hi > lo:
            continue
        msk = (pt >= b - _p_b_tolak_250) & (pt <= b - _p_b_tolak_4)
        cand = pp[msk & isph]
        cand = cand[(cand >= lo) & (cand < hi)]
        if not len(cand):
            continue
        allp = pp[msk]
        ok = [v for v in cand if np.sum(np.abs(allp - v) <= _p_a14_kali_0_5 * a14[b]) >= _p_np_ambang_2]
        if ok:
            fl[b] = np.array(ok)
    return (fl, a14)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_range_5 = P['range_5']
    _p_eq_4 = P['eq_4']
    _p_i_tolak_14 = P['i_tolak_14']
    _p_shift_63 = P['shift_63']
    _p_i_tolak_15 = P['i_tolak_15']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_50 = P['rolling_50']
    _p_i_tolak_4 = P['i_tolak_4']
    _p_rolling_4 = P['rolling_4']
    _p_a14_kali_0_5 = P['a14_kali_0_5']
    qqq = idx['QQQ'].close
    for g in fr.values():
        O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
        n = len(g)
        q = qqq.reindex(g.index).ffill()
        mkt = (q > q.rolling(_p_rolling_50).mean()).values
        up = (g.close > g.close.shift()).values
        fl, a14 = _flip(g, P=P)
        sgA = np.zeros(n, bool)
        Ls = np.full(n, np.nan)
        hold = np.zeros(n, bool)
        Lh = np.full(n, np.nan)
        for i in range(_p_range_5, n):
            best = np.nan
            bh = np.nan
            for b in range(max(1, i - _p_i_tolak_15), i):
                if b not in fl:
                    continue
                mn = C[b:i + 1].min()
                for Lv in fl[b]:
                    if mn > Lv:
                        if np.isnan(bh) or Lv > bh:
                            bh = Lv
                        if L[i] <= Lv + _p_a14_kali_0_5 * a14[i] and C[i] > Lv and (np.isnan(best) or Lv > best):
                            best = Lv
            if not np.isnan(bh):
                hold[i] = True
                Lh[i] = bh
            ext = up[i - _p_i_tolak_4:i + 1].all()
            if not np.isnan(best) and mkt[i] and (not ext):
                sgA[i] = True
                Ls[i] = best
        stop = Ls - a14
        Lff = pd.Series(Ls).ffill().values
        on = g.open.shift(-1).values
        sig = sgA & ~(on <= stop)
        s20 = g.close.rolling(_p_rolling_20).mean().values
        Le = np.nan
        i = n - 1
        for b in range(max(1, i - _p_i_tolak_14), i + 1):
            if b not in fl:
                continue
            mn = C[b:i + 1].min()
            for Lv in fl[b]:
                if mn > Lv and (np.isnan(Le) or Lv > Le):
                    Le = Lv
        g['_Le'] = np.r_[np.full(n - 1, np.nan), [Le]] if n else []
        g['_up4'] = pd.Series(up, g.index).rolling(_p_rolling_4).sum().eq(_p_eq_4).values
        g['_hold'] = hold
        g['_Lh'] = Lh
        g['_mkt'] = mkt
        g['_a14'] = a14
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (C < Lff) | (C < s20)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M15.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_70': 70,
    'atrw_14': 14,
    'i_tolak_16': 16,
    'rolling_20': 20,
    'bb_tolak_4': 4,
    'rolling_7': 7,
    'a14_kali_0_5': 0.5,
    'h_kali_0_382': 0.382,
    'i_tolak_60': 60,
    'shift_63': 63,
}
ID = 'M15'
NAMA = 'Break & Retest + Henti ATR'
VARIAN = 'V2 Ekori SMA20 tanpa sasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _br(g, *, P=PARAM):
    """Pecah & uji semula (kod M15 kompilasi 8.2). Pulang sig (tanpa langkau), SL, R, T dan b bagi setiap i."""
    _p_range_70 = P['range_70']
    _p_i_tolak_16 = P['i_tolak_16']
    _p_bb_tolak_4 = P['bb_tolak_4']
    _p_a14_kali_0_5 = P['a14_kali_0_5']
    _p_h_kali_0_382 = P['h_kali_0_382']
    _p_i_tolak_60 = P['i_tolak_60']
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g)
    a14 = _atrw(g, n=P['atrw_14'], P=P).values
    s20 = g.close.rolling(P['rolling_20']).mean().values
    PH = (g.high == g.high.rolling(P['rolling_7'], center=True).max()).values
    lastpv = np.full(n, -1)
    cur = -1
    for t in range(n):
        if PH[t]:
            cur = t
        lastpv[t] = cur
    sg = np.zeros(n, bool)
    SL = np.full(n, np.nan)
    RR_ = np.full(n, np.nan)
    RZ = np.full(n, np.nan)
    TT = np.full(n, np.nan)
    for i in range(_p_range_70, n):
        b = None
        for bb in range(i - 1, i - _p_i_tolak_16, -1):
            p = lastpv[bb - _p_bb_tolak_4]
            if p >= 0 and C[bb] > H[p] and (C[bb - 1] <= H[p]):
                b = bb
                R_ = H[p]
                tR = p
                break
        if b is None:
            continue
        if C[b:i + 1].min() > L[tR:b + 1].min():
            RZ[i] = R_
        if not (C[b:i + 1].min() > L[tR:b + 1].min() and L[i] <= R_ + _p_a14_kali_0_5 * a14[i] and (C[i] >= R_ - _p_a14_kali_0_5 * a14[i])):
            continue
        cdl = min(O[i], C[i]) >= H[i] - _p_h_kali_0_382 * (H[i] - L[i]) and H[i] > L[i] or (C[i - 1] < O[i - 1] and C[i] > O[i] and (C[i] - O[i] > O[i - 1] - C[i - 1])) or C[i] > H[i - 1]
        T_ = H[i - _p_i_tolak_60:i].max()
        SL_ = L[b:i + 1].min() - a14[i]
        TT[i] = T_
        SL[i] = SL_
        if cdl and T_ > C[i] and (C[i] > s20[i]) and ((T_ - C[i]) / (C[i] - SL_) >= 1):
            sg[i] = True
    return (sg, SL, RZ, TT, a14)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_20 = P['rolling_20']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        sg, SL, RZ, TT, a14 = _br(g, P=P)
        idx_ = g.index
        stop = pd.Series(SL, idx_)
        sig = pd.Series(sg, idx_)
        lk = (g.open.shift(-1) <= stop).fillna(False)
        S20 = g.close.rolling(_p_rolling_20).mean()
        g['_R'] = RZ
        g['_S20'] = S20
        g['_A'] = a14
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < S20
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'atrw_14': ('int', 7, 28),
    'rolling_20': ('int', 10, 40),
    'rolling_7': ('int', 4, 14),
    'a14_kali_0_5': ('float', 0.25, 0.75),
    'h_kali_0_382': ('float', 0.191, 0.573),
    'shift_63': ('int', 32, 126),
}
TALA = ['rolling_20', 'atrw_14', 'rolling_7', 'h_kali_0_382']

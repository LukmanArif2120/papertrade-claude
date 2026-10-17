# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M09.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'bahagi_2': 2,
    'bahagi_2_bahagi_11': 11,
    'range_7': 7,
    'atrw_200': 200,
    'a200_kali_2': 2,
    'buy_bahagi_2': 2,
    'atrw_14': 14,
    'i_tolak_3': 3,
    'rolling_20': 20,
    'buy_kali_100': 100,
    'age_ambang_50': 50,
    'a_bahagi_100': 100,
    'rolling_15': 15,
    'dl_ambang_30': 30,
    'a14_kali_0_5': 0.5,
    'up_kali_100': 100,
    'cc_tolak_3': 3,
    'cc_tambah_4': 4,
}
ID = 'M09'
NAMA = 'Volumatic VIDYA Pivot Retest'
VARIAN = 'V2 V1 tanpa sasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300

def _atrw(g, n, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _kira(g, *, P=PARAM):
    _p_range_7 = P['range_7']
    _p_buy_bahagi_2 = P['buy_bahagi_2']
    _p_i_tolak_3 = P['i_tolak_3']
    _p_buy_kali_100 = P['buy_kali_100']
    _p_age_ambang_50 = P['age_ambang_50']
    _p_a_bahagi_100 = P['a_bahagi_100']
    _p_dl_ambang_30 = P['dl_ambang_30']
    _p_a14_kali_0_5 = P['a14_kali_0_5']
    _p_cc_tolak_3 = P['cc_tolak_3']
    _p_cc_tambah_4 = P['cc_tambah_4']
    O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
    n = len(g)
    c = g.close
    dl = c.diff()
    up = dl.clip(lower=0).rolling(P['rolling_20']).sum()
    dn = (-dl.clip(upper=0)).rolling(P['rolling_20']).sum()
    CMO = ((up - dn) / (up + dn) * P['up_kali_100']).abs().fillna(0).values
    a = P['bahagi_2'] / P['bahagi_2_bahagi_11']
    Vr = np.zeros(n)
    for t in range(1, n):
        Vr[t] = a * CMO[t] / _p_a_bahagi_100 * C[t] + (1 - a * CMO[t] / _p_a_bahagi_100) * Vr[t - 1]
    VID = pd.Series(Vr).rolling(P['rolling_15']).mean().values
    A200 = _atrw(g, P['atrw_200'], P=P).values
    UB = VID + P['a200_kali_2'] * A200
    LB = VID - P['a200_kali_2'] * A200
    upT = np.zeros(n, bool)
    chg = np.zeros(n, bool)
    for t in range(1, n):
        upT[t] = upT[t - 1]
        if not np.isnan(UB[t]) and C[t] > UB[t] and (C[t - 1] <= UB[t - 1]):
            upT[t] = True
        if not np.isnan(LB[t]) and C[t] < LB[t] and (C[t - 1] >= LB[t - 1]):
            upT[t] = False
        chg[t] = upT[t] != upT[t - 1]
    buy = sell = 0.0
    DL = np.zeros(n)
    for t in range(1, n):
        if chg[t] or chg[t - 1]:
            buy = sell = 0.0
        elif C[t] > O[t]:
            buy += V[t]
        elif C[t] < O[t]:
            sell += V[t]
        av = (buy + sell) / _p_buy_bahagi_2
        DL[t] = (buy - sell) / av * _p_buy_kali_100 if av > 0 else 0
    line = np.where(upT, LB, UB)
    a14 = _atrw(g, P['atrw_14'], P=P).values
    sg = np.zeros(n, bool)
    st = np.full(n, np.nan)
    levA = np.full(n, np.nan)
    ageA = np.full(n, np.nan)
    pendB = np.zeros(n, bool)
    levB = np.full(n, np.nan)
    lev = np.nan
    age = 0
    touched = False
    pb = -1
    pblev = np.nan
    for i in range(_p_range_7, n):
        cc = i - _p_i_tolak_3
        if upT[i] and C[cc] == C[cc - _p_cc_tolak_3:cc + _p_cc_tambah_4].min() and (L[cc] > line[cc]):
            lev = L[cc]
            age = 0
            touched = False
        if not upT[i]:
            lev = np.nan
        if pb == i - 1 and upT[i] and (not np.isnan(lev)) and (lev == pblev):
            if C[i] > O[i] and C[i] >= pblev and (DL[i] >= _p_dl_ambang_30):
                sg[i] = True
                st[i] = min(L[i - 1], L[i]) - _p_a14_kali_0_5 * a14[i]
        if np.isnan(lev):
            continue
        age += 1
        if age > _p_age_ambang_50 or touched:
            continue
        if L[i] <= lev:
            touched = True
            if C[i] >= lev and C[i] > O[i] and (DL[i] >= _p_dl_ambang_30):
                sg[i] = True
                st[i] = L[i] - _p_a14_kali_0_5 * a14[i]
            elif C[i] < O[i] and C[i] >= lev:
                pb = i
                pblev = lev
                pendB[i] = True
                levB[i] = lev
        else:
            levA[i] = lev
            ageA[i] = age
    return (sg, st, upT, DL, levA, pendB, levB, ageA)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    for g in fr.values():
        sg, st, upT, DL, levA, pendB, levB, ageA = _kira(g, P=P)
        stop = pd.Series(st, g.index)
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)
        g['_up'] = upT
        g['_dl'] = DL
        g['_lev'] = levA
        g['_pb'] = pendB
        g['_levb'] = levB
        g['_age'] = ageA
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ~pd.Series(upT, g.index)
        g['rank'] = DL
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M31.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_20': 20,
    'sd_kali_2': 2,
    'rolling_10': 10,
    'shift_63': 63,
    'shift_5': 5,
}
ID = 'M31'
NAMA = 'Band Walk (BB 20/2)'
VARIAN = 'V0 Peraturan pengguna (henti tutup<LOWER isyarat, keluar MID turun)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 30

def _bb(c, *, P=PARAM):
    mid = c.rolling(P['rolling_20']).mean()
    sd = c.rolling(P['rolling_20']).std(ddof=0)
    return (mid, mid + P['sd_kali_2'] * sd, mid - P['sd_kali_2'] * sd)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_10 = P['rolling_10']
    _p_shift_63 = P['shift_63']
    _p_shift_5 = P['shift_5']
    for g in fr.values():
        c = g.close
        n = len(g)
        mid, up, lo = _bb(c, P=P)
        w = up - lo
        s10 = c.rolling(_p_rolling_10).mean()
        sgs = ((c > up) & (c.shift() <= up.shift()) & (w > w.shift()) & (mid > mid.shift(_p_shift_5)) & (s10 > mid)).fillna(False).values
        dn = (mid < mid.shift(_p_shift_5)).fillna(False).values
        cv_ = c.values
        lov = lo.values
        exv = np.zeros(n, bool)
        i = WARM
        while i < n - 1:
            if not sgs[i]:
                i += 1
                continue
            lv = lov[i]
            j = i + 1
            while j < n:
                if (dn[j] or cv_[j] < lv) and j + 1 < n:
                    exv[j] = True
                    j += 1
                    break
                j += 1
            else:
                j = n - 1
            i = j + 1
        g['_mid'] = mid
        g['_up'] = up
        g['_lo'] = lo
        g['_s10'] = s10
        g['sig'] = pd.Series(sgs, g.index)
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(exv, g.index)
        g['rank'] = c / c.shift(_p_shift_63) - 1

def _bb_esok(c_last19, X):
    X = np.asarray(X, float)
    s = c_last19.sum() + X
    s2 = (c_last19 ** 2).sum() + X ** 2
    mid = s / 20
    sd = np.sqrt(np.maximum(s2 / 20 - mid ** 2, 0))
    return (mid, mid + 2 * sd, mid - 2 * sd)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_20': ('int', 10, 40),
    'sd_kali_2': ('float', 1.0, 3.0),
    'rolling_10': ('int', 5, 20),
    'shift_63': ('int', 32, 126),
    'shift_5': ('int', 2, 10),
}
TALA = ['rolling_20', 'sd_kali_2', 'rolling_10', 'shift_5']

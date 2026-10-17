# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M55.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'nilai_15': 15,
    'nilai_30': 30,
    'nilai_60': 60,
    'rolling_4': 4,
    'shift_63': 63,
    'rolling_3': 3,
    'shift_10': 10,
}
ID = 'M55'
NAMA = 'Guppy GMMA'
VARIAN = 'V4 Undur ke kumpulan panjang lalu lantun (Persediaan 2)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230
PEND = [3, 5, 8, 10, 12, 15]
PANJ = [30, 35, 40, 45, 50, 60]

def _gmma(c, *, P=PARAM):
    P_ = pd.concat([c.ewm(span=n, adjust=False).mean() for n in PEND], axis=1)
    J = pd.concat([c.ewm(span=n, adjust=False).mean() for n in PANJ], axis=1)
    J.columns = PANJ
    P_.columns = PEND
    return (P_, J)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_nilai_15 = P['nilai_15']
    _p_nilai_30 = P['nilai_30']
    _p_nilai_60 = P['nilai_60']
    _p_rolling_4 = P['rolling_4']
    _p_shift_63 = P['shift_63']
    _p_rolling_3 = P['rolling_3']
    _p_shift_10 = P['shift_10']
    for g in fr.values():
        c = g.close
        P_, J = _gmma(c, P=P)
        pp = P_.mean(axis=1)
        pj = J.mean(axis=1)
        jmax = J.max(axis=1)
        e15 = P_[_p_nilai_15]
        e30 = J[_p_nilai_30]
        e60 = J[_p_nilai_60]
        sentuh = (g.low <= jmax).astype(int)
        sentuh3 = sentuh.shift(1).rolling(_p_rolling_3).sum() >= 1
        asas = (e30 > e60) & (e60 > e60.shift(_p_shift_10)) & (pp > pj)
        undur = asas & sentuh3 & (c > e15) & (c.shift() <= e15.shift())
        stop = g.low.rolling(_p_rolling_4).min()
        bo = g.open.shift(-1)
        g['sig'] = (undur & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pp < pj
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_asas'] = asas
        g['_sentuh3b'] = sentuh.rolling(_p_rolling_3).sum() >= 1
        g['_e15'] = e15
        g['_jmax'] = jmax
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_4': ('int', 2, 8),
    'shift_63': ('int', 32, 126),
    'rolling_3': ('int', 2, 6),
    'shift_10': ('int', 5, 20),
}
TALA = ['rolling_4', 'rolling_3', 'shift_10']

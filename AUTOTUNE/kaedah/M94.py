# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M94.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
PARAM = {
    'n': 252,
    'nilai_2': 2,
    'rank_ambang_0_8': 0.8,
    'shift_21': 21,
    'shift_252': 252,
    'tmax': 126,
}
ID = 'M94'
NAMA = 'Pecutan Momentum (Chen, Yu & Wang)'
VARIAN = 'V0 Rotasi sumber (bulanan, langkau 21h, pegang 126h)'
TMAX = 126
WARM = 281
ADA_HENTI = False
SILANG = True
PERLU_BAR = 300
N = 252

def _wg(n=N, *, P=PARAM):
    t = np.arange(n, dtype=float)
    X = np.column_stack([np.ones(n), t, t * t])
    return (np.linalg.inv(X.T @ X) @ X.T)[P['nilai_2']]

def _pecut(c, *, P=PARAM):
    v = c.values.astype(float)
    out = np.full(len(v), np.nan)
    if len(v) >= P['n']:
        w = sliding_window_view(v, P['n'])
        out[P['n'] - 1:] = w @ _wg(n=P['n'], P=P) / w[:, 0]
    return pd.Series(out, c.index)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_21 = P['shift_21']
    _p_shift_252 = P['shift_252']
    P_ = {}
    R = {}
    for t, g in fr.items():
        P_[t] = _pecut(g.close, P=P)
        R[t] = g.close / g.close.shift(_p_shift_252) - 1
    P_ = pd.DataFrame(P_)
    R = pd.DataFrame(R)
    pem = R.rank(axis=1, pct=True) > P['rank_ambang_0_8']
    Pp = P_.where(pem & P_.notna())
    atas = (Pp.rank(axis=1, pct=True) > P['rank_ambang_0_8']) & pem
    K = Pp.where(atas).rank(axis=1, ascending=False, method='first')
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    hb = set(pd.Series(tarikh, tarikh).groupby(tarikh.to_period('M')).max())
    akhir = tarikh[-1]
    if (akhir + pd.offsets.BDay(1)).month == akhir.month:
        hb.discard(akhir)
    for t, g in fr.items():
        a = atas[t].reindex(g.index).fillna(False).astype(bool)
        p = pem[t].reindex(g.index).fillna(False).astype(bool)
        pc = P_[t].reindex(g.index)
        hbs = pd.Series(g.index.isin(list(hb)), g.index)
        g['_atas'] = a
        g['_pem'] = p
        g['_pecut'] = pc
        g['_kedrot'] = K[t].reindex(g.index)
        g['sig'] = hbs & a.shift(_p_shift_21, fill_value=False) & p.shift(_p_shift_21, fill_value=False)
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = False
        g['rank'] = pc.shift(_p_shift_21)

def _hari_ke_rotasi(akhir):
    hb = akhir + pd.offsets.BMonthEnd(0)
    if hb == akhir:
        hb = akhir + pd.offsets.BMonthEnd(1)
    return (len(pd.bdate_range(akhir, hb)) - 1, hb)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

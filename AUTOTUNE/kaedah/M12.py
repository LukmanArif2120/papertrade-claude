# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M12.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    't_tolak_2': 2,
    'psar_a0_0_02': 0.02,
    'psar_da_0_02': 0.02,
    'psar_amax_0_2': 0.2,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M12'
NAMA = 'Parabolic SAR'
VARIAN = 'V5 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _psar(g, a0=0.02, da=0.02, amax=0.2, *, P=PARAM):
    _p_t_tolak_2 = P['t_tolak_2']
    H, L = (g.high.values.astype(float), g.low.values.astype(float))
    n = len(g)
    UP = np.zeros(n, bool)
    SAR = np.zeros(n)
    upt = True
    s_ = L[0]
    ep = H[0]
    af = a0
    UP[0] = True
    SAR[0] = s_
    EP = np.zeros(n)
    AF = np.zeros(n)
    EP[0] = ep
    AF[0] = af
    for t in range(1, n):
        if upt:
            s_ = min(s_ + af * (ep - s_), L[t - 1], L[max(t - _p_t_tolak_2, 0)])
            if L[t] <= s_:
                upt = False
                s_ = ep
                ep = L[t]
                af = a0
            elif H[t] > ep:
                ep = H[t]
                af = min(af + da, amax)
        else:
            s_ = max(s_ - af * (s_ - ep), H[t - 1], H[max(t - _p_t_tolak_2, 0)])
            if H[t] >= s_:
                upt = True
                s_ = ep
                ep = H[t]
                af = a0
            elif L[t] < ep:
                ep = L[t]
                af = min(af + da, amax)
        UP[t] = upt
        SAR[t] = s_
        EP[t] = ep
        AF[t] = af
    _psar.ep = pd.Series(EP, g.index)
    _psar.af = pd.Series(AF, g.index)
    return (pd.Series(UP, g.index), pd.Series(SAR, g.index))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_psar_a0_0_02 = P['psar_a0_0_02']
    _p_psar_da_0_02 = P['psar_da_0_02']
    _p_psar_amax_0_2 = P['psar_amax_0_2']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c, o = (g.close, g.open)
        up, sar = _psar(g, a0=_p_psar_a0_0_02, da=_p_psar_da_0_02, amax=_p_psar_amax_0_2, P=P)
        s50 = c.rolling(_p_rolling_50).mean()
        asas = up & ~up.shift(1, fill_value=True) & (c > s50)
        sig = asas & ~(o.shift(-1) <= sar)
        g['_up'] = up
        g['_sar'] = sar
        g['_s50'] = s50
        g['_ep'] = _psar.ep
        g['_af'] = _psar.af
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = sar
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'psar_a0_0_02': ('float', 0.01, 0.03),
    'psar_da_0_02': ('float', 0.01, 0.03),
    'psar_amax_0_2': ('float', 0.1, 0.3),
    'rolling_50': ('int', 25, 100),
    'shift_63': ('int', 32, 126),
}
TALA = ['psar_a0_0_02', 'psar_da_0_02', 'psar_amax_0_2', 'rolling_50']

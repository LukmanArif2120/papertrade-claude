# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M30.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'l_kali_0_99': 0.99,
    'sd_kali_2': 2,
    'sd_kali_4': 4,
    'quantile_0_2': 0.2,
    'atrw_14': 14,
    'rolling_20': 20,
    'atrw_kali_0_5': 0.5,
    'shift_63': 63,
    'rolling_126': 126,
    'rolling_10': 10,
    'rolling_11': 11,
    'rolling_50': 50,
}
ID = 'M30'
NAMA = 'BB Free Bar + Himpitan 50/2.5'
VARIAN = 'V3 V1 tetapi BB20/2'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 200

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_sd_kali_2 = P['sd_kali_2']
    _p_sd_kali_4 = P['sd_kali_4']
    _p_quantile_0_2 = P['quantile_0_2']
    _p_atrw_14 = P['atrw_14']
    _p_rolling_20 = P['rolling_20']
    _p_atrw_kali_0_5 = P['atrw_kali_0_5']
    _p_shift_63 = P['shift_63']
    _p_rolling_126 = P['rolling_126']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_11 = P['rolling_11']
    _p_rolling_50 = P['rolling_50']
    for g in fr.values():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        bm = c.rolling(_p_rolling_20).mean()
        sd = c.rolling(_p_rolling_20).std(ddof=0)
        bbu = bm + _p_sd_kali_2 * sd
        bw = _p_sd_kali_4 * sd / bm
        sqz = bw <= bw.rolling(_p_rolling_126).quantile(_p_quantile_0_2)
        sq = sqz.shift(1).rolling(_p_rolling_10).max() == 1
        dec = c >= bbu + _p_atrw_kali_0_5 * _atrw(g, n=_p_atrw_14, P=P)
        dec_lalu = dec.shift(1).rolling(_p_rolling_10).max() == 1
        hh20 = h.shift(1).rolling(_p_rolling_20).max()
        sig = sq & dec & ~dec_lalu & (c > hh20)
        stop = _p_l_kali_0_99 * l.rolling(_p_rolling_11).min()
        sig = sig & ~(o.shift(-1) <= stop)
        g['_sqz'] = sqz
        g['_dec'] = dec
        g['_sq'] = sq
        g['_bbu'] = bbu
        g['_dec_lalu'] = dec_lalu
        g['_hh20'] = hh20
        g['_atrw'] = _atrw(g, n=_p_atrw_14, P=P)
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < c.rolling(_p_rolling_50).mean()).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'l_kali_0_99': ('float', 0.495, 0.99),
    'sd_kali_2': ('float', 1.0, 3.0),
    'sd_kali_4': ('float', 2.0, 6.0),
    'quantile_0_2': ('float', 0.1, 0.3),
    'atrw_14': ('int', 7, 28),
    'rolling_20': ('int', 10, 40),
    'atrw_kali_0_5': ('float', 0.25, 0.75),
    'shift_63': ('int', 32, 126),
    'rolling_126': ('int', 63, 252),
    'rolling_10': ('int', 5, 20),
    'rolling_11': ('int', 6, 22),
    'rolling_50': ('int', 25, 100),
}
TALA = ['rolling_50', 'l_kali_0_99', 'rolling_11', 'rolling_20', 'atrw_14', 'rolling_10']

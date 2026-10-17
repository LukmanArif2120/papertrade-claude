# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M04.py
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
    'rolling_20': 20,
    'rolling_50': 50,
    'vs20_kali_1_5': 1.5,
    'shift_63': 63,
    'rolling_126': 126,
    'rolling_10': 10,
    'rolling_11': 11,
}
ID = 'M04'
NAMA = 'BB Squeeze Breakout'
VARIAN = 'U2 asas V2 + E1 volume>=1.5xSMA20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_sd_kali_2 = P['sd_kali_2']
    _p_sd_kali_4 = P['sd_kali_4']
    _p_quantile_0_2 = P['quantile_0_2']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_50 = P['rolling_50']
    _p_vs20_kali_1_5 = P['vs20_kali_1_5']
    _p_shift_63 = P['shift_63']
    _p_rolling_126 = P['rolling_126']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_11 = P['rolling_11']
    for g in fr.values():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        bm = c.rolling(_p_rolling_20).mean()
        sd = c.rolling(_p_rolling_20).std(ddof=0)
        BBU = bm + _p_sd_kali_2 * sd
        BW = _p_sd_kali_4 * sd / bm
        s50 = c.rolling(_p_rolling_50).mean()
        sqk = BW <= BW.rolling(_p_rolling_126).quantile(_p_quantile_0_2)
        sq = sqk.shift(1).rolling(_p_rolling_10).max() == 1
        vs20 = v.rolling(_p_rolling_20).mean()
        stop = _p_l_kali_0_99 * l.rolling(_p_rolling_11).min()
        sig = sq & (c > BBU) & (c.shift() <= BBU.shift()) & (v >= _p_vs20_kali_1_5 * vs20)
        bmk = o.shift(-1)
        sig = sig & ((bmk > stop) | bmk.isna())
        g['_sq'] = sq
        g['_bbu'] = BBU
        g['_vs20'] = vs20
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

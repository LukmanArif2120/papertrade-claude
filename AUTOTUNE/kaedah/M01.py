# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M01.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rsi_13': 13,
    'sd_kali_2': 2,
    'rolling_30': 30,
    'r13_ambang_25': 25,
}
ID = 'M01'
NAMA = 'Bollinger Band + RSI'
VARIAN = 'V0 Video tulen'
TMAX = None
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 230

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rsi_13 = P['rsi_13']
    _p_sd_kali_2 = P['sd_kali_2']
    _p_rolling_30 = P['rolling_30']
    _p_r13_ambang_25 = P['r13_ambang_25']
    for g in fr.values():
        c = g.close
        bbm = c.rolling(_p_rolling_30).mean()
        sd = c.rolling(_p_rolling_30).std(ddof=0)
        bbl = bbm - _p_sd_kali_2 * sd
        r13 = rsi(c, _p_rsi_13)
        g['_bbl'] = bbl
        g['_rsi13'] = r13
        g['sig'] = ((c < bbl) & (r13 < _p_r13_ambang_25)).fillna(False)
        g['stop'] = np.nan
        g['tgt'] = bbm
        g['exitc'] = False
        g['rank'] = -r13

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

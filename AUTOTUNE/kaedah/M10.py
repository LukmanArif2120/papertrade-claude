# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M10.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'high_bahagi_3': 3,
    'md_kali_0_015': 0.015,
    'e125_kali_0_99': 0.99,
    'cci_20': 20,
    'cci_ambang_100': 100,
    'ewm_span_60': 60,
    'ewm_span_125': 125,
    'ewm_span_250': 250,
    'rolling_11': 11,
}
ID = 'M10'
NAMA = 'EMA3 + CCI + MACD'
VARIAN = 'V4 V1 pencetus CCI>+100'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300

def _cci(g, n=20, *, P=PARAM):
    tp = (g.high + g.low + g.close) / P['high_bahagi_3']
    md = tp.rolling(n).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    return (tp - tp.rolling(n).mean()) / (P['md_kali_0_015'] * md)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_e125_kali_0_99 = P['e125_kali_0_99']
    _p_cci_20 = P['cci_20']
    _p_cci_ambang_100 = P['cci_ambang_100']
    _p_ewm_span_60 = P['ewm_span_60']
    _p_ewm_span_125 = P['ewm_span_125']
    _p_ewm_span_250 = P['ewm_span_250']
    _p_rolling_11 = P['rolling_11']
    for g in fr.values():
        c, l, o = (g.close, g.low, g.open)
        e60 = c.ewm(span=_p_ewm_span_60, adjust=False).mean()
        e125 = c.ewm(span=_p_ewm_span_125, adjust=False).mean()
        e250 = c.ewm(span=_p_ewm_span_250, adjust=False).mean()
        cci = _cci(g, n=_p_cci_20, P=P)
        susun = (c > e250) & (e60 > e125) & (e125 > e250)
        sentuh = (l - e60).rolling(_p_rolling_11).min() <= 0
        lemah = cci.rolling(_p_rolling_11).min() < -_p_cci_ambang_100
        stop = _p_e125_kali_0_99 * e125
        asas = susun & sentuh & lemah & (cci.shift() <= _p_cci_ambang_100) & (cci > _p_cci_ambang_100) & (c > e60)
        sig = asas & ~(o.shift(-1) <= stop)
        g['_susun'] = susun
        g['_sentuh'] = sentuh
        g['_lemah'] = lemah
        g['_cci'] = cci
        g['_e60'] = e60
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < e125).fillna(False)
        g['rank'] = c / e250 - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

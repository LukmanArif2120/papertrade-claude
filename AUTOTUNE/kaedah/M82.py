# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M82.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'e_kali_1_1': 1.1,
    'sd250_kali_100': 100,
    'sma20_ambang_5000000': 5000000,
    'sma20_ambang_10': 10,
    'shift_65': 65,
    'rolling_20': 20,
    'rolling_250': 250,
    'sd250_ambang_20': 20,
    'shift_125': 125,
    'ewm_span_50': 50,
    'ewm_span_200': 200,
    'ewm_span_25': 25,
    'ewm_span_125': 125,
}
ID = 'M82'
NAMA = 'Arthur Hill Rotasi Sasaran 10%'
VARIAN = 'V0 Sumber tulen (sasaran 10% tutup / EMA25<EMA125, tiada henti)'
TMAX = None
WARM = 250
ADA_HENTI = False
SILANG = False
PERLU_BAR = 260

def _exitc(g, sig, tren_turun, warm, *, P=PARAM):
    """Andaian saya: CAPAI10 (tutup_j >= 1.10 x buka_masuk) bergantung pada harga masuk dagangan,
    jadi jujukan dagangan enjin (tiada henti) disimulasi di sini dan exitc ditanda pada hari j
    (jual buka j+1, sama seperti enjin). Tiada pandang ke hadapan: hanya guna data <= j."""
    _p_e_kali_1_1 = P['e_kali_1_1']
    o, c = (g.open.values, g.close.values)
    n = len(g)
    ex = tren_turun.copy()
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        e = o[i + 1]
        j = i + 1
        jx = n - 1
        while j < n:
            if (c[j] >= _p_e_kali_1_1 * e or tren_turun[j]) and j + 1 < n:
                ex[j] = True
                jx = j + 1
                break
            j += 1
        i = jx + 1
    return ex

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_sd250_kali_100 = P['sd250_kali_100']
    _p_sma20_ambang_5000000 = P['sma20_ambang_5000000']
    _p_sma20_ambang_10 = P['sma20_ambang_10']
    _p_shift_65 = P['shift_65']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_250 = P['rolling_250']
    _p_sd250_ambang_20 = P['sd250_ambang_20']
    _p_shift_125 = P['shift_125']
    _p_ewm_span_25 = P['ewm_span_25']
    _p_ewm_span_125 = P['ewm_span_125']
    spy = idx['SPY'].close
    pas = spy.ewm(span=P['ewm_span_50'], adjust=False).mean() > spy.ewm(span=P['ewm_span_200'], adjust=False).mean()
    for g in fr.values():
        c = g.close
        e25 = c.ewm(span=_p_ewm_span_25, adjust=False).mean()
        e125 = c.ewm(span=_p_ewm_span_125, adjust=False).mean()
        roc65 = c / c.shift(_p_shift_65) - 1
        sma20 = c.rolling(_p_rolling_20).mean()
        sd250 = c.rolling(_p_rolling_250).std(ddof=0)
        vol250 = g.volume.rolling(_p_rolling_250).mean()
        layak = (e25 > e125) & (roc65 < 1.0) & (sma20 > _p_sma20_ambang_10) & (sd250 / sma20 * _p_sd250_kali_100 < _p_sd250_ambang_20) & (sma20 * vol250 > _p_sma20_ambang_5000000)
        mkt = pas.reindex(g.index, method='ffill').fillna(False).astype(bool)
        sig = (layak & mkt).fillna(False)
        turun = (e25 < e125).values
        g['_e25'] = e25
        g['_e125'] = e125
        g['_roc65'] = roc65
        g['_vr'] = sd250 / sma20 * _p_sd250_kali_100
        g['_cair'] = (sma20 > _p_sma20_ambang_10) & (sma20 * vol250 > _p_sma20_ambang_5000000)
        g['_mkt'] = mkt
        g['sig'] = sig
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = _exitc(g, sig.values, turun, WARM, P=P)
        g['rank'] = c / c.shift(_p_shift_125) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M02.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'r': 3.0,
    's200_kali_0_99': 0.99,
    'rolling_200': 200,
    'shift_63': 63,
    'ewm_span_9': 9,
    'ewm_span_12': 12,
    'ewm_span_26': 26,
    'tmax': 20,
}
ID = 'M02'
NAMA = 'MACD + SMA200'
VARIAN = 'V5 V1+sasaran 3R'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210
_R = 3.0

def _isi_tgt(g, sig, st, *, P=PARAM):
    """Sasaran tetap = buka_masuk + 3 x (buka_masuk - henti), diisi sepanjang tempoh dagangan.
       Simulasi meniru gelung enjin.trades (tmax=TMAX, warm=WARM) supaya lajur tgt betul bagi setiap dagangan.
       Hanya buka hari i+1 (harga pesanan) diguna; isyarat sendiri tiada pandang ke hadapan."""
    _p_r = P['r']
    o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
    n = len(g)
    tg = np.full(n, np.nan)
    i = WARM
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        e = o[i + 1]
        sp = st[i]
        tf = e + _p_r * (e - sp)
        j = i + 1
        x = None
        while j < n:
            tg[j - 1] = tf
            if j > i + 1 and o[j] <= sp:
                x = 1
                break
            if l[j] <= sp:
                x = 1
                break
            if j > i + 1:
                if o[j] >= tf:
                    x = 1
                    break
                if h[j] >= tf:
                    x = 1
                    break
            if TMAX and j - i >= TMAX:
                x = 1
                break
            j += 1
        if x is None:
            j = n - 1
        i = j + 1
    return tg

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_s200_kali_0_99 = P['s200_kali_0_99']
    _p_rolling_200 = P['rolling_200']
    _p_shift_63 = P['shift_63']
    _p_ewm_span_9 = P['ewm_span_9']
    _p_ewm_span_12 = P['ewm_span_12']
    _p_ewm_span_26 = P['ewm_span_26']
    for g in fr.values():
        c, o = (g.close, g.open)
        s200 = c.rolling(_p_rolling_200).mean()
        m = c.ewm(span=_p_ewm_span_12, adjust=False).mean() - c.ewm(span=_p_ewm_span_26, adjust=False).mean()
        s = m.ewm(span=_p_ewm_span_9, adjust=False).mean()
        stop = _p_s200_kali_0_99 * s200
        sig = (c > s200) & (m < 0) & (s < 0) & (m.shift() <= s.shift()) & (m > s)
        bm = o.shift(-1)
        sig = (sig & ((bm > stop) | bm.isna())).fillna(False)
        g['_m'] = m
        g['_s'] = s
        g['_s200'] = s200
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _isi_tgt(g, sig.values, stop.values, P=P)
        g['exitc'] = False
        g['rank'] = c / c.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

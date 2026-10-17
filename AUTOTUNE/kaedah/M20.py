# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M20.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'l_kali_0_99': 0.99,
    'ema_a1_10': 10,
    'ema_a1_15': 15,
    'c_kali_2': 2,
    'fillna_99_0': 99.0,
    'rolling_100': 100,
    'shift_5': 5,
    'atrw_14': 14,
    'range_a1_6': 6,
    'tmax': 20,
}
ID = 'M20'
NAMA = 'EMA10/15 Crossover + Sudut'
VARIAN = 'V3 V1 tanpa syarat sudut'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230
ema = lambda s, k, *, P=PARAM: s.ewm(span=k, adjust=False).mean()

def _kunci(g, sig, stop, T, warm, tmax=None, ex=None, *, P=PARAM):
    """Cermin gelung trades() enjin supaya lajur tgt kekal pada nilai hari isyarat sepanjang dagangan
    (laporan M19: sasaran dikunci pada hari isyarat, isian ke hadapan daripada isyarat yang diambil)."""
    o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
    n = len(g)
    tg = np.full(n, np.nan)
    ex = np.zeros(n, bool) if ex is None else ex
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        Ti = T[i]
        sp = stop[i] if not np.isnan(stop[i]) else -np.inf
        j = i + 1
        keluar = False
        while j < n:
            if j > i + 1 and o[j] <= sp:
                keluar = True
                break
            if l[j] <= sp:
                keluar = True
                break
            if not np.isnan(Ti) and j > i + 1 and (o[j] >= Ti or h[j] >= Ti):
                keluar = True
                break
            if ex[j] and j + 1 < n:
                j += 1
                keluar = True
                break
            if tmax and j - i >= tmax:
                keluar = True
                break
            j += 1
        if not keluar:
            j = n - 1
        tg[i:j + 1] = Ti
        i = j + 1
    tg[n - 1] = T[n - 1] if sig[n - 1] else tg[n - 1]
    return tg

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_ema_a1_10 = P['ema_a1_10']
    _p_ema_a1_15 = P['ema_a1_15']
    _p_c_kali_2 = P['c_kali_2']
    _p_fillna_99_0 = P['fillna_99_0']
    _p_rolling_100 = P['rolling_100']
    _p_shift_5 = P['shift_5']
    _p_atrw_14 = P['atrw_14']
    _p_range_a1_6 = P['range_a1_6']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        E10, E15 = (ema(c, _p_ema_a1_10), ema(c, _p_ema_a1_15))
        Hi = np.maximum(E10, E15)
        Lo = np.minimum(E10, E15)
        below = pd.concat([c.shift(k) < Lo.shift(k) for k in range(1, _p_range_a1_6)], axis=1).any(axis=1)
        S100 = c.rolling(_p_rolling_100).mean()
        sig = (c > Hi) & (c.shift() <= Hi.shift()) & below & (c > S100)
        stop = _p_l_kali_0_99 * l
        T = c + _p_c_kali_2 * (c - stop)
        lk = ((o.shift(-1) <= stop) | (o.shift(-1) >= T)).fillna(False)
        sig = (sig & ~lk).fillna(False)
        SL = (E10 - E10.shift(_p_shift_5)) / _atrw(g, n=_p_atrw_14, P=P)
        g['_Hi'] = Hi
        g['_Lo'] = Lo
        g['_S100'] = S100
        g['_below'] = below
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _kunci(g, sig.values, stop.values.astype(float), T.values.astype(float), WARM, TMAX, P=P)
        g['exitc'] = False
        g['rank'] = SL.fillna(-_p_fillna_99_0)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M19.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'l_kali_0_99': 0.99,
    'fillna_9_0': 9.0,
    'rolling_20': 20,
    'shift_2': 2,
    'shift_3': 3,
    'shift_63': 63,
    'tmax': 20,
}
ID = 'M19'
NAMA = 'Sneaky Pivot (proksi harian)'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

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

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_fillna_9_0 = P['fillna_9_0']
    _p_rolling_20 = P['rolling_20']
    _p_shift_2 = P['shift_2']
    _p_shift_3 = P['shift_3']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        RL20 = l.shift(_p_shift_3).rolling(_p_rolling_20).min()
        RH20 = h.shift(_p_shift_3).rolling(_p_rolling_20).max()
        stop = _p_l_kali_0_99 * np.minimum(l.shift(_p_shift_2), l.shift(1))
        sig = (l.shift(_p_shift_2) <= RL20) & (c.shift(1) > o.shift(1)) & (c > h.shift(1)) & (c < RH20)
        lk = ((o.shift(-1) <= stop) | (o.shift(-1) >= RH20)).fillna(False)
        sig = (sig & ~lk).fillna(False)
        g['_RL20'] = RL20
        g['_RH20'] = RH20
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _kunci(g, sig.values, stop.values.astype(float), RH20.values.astype(float), WARM, TMAX, P=P)
        g['exitc'] = False
        g['rank'] = (c / c.shift(_p_shift_63) - 1).fillna(-_p_fillna_9_0)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'l_kali_0_99': ('float', 0.495, 0.99),
    'fillna_9_0': ('float', 4.5, 13.5),
    'rolling_20': ('int', 10, 40),
    'shift_2': ('int', 2, 4),
    'shift_3': ('int', 2, 6),
    'shift_63': ('int', 32, 126),
    'tmax': ('int', 10, 40),
}
TALA = ['tmax', 'rolling_20', 'l_kali_0_99', 'shift_2', 'shift_3']

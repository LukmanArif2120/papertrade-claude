# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M149.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'ema_15': 15,
    'atr_15': 15,
    'k_ambang_15': 15,
    'a_kali_4': 4,
    'atr_kali_2_5': 2.5,
    'k_ambang_3': 3,
    'susut_ambang_0_2': 0.2,
    'p_susut_ambang_0_2_ambang_0_8': 0.8,
    'a_kali_2': 2,
    'rank_shift_63': 63,
    'had_henti': 0.85,
}
ID = 'M149'
NAMA = '3-Step Pullback'
VARIAN = 'V1 WFO beku: henti ASAL, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_ema_15 = P['ema_15']
    _p_atr_15 = P['atr_15']
    _p_k_ambang_15 = P['k_ambang_15']
    _p_a_kali_4 = P['a_kali_4']
    _p_atr_kali_2_5 = P['atr_kali_2_5']
    _p_k_ambang_3 = P['k_ambang_3']
    _p_susut_ambang_0_2 = P['susut_ambang_0_2']
    _p_p_susut_ambang_0_2_ambang_0_8 = P['p_susut_ambang_0_2_ambang_0_8']
    _p_a_kali_2 = P['a_kali_2']
    for g in fr.values():
        o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
        n = len(g)
        e = ema(g.close, _p_ema_15).values
        a = atr(g, _p_atr_15).values
        sig = np.zeros(n, bool)
        t0 = -1
        mx = -np.inf
        for i in range(1, n):
            if np.isnan(a[i]):
                continue
            if c[i] > e[i] + _p_a_kali_2 * a[i]:
                t0 = i
                mx = h[i]
                continue
            if t0 < 0:
                continue
            mx = max(mx, h[i])
            k = i - t0
            if k > _p_k_ambang_15:
                t0 = -1
                continue
            lebar = _p_a_kali_4 * a[i]
            susut = (mx - min(l[t0 + 1:i + 1])) / lebar
            if k >= _p_k_ambang_3 and _p_susut_ambang_0_2 <= susut <= _p_p_susut_ambang_0_2_ambang_0_8 and (c[i] > o[i]) and (c[i] > h[i - 1]):
                sig[i] = True
                t0 = -1
        stop = g.close - _p_atr_kali_2_5 * atr(g, _p_atr_15)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ASAL'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'ema_15': ('int', 8, 30),
    'atr_15': ('int', 8, 30),
    'a_kali_4': ('float', 2.0, 6.0),
    'atr_kali_2_5': ('float', 1.25, 3.75),
    'susut_ambang_0_2': ('float', 0.1, 0.3),
    'p_susut_ambang_0_2_ambang_0_8': ('float', 0.4, 0.99),
    'a_kali_2': ('float', 1.0, 3.0),
    'rank_shift_63': ('int', 32, 126),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['had_henti', 'atr_15', 'atr_kali_2_5', 'ema_15', 'a_kali_4', 'susut_ambang_0_2']

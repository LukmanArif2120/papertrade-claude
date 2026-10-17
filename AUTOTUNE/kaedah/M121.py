# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M121.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'ema_20': 20,
    'range_2': 2,
    'kira_ambang_2': 2,
    'pos_ambang_0_75': 0.75,
    'i_tolak_2': 2,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
    'tmax': 63,
}
ID = 'M121'
NAMA = 'High 2 bull flag (Brooks)'
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_ema_20 = P['ema_20']
    _p_range_2 = P['range_2']
    _p_kira_ambang_2 = P['kira_ambang_2']
    _p_pos_ambang_0_75 = P['pos_ambang_0_75']
    _p_i_tolak_2 = P['i_tolak_2']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        e20 = ema(g.close, _p_ema_20)
        tren = ((g.close > e20) & (e20 > e20.shift())).values
        pos = ((g.close - g.low) / (g.high - g.low)).where(g.high > g.low).values
        n = len(g)
        h2 = np.zeros(n, bool)
        sw = -np.inf
        dalam = False
        kira = 0
        for i in range(_p_range_2, n):
            if h[i] > sw and (not dalam):
                sw = h[i]
                continue
            if h[i] > sw and dalam:
                sw = h[i]
                dalam = False
                kira = 0
                continue
            if not dalam and h[i] < h[i - 1]:
                dalam = True
                kira = 0
                continue
            if dalam and h[i] > h[i - 1] and (h[i - 1] < h[i - _p_i_tolak_2]):
                kira += 1
                if kira == _p_kira_ambang_2 and tren[i] and (pos[i] >= _p_pos_ambang_0_75):
                    h2[i] = True
        H2 = pd.Series(h2, g.index)
        stop = g.low.shift(1)
        sig = H2.shift(1, fill_value=False) & (g.close > g.high.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'ema_20': ('int', 10, 40),
    'kira_ambang_2': ('int', 1, 3),
    'pos_ambang_0_75': ('float', 0.375, 0.99),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 7.5, 22.5),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['henti_pct', 'had_henti', 'ema_20', 'kira_ambang_2', 'pos_ambang_0_75']

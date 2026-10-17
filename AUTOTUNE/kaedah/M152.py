# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M152.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_12': 12,
    'pos_ambang_0_75': 0.75,
    'range_5': 5,
    'range_a1_12': 12,
    'rolling_5': 5,
    'naik_aliran_sma_50': 50,
    'naik_aliran_shift_20': 20,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
    'tmax': 42,
}
ID = 'M152'
NAMA = 'Spike & Ledge'
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_range_12 = P['range_12']
    _p_pos_ambang_0_75 = P['pos_ambang_0_75']
    _p_range_5 = P['range_5']
    _p_range_a1_12 = P['range_a1_12']
    _p_rolling_5 = P['rolling_5']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        naik = naik_aliran(g.close, P=P).values
        pos = ((g.close - g.low) / (g.high - g.low)).where(g.high > g.low).values
        l5 = g.low.shift(1).rolling(_p_rolling_5).min().values
        S = naik & (l < l5) & (pos >= _p_pos_ambang_0_75)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        for i in range(_p_range_12, n):
            for k in range(_p_range_5, _p_range_a1_12):
                s = i - k
                if not S[s]:
                    continue
                para = slice(s + 1, i)
                if l[para].min() > l[s] and c[i] > c[para].max():
                    sig[i] = True
                    stop[i] = l[para].min()
                    break
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st, P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'pos_ambang_0_75': ('float', 0.375, 0.99),
    'rolling_5': ('int', 2, 10),
    'naik_aliran_sma_50': ('int', 25, 100),
    'naik_aliran_shift_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 7.5, 22.5),
    'had_henti': ('float', 0.425, 0.99),
    'tmax': ('int', 21, 60),
}
TALA = ['tmax', 'henti_pct', 'had_henti']

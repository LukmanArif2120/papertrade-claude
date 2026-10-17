# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M151.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_21': 21,
    'sma_20': 20,
    'i_ambang_10': 10,
    'rank_shift_63': 63,
    'henti_atr': 1.5,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
}
ID = 'M151'
NAMA = 'Outside Bar Failure'
VARIAN = 'V1 WFO beku: henti ATR1.5, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_range_21 = P['range_21']
    _p_sma_20 = P['sma_20']
    _p_i_ambang_10 = P['i_ambang_10']
    for g in fr.values():
        o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
        n = len(g)
        s20 = sma(g.close, _p_sma_20).values
        sig = np.zeros(n, bool)
        t = -1
        lo = np.nan
        tembus = False
        u = np.nan
        for i in range(_p_range_21, n):
            if h[i] > h[i - 1] and l[i] < l[i - 1] and (c[i] < o[i]) and (s20[i] > s20[i - 1]):
                t = i
                lo = l[i]
                tembus = False
                u = np.nan
                continue
            if t < 0:
                continue
            if i - t > _p_i_ambang_10 or h[i] < lo:
                t = -1
                continue
            if not tembus:
                if l[i] < lo:
                    tembus = True
                continue
            if not np.isnan(u) and c[i] > u:
                sig[i] = True
                t = -1
                continue
            if c[i] > o[i]:
                u = h[i]
        siap_lajur(g, pd.Series(sig, g.index), pd.Series(np.nan, g.index), P=P)
HENTI_KOD = 'ATR1.5'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'sma_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 0.75, 2.25),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_chan': ('float', 2.0, 6.0),
    'keluar_chan_tinggi': ('int', 11, 44),
    'keluar_chan_atr': ('int', 11, 44),
}
TALA = ['henti_atr', 'keluar_chan', 'keluar_chan_tinggi', 'keluar_chan_atr', 'sma_20']

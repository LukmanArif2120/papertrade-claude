# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M148.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'wma_180': 180,
    'i_ambang_20': 20,
    'p_ambang_20': 20,
    'pulang_5_0': 5.0,
    'p_ambang_100': 100,
    'pulang_10_0': 10.0,
    'pulang_50_0': 50.0,
    'p_ambang_500': 500,
    'rank_shift_63': 63,
    'henti_pct': 6,
    'had_henti': 0.85,
    'keluar_ema': 10,
    'tmax': 42,
}
ID = 'M148'
NAMA = 'Natural Number Method'
VARIAN = 'V1 WFO beku: henti PCT6, keluar EMA10, tmax 42'
TMAX = 42
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 200

def langkah(p, *, P=PARAM):
    return 1.0 if p < P['p_ambang_20'] else P['pulang_5_0'] if p < P['p_ambang_100'] else P['pulang_10_0'] if p < P['p_ambang_500'] else P['pulang_50_0']

def _entri(fr, idx, *, P=PARAM):
    _p_wma_180 = P['wma_180']
    _p_i_ambang_20 = P['i_ambang_20']
    for g in fr.values():
        h, c = (g.high.values, g.close.values)
        w = wma(g.close, _p_wma_180).values
        n = len(g)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        b = -1
        lv = st = np.nan
        for i in range(1, n):
            if np.isnan(w[i]) or np.isnan(w[i - 1]):
                continue
            if c[i] > w[i] and c[i - 1] <= w[i - 1]:
                k = langkah(h[i], P=P)
                lv = (np.floor(h[i] / k) + 1) * k
                st = lv - k
                b = i
                continue
            if b >= 0:
                if c[i] <= w[i] or i - b > _p_i_ambang_20:
                    b = -1
                    continue
                if c[i] > lv:
                    sig[i] = True
                    stop[i] = st
                    b = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, exitc=g.close < pd.Series(w, g.index), P=P)
HENTI_KOD = 'PCT6'
KELUAR_KOD = 'EMA10'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'wma_180': ('int', 90, 360),
    'pulang_5_0': ('float', 2.5, 7.5),
    'pulang_10_0': ('float', 5.0, 15.0),
    'pulang_50_0': ('float', 25.0, 75.0),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 3.0, 9.0),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_ema': ('int', 5, 20),
    'tmax': ('int', 21, 60),
}
TALA = ['tmax', 'henti_pct', 'keluar_ema', 'had_henti', 'wma_180', 'pulang_5_0']

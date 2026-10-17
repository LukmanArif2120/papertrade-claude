# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M118.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'sma_50': 50,
    'rolling_9': 9,
    'rank_shift_63': 63,
    'henti_low': 5,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M118'
NAMA = 'Expansion Pivot (Cooper)'
VARIAN = 'V1 WFO beku: henti LOW5, keluar SMA50, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_rolling_9 = P['rolling_9']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        s50 = sma(c, _p_sma_50)
        rng = h - l
        luas = rng > rng.shift(1).rolling(_p_rolling_9).max()
        dekat = pd.concat([l, l.shift()], axis=1).min(axis=1) <= s50
        persediaan = luas & dekat & (c > s50) & (c > o)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'LOW5'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M120.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'c_ambang_30': 30,
    'rolling_60': 60,
    'rolling_5': 5,
    'rank_shift_63': 63,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M120'
NAMA = 'Reversal New Highs'
VARIAN = 'V1 WFO beku: henti ASAL, keluar SMA50, tmax tiada'
TMAX = None
WARM = 70
ADA_HENTI = True
SILANG = False
PERLU_BAR = 70

def _entri(fr, idx, *, P=PARAM):
    _p_c_ambang_30 = P['c_ambang_30']
    _p_rolling_60 = P['rolling_60']
    _p_rolling_5 = P['rolling_5']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        rng = h - l
        luar = (l < l.shift()) & (h > h.shift())
        persediaan = (c > _p_c_ambang_30) & luar & (rng >= rng.rolling(_p_rolling_5).max()) & (h >= h.rolling(_p_rolling_60).max())
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ASAL'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'c_ambang_30': ('int', 15, 45),
    'rolling_60': ('int', 30, 120),
    'rolling_5': ('int', 2, 10),
    'rank_shift_63': ('int', 32, 126),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_sma': ('int', 25, 100),
}
TALA = ['keluar_sma', 'had_henti', 'c_ambang_30', 'rolling_60', 'rolling_5']

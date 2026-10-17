# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M128.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_50': 50,
    'h_ambang_0_45': 0.45,
    'shift_20': 20,
    'rank_shift_63': 63,
    'henti_pct': 10,
    'had_henti': 0.85,
    'keluar_sma': 20,
    'tmax': 42,
}
ID = 'M128'
NAMA = 'Inventory Retracement Bar (IRB, Rob Hoffman)'
VARIAN = 'V1 WFO beku: henti PCT10, keluar SMA20, tmax 42'
TMAX = 42
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_h_ambang_0_45 = P['h_ambang_0_45']
    _p_shift_20 = P['shift_20']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        s50 = sma(c, _p_sma_50)
        naik = (c > s50) & (s50 > s50.shift(_p_shift_20))
        r = (h - l).where(h > l)
        irb = naik & ((h - o) / r >= _p_h_ambang_0_45) & ((h - c) / r >= _p_h_ambang_0_45)
        stop = l.shift(1)
        sig = irb.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT10'
KELUAR_KOD = 'SMA20'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

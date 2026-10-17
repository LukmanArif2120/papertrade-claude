# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M119.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'sma_50': 50,
    'pos_ambang_0_25': 0.25,
    'pos_ambang_0_75': 0.75,
    'sma_10': 10,
    'rank_shift_63': 63,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
    'tmax': 42,
}
ID = 'M119'
NAMA = '180 Bullish (Cooper)'
VARIAN = 'V1 WFO beku: henti ASAL, keluar CHAN4, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_pos_ambang_0_25 = P['pos_ambang_0_25']
    _p_pos_ambang_0_75 = P['pos_ambang_0_75']
    _p_sma_10 = P['sma_10']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        pos = ((c - l) / (h - l)).where(h > l)
        persediaan = (pos.shift() <= _p_pos_ambang_0_25) & (pos >= _p_pos_ambang_0_75) & (c > sma(c, _p_sma_10)) & (c > sma(c, _p_sma_50))
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ASAL'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

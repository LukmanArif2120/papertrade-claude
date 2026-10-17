# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M124.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'stoch_k_39': 39,
    'stoch_k_d_3': 3,
    'k_ambang_50': 50,
    'rank_shift_63': 63,
    'henti_atr': 2.0,
    'had_henti': 0.85,
    'keluar_chan': 3,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
    'tmax': 63,
}
ID = 'M124'
NAMA = "'Last' Stochastic Technique (ChartSchool)"
VARIAN = 'V1 WFO beku: henti ATR2, keluar CHAN3, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_stoch_k_39 = P['stoch_k_39']
    _p_stoch_k_d_3 = P['stoch_k_d_3']
    _p_k_ambang_50 = P['k_ambang_50']
    for g in fr.values():
        c = g.close
        k = stoch_k(g, _p_stoch_k_39, _p_stoch_k_d_3)
        tinggi = mingguan_lalu(g, lambda gb: gb.close.max())
        rendah = mingguan_lalu(g, lambda gb: gb.close.min())
        sig = (k > _p_k_ambang_50) & (k.shift() <= _p_k_ambang_50) & (c > tinggi)
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=(k < _p_k_ambang_50) & (c < rendah), P=P)
HENTI_KOD = 'ATR2'
KELUAR_KOD = 'CHAN3'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'stoch_k_39': ('int', 20, 78),
    'stoch_k_d_3': ('int', 2, 6),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.0, 3.0),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_chan': ('float', 1.5, 4.5),
    'keluar_chan_tinggi': ('int', 11, 44),
    'keluar_chan_atr': ('int', 11, 44),
}
TALA = ['henti_atr', 'keluar_chan', 'keluar_chan_tinggi', 'keluar_chan_atr', 'stoch_k_39', 'stoch_k_d_3']

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M130.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'rolling_20': 20,
    'pb_kali_1_5': 1.5,
    'sma_5': 5,
    'sma_10': 10,
    'sma_20': 20,
    'rolling_3': 3,
    'shift_2': 2,
    'b_kali_0_5': 0.5,
    'rank_shift_63': 63,
    'henti_atr': 3.5,
    'had_henti': 0.85,
}
ID = 'M130'
NAMA = '多方炮 (dua lilin hijau mengapit satu merah)'
VARIAN = 'V1 WFO beku: henti ATR3.5, keluar ASAL, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_rolling_20 = P['rolling_20']
    _p_pb_kali_1_5 = P['pb_kali_1_5']
    _p_sma_5 = P['sma_5']
    _p_sma_10 = P['sma_10']
    _p_sma_20 = P['sma_20']
    _p_rolling_3 = P['rolling_3']
    _p_shift_2 = P['shift_2']
    _p_b_kali_0_5 = P['b_kali_0_5']
    for g in fr.values():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        b = (c - o).abs()
        pb = b.rolling(_p_rolling_20).mean()
        L1 = (c > o) & (b >= _p_pb_kali_1_5 * pb)
        L2 = (c < o) & (b < _p_b_kali_0_5 * b.shift(1)) & (v < v.shift(1)) & (l > o.shift(1))
        L3 = (c > o) & (v > v.shift(1)) & (o <= c.shift(1)) & (c >= o.shift(1))
        susun = (sma(c, _p_sma_5) > sma(c, _p_sma_10)) & (sma(c, _p_sma_10) > sma(c, _p_sma_20))
        sig = L1.shift(_p_shift_2, fill_value=False) & L2.shift(1, fill_value=False) & L3 & susun
        stop = l.rolling(_p_rolling_3).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR3.5'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_20': ('int', 10, 40),
    'pb_kali_1_5': ('float', 0.75, 2.25),
    'sma_5': ('int', 2, 10),
    'sma_10': ('int', 5, 20),
    'sma_20': ('int', 10, 40),
    'rolling_3': ('int', 2, 6),
    'shift_2': ('int', 2, 4),
    'b_kali_0_5': ('float', 0.25, 0.75),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.75, 5.25),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['henti_atr', 'had_henti', 'rolling_3', 'sma_10', 'rolling_20', 'pb_kali_1_5']

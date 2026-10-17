# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M161.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'supertrend_hijau_10': 10,
    'supertrend_hijau_k_3_0': 3.0,
    'ema_10': 10,
    'ema_21': 21,
    'atr_kali_1_5': 1.5,
    'rolling_10': 10,
    'rolling_5': 5,
    'atr_14': 14,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
}
ID = 'M161'
NAMA = 'EMA 10/21 + Supertrend (10,3)'
VARIAN = 'V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_supertrend_hijau_10 = P['supertrend_hijau_10']
    _p_supertrend_hijau_k_3_0 = P['supertrend_hijau_k_3_0']
    _p_ema_10 = P['ema_10']
    _p_ema_21 = P['ema_21']
    _p_atr_kali_1_5 = P['atr_kali_1_5']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_5 = P['rolling_5']
    _p_atr_14 = P['atr_14']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        e10, e21 = (ema(c, _p_ema_10), ema(c, _p_ema_21))
        st = supertrend_hijau(g, _p_supertrend_hijau_10, _p_supertrend_hijau_k_3_0)
        A = (l <= e10) & (c > o) & (c > e10)
        rng5 = h.shift(1).rolling(_p_rolling_5).max() - l.shift(1).rolling(_p_rolling_5).min()
        B = (rng5 <= _p_atr_kali_1_5 * atr(g, n=_p_atr_14)) & (c > h.shift(1).rolling(_p_rolling_5).max())
        sig = (e10 > e21) & st & (A | B)
        stop = l.rolling(_p_rolling_10).min()
        siap_lajur(g, sig & ~langkau(g, stop), stop, exitc=(c < e21) & (c.shift() < e21.shift()), P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'supertrend_hijau_10': ('int', 5, 20),
    'supertrend_hijau_k_3_0': ('float', 1.5, 4.5),
    'ema_10': ('int', 5, 20),
    'ema_21': ('int', 10, 42),
    'atr_kali_1_5': ('float', 0.75, 2.25),
    'rolling_10': ('int', 5, 20),
    'rolling_5': ('int', 2, 10),
    'atr_14': ('int', 7, 28),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 7.5, 22.5),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['henti_pct', 'had_henti', 'ema_21', 'rolling_10', 'rolling_5', 'supertrend_hijau_10']

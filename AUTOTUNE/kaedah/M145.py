# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M145.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'ema_20': 20,
    'pos_ambang_0_75': 0.75,
    'ffill_limit_3': 3,
    'rolling_20': 20,
    'rolling_3': 3,
    'rolling_10': 10,
    'rank_shift_63': 63,
    'henti_low': 10,
    'had_henti': 0.85,
}
ID = 'M145'
NAMA = 'Yum-Yum Continuation'
VARIAN = 'V1 WFO beku: henti LOW10, keluar ASAL, tmax tiada'
TMAX = None
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_ema_20 = P['ema_20']
    _p_pos_ambang_0_75 = P['pos_ambang_0_75']
    _p_ffill_limit_3 = P['ffill_limit_3']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_3 = P['rolling_3']
    _p_rolling_10 = P['rolling_10']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        e = ema(c, _p_ema_20)
        r = h - l
        pos = ((c - l) / r).where(r > 0)
        yy = (c > e) & (e > e.shift()) & (r > r.shift(1).rolling(_p_rolling_10).mean()) & (c > h.shift(1).rolling(_p_rolling_20).max()) & (pos >= _p_pos_ambang_0_75) & (c > o)
        tahap = h.where(yy).ffill(limit=_p_ffill_limit_3).shift(1)
        lw = l.where(yy).ffill(limit=_p_ffill_limit_3).shift(1)
        sig = tahap.notna() & (c > tahap) & ~yy.shift(1, fill_value=False).rolling(_p_rolling_3).max().isna()
        sig = sig & ~(c.shift() > tahap)
        siap_lajur(g, sig & ~langkau(g, lw), lw, P=P)
HENTI_KOD = 'LOW10'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

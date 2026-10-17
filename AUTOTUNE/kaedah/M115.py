# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M115.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'between_3': 3,
    'between_a1_5': 5,
    'sma_10': 10,
    'ema_20': 20,
    'ema_30': 30,
    'shift_2': 2,
    'rank_shift_63': 63,
    'had_henti': 0.85,
    'tmax': 42,
}
ID = 'M115'
NAMA = 'Bow Tie (Landry)'
VARIAN = 'V1 WFO beku: henti ASAL, keluar ASAL, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_between_3 = P['between_3']
    _p_between_a1_5 = P['between_a1_5']
    _p_sma_10 = P['sma_10']
    _p_ema_20 = P['ema_20']
    _p_ema_30 = P['ema_30']
    _p_shift_2 = P['shift_2']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        susun = (sma(c, _p_sma_10) > ema(c, _p_ema_20)) & (ema(c, _p_ema_20) > ema(c, _p_ema_30))
        run = susun.groupby((~susun).cumsum()).cumsum()
        naik = c > c.shift()
        undur = (c < c.shift()) & (h < h.shift())
        persediaan = susun & undur & naik.shift(1, fill_value=False) & naik.shift(_p_shift_2, fill_value=False) & run.shift(1).between(_p_between_3, _p_between_a1_5)
        stop = l.shift(1)
        sig = persediaan.shift(1, fill_value=False) & (c > h.shift(1)) & susun
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ASAL'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

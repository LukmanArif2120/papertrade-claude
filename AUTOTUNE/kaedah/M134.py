# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M134.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_10': 10,
    'run_ambang_5': 5,
    'rolling_60': 60,
    'rank_shift_63': 63,
    'henti_atr': 2.0,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
}
ID = 'M134'
NAMA = 'First Kiss After Daylight (Landry)'
VARIAN = 'V1 WFO beku: henti ATR2, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_sma_10 = P['sma_10']
    _p_run_ambang_5 = P['run_ambang_5']
    _p_rolling_60 = P['rolling_60']
    for g in fr.values():
        h, l, c = (g.high, g.low, g.close)
        s10 = sma(c, _p_sma_10)
        atas = l > s10
        run = atas.groupby((~atas).cumsum()).cumsum()
        cium = (l <= s10) & (run.shift(1) >= _p_run_ambang_5)
        lowu = (l <= l.rolling(_p_rolling_60).min()).astype(float).rolling(_p_rolling_60).max() > 0
        stop = l.shift(1)
        sig = (cium & lowu).shift(1, fill_value=False) & (c > h.shift(1))
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'ATR2'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

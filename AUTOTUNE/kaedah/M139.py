# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M139.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'atr_kali_0_5': 0.5,
    'sma_5': 5,
    'sma_10': 10,
    'sma_20': 20,
    'atr_14': 14,
    'rolling_20': 20,
    'shift_2': 2,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
    'tmax': 21,
}
ID = 'M139'
NAMA = '均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik)'
VARIAN = 'V1 WFO beku: henti PCT15, keluar TIADA, tmax 21'
TMAX = 21
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_atr_kali_0_5 = P['atr_kali_0_5']
    _p_sma_5 = P['sma_5']
    _p_sma_10 = P['sma_10']
    _p_sma_20 = P['sma_20']
    _p_atr_14 = P['atr_14']
    _p_rolling_20 = P['rolling_20']
    _p_shift_2 = P['shift_2']
    for g in fr.values():
        c, l = (g.close, g.low)
        m = pd.concat([sma(c, _p_sma_5), sma(c, _p_sma_10), sma(c, _p_sma_20)], axis=1)
        himpun = m.max(axis=1) - m.min(axis=1) <= _p_atr_kali_0_5 * atr(g, n=_p_atr_14)
        pertama = himpun.shift(1, fill_value=False) & (himpun.shift(_p_shift_2).astype(float).rolling(_p_rolling_20).max() == 0)
        sig = pertama & (c > m.max(axis=1))
        stop = l
        siap_lajur(g, sig & ~langkau(g, stop), stop, P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M138.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'rolling_5': 5,
    'rolling_20': 20,
    'vrun_kali_0_5': 0.5,
    'r_ambang_5': 5,
    'brun_kali_0_5': 0.5,
    'v_kali_3': 3,
    'shift_6': 6,
    'rank_shift_63': 63,
    'henti_atr': 4.0,
    'had_henti': 0.85,
    'tmax': 63,
}
ID = 'M138'
NAMA = '直升机空中加油 (Helikopter isi minyak di udara)'
VARIAN = 'V1 WFO beku: henti ATR4, keluar TIADA, tmax 63'
TMAX = 63
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_rolling_5 = P['rolling_5']
    _p_rolling_20 = P['rolling_20']
    _p_vrun_kali_0_5 = P['vrun_kali_0_5']
    _p_r_ambang_5 = P['r_ambang_5']
    _p_brun_kali_0_5 = P['brun_kali_0_5']
    _p_v_kali_3 = P['v_kali_3']
    _p_shift_6 = P['shift_6']
    for g in fr.values():
        o, c, v = (g.open, g.close, g.volume)
        naik = c > c.shift()
        run = naik.groupby((~naik).cumsum()).cumsum()
        r = run.shift(1).fillna(0)
        vrun = v.shift(1).rolling(_p_rolling_5).mean()
        brun = (c - o).abs().shift(1).rolling(_p_rolling_5).mean()
        v20 = v.shift(_p_shift_6).rolling(_p_rolling_20).mean()
        turun = (c < o) & (o - c < _p_brun_kali_0_5 * brun) & (v < _p_vrun_kali_0_5 * vrun)
        sig = (r >= _p_r_ambang_5) & (vrun > v20) & turun
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=v > _p_v_kali_3 * v.rolling(_p_rolling_20).mean().shift(1), P=P)
HENTI_KOD = 'ATR4'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_5': ('int', 2, 10),
    'rolling_20': ('int', 10, 40),
    'vrun_kali_0_5': ('float', 0.25, 0.75),
    'r_ambang_5': ('int', 2, 8),
    'brun_kali_0_5': ('float', 0.25, 0.75),
    'v_kali_3': ('float', 1.5, 4.5),
    'shift_6': ('int', 3, 12),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 2.0, 6.0),
    'had_henti': ('float', 0.425, 0.99),
}
TALA = ['henti_atr', 'v_kali_3', 'had_henti', 'rolling_20', 'rolling_5', 'vrun_kali_0_5']

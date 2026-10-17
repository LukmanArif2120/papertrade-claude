# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M159.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'o_bahagi_4': 4,
    'o_bahagi_2': 2,
    'ho_bahagi_2': 2,
    'hh_kali_0_1': 0.1,
    'shift_5': 5,
    'rank_shift_63': 63,
    'henti_pct': 15,
    'had_henti': 0.85,
    'keluar_sma': 20,
    'tmax': 10,
}
ID = 'M159'
NAMA = 'Heikin-Ashi Trend'
VARIAN = 'V1 WFO beku: henti PCT15, keluar SMA20, tmax 10'
TMAX = 10
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_o_bahagi_4 = P['o_bahagi_4']
    _p_o_bahagi_2 = P['o_bahagi_2']
    _p_ho_bahagi_2 = P['ho_bahagi_2']
    _p_hh_kali_0_1 = P['hh_kali_0_1']
    _p_shift_5 = P['shift_5']
    for g in fr.values():
        o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
        n = len(g)
        hc = (o + h + l + c) / _p_o_bahagi_4
        ho = np.empty(n)
        ho[0] = (o[0] + c[0]) / _p_o_bahagi_2
        for i in range(1, n):
            ho[i] = (ho[i - 1] + hc[i - 1]) / _p_ho_bahagi_2
        hh = np.maximum(h, np.maximum(ho, hc))
        hl = np.minimum(l, np.minimum(ho, hc))
        hcs, hos = (pd.Series(hc, g.index), pd.Series(ho, g.index))
        bull = hcs > hos
        bayang = np.minimum(ho, hc) - hl <= _p_hh_kali_0_1 * (hh - hl)
        sig = bull & pd.Series(bayang, g.index) & (g.close > g.close.shift(_p_shift_5))
        siap_lajur(g, sig, pd.Series(np.nan, g.index), exitc=hcs < hos, P=P)
HENTI_KOD = 'PCT15'
KELUAR_KOD = 'SMA20'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'hh_kali_0_1': ('float', 0.05, 0.15),
    'shift_5': ('int', 2, 10),
    'rank_shift_63': ('int', 32, 126),
    'henti_pct': ('float', 7.5, 22.5),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_sma': ('int', 10, 40),
    'tmax': ('int', 5, 20),
}
TALA = ['tmax', 'henti_pct', 'keluar_sma', 'had_henti', 'hh_kali_0_1', 'shift_5']

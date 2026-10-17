# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M143.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_5': 5,
    'hh_ambang_0_15': 0.15,
    'i_ambang_10': 10,
    'c_kali_1_07': 1.07,
    'v20_kali_2': 2,
    'rolling_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 3.5,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
    'tmax': 21,
}
ID = 'M143'
NAMA = '장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang)'
VARIAN = 'V1 WFO beku: henti ATR3.5, keluar CHAN4, tmax 21'
TMAX = 21
WARM = 40
ADA_HENTI = True
SILANG = False
PERLU_BAR = 40

def _entri(fr, idx, *, P=PARAM):
    _p_sma_5 = P['sma_5']
    _p_hh_ambang_0_15 = P['hh_ambang_0_15']
    _p_i_ambang_10 = P['i_ambang_10']
    _p_c_kali_1_07 = P['c_kali_1_07']
    _p_v20_kali_2 = P['v20_kali_2']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        o, h, l, c, v = (g.open.values, g.high.values, g.low.values, g.close.values, g.volume.values)
        n = len(g)
        s5 = sma(g.close, _p_sma_5).values
        v20 = g.volume.rolling(_p_rolling_20).mean().shift(1).values
        hh = g.high.rolling(_p_rolling_20).max().shift(1).values
        ll = g.low.rolling(_p_rolling_20).min().shift(1).values
        sig = np.zeros(n, bool)
        b = -1
        for i in range(1, n):
            if (hh[i] - ll[i]) / ll[i] <= _p_hh_ambang_0_15 and c[i] >= _p_c_kali_1_07 * c[i - 1] and (c[i] > o[i]) and (v[i] >= _p_v20_kali_2 * v20[i]):
                b = i
                continue
            if b >= 0 and i - b <= _p_i_ambang_10:
                if l[i] <= s5[i] and c[i] >= s5[i]:
                    sig[i] = True
                    b = -1
            elif b >= 0:
                b = -1
        stop = g.low
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, stop), stop, exitc=g.close < sma(g.close, _p_sma_5), P=P)
HENTI_KOD = 'ATR3.5'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'sma_5': ('int', 2, 10),
    'hh_ambang_0_15': ('float', 0.075, 0.225),
    'c_kali_1_07': ('float', 0.535, 1.605),
    'v20_kali_2': ('float', 1.0, 3.0),
    'rolling_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.75, 5.25),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_chan': ('float', 2.0, 6.0),
    'keluar_chan_tinggi': ('int', 11, 44),
    'keluar_chan_atr': ('int', 11, 44),
    'tmax': ('int', 10, 42),
}
TALA = ['tmax', 'henti_atr', 'keluar_chan', 'keluar_chan_tinggi', 'sma_5', 'rolling_20']

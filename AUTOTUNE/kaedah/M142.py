# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M142.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_250': 250,
    'shift_20': 20,
    'i_ambang_10': 10,
    'v20_kali_2': 2,
    'h20_kali_1_03': 1.03,
    'rolling_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 3.5,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
}
ID = 'M142'
NAMA = 'Pecahan volum dari dasar (底部放量)'
VARIAN = 'V1 WFO beku: henti ATR3.5, keluar CHAN4, tmax tiada'
TMAX = None
WARM = 270
ADA_HENTI = True
SILANG = False
PERLU_BAR = 270

def _entri(fr, idx, *, P=PARAM):
    _p_sma_250 = P['sma_250']
    _p_shift_20 = P['shift_20']
    _p_i_ambang_10 = P['i_ambang_10']
    _p_v20_kali_2 = P['v20_kali_2']
    _p_h20_kali_1_03 = P['h20_kali_1_03']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        h, l, c, v = (g.high.values, g.low.values, g.close.values, g.volume.values)
        n = len(g)
        m250 = sma(g.close, _p_sma_250).values
        m250l = pd.Series(m250).shift(_p_shift_20).values
        v20 = g.volume.rolling(_p_rolling_20).mean().shift(1).values
        h20 = g.high.rolling(_p_rolling_20).max().shift(1).values
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        b = -1
        lv = sl = np.nan
        for i in range(1, n):
            if v[i] >= _p_v20_kali_2 * v20[i] and c[i] > _p_h20_kali_1_03 * h20[i] and (c[i] > m250[i]) and (m250[i] > m250l[i]):
                b = i
                lv = h20[i]
                sl = l[i]
                continue
            if b >= 0 and i - b <= _p_i_ambang_10:
                if l[i] < lv:
                    b = -1
                    continue
                if c[i] < c[i - 1]:
                    sig[i] = True
                    stop[i] = sl
                    b = -1
            elif b >= 0:
                b = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, P=P)
HENTI_KOD = 'ATR3.5'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'sma_250': ('int', 125, 500),
    'shift_20': ('int', 10, 40),
    'v20_kali_2': ('float', 1.0, 3.0),
    'h20_kali_1_03': ('float', 0.515, 1.545),
    'rolling_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.75, 5.25),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_chan': ('float', 2.0, 6.0),
    'keluar_chan_tinggi': ('int', 11, 44),
    'keluar_chan_atr': ('int', 11, 44),
}
TALA = ['henti_atr', 'keluar_chan', 'keluar_chan_tinggi', 'keluar_chan_atr', 'rolling_20', 'sma_250']

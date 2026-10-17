# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M132.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'sma_50': 50,
    'range_100': 100,
    'i_ambang_3': 3,
    't_tolak_5': 5,
    't_ambang_40': 40,
    'i_tolak_40': 40,
    't_tolak_60': 60,
    'dalam_ambang_0_08': 0.08,
    'p_dalam_ambang_0_08_ambang_0_35': 0.35,
    'shift_20': 20,
    'pv_kali_1_02': 1.02,
    'rank_shift_63': 63,
    'henti_atr': 4.0,
    'had_henti': 0.85,
    'keluar_chan': 4,
    'keluar_chan_tinggi': 22,
    'keluar_chan_atr': 22,
    'tmax': 42,
}
ID = 'M132'
NAMA = 'Ascending Scallop (Bulkowski)'
VARIAN = 'V1 WFO beku: henti ATR4, keluar CHAN4, tmax 42'
TMAX = 42
WARM = 120
ADA_HENTI = True
SILANG = False
PERLU_BAR = 120

def _entri(fr, idx, *, P=PARAM):
    _p_sma_50 = P['sma_50']
    _p_range_100 = P['range_100']
    _p_i_ambang_3 = P['i_ambang_3']
    _p_t_tolak_5 = P['t_tolak_5']
    _p_t_ambang_40 = P['t_ambang_40']
    _p_i_tolak_40 = P['i_tolak_40']
    _p_t_tolak_60 = P['t_tolak_60']
    _p_dalam_ambang_0_08 = P['dalam_ambang_0_08']
    _p_p_dalam_ambang_0_08_ambang_0_35 = P['p_dalam_ambang_0_08_ambang_0_35']
    _p_shift_20 = P['shift_20']
    _p_pv_kali_1_02 = P['pv_kali_1_02']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        s50 = sma(g.close, _p_sma_50)
        naik = ((g.close > s50) & (s50 > s50.shift(_p_shift_20))).values
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        for i in range(_p_range_100, n):
            if not naik[i]:
                continue
            w = slice(i - _p_i_tolak_40, i)
            t = i - _p_i_tolak_40 + int(np.argmin(l[w]))
            lv = l[t]
            if i - t < _p_i_ambang_3:
                continue
            a0 = max(0, t - _p_t_tolak_60)
            a1 = t - _p_t_tolak_5
            if a1 <= a0:
                continue
            pk = a0 + int(np.argmax(h[a0:a1]))
            pv = h[pk]
            if t - pk > _p_t_ambang_40:
                continue
            dalam = (pv - lv) / pv
            if not _p_dalam_ambang_0_08 <= dalam <= _p_p_dalam_ambang_0_08_ambang_0_35:
                continue
            if c[i] > pv and c[i - 1] <= pv and (h[t:i].max() <= pv * _p_pv_kali_1_02):
                sig[i] = True
                stop[i] = lv
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, P=P)
HENTI_KOD = 'ATR4'
KELUAR_KOD = 'CHAN4'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

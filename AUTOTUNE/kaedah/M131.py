# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M131.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_4': 4,
    'i_tolak_2': 2,
    'tahap_ambang_2': 2,
    'tahap_ambang_3': 3,
    'len_ambang_2': 2,
    'tahap_2': 2,
    'tahap_3': 3,
    'k_tolak_2': 2,
    'k_tambah_2': 2,
    'nilai_2': 2,
    'rank_shift_63': 63,
    'henti_atr': 2.0,
    'had_henti': 0.85,
    'tmax': 63,
}
ID = 'M131'
NAMA = 'Ross Hook (Joe Ross)'
VARIAN = 'V1 WFO beku: henti ATR2, keluar TIADA, tmax 63'
TMAX = 63
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_range_4 = P['range_4']
    _p_i_tolak_2 = P['i_tolak_2']
    _p_tahap_ambang_2 = P['tahap_ambang_2']
    _p_tahap_ambang_3 = P['tahap_ambang_3']
    _p_len_ambang_2 = P['len_ambang_2']
    _p_tahap_2 = P['tahap_2']
    _p_tahap_3 = P['tahap_3']
    _p_k_tolak_2 = P['k_tolak_2']
    _p_k_tambah_2 = P['k_tambah_2']
    _p_nilai_2 = P['nilai_2']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        p_low = []
        p_high = []
        tahap = 0
        t2 = t3 = cg = np.nan
        mx = -np.inf
        guna = -1
        for i in range(_p_range_4, n):
            k = i - _p_i_tolak_2
            if l[k] < min(l[k - _p_k_tolak_2], l[k - 1], l[k + 1], l[k + _p_k_tambah_2]):
                p_low.append((k, l[k]))
            if h[k] > max(h[k - _p_k_tolak_2], h[k - 1], h[k + 1], h[k + _p_k_tambah_2]):
                p_high.append((k, h[k]))
            if tahap == 0 and len(p_low) >= _p_len_ambang_2 and p_high:
                (a, la), (b, lb) = (p_low[-_p_nilai_2], p_low[-1])
                hh = [x for x in p_high if a < x[0] < b]
                if hh and lb > la and (b != guna):
                    tahap = 1
                    t2 = max((x[1] for x in hh))
                    t3 = lb
                    guna = b
            if tahap == 1:
                if l[i] < t3:
                    tahap = 0
                    continue
                if c[i] > t2:
                    tahap = _p_tahap_2
                    mx = h[i]
                    continue
            if tahap == _p_tahap_ambang_2:
                if l[i] < t3:
                    tahap = 0
                    continue
                if h[i] > mx:
                    mx = h[i]
                elif h[i] < h[i - 1]:
                    tahap = _p_tahap_3
                    cg = mx
                continue
            if tahap == _p_tahap_ambang_3:
                if l[i] < t3:
                    tahap = 0
                    continue
                if c[i] > cg:
                    sig[i] = True
                    stop[i] = t3
                    tahap = 0
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, P=P)
HENTI_KOD = 'ATR2'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

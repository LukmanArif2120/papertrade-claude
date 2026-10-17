# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M156.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_41': 41,
    'i_tolak_10': 10,
    'h_kali_0_382': 0.382,
    'h_kali_0_618': 0.618,
    'k_tolak_20': 20,
    'naik_aliran_sma_50': 50,
    'naik_aliran_shift_20': 20,
    'rank_shift_63': 63,
    'henti_atr': 3.0,
    'had_henti': 0.85,
    'tmax': 10,
}
ID = 'M156'
NAMA = 'Single Penetration (DiNapoli)'
VARIAN = 'V1 WFO beku: henti ATR3, keluar TIADA, tmax 10'
TMAX = 10
WARM = 80
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

def _entri(fr, idx, *, P=PARAM):
    _p_range_41 = P['range_41']
    _p_i_tolak_10 = P['i_tolak_10']
    _p_h_kali_0_382 = P['h_kali_0_382']
    _p_h_kali_0_618 = P['h_kali_0_618']
    _p_k_tolak_20 = P['k_tolak_20']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        naik = naik_aliran(g.close, P=P).values
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        guna = -1
        for i in range(_p_range_41, n):
            if not naik[i]:
                continue
            k = i - _p_i_tolak_10 + int(np.argmax(h[i - _p_i_tolak_10:i]))
            if h[k] < h[k - _p_k_tolak_20:k].max(initial=-np.inf) or k == guna:
                continue
            L = l[k - _p_k_tolak_20:k].min()
            H = h[k]
            p38, p62 = (H - _p_h_kali_0_382 * (H - L), H - _p_h_kali_0_618 * (H - L))
            if l[k + 1:i].min(initial=np.inf) <= p38:
                continue
            if l[i] <= p38 and c[i] > p62:
                sig[i] = True
                stop[i] = p62
                guna = k
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st, P=P)
HENTI_KOD = 'ATR3'
KELUAR_KOD = 'TIADA'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'h_kali_0_382': ('float', 0.191, 0.573),
    'h_kali_0_618': ('float', 0.309, 0.927),
    'naik_aliran_sma_50': ('int', 25, 100),
    'naik_aliran_shift_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_atr': ('float', 1.5, 4.5),
    'had_henti': ('float', 0.425, 0.99),
    'tmax': ('int', 5, 20),
}
TALA = ['tmax', 'henti_atr', 'had_henti', 'h_kali_0_382', 'h_kali_0_618']

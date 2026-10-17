# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M136.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'range_2': 2,
    'i_ambang_10': 10,
    'len_ambang_3': 3,
    'nilai_2': 2,
    'nilai_3': 3,
    'rank_shift_63': 63,
    'henti_pct': 10,
    'had_henti': 0.85,
}
ID = 'M136'
NAMA = 'Short/Intermediate-term Low (Larry Williams)'
VARIAN = 'V1 WFO beku: henti PCT10, keluar ASAL, tmax tiada'
TMAX = None
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_range_2 = P['range_2']
    _p_i_ambang_10 = P['i_ambang_10']
    _p_len_ambang_3 = P['len_ambang_3']
    _p_nilai_2 = P['nilai_2']
    _p_nilai_3 = P['nilai_3']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        n = len(g)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        ljp = []
        bersedia = -1
        for i in range(_p_range_2, n):
            k = i - 1
            if l[k] < l[k - 1] and l[k] < l[i]:
                ljp.append(l[k])
                if len(ljp) >= _p_len_ambang_3 and ljp[-_p_nilai_2] < ljp[-_p_nilai_3] and (ljp[-_p_nilai_2] < ljp[-1]):
                    bersedia = i
            if bersedia >= 0 and i - bersedia <= _p_i_ambang_10 and (c[i] > h[i - 1]):
                sig[i] = True
                stop[i] = ljp[-1]
                bersedia = -1
            elif bersedia >= 0 and i - bersedia > _p_i_ambang_10:
                bersedia = -1
        s = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, s), s, P=P)
HENTI_KOD = 'PCT10'
KELUAR_KOD = 'ASAL'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

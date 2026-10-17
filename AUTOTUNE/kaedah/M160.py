# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M160.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
from enjin import atr
import numpy as np, pandas as pd
PARAM = {
    'atr_14': 14,
    'a_kali_3': 3,
    'rt_ambang_0_3': 0.3,
    'p_rt_ambang_0_3_ambang_0_7': 0.7,
    'rank_shift_63': 63,
    'henti_low': 10,
    'had_henti': 0.85,
    'keluar_ema': 21,
    'tmax': 42,
}
ID = 'M160'
NAMA = 'Measured Move Up'
VARIAN = 'V1 WFO beku: henti LOW10, keluar EMA21, tmax 42'
TMAX = 42
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

def _entri(fr, idx, *, P=PARAM):
    _p_atr_14 = P['atr_14']
    _p_a_kali_3 = P['a_kali_3']
    _p_rt_ambang_0_3 = P['rt_ambang_0_3']
    _p_p_rt_ambang_0_3_ambang_0_7 = P['p_rt_ambang_0_3_ambang_0_7']
    for g in fr.values():
        h, l, c = (g.high.values, g.low.values, g.close.values)
        a = atr(g, n=_p_atr_14).values
        n = len(g)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        arah = 0
        ext = np.nan
        A = B = np.nan
        lo = np.inf
        aktif = False
        for i in range(1, n):
            if np.isnan(a[i]):
                continue
            if arah >= 0:
                if np.isnan(ext) or h[i] > ext:
                    ext = h[i]
                if ext - l[i] >= _p_a_kali_3 * a[i]:
                    B = ext
                    arah = -1
                    ext = l[i]
                    aktif = not np.isnan(A)
                    lo = l[i]
            else:
                if l[i] < ext:
                    ext = l[i]
                if h[i] - ext >= _p_a_kali_3 * a[i]:
                    A = ext
                    arah = 1
                    ext = h[i]
                    aktif = False
            if aktif:
                lo = min(lo, l[i])
                rt = (B - lo) / (B - A) if B > A else np.nan
                if lo <= A:
                    aktif = False
                    continue
                if _p_rt_ambang_0_3 <= rt <= _p_p_rt_ambang_0_3_ambang_0_7 and c[i] > h[i - 1]:
                    sig[i] = True
                    stop[i] = lo
                    aktif = False
        st = pd.Series(stop, g.index)
        siap_lajur(g, pd.Series(sig, g.index) & ~langkau(g, st), st, P=P)
HENTI_KOD = 'LOW10'
KELUAR_KOD = 'EMA21'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

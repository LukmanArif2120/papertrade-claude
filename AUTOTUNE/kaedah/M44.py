# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M44.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    't_ambang_0_15': 0.15,
    't_tambah_0_1': 0.1,
    'c_ambang_0_2': 0.2,
    'rolling_50': 50,
    'shift_26': 26,
    'shift_89': 89,
    'rolling_25': 25,
    'rolling_9': 9,
    'open_kali_0_92': 0.92,
    'iloc_kali_0_92': 0.92,
    'tb_kali_1_05': 1.05,
    'shift_63': 63,
}
ID = 'M44'
NAMA = 'Tapak Rata IBD'
VARIAN = 'V3 V1 tanpa syarat volum'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _tapak(g, *, P=PARAM):
    c = g.close
    T = g.high.rolling(P['rolling_25']).max().shift(1)
    R = g.low.rolling(P['rolling_25']).min().shift(1)
    dalam = (T - R) / T <= P['t_ambang_0_15']
    awal = g.high.rolling(P['rolling_9']).max().shift(1) < T
    tb = T + P['t_tambah_0_1']
    dahulu = c.shift(P['shift_26']) / c.shift(P['shift_89']) - 1 >= P['c_ambang_0_2']
    s50 = c.rolling(P['rolling_50']).mean()
    return (T, R, dalam, awal, tb, dahulu, s50)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_open_kali_0_92 = P['open_kali_0_92']
    _p_iloc_kali_0_92 = P['iloc_kali_0_92']
    _p_tb_kali_1_05 = P['tb_kali_1_05']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c = g.close
        T, R, dalam, awal, tb, dahulu, s50 = _tapak(g, P=P)
        pecah = (c > tb) & (c.shift() <= tb)
        dekat = c <= _p_tb_kali_1_05 * tb
        g['sig'] = dalam & awal & pecah & dahulu & dekat & (c > s50)
        st = _p_open_kali_0_92 * g.open.shift(-1)
        st.iloc[-1] = _p_iloc_kali_0_92 * c.iloc[-1]
        g['stop'] = st
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_T'] = T
        g['_R'] = R
        g['_dalam'] = dalam
        g['_awal'] = awal
        g['_dahulu'] = dahulu
        g['_s50'] = s50
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

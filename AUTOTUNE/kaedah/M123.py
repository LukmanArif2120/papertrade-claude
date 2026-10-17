# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M123.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from _k145 import *
import numpy as np, pandas as pd
PARAM = {
    'cci_20': 20,
    'v_ambang_100': 100,
    'cd_ambang_100': 100,
    'cds_ambang_100': 100,
    'rank_shift_63': 63,
    'henti_low': 1,
    'had_henti': 0.85,
    'keluar_sma': 50,
}
ID = 'M123'
NAMA = 'CCI Correction (Lambert, ChartSchool)'
VARIAN = 'V1 WFO beku: henti LOW1, keluar SMA50, tmax tiada'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 200

def _entri(fr, idx, *, P=PARAM):
    _p_cci_20 = P['cci_20']
    _p_v_ambang_100 = P['v_ambang_100']
    _p_cd_ambang_100 = P['cd_ambang_100']
    _p_cds_ambang_100 = P['cds_ambang_100']
    for g in fr.values():
        wk = g.index.to_period('W-FRI')
        w = g.groupby(wk).agg(high=('high', 'max'), low=('low', 'min'), close=('close', 'last'))
        cw = cci(w.high, w.low, w.close, _p_cci_20).values
        b = np.zeros(len(cw), bool)
        st = False
        for j, v in enumerate(cw):
            if v > _p_v_ambang_100:
                st = True
            elif v < -_p_v_ambang_100:
                st = False
            b[j] = st
        bias_w = pd.Series(b, w.index)
        bias = pd.Series(wk.map(lambda p: bias_w.get(p - 1, False)), g.index).astype(bool)
        cd = cci(g.high, g.low, g.close, _p_cci_20).values
        n = len(g)
        turun = False
        sg = np.zeros(n, bool)
        for i in range(1, n):
            if cd[i] < -_p_cd_ambang_100:
                turun = True
            if turun and cd[i] > 0 and (cd[i - 1] <= 0):
                sg[i] = True
                turun = False
            elif cd[i] > 0:
                turun = False
        cds = pd.Series(cd, g.index)
        siap_lajur(g, pd.Series(sg, g.index) & bias, pd.Series(np.nan, g.index), exitc=(cds < _p_cds_ambang_100) & (cds.shift() >= _p_cds_ambang_100), P=P)
HENTI_KOD = 'LOW1'
KELUAR_KOD = 'SMA50'

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _entri(fr, idx, P=P)
    pasang(fr, HENTI_KOD, KELUAR_KOD, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'cci_20': ('int', 10, 40),
    'rank_shift_63': ('int', 32, 126),
    'henti_low': ('int', 1, 2),
    'had_henti': ('float', 0.425, 0.99),
    'keluar_sma': ('int', 25, 100),
}
TALA = ['henti_low', 'keluar_sma', 'had_henti', 'cci_20']

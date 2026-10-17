# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M68.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'n': 10,
    'pangsi_ambang_0_12': 0.12,
    'pangsi_ambang_0_2': 0.2,
    'rolling_50': 50,
    'ewm_span_10': 10,
    'ewm_span_20': 20,
    'rolling_63': 63,
    'rolling_30': 30,
    'shift_63': 63,
}
ID = 'M68'
NAMA = "Kell Base n' Break"
VARIAN = 'V3 V1 keluar close<SMA50 (+tutup>SMA50)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N = 10

def _syarat(g, *, P=PARAM):
    c = g.close
    e10 = c.ewm(span=P['ewm_span_10'], adjust=False).mean()
    e20 = c.ewm(span=P['ewm_span_20'], adjust=False).mean()
    s50 = c.rolling(P['rolling_50']).mean()
    pangsi = g.high.rolling(P['n']).max().shift(1)
    lowt = g.low.rolling(P['n']).min().shift(1)
    ketat = pangsi / lowt - 1 <= P['pangsi_ambang_0_12']
    sokong = ((c >= e20).astype(int).rolling(P['n']).sum().shift(1) == P['n']) & (e10.shift(1) > e20.shift(1))
    baharu = pangsi >= g.high.rolling(P['rolling_63']).max().shift(1)
    naikdulu = pangsi / g.low.rolling(P['rolling_30']).min().shift(P['n'] + 1) - 1 >= P['pangsi_ambang_0_2']
    return (pangsi, lowt, ketat, sokong, baharu, naikdulu, s50, e20)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        pangsi, lowt, ketat, sokong, baharu, naikdulu, s50, e20 = _syarat(g, P=P)
        sig = (g.close > pangsi) & ketat & sokong & baharu & naikdulu & (g.close > s50)
        langkau = g.open.shift(-1) <= lowt
        g['sig'] = sig & ~langkau
        g['stop'] = lowt
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

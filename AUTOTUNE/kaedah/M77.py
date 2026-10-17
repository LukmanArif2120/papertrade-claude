# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M77.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'shift_10': 10,
    'rolling_50': 50,
    'rolling_200': 200,
    'rolling_20': 20,
    'shift_63': 63,
    'rolling_5': 5,
    'clv_ambang_0_6': 0.6,
    'shift_2': 2,
}
ID = 'M77'
NAMA = 'Undercut & Rally pada Purata Bergerak (MAU&R)'
VARIAN = 'V2 V1 henti=low hari isyarat'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_10 = P['shift_10']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_200 = P['rolling_200']
    _p_rolling_20 = P['rolling_20']
    _p_shift_63 = P['shift_63']
    _p_rolling_5 = P['rolling_5']
    _p_clv_ambang_0_6 = P['clv_ambang_0_6']
    _p_shift_2 = P['shift_2']
    for g in fr.values():
        c = g.close
        P_ = c.rolling(_p_rolling_50).mean()
        s200 = c.rolling(_p_rolling_200).mean()
        bawah = c < P_
        atas = c > P_
        ada_atas = atas.astype(int).shift(_p_shift_2).rolling(_p_rolling_5).sum() > 0
        tembus = bawah.shift(1, fill_value=False) & ada_atas
        naikp = P_ > P_.shift(_p_shift_10)
        rng = g.high - g.low
        clv = ((c - g.low) / rng).where(rng > 0, 0.0)
        vol20 = g.volume.shift(1).rolling(_p_rolling_20).mean()
        stop = g.low.copy()
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_P'] = P_
        g['_s200'] = s200
        g['_tembus'] = tembus
        g['_naikp'] = naikp
        g['_clv'] = clv
        g['_vol20'] = vol20
        g['sig'] = tembus & atas & naikp & (c > s200) & (clv > _p_clv_ambang_0_6) & (g.volume > vol20) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < P_
        g['rank'] = c / c.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'shift_10': ('int', 5, 20),
    'rolling_50': ('int', 25, 100),
    'rolling_200': ('int', 100, 400),
    'rolling_20': ('int', 10, 40),
    'shift_63': ('int', 32, 126),
    'rolling_5': ('int', 2, 10),
    'clv_ambang_0_6': ('float', 0.3, 0.9),
    'shift_2': ('int', 2, 4),
}
TALA = ['rolling_50', 'rolling_200', 'rolling_20', 'rolling_5', 'clv_ambang_0_6', 'shift_10']

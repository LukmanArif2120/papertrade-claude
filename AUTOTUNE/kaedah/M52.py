# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M52.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_10': 10,
    'c_kali_0_6': 0.6,
    'shift_20': 20,
    'roc_ambang_0_3': 0.3,
    'rolling_50': 50,
    'bo_kali_0_6': 0.6,
    'rolling_20': 20,
}
ID = 'M52'
NAMA = 'Radge Weekend Trend Trader'
VARIAN = 'V3 V1 keluar tutup<SMA50 harian'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _idx_mingguan(idx, *, P=PARAM):
    s = idx['SPY'].close
    wk = s.index.to_period('W-SUN')
    tms = s.groupby(wk).last()
    return tms > tms.rolling(P['rolling_10']).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_c_kali_0_6 = P['c_kali_0_6']
    _p_shift_20 = P['shift_20']
    _p_roc_ambang_0_3 = P['roc_ambang_0_3']
    _p_rolling_50 = P['rolling_50']
    _p_bo_kali_0_6 = P['bo_kali_0_6']
    _p_rolling_20 = P['rolling_20']
    IDX = _idx_mingguan(idx, P=P)
    for g in fr.values():
        c = g.close
        wk = g.index.to_period('W-SUN')
        ws = pd.Series(wk, g.index)
        akhir = ws != ws.shift(-1)
        tm = c.groupby(wk).last()
        t20 = tm >= tm.rolling(_p_rolling_20).max()
        roc = tm / tm.shift(_p_shift_20) - 1
        idxw = IDX.reindex(tm.index).ffill().fillna(False).astype(bool)
        sw = t20 & (roc >= _p_roc_ambang_0_3) & idxw
        s50 = c.rolling(_p_rolling_50).mean()
        sigw = sw.reindex(wk).values
        sig = pd.Series(sigw, g.index).fillna(False).astype(bool) & akhir & (c > s50)
        g['sig'] = sig
        bo = g.open.shift(-1)
        g['stop'] = (_p_bo_kali_0_6 * bo).fillna(_p_c_kali_0_6 * c)
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = pd.Series(roc.reindex(wk).values, g.index)
        g['_t20'] = pd.Series(t20.reindex(wk).values, g.index)
        g['_roc'] = g['rank']
        g['_idx'] = pd.Series(idxw.reindex(wk).values, g.index)
        g['_s50'] = s50
        g['_akhir'] = akhir
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_10': ('int', 5, 20),
    'c_kali_0_6': ('float', 0.3, 0.9),
    'shift_20': ('int', 10, 40),
    'roc_ambang_0_3': ('float', 0.15, 0.45),
    'rolling_50': ('int', 25, 100),
    'bo_kali_0_6': ('float', 0.3, 0.9),
    'rolling_20': ('int', 10, 40),
}
TALA = ['c_kali_0_6', 'bo_kali_0_6', 'rolling_50', 'rolling_10', 'roc_ambang_0_3', 'rolling_20']

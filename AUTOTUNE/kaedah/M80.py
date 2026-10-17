# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M80.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_5': 5,
    'n_atas_ambang_5': 5,
    'rma_atr_kali_3': 3,
    'rolling_10': 10,
    'rolling_8': 8,
    'shift_63': 63,
    'rma_atr_14': 14,
    'shift_5': 5,
}
ID = 'M80'
NAMA = 'Radge Saluran Purata Bergerak (MAC)'
VARIAN = 'V2 V1 dengan henti tutup-3xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_5 = P['rolling_5']
    _p_n_atas_ambang_5 = P['n_atas_ambang_5']
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_8 = P['rolling_8']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_shift_5 = P['shift_5']
    for g in fr.values():
        ga = g.high.rolling(_p_rolling_10).mean()
        gb = g.low.rolling(_p_rolling_8).mean()
        atas = g.low > ga
        bawah = g.high < gb
        n_atas = atas.astype(int).rolling(_p_rolling_5).sum()
        masuk5 = (n_atas == _p_n_atas_ambang_5) & ~atas.shift(_p_shift_5, fill_value=False).astype(bool)
        keluar5 = bawah.astype(int).rolling(_p_rolling_5).sum() == _p_rolling_5
        run = atas.astype(int).groupby((~atas).cumsum()).cumsum()
        g['_ga'] = ga
        g['_gb'] = gb
        g['_run'] = run
        g['sig'] = masuk5
        g['stop'] = g.close - _p_rma_atr_kali_3 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = keluar5
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_5': ('int', 2, 10),
    'n_atas_ambang_5': ('int', 2, 8),
    'rma_atr_kali_3': ('float', 1.5, 4.5),
    'rolling_10': ('int', 5, 20),
    'rolling_8': ('int', 4, 16),
    'shift_63': ('int', 32, 126),
    'rma_atr_14': ('int', 7, 28),
    'shift_5': ('int', 2, 10),
}
TALA = ['rma_atr_kali_3', 'rolling_8', 'rma_atr_14', 'rolling_5', 'n_atas_ambang_5', 'rolling_10']

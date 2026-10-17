# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M107.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_200': 200,
    'rma_atr_kali_3': 3,
    'rolling_50': 50,
    'shift_63': 63,
    'rma_atr_14': 14,
}
ID = 'M107'
NAMA = 'Golden Cross SMA50/200'
VARIAN = 'V5 V1 + SPY>SMA200'
TMAX = None
WARM = 201
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _spy_ok(idx, index, *, P=PARAM):
    s = idx['SPY'].close
    ok = s > s.rolling(P['rolling_200']).mean()
    return ok.reindex(index, method='ffill').fillna(False).astype(bool)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_200 = P['rolling_200']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    for g in fr.values():
        s50 = g.close.rolling(_p_rolling_50).mean()
        s200 = g.close.rolling(_p_rolling_200).mean()
        emas = (s50 > s200) & (s50.shift() <= s200.shift())
        spy = _spy_ok(idx, g.index, P=P)
        g['_s50'] = s50
        g['_s200'] = s200
        g['_spy'] = spy
        g['sig'] = emas & spy
        g['stop'] = g.close - _p_rma_atr_kali_3 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = s50 < s200
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_200': ('int', 100, 400),
    'rma_atr_kali_3': ('float', 1.5, 4.5),
    'rolling_50': ('int', 25, 100),
    'shift_63': ('int', 32, 126),
    'rma_atr_14': ('int', 7, 28),
}
TALA = ['rma_atr_kali_3', 'rma_atr_14', 'rolling_200', 'rolling_50']

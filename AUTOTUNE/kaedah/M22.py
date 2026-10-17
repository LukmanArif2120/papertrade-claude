# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M22.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'ema_a1_10': 10,
    'ema_a1_20': 20,
    'g_ambang_0_1': 0.1,
    'vr_ambang_3': 3,
    'rolling_20': 20,
    'rolling_10': 10,
    'rolling_50': 50,
}
ID = 'M22'
NAMA = 'Qullamaggie Episodic Pivot'
VARIAN = 'V0 Sumber tulen (QQQ EMA, jurang>=10%, vol>=3x, henti low hari jurang, keluar<SMA10)'
TMAX = None
WARM = 70
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
ema = lambda s, k, *, P=PARAM: s.ewm(span=k, adjust=False).mean()

def _mkt(idx, index, *, P=PARAM):
    q = idx['QQQ'].close
    e10, e20 = (ema(q, P['ema_a1_10']), ema(q, P['ema_a1_20']))
    m = (e10 > e20) & (e10 > e10.shift()) & (e20 > e20.shift())
    return (m.reindex(index).fillna(False).astype(bool), (e10 > e20).reindex(index).ffill().fillna(False))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_g_ambang_0_1 = P['g_ambang_0_1']
    _p_vr_ambang_3 = P['vr_ambang_3']
    _p_rolling_20 = P['rolling_20']
    _p_rolling_10 = P['rolling_10']
    _p_rolling_50 = P['rolling_50']
    for g in fr.values():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        MK, _ = _mkt(idx, g.index, P=P)
        G = o / c.shift() - 1
        VR = v / v.rolling(_p_rolling_50).mean().shift(1)
        EP = (G >= _p_g_ambang_0_1) & (VR >= _p_vr_ambang_3)
        ADRp = (h / l).shift(1).rolling(_p_rolling_20).mean() - 1
        RISK = (c - l) / c
        sig = MK & EP & (c >= o) & (RISK <= ADRp)
        lk = (o.shift(-1) <= l).fillna(False)
        g['_ADRp'] = ADRp
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = l
        g['tgt'] = np.nan
        g['exitc'] = c < c.rolling(_p_rolling_10).mean()
        g['rank'] = VR
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M48.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rolling_3': 3,
    'rendah_ambang_2': 2,
    'pdm_kali_100': 100,
    'mdm_kali_100': 100,
    'pdi_kali_100': 100,
    'wilder_14': 14,
    'adx_ambang_30': 30,
    'high_tambah_0_125': 0.125,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M48'
NAMA = 'Cooper 1-2-3-4'
VARIAN = 'V3 V1 henti low hari 3 - 1xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _wilder(g, n=14, *, P=PARAM):
    h, l, c = (g.high, g.low, g.close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    up = h.diff()
    dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), g.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), g.index)
    a = 1 / n
    atr_ = tr.ewm(alpha=a, adjust=False).mean()
    pdi = P['pdm_kali_100'] * pdm.ewm(alpha=a, adjust=False).mean() / atr_
    mdi = P['mdm_kali_100'] * mdm.ewm(alpha=a, adjust=False).mean() / atr_
    dx = P['pdi_kali_100'] * (pdi - mdi).abs() / (pdi + mdi)
    return (dx.ewm(alpha=a, adjust=False).mean(), pdi, mdi, atr_)

def _undur(g, *, P=PARAM):
    """Bagi tiga hari berakhir hari k: setiap hari RENDAH atau DALAM, >=2 RENDAH."""
    rendah = g.low < g.low.shift()
    dalam = (g.high <= g.high.shift()) & (g.low >= g.low.shift())
    ok = (rendah | dalam).astype(int).rolling(P['rolling_3']).sum() == P['rolling_3']
    nr = rendah.astype(int).rolling(P['rolling_3']).sum() >= P['rendah_ambang_2']
    return ok & nr

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_wilder_14 = P['wilder_14']
    _p_adx_ambang_30 = P['adx_ambang_30']
    _p_high_tambah_0_125 = P['high_tambah_0_125']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        adx, pdi, mdi, a14 = _wilder(g, n=_p_wilder_14, P=P)
        s50 = g.close.rolling(_p_rolling_50).mean()
        kuat = (adx >= _p_adx_ambang_30) & (pdi > mdi)
        und = _undur(g, P=P)
        setup = kuat & und
        cetus = g.close > g.high.shift() + _p_high_tambah_0_125
        sig = setup.shift(1, fill_value=False) & cetus & (g.close > s50)
        stop = g.low.shift() - a14
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
        g['_setup'] = setup
        g['_s50'] = s50
        g['_adx'] = adx
        g['_a14'] = a14
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M88.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_16': 16,
    'i_tolak_15': 15,
    'd2_tolak_40': 40,
    'd2_tolak_5': 5,
    'l1_kali_1_1': 1.1,
    'bm_kali_0_92': 0.92,
    'shift_63': 63,
    'l1_kali_0_9': 0.9,
    'rolling_50': 50,
    'rolling_20': 20,
}
ID = 'M88'
NAMA = "O'Neil Shakeout +3"
VARIAN = 'V1 Dikunci (BELI 1.10xL1; vol>VOL50; henti max(L2;0.92x masuk); keluar tutup<low20)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _argmin_baru(a, *, P=PARAM):
    """indeks minimum; jika seri, yang paling baharu"""
    return len(a) - 1 - int(np.argmin(a[::-1]))

def _w(g, *, P=PARAM):
    _p_range_16 = P['range_16']
    _p_i_tolak_15 = P['i_tolak_15']
    _p_d2_tolak_40 = P['d2_tolak_40']
    _p_d2_tolak_5 = P['d2_tolak_5']
    h, l = (g.high.values, g.low.values)
    n = len(g)
    L1 = np.full(n, np.nan)
    L2 = np.full(n, np.nan)
    TG = np.full(n, np.nan)
    for i in range(_p_range_16, n):
        a = i - _p_i_tolak_15
        d2 = a + _argmin_baru(l[a:i], P=P)
        s, e = (d2 - _p_d2_tolak_40, d2 - _p_d2_tolak_5)
        if s < 0 or e < s:
            continue
        d1 = s + _argmin_baru(l[s:e + 1], P=P)
        L1[i] = l[d1]
        L2[i] = l[d2]
        TG[i] = h[d1 + 1:d2].max() if d2 - d1 > 1 else np.nan
    return (L1, L2, TG)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_l1_kali_1_1 = P['l1_kali_1_1']
    _p_bm_kali_0_92 = P['bm_kali_0_92']
    _p_shift_63 = P['shift_63']
    _p_l1_kali_0_9 = P['l1_kali_0_9']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        L1, L2, TG = _w(g, P=P)
        L1 = pd.Series(L1, g.index)
        L2 = pd.Series(L2, g.index)
        TG = pd.Series(TG, g.index)
        bentuk = (L2 < L1) & (L2 >= _p_l1_kali_0_9 * L1) & (TG >= _p_l1_kali_1_1 * L1)
        beli = _p_l1_kali_1_1 * L1
        naik = (g.close > beli) & (g.close.shift() <= beli)
        vol50 = g.volume.rolling(_p_rolling_50).mean().shift(1)
        g['_bentuk'] = bentuk
        g['_beli'] = beli
        g['_L1'] = L1
        g['_L2'] = L2
        g['_tg'] = TG
        g['_v50'] = vol50
        g['sig'] = bentuk & naik & (g.volume > vol50)
        bm = g.open.shift(-1).fillna(g.close)
        st = np.maximum(L2, _p_bm_kali_0_92 * bm)
        g['stop'] = st.where(bm > L2, _p_bm_kali_0_92 * bm)
        g['tgt'] = np.nan
        g['exitc'] = g.close < g.low.rolling(_p_rolling_20).min().shift(1)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

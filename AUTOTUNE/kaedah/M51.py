# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M51.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'dalam_max': 0.5,
    'i_ambang_475': 475,
    'i_tolak_25': 25,
    'r_tolak_320': 320,
    'lft_tolak_130': 130,
    'panjang_ambang_35': 35,
    'panjang_ambang_35_ambang_325': 325,
    'dc_ambang_0_12': 0.12,
    'naik_ambang_0_3': 0.3,
    'rp_ambang_0_12': 0.12,
    'i_tolak_4': 4,
    'r_tolak_29': 29,
    'kiri_kali_0_9': 0.9,
    'kiri_kali_1_05': 1.05,
    'kiri_bahagi_2': 2,
    'range_475': 475,
    'c_kali_0_92': 0.92,
    'rolling_50': 50,
    'bo_kali_0_92': 0.92,
    'shift_63': 63,
    'p_kali_1_05': 1.05,
    'v50_kali_1_4': 1.4,
}
ID = 'M51'
NAMA = "O'Neil Cawan & Pemegang"
VARIAN = 'V3 V1 kedalaman cawan 12-50%'
TMAX = None
WARM = 480
ADA_HENTI = True
SILANG = False
PERLU_BAR = 482
DALAM_MAX = 0.5

def _corak(g, i, *, P=PARAM):
    """Pulangkan dict geometri cawan & pemegang pada hari i (tanpa syarat PECAH), atau None."""
    h = g.high.values
    l = g.low.values
    if i < P['i_ambang_475']:
        return None
    w = h[i - P['i_tolak_25']:i - P['i_tolak_4']]
    r = i - P['i_tolak_25'] + (len(w) - 1 - np.argmax(w[::-1]))
    piv = h[r]
    if r + 1 <= i - 1 and h[r + 1:i].max() > piv:
        return None
    rp = l[r + 1:i].min()
    wl = h[r - P['r_tolak_320']:r - P['r_tolak_29']]
    lft = r - P['r_tolak_320'] + (len(wl) - 1 - np.argmax(wl[::-1]))
    kiri = h[lft]
    panjang = i - lft
    dasar = l[lft:r + 1].min()
    dc = 1 - dasar / kiri
    if lft - P['lft_tolak_130'] < 0:
        return None
    naik = kiri / l[lft - P['lft_tolak_130']:lft].min() - 1
    lompang = h[r - P['r_tolak_29']:r].max() <= piv
    cawan = P['panjang_ambang_35'] <= panjang <= P['panjang_ambang_35_ambang_325'] and P['dc_ambang_0_12'] <= dc <= P['dalam_max'] and (naik >= P['naik_ambang_0_3']) and (P['kiri_kali_0_9'] * kiri <= piv <= P['kiri_kali_1_05'] * kiri) and lompang
    pem = 1 - rp / piv <= P['rp_ambang_0_12'] and rp >= (kiri + dasar) / P['kiri_bahagi_2']
    return dict(cawan=cawan, pem=pem, piv=piv, rp=rp, kiri=kiri, dasar=dasar, dc=dc)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_range_475 = P['range_475']
    _p_c_kali_0_92 = P['c_kali_0_92']
    _p_rolling_50 = P['rolling_50']
    _p_bo_kali_0_92 = P['bo_kali_0_92']
    _p_shift_63 = P['shift_63']
    _p_p_kali_1_05 = P['p_kali_1_05']
    _p_v50_kali_1_4 = P['v50_kali_1_4']
    for g in fr.values():
        c = g.close
        n = len(g)
        s50 = c.rolling(_p_rolling_50).mean()
        vol50 = g.volume.rolling(_p_rolling_50).mean().shift(1)
        cv = c.values
        vv = g.volume.values
        v50 = vol50.values
        s = s50.values
        sig = np.zeros(n, bool)
        piv = np.full(n, np.nan)
        for i in range(_p_range_475, n):
            if not cv[i] > s[i] or not vv[i] >= _p_v50_kali_1_4 * v50[i]:
                continue
            k = _corak(g, i, P=P)
            if k is None:
                continue
            p = k['piv']
            pecah = cv[i] > p and cv[i - 1] <= p and (cv[i] <= _p_p_kali_1_05 * p)
            if k['cawan'] and k['pem'] and pecah:
                sig[i] = True
                piv[i] = p
        g['sig'] = sig
        bo = g.open.shift(-1)
        g['stop'] = (_p_bo_kali_0_92 * bo).fillna(_p_c_kali_0_92 * c)
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_s50'] = s50
        g['_vol50'] = vol50
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'dalam_max': ('float', 0.25, 0.75),
    'panjang_ambang_35': ('int', 18, 52),
    'panjang_ambang_35_ambang_325': ('int', 162, 488),
    'dc_ambang_0_12': ('float', 0.06, 0.18),
    'naik_ambang_0_3': ('float', 0.15, 0.45),
    'rp_ambang_0_12': ('float', 0.06, 0.18),
    'kiri_kali_0_9': ('float', 0.45, 0.99),
    'kiri_kali_1_05': ('float', 0.525, 1.575),
    'c_kali_0_92': ('float', 0.46, 0.99),
    'rolling_50': ('int', 25, 100),
    'bo_kali_0_92': ('float', 0.46, 0.99),
    'shift_63': ('int', 32, 126),
    'v50_kali_1_4': ('float', 0.7, 2.1),
}
TALA = ['rolling_50', 'c_kali_0_92', 'bo_kali_0_92', 'dalam_max', 'panjang_ambang_35', 'panjang_ambang_35_ambang_325']

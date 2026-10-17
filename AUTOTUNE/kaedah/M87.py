# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M87.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'p_ambang_3': 3,
    'p3_tambah_0_1': 0.1,
    'i_ambang_45': 45,
    'p_i_ambang_45_ambang_80': 80,
    'p_tolak_3': 3,
    'p_tolak_2': 2,
    'd_ambang_0_1': 0.1,
    'p_d_ambang_0_1_ambang_0_2': 0.2,
    'hr_kali_0_9': 0.9,
    'lr_kali_1_1': 1.1,
    'open_kali_0_92': 0.92,
    'rolling_50': 50,
    'beli_kali_1_05': 1.05,
    'shift_63': 63,
}
ID = 'M87'
NAMA = 'IBD Tapak Menaik'
VARIAN = 'V4 V1 tanpa DAHULU'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _zigzag(h, l, *, P=PARAM):
    """Zigzag 10% tanpa pandang ke hadapan. Pulang senarai (bar_sah, tarikh_puncak_idx, nilai) puncak disahkan."""
    _p_hr_kali_0_9 = P['hr_kali_0_9']
    _p_lr_kali_1_1 = P['lr_kali_1_1']
    n = len(h)
    puncak = []
    naik = True
    HR = h[0]
    tHR = 0
    LR = np.nan
    for k in range(n):
        if naik:
            if h[k] > HR:
                HR = h[k]
                tHR = k
            if l[k] <= _p_hr_kali_0_9 * HR:
                puncak.append((k, tHR, HR))
                naik = False
                LR = l[k]
        else:
            if l[k] < LR:
                LR = l[k]
            if h[k] >= _p_lr_kali_1_1 * LR:
                naik = True
                HR = h[k]
                tHR = k
    return puncak

def _kira(g, *, P=PARAM):
    _p_p_ambang_3 = P['p_ambang_3']
    _p_p3_tambah_0_1 = P['p3_tambah_0_1']
    _p_i_ambang_45 = P['i_ambang_45']
    _p_p_i_ambang_45_ambang_80 = P['p_i_ambang_45_ambang_80']
    _p_p_tolak_3 = P['p_tolak_3']
    _p_p_tolak_2 = P['p_tolak_2']
    _p_d_ambang_0_1 = P['d_ambang_0_1']
    _p_p_d_ambang_0_1_ambang_0_2 = P['p_d_ambang_0_1_ambang_0_2']
    h, l, c = (g.high.values, g.low.values, g.close.values)
    n = len(g)
    pk = _zigzag(h, l, P=P)
    out = {k: np.full(n, np.nan) for k in ['beli', 'P1', 'P2', 'P3', 'T1', 'T2', 'T3', 'tp1']}
    ok = np.zeros(n, bool)
    p = 0
    for i in range(n):
        while p < len(pk) and pk[p][0] <= i:
            p += 1
        if p < _p_p_ambang_3:
            continue
        (_, t1, P1), (_, t2, P2), (_, t3, P3) = (pk[p - _p_p_tolak_3], pk[p - _p_p_tolak_2], pk[p - 1])
        T1 = l[t1:t2 + 1].min()
        T2 = l[t2:t3 + 1].min()
        T3 = l[t3:i + 1].min()
        out['beli'][i] = P3 + _p_p3_tambah_0_1
        for k, v in [('P1', P1), ('P2', P2), ('P3', P3), ('T1', T1), ('T2', T2), ('T3', T3), ('tp1', t1)]:
            out[k][i] = v
        D = [1 - T1 / P1, 1 - T2 / P2, 1 - T3 / P3]
        tangga = P1 < P2 < P3 and T1 < T2 < T3
        dalam = all((_p_d_ambang_0_1 <= d <= _p_p_d_ambang_0_1_ambang_0_2 for d in D))
        tempoh = _p_i_ambang_45 <= i - t1 <= _p_p_i_ambang_45_ambang_80
        ok[i] = tangga and dalam and tempoh
    return (ok, out)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_open_kali_0_92 = P['open_kali_0_92']
    _p_rolling_50 = P['rolling_50']
    _p_beli_kali_1_05 = P['beli_kali_1_05']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        ok, o = _kira(g, P=P)
        beli = pd.Series(o['beli'], g.index)
        s50 = g.close.rolling(_p_rolling_50).mean()
        pecah = (g.close > beli) & (g.close.shift() <= beli) & (g.close <= _p_beli_kali_1_05 * beli)
        g['_ok'] = ok
        g['_beli'] = beli
        g['_s50'] = s50
        g['_tp1'] = o['tp1']
        g['_P3'] = o['P3']
        g['_T3'] = o['T3']
        g['sig'] = pecah & pd.Series(ok, g.index) & (g.close > s50)
        g['stop'] = _p_open_kali_0_92 * g.open.shift(-1).fillna(g.close)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

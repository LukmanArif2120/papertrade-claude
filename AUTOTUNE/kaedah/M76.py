# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M76.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as _swv
PARAM = {
    'n': 40,
    'n_tolak_2': 2,
    'rolling_3': 3,
    'i_tolak_8': 8,
    'i_tolak_2': 2,
    'rp_kali_1_05': 1.05,
    'rolling_20': 20,
    'rolling_200': 200,
    'shift_63': 63,
    'clv_ambang_0_6': 0.6,
}
ID = 'M76'
NAMA = 'Undercut & Rally pada Low Penting'
VARIAN = 'V1 Dikunci (UR + CLV>0.60 + tutup>SMA200)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210
N = 40

def _ur(g, *, P=PARAM):
    _p_n = P['n']
    _p_i_tolak_8 = P['i_tolak_8']
    _p_i_tolak_2 = P['i_tolak_2']
    _p_rp_kali_1_05 = P['rp_kali_1_05']
    lo = g.low.values.astype(float)
    hi = g.high.values.astype(float)
    c = g.close.values.astype(float)
    n = len(g)
    RP = np.full(n, np.nan)
    sah = np.zeros(n, bool)
    W = P['n'] - P['n_tolak_2']
    if n >= P['n'] + 1:
        wl = _swv(lo, W)
        for i in range(_p_n, n):
            w = wl[i - _p_n]
            rp = w.min()
            RP[i] = rp
            kk = np.where(w == rp)[0][-1]
            k = i - _p_n + kk
            if k <= i - _p_i_tolak_8:
                seg = hi[k + 1:i - _p_i_tolak_2]
                if len(seg) and seg.max() > _p_rp_kali_1_05 * rp:
                    sah[i] = True
    RP = pd.Series(RP, g.index)
    LT = g.low.rolling(P['rolling_3']).min()
    tembus = LT < RP
    rampas = (g.close > RP) & ((g.close.shift() <= RP) | (g.low < RP))
    ur = pd.Series(sah, g.index) & tembus & rampas
    return (ur, RP, LT)

def _exitc_berjaga(g, warm, *, P=PARAM):
    """Replika urutan dagangan enjin (tmax None) untuk mengisi exitc = BERJAGA & tutup<SMA20."""
    o, l, c = (g.open.values, g.low.values, g.close.values)
    sig = g.sig.fillna(False).astype(bool).values
    st = g.stop.astype(float).values
    atas = (g.close > g._s20).values
    bawah = (g.close < g._s20).values
    n = len(g)
    ex = np.zeros(n, bool)
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        jaga = bool(atas[i])
        j = i + 1
        keluar = n - 1
        while j < n:
            if j > i + 1 and o[j] <= sp:
                keluar = j
                break
            if l[j] <= sp:
                keluar = j
                break
            if jaga and bawah[j] and (j + 1 < n):
                ex[j] = True
                keluar = j + 1
                break
            if atas[j]:
                jaga = True
            j += 1
        i = keluar + 1
    return ex

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_20 = P['rolling_20']
    _p_rolling_200 = P['rolling_200']
    _p_shift_63 = P['shift_63']
    _p_clv_ambang_0_6 = P['clv_ambang_0_6']
    for g in fr.values():
        c = g.close
        ur, RP, LT = _ur(g, P=P)
        rng = g.high - g.low
        clv = ((c - g.low) / rng).where(rng > 0, 0.0)
        s20 = c.rolling(_p_rolling_20).mean()
        s200 = c.rolling(_p_rolling_200).mean()
        stop = LT
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_RP'] = RP
        g['_LT'] = LT
        g['_clv'] = clv
        g['_s20'] = s20
        g['_s200'] = s200
        g['_ur'] = ur
        g['sig'] = ur & (clv > _p_clv_ambang_0_6) & (c > s200) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['exitc'] = _exitc_berjaga(g, WARM, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'n': ('int', 20, 80),
    'rolling_3': ('int', 2, 6),
    'rp_kali_1_05': ('float', 0.525, 1.575),
    'rolling_20': ('int', 10, 40),
    'rolling_200': ('int', 100, 400),
    'shift_63': ('int', 32, 126),
    'clv_ambang_0_6': ('float', 0.3, 0.9),
}
TALA = ['rolling_3', 'n', 'rp_kali_1_05', 'rolling_200', 'clv_ambang_0_6']

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M34.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'h_bahagi_2': 2,
    'dm_bahagi_2': 2,
    'linreg_end_20': 20,
    'rolling_20': 20,
    'sd_kali_2': 2,
    'a20_kali_1_5': 1.5,
    'rolling_50': 50,
    'shift_5': 5,
    'bahagi_20': 20,
    'rolling_10': 10,
    'shift_63': 63,
}
ID = 'M34'
NAMA = 'Carter TTM Squeeze'
VARIAN = 'V2 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80
_X = np.arange(20, dtype=float)
_XM = _X.mean()
_SXX = ((_X - _XM) ** 2).sum()

def _linreg_end(s, n=20, *, P=PARAM):
    y = s.values.astype(float)
    out = np.full(len(y), np.nan)
    if len(y) >= n:
        w = np.lib.stride_tricks.sliding_window_view(y, n)
        ym = w.mean(axis=1)
        b = ((w - ym[:, None]) * (_X - _XM)).sum(axis=1) / _SXX
        out[n - 1:] = ym + b * (n - 1 - _XM)
    return pd.Series(out, s.index)

def _komponen(g, *, P=PARAM):
    h, l, c = (g.high, g.low, g.close)
    s20 = c.rolling(P['rolling_20']).mean()
    sd = c.rolling(P['rolling_20']).std(ddof=0)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a20 = tr.ewm(alpha=1 / P['bahagi_20'], adjust=False).mean()
    bba, bbb = (s20 + P['sd_kali_2'] * sd, s20 - P['sd_kali_2'] * sd)
    kca, kcb = (s20 + P['a20_kali_1_5'] * a20, s20 - P['a20_kali_1_5'] * a20)
    himpit = (bba < kca) & (bbb > kcb)
    dm = (h.rolling(P['rolling_20']).max() + l.rolling(P['rolling_20']).min()) / P['h_bahagi_2']
    d = c - (dm + s20) / P['dm_bahagi_2']
    mom = _linreg_end(d, n=P['linreg_end_20'], P=P)
    s50 = c.rolling(P['rolling_50']).mean()
    aliran = (c > s50) & (s50 > s50.shift(P['shift_5']))
    return (himpit, mom, s50, aliran)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_10 = P['rolling_10']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        himpit, mom, s50, aliran = _komponen(g, P=P)
        lepas = himpit.shift(1, fill_value=False) & ~himpit
        sig = lepas & (mom > 0) & (mom > mom.shift()) & aliran
        g['_himpit'] = himpit
        g['_mom'] = mom
        g['_s50'] = s50
        g['_aliran'] = aliran
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = g.low.rolling(_p_rolling_10).min()
        g['tgt'] = np.nan
        g['exitc'] = (g.close < s50).fillna(False)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _esok(g, X):
    """Nilai indikator TTM esok bagi tatasusunan tutup esok X.
    Andaian saya: high = low = tutup esok = X untuk tetingkap high/low 20 hari; tetapi julat sebenar esok diandaikan
    = max(ATR20 hari ini, |X - tutup hari ini|) supaya ATR tidak mengecut secara buatan (andaian konservatif)."""
    X = np.asarray(X, float)
    h, l, c = (g.high.values.astype(float), g.low.values.astype(float), g.close.values.astype(float))
    c19 = c[-19:]
    s20 = (c19.sum() + X) / 20
    sd = np.sqrt(np.maximum(((c19 ** 2).sum() + X ** 2) / 20 - s20 ** 2, 0))
    tr = pd.concat([g.high - g.low, (g.high - g.close.shift()).abs(), (g.low - g.close.shift()).abs()], axis=1).max(axis=1)
    a20_hi = float(tr.ewm(alpha=1 / 20, adjust=False).mean().iloc[-1])
    a20 = a20_hi * 19 / 20 + np.maximum(a20_hi, np.abs(X - c[-1])) / 20
    himpit = (s20 + 2 * sd < s20 + 1.5 * a20) & (s20 - 2 * sd > s20 - 1.5 * a20)
    hh = np.maximum(h[-19:].max(), X)
    ll = np.minimum(l[-19:].min(), X)
    d_new = X - ((hh + ll) / 2 + s20) / 2
    s20s = g.close.rolling(20).mean()
    dm = (g.high.rolling(20).max() + g.low.rolling(20).min()) / 2
    d_old = (g.close - (dm + s20s) / 2).values[-19:]
    W = np.concatenate([np.broadcast_to(d_old, (len(X), 19)), d_new[:, None]], axis=1)
    ym = W.mean(axis=1)
    b = ((W - ym[:, None]) * (_X - _XM)).sum(axis=1) / _SXX
    mom = ym + b * (19 - _XM)
    s50 = (c[-49:].sum() + X) / 50
    s50_5 = g.close.rolling(50).mean().values[-5]
    aliran = (X > s50) & (s50 > s50_5)
    return (himpit, mom, aliran)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'sd_kali_2': ('float', 1.0, 3.0),
    'a20_kali_1_5': ('float', 0.75, 2.25),
    'rolling_50': ('int', 25, 100),
    'shift_5': ('int', 2, 10),
    'bahagi_20': ('int', 10, 40),
    'rolling_10': ('int', 5, 20),
    'shift_63': ('int', 32, 126),
}
TALA = ['rolling_10', 'rolling_50', 'sd_kali_2', 'a20_kali_1_5', 'bahagi_20', 'shift_5']

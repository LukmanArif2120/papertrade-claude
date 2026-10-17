# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M91.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'pdm_kali_100': 100,
    'mdm_kali_100': 100,
    'pdi_kali_100': 100,
    'where_a1_50_0': 50.0,
    'rolling_3': 3,
    'close_kali_100': 100,
    'sto_14': 14,
    'sto_70': 70,
    's14_ambang_50': 50,
    'adx_14': 14,
    's14_ambang_80': 80,
    'rolling_10': 10,
    'shift_63': 63,
    'adx_ambang_20': 20,
    'rolling_250': 250,
    'rolling_20': 20,
    's70_ambang_50': 50,
}
ID = 'M91'
NAMA = 'Stochastic Pop (Bernstein/Steckler)'
VARIAN = 'V2 V1 + tutup>HH20 (pecah keluar)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280

def _sto(g, n, *, P=PARAM):
    ll = g.low.rolling(n).min()
    hh = g.high.rolling(n).max()
    d = hh - ll
    k = (P['close_kali_100'] * (g.close - ll) / d.replace(0, np.nan)).where(d != 0, P['where_a1_50_0'])
    k[ll.isna()] = np.nan
    return k.rolling(P['rolling_3']).mean()

def _adx(g, n=14, *, P=PARAM):
    h, l, c = (g.high, g.low, g.close)
    up = h.diff()
    dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), g.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), g.index)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a = 1 / n
    atr_ = tr.ewm(alpha=a, adjust=False).mean()
    pdi = P['pdm_kali_100'] * pdm.ewm(alpha=a, adjust=False).mean() / atr_
    mdi = P['mdm_kali_100'] * mdm.ewm(alpha=a, adjust=False).mean() / atr_
    dx = P['pdi_kali_100'] * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=a, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_sto_14 = P['sto_14']
    _p_sto_70 = P['sto_70']
    _p_s14_ambang_50 = P['s14_ambang_50']
    _p_adx_14 = P['adx_14']
    _p_s14_ambang_80 = P['s14_ambang_80']
    _p_rolling_10 = P['rolling_10']
    _p_shift_63 = P['shift_63']
    _p_adx_ambang_20 = P['adx_ambang_20']
    _p_rolling_250 = P['rolling_250']
    _p_rolling_20 = P['rolling_20']
    _p_s70_ambang_50 = P['s70_ambang_50']
    for g in fr.values():
        s14 = _sto(g, _p_sto_14, P=P)
        s70 = _sto(g, _p_sto_70, P=P)
        adx = _adx(g, n=_p_adx_14, P=P)
        v250 = g.volume.rolling(_p_rolling_250).mean().shift(1)
        hh20 = g.high.rolling(_p_rolling_20).max().shift(1)
        pop = (s14 > _p_s14_ambang_80) & (s14.shift() <= _p_s14_ambang_80)
        g['_s14'] = s14
        g['_s70'] = s70
        g['_adx'] = adx
        g['_v250'] = v250
        g['_hh20'] = hh20
        g['sig'] = pop & (s70 > _p_s70_ambang_50) & (adx < _p_adx_ambang_20) & (g.volume > v250) & (g.close > hh20)
        g['stop'] = g.low.rolling(_p_rolling_10).min()
        g['tgt'] = np.nan
        g['exitc'] = s14 < _p_s14_ambang_50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _cari_paras(g, idx, ekor, bawah=-0.05, atas=0.02, vol=None):
    """Tutup esok minimum (dalam julat tutup*(1+bawah)..tutup*(1+atas)) yang menjadikan sig bar esok benar,
    dengan menjalankan sedia() asal pada ekor data + satu bar esok rekaan.
    Andaian saya: bar esok open=high=low=close=C; volum esok = `vol` jika diberi, jika tidak purata volum 10 hari."""
    c0 = float(g.close.iloc[-1])
    asas = g[['open', 'high', 'low', 'close', 'volume', 'turnover']].iloc[-ekor:].astype(float)
    v = float(asas.volume.iloc[-10:].mean()) if vol is None else float(vol)
    esok = asas.index[-1] + pd.offsets.BDay(1)

    def cuba(C):
        b = asas.copy()
        b.loc[esok] = [C, C, C, C, v, C * v]
        d = {'x': b}
        sedia(d, {})
        return bool(d['x'].sig.iloc[-1])
    grid = np.round(np.arange(bawah, atas + 1e-09, 0.0025), 6)
    sebelum = None
    for p in grid:
        if cuba(c0 * (1 + p)):
            if sebelum is None:
                return c0 * (1 + p)
            lo, hi = (c0 * (1 + sebelum), c0 * (1 + p))
            for _ in range(18):
                m = (lo + hi) / 2
                if cuba(m):
                    hi = m
                else:
                    lo = m
            return hi
        sebelum = p
    return None

def _jarak(paras, tutup):
    return (paras - tutup) / tutup * 100
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

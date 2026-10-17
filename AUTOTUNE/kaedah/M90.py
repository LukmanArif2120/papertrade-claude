# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M90.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'c_kali_100': 100,
    'roc_kali_4': 4,
    'roc_kali_3': 3,
    'roc_kali_2': 2,
    'rolling_9': 9,
    'rolling_15': 15,
    'rolling_10': 10,
    'roc_30': 30,
    'roc_10': 10,
    'roc_20': 20,
    'roc_15': 15,
    'rma_atr_kali_2': 2,
    'rolling_50': 50,
    'shift_63': 63,
    'rma_atr_14': 14,
}
ID = 'M90'
NAMA = 'Pring KST'
VARIAN = 'V3 V1 + tutup>SMA50, keluar tutup<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _kst(c, *, P=PARAM):
    _p_c_kali_100 = P['c_kali_100']
    roc = lambda n: _p_c_kali_100 * (c / c.shift(n) - 1)
    kst = roc(P['roc_10']).rolling(P['rolling_10']).mean() + P['roc_kali_2'] * roc(P['roc_15']).rolling(P['rolling_10']).mean() + P['roc_kali_3'] * roc(P['roc_20']).rolling(P['rolling_10']).mean() + P['roc_kali_4'] * roc(P['roc_30']).rolling(P['rolling_15']).mean()
    return (kst, kst.rolling(P['rolling_9']).mean())

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    for g in fr.values():
        kst, isy = _kst(g.close, P=P)
        s50 = g.close.rolling(_p_rolling_50).mean()
        silang = (kst > isy) & (kst.shift() <= isy.shift())
        g['_kst'] = kst
        g['_isy'] = isy
        g['_s50'] = s50
        g['sig'] = silang & (kst > 0) & (g.close > s50)
        g['stop'] = g.close - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
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
JULAT = {
    'roc_kali_4': ('float', 2.0, 6.0),
    'roc_kali_3': ('float', 1.5, 4.5),
    'roc_kali_2': ('float', 1.0, 3.0),
    'rolling_9': ('int', 4, 18),
    'rolling_15': ('int', 8, 30),
    'rolling_10': ('int', 5, 20),
    'roc_30': ('int', 15, 60),
    'roc_10': ('int', 5, 20),
    'roc_20': ('int', 10, 40),
    'roc_15': ('int', 8, 30),
    'rma_atr_kali_2': ('float', 1.0, 3.0),
    'rolling_50': ('int', 25, 100),
    'shift_63': ('int', 32, 126),
    'rma_atr_14': ('int', 7, 28),
}
TALA = ['rma_atr_kali_2', 'rma_atr_14', 'rolling_50', 'rolling_10', 'roc_kali_4', 'roc_kali_3']

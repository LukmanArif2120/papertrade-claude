# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M92.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
PARAM = {
    'high_bahagi_3': 3,
    'sp_kali_0_015': 0.015,
    'cci_50': 50,
    'rma_atr_kali_2': 2,
    'cci_ambang_100': 100,
    'shift_63': 63,
    'rma_atr_14': 14,
}
ID = 'M92'
NAMA = 'CCI-50'
VARIAN = 'V2 V1 isyarat silang atas sifar (NAIK0)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _cci(g, n=50, *, P=PARAM):
    tp = ((g.high + g.low + g.close) / P['high_bahagi_3']).values.astype(float)
    out = np.full(len(tp), np.nan)
    if len(tp) >= n:
        w = sliding_window_view(tp, n)
        ma = w.mean(axis=1)
        sp = np.abs(w - ma[:, None]).mean(axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            c = np.where(sp == 0, 0.0, (tp[n - 1:] - ma) / (P['sp_kali_0_015'] * sp))
        out[n - 1:] = c
    return pd.Series(out, g.index)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_cci_50 = P['cci_50']
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_cci_ambang_100 = P['cci_ambang_100']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    for g in fr.values():
        cci = _cci(g, n=_p_cci_50, P=P)
        g['_cci'] = cci
        g['sig'] = (cci > 0) & (cci.shift() <= 0)
        g['stop'] = g.close - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = (cci < _p_cci_ambang_100) & (cci.shift() >= _p_cci_ambang_100)
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

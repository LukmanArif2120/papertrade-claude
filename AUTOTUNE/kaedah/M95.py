# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M95.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
PARAM = {
    'clip_a1_30': 30,
    'hsh_252': 252,
    'hshp_bahagi_252': 252,
    'rma_atr_kali_2': 2,
    'roc_kali_1em05': 1e-05,
    'rolling_252': 252,
    'rolling_50': 50,
    'hshp_ambang_21': 21,
    'pth_ambang_0_85': 0.85,
    'rma_atr_14': 14,
    'rolling_20': 20,
    'shift_63': 63,
}
ID = 'M95'
NAMA = 'Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur)'
VARIAN = 'V1 Dikunci: PECAH20+PTH>=0.85+HSHP<=21+tutup>SMA50'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _hsh(h, n=252, *, P=PARAM):
    v = h.values.astype(float)
    out = np.full(len(v), np.nan)
    if len(v) >= n:
        w = sliding_window_view(v, n)[:, ::-1]
        out[n - 1:] = w.argmax(axis=1)
    return pd.Series(out, h.index)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_clip_a1_30 = P['clip_a1_30']
    _p_hsh_252 = P['hsh_252']
    _p_hshp_bahagi_252 = P['hshp_bahagi_252']
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_roc_kali_1em05 = P['roc_kali_1em05']
    _p_rolling_252 = P['rolling_252']
    _p_rolling_50 = P['rolling_50']
    _p_hshp_ambang_21 = P['hshp_ambang_21']
    _p_pth_ambang_0_85 = P['pth_ambang_0_85']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_rolling_20 = P['rolling_20']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        h252 = g.high.rolling(_p_rolling_252).max()
        hsh = _hsh(g.high, n=_p_hsh_252, P=P)
        hshp = hsh.shift(1)
        rrp = 1 - hshp / _p_hshp_bahagi_252
        pth = g.close / h252
        s50 = g.close.rolling(_p_rolling_50).mean()
        hh20 = g.high.rolling(_p_rolling_20).max().shift(1)
        g['_pth'] = pth
        g['_hshp'] = hshp
        g['_hh20'] = hh20
        g['_s50'] = s50
        g['_hsh'] = hsh
        g['sig'] = (g.close > hh20) & (pth >= _p_pth_ambang_0_85) & (hshp <= _p_hshp_ambang_21) & (g.close > s50)
        g['stop'] = g.close - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        roc = (g.close / g.close.shift(_p_shift_63) - 1).clip(-1, _p_clip_a1_30)
        g['rank'] = rrp + _p_roc_kali_1em05 * roc

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

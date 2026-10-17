# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M73.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rma_kali_100': 100,
    'pdi_kali_100': 100,
    'adx_5': 5,
    'adx_ambang_40': 40,
    'shift_63': 63,
    'rolling_5': 5,
}
ID = 'M73'
NAMA = 'ADX(5) > 40 + Julat Terkecil 6 Hari'
VARIAN = 'V0 Sumber tulen (ADX5>40 + NR6; tiada henti; keluar tutup>high semalam)'
TMAX = None
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 60

def _rma(x, n, *, P=PARAM):
    """Wilder RMA disemai purata mudah n nilai sah pertama (seperti kad)."""
    v = x.values.astype(float)
    out = np.full(len(v), np.nan)
    ok = np.where(~np.isnan(v))[0]
    if len(ok) < n:
        return pd.Series(out, x.index)
    s = ok[0]
    e = s + n - 1
    if np.isnan(v[s:e + 1]).any():
        return pd.Series(out, x.index)
    out[e] = v[s:e + 1].mean()
    for k in range(e + 1, len(v)):
        out[k] = out[k - 1] + (v[k] - out[k - 1]) / n
    return pd.Series(out, x.index)

def _adx(g, n=5, *, P=PARAM):
    c = g.close
    pc = c.shift()
    tr = pd.concat([g.high - g.low, (g.high - pc).abs(), (g.low - pc).abs()], axis=1).max(axis=1)
    tr[pc.isna()] = np.nan
    nd = g.high - g.high.shift()
    td = g.low.shift() - g.low
    pdm = pd.Series(np.where((nd > td) & (nd > 0), nd, 0.0), g.index)
    pdm[nd.isna()] = np.nan
    mdm = pd.Series(np.where((td > nd) & (td > 0), td, 0.0), g.index)
    mdm[td.isna()] = np.nan
    rtr = _rma(tr, n, P=P)
    pdi = P['rma_kali_100'] * _rma(pdm, n, P=P) / rtr
    mdi = P['rma_kali_100'] * _rma(mdm, n, P=P) / rtr
    den = pdi + mdi
    dx = (P['pdi_kali_100'] * (pdi - mdi).abs() / den).where(den != 0, 0.0).where(den.notna())
    return (_rma(dx, n, P=P), pdi, mdi)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_adx_5 = P['adx_5']
    _p_adx_ambang_40 = P['adx_ambang_40']
    _p_shift_63 = P['shift_63']
    _p_rolling_5 = P['rolling_5']
    for g in fr.values():
        adx, pdi, mdi = _adx(g, _p_adx_5, P=P)
        jul = g.high - g.low
        nr6 = jul < jul.shift(1).rolling(_p_rolling_5).min()
        g['_adx5'] = adx
        g['_nr6'] = nr6
        g['_pdi'] = pdi
        g['_mdi'] = mdi
        g['sig'] = (adx > _p_adx_ambang_40) & nr6
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = g.close > g.high.shift()
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'adx_5': ('int', 2, 10),
    'adx_ambang_40': ('int', 20, 60),
    'shift_63': ('int', 32, 126),
    'rolling_5': ('int', 2, 10),
}
TALA = ['adx_5', 'adx_ambang_40', 'rolling_5']

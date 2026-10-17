# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M106.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'wp_kali_100': 100,
    'wn_kali_100': 100,
    'np_kali_100': 100,
    'adx_bahagi_14': 14,
    'adx_kali_13': 13,
    'dmi_14': 14,
    'a14_kali_2': 2,
    'adx_ambang_25': 25,
    'shift_63': 63,
}
ID = 'M106'
NAMA = 'DMI Wilder'
VARIAN = 'V5 V1 dengan henti tutup-2xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _w14(x, n=14, start=1, *, P=PARAM):
    out = np.full(len(x), np.nan)
    if len(x) < start + n:
        return out
    out[start + n - 1] = x[start:start + n].sum()
    for i in range(start + n, len(x)):
        out[i] = out[i - 1] - out[i - 1] / n + x[i]
    return out

def _dmi(g, n=14, *, P=PARAM):
    _p_adx_bahagi_14 = P['adx_bahagi_14']
    _p_adx_kali_13 = P['adx_kali_13']
    h, l, c = (g.high.values, g.low.values, g.close.values)
    tr = pd.concat([g.high - g.low, (g.high - g.close.shift()).abs(), (g.low - g.close.shift()).abs()], axis=1).max(axis=1).values
    up = np.r_[np.nan, h[1:] - h[:-1]]
    dn = np.r_[np.nan, l[:-1] - l[1:]]
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    wtr, wp, wn = (_w14(tr, n, P=P), _w14(pdm, n, P=P), _w14(ndm, n, P=P))
    with np.errstate(invalid='ignore', divide='ignore'):
        pdi = P['wp_kali_100'] * wp / wtr
        ndi = P['wn_kali_100'] * wn / wtr
        dx = P['np_kali_100'] * np.abs(pdi - ndi) / (pdi + ndi)
    adx = np.full(len(c), np.nan)
    f = n
    if len(c) >= f + n:
        adx[f + n - 1] = np.nanmean(dx[f:f + n])
        for i in range(f + n, len(c)):
            adx[i] = (_p_adx_kali_13 * adx[i - 1] + dx[i]) / _p_adx_bahagi_14
    atr14 = wtr / n
    return (pd.Series(pdi, g.index), pd.Series(ndi, g.index), pd.Series(adx, g.index), pd.Series(atr14, g.index))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_dmi_14 = P['dmi_14']
    _p_a14_kali_2 = P['a14_kali_2']
    _p_adx_ambang_25 = P['adx_ambang_25']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        pdi, ndi, adx, a14 = _dmi(g, n=_p_dmi_14, P=P)
        silang = (pdi > ndi) & (pdi.shift() <= ndi.shift())
        stop = g.close - _p_a14_kali_2 * a14
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_pdi'] = pdi
        g['_ndi'] = ndi
        g['_adx'] = adx
        g['sig'] = silang & (adx > _p_adx_ambang_25) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ndi > pdi
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}

def _di_esok(wtr, wp, wn, adx, h0, l0, c0, x, n=14):
    up = x - h0
    dn = l0 - x
    pdm = up if up > dn and up > 0 else 0.0
    ndm = dn if dn > up and dn > 0 else 0.0
    tr = max(0.0, abs(x - c0))
    wtr1 = wtr - wtr / n + tr
    wp1 = wp - wp / n + pdm
    wn1 = wn - wn / n + ndm
    pdi = 100 * wp1 / wtr1
    ndi = 100 * wn1 / wtr1
    dx = 100 * abs(pdi - ndi) / (pdi + ndi) if pdi + ndi > 0 else 0.0
    return (pdi, ndi, (13 * adx + dx) / 14)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'adx_kali_13': ('float', 6.5, 19.5),
    'dmi_14': ('int', 7, 28),
    'a14_kali_2': ('float', 1.0, 3.0),
    'adx_ambang_25': ('int', 12, 38),
    'shift_63': ('int', 32, 126),
}
TALA = ['dmi_14', 'a14_kali_2', 'adx_kali_13', 'adx_ambang_25']

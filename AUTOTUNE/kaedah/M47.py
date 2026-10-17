# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M47.py
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
    'adx_ambang_30': 30,
    'adx_14': 14,
    'shift_63': 63,
    'ewm_span_20': 20,
    'rolling_20': 20,
}
ID = 'M47'
NAMA = 'Holy Grail Raschke'
VARIAN = 'V3 V1 tanpa syarat ADX naik'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _adx(g, n=14, *, P=PARAM):
    h, l, c = (g.high, g.low, g.close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    up = h.diff()
    dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), g.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), g.index)
    a = 1 / n
    atr_ = tr.ewm(alpha=a, adjust=False).mean()
    pdi = P['pdm_kali_100'] * pdm.ewm(alpha=a, adjust=False).mean() / atr_
    mdi = P['mdm_kali_100'] * mdm.ewm(alpha=a, adjust=False).mean() / atr_
    dx = P['pdi_kali_100'] * (pdi - mdi).abs() / (pdi + mdi)
    return (dx.ewm(alpha=a, adjust=False).mean(), pdi, mdi)

def _tgt_tetap(g, sig, stop, tgt_isyarat, warm, *, P=PARAM):
    """Cerminkan gelung trades() enjin supaya lajur tgt kekal pada nilai hari isyarat
    sepanjang dagangan (laporan M47: sasaran dikunci pada hari isyarat). Enjin tidak diubah."""
    o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
    n = len(g)
    tg = np.full(n, np.nan)
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        T = tgt_isyarat[i]
        sp = stop[i] if not np.isnan(stop[i]) else -np.inf
        j = i + 1
        while j < n:
            if j > i + 1 and o[j] <= sp:
                break
            if l[j] <= sp:
                break
            if not np.isnan(T) and j > i + 1:
                if o[j] >= T or h[j] >= T:
                    break
            j += 1
        tg[i:min(j, n - 1) + 1] = T
        if j >= n:
            j = n - 1
        i = j + 1
    return tg

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_adx_ambang_30 = P['adx_ambang_30']
    _p_adx_14 = P['adx_14']
    _p_shift_63 = P['shift_63']
    _p_ewm_span_20 = P['ewm_span_20']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        adx, pdi, mdi = _adx(g, n=_p_adx_14, P=P)
        e20 = g.close.ewm(span=_p_ewm_span_20, adjust=False).mean()
        kuat = adx > _p_adx_ambang_30
        arah = pdi > mdi
        sentuh = (g.low <= e20) & (g.close.shift() > e20.shift())
        setup = kuat & arah & sentuh
        cetus = g.close > g.high.shift()
        puncak = g.high.rolling(_p_rolling_20).max().shift(1)
        stop = g.low.shift()
        sig = setup.shift(1, fill_value=False) & cetus
        bo = g.open.shift(-1)
        sig = sig & ~((bo <= stop) | (bo >= puncak))
        sig = sig.fillna(False).astype(bool)
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _tgt_tetap(g, sig.values, stop.values.astype(float), puncak.values.astype(float), WARM, P=P)
        if sig.iloc[-1]:
            g.iloc[-1, g.columns.get_loc('tgt')] = puncak.iloc[-1]
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
        g['_setup'] = setup
        g['_e20'] = e20
        g['_adx'] = adx
        g['_puncak'] = puncak
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'adx_ambang_30': ('int', 15, 45),
    'adx_14': ('int', 7, 28),
    'shift_63': ('int', 32, 126),
    'ewm_span_20': ('int', 10, 40),
    'rolling_20': ('int', 10, 40),
}
TALA = ['adx_ambang_30', 'adx_14', 'ewm_span_20', 'rolling_20']

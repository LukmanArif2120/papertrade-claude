# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M59.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'bawah': 39,
    'atas': 69,
    'lb': 65,
    'rsi_14': 14,
    'r_ambang_40': 40,
    'rma_atr_kali_3': 3,
    'shift_63': 63,
    'rma_atr_14': 14,
}
ID = 'M59'
NAMA = 'Anjakan Julat RSI'
VARIAN = 'V3 V1 LB65 ambang 39/69 (imbasan Hill 2019)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
LB, BAWAH, ATAS = (65, 39, 69)

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_bawah = P['bawah']
    _p_atas = P['atas']
    _p_lb = P['lb']
    _p_rsi_14 = P['rsi_14']
    _p_r_ambang_40 = P['r_ambang_40']
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    for g in fr.values():
        r = rsi(g.close, _p_rsi_14)
        rmin = r.rolling(_p_lb).min()
        rmax = r.rolling(_p_lb).max()
        k = (rmin > _p_bawah) & (rmax > _p_atas)
        g['_rsi'] = r
        g['_rmin'] = rmin
        g['_rmax'] = rmax
        g['sig'] = k & ~k.shift(1, fill_value=False)
        g['stop'] = g.close - _p_rma_atr_kali_3 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = r < _p_r_ambang_40
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def _rsi_esok(au, ad, c0, x, n=14):
    d = x - c0
    a = au * (1 - 1 / n) + max(d, 0) / n
    b = ad * (1 - 1 / n) + max(-d, 0) / n
    return 100.0 if b == 0 else 100 - 100 / (1 + a / b)

def _cari(au, ad, c0, sasar, naik=True):
    """Tutup esok minimum (naik=True) supaya RSI esok > sasar; carian binari (RSI menokok dengan tutup)."""
    lo, hi = (c0 * 0.5, c0 * 1.5)
    for _ in range(80):
        m = (lo + hi) / 2
        if _rsi_esok(au, ad, c0, m) > sasar:
            hi = m
        else:
            lo = m
    return hi
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

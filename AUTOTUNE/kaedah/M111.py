# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M111.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'n': 7,
    'm': 3.0,
    'sistem_mula_199': 199,
    'close_kali_0_88': 0.88,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M111'
NAMA = 'Sistem Volatiliti Wilder'
VARIAN = 'V5 V1 henti maks(tutup-3xATR7; 0.88xtutup)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N, M = (7, 3.0)

def _rma_atr(g, n, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _sistem(c, a, mula=199, m=M, *, P=PARAM):
    L = len(c)
    naik = np.zeros(L, bool)
    sic = np.full(L, np.nan)
    henti = np.full(L, np.nan)
    if L <= mula:
        return (naik, sic, henti)
    sic[mula] = c[mula]
    for i in range(mula + 1, L):
        if not naik[i - 1]:
            henti[i] = sic[i - 1] + m * a[i - 1]
            if c[i] > henti[i]:
                naik[i] = True
                sic[i] = c[i]
            else:
                sic[i] = min(sic[i - 1], c[i])
        else:
            henti[i] = sic[i - 1] - m * a[i - 1]
            if c[i] < henti[i]:
                naik[i] = False
                sic[i] = c[i]
            else:
                naik[i] = True
                sic[i] = max(sic[i - 1], c[i])
    return (naik, sic, henti)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_n = P['n']
    _p_m = P['m']
    _p_sistem_mula_199 = P['sistem_mula_199']
    _p_close_kali_0_88 = P['close_kali_0_88']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        a = _rma_atr(g, _p_n, P=P)
        c = g.close.values
        naik, sic, henti = _sistem(c, a.values, mula=_p_sistem_mula_199, m=_p_m, P=P)
        naik_s = pd.Series(naik, g.index)
        pusing = naik_s & ~naik_s.shift(1, fill_value=True)
        sma50 = g.close.rolling(_p_rolling_50).mean()
        g['_naik'] = naik
        g['_sic'] = sic
        g['_atr'] = a
        g['_sma50'] = sma50
        g['sig'] = pusing & (g.close > sma50)
        g['stop'] = np.maximum(g.close - _p_m * a, _p_close_kali_0_88 * g.close)
        g['tgt'] = np.nan
        g['exitc'] = ~naik_s & naik_s.shift(1, fill_value=False)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

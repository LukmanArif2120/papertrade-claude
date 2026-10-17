# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M67.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'b_ambang_3': 3,
    'nilai_3': 3,
    'rolling_200': 200,
    'ewm_span_20': 20,
    'ewm_span_50': 50,
    'i_tolak_6': 6,
    'shift_10': 10,
    'nilai_2': 2,
    'rma_atr_14': 14,
    'a_kali_2': 2,
    'shift_63': 63,
}
ID = 'M67'
NAMA = 'Rayner Teo: Ujian Ketiga pada Purata 50'
VARIAN = 'V6 Versi Financial Wisdom: zon EMA20-EMA50, henti 2xATR'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
BIL_SYARAT = lambda b, *, P=PARAM: b == P['b_ambang_3']

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _kira(g, *, P=PARAM):
    _p_i_tolak_6 = P['i_tolak_6']
    c, lo = (g.close.values, g.low.values)
    e20 = g.close.ewm(span=P['ewm_span_20'], adjust=False).mean()
    e50 = g.close.ewm(span=P['ewm_span_50'], adjust=False).mean()
    s200 = g.close.rolling(P['rolling_200']).mean()
    naik = ((g.close > s200) & (e50 > e50.shift(P['shift_10'])) & (e20 > e50)).values
    E20, P_ = (e20.values, e50.values)
    n = len(g)
    uji = (lo <= E20) & (c >= P_)
    atas = lo > E20
    mula = np.zeros(n, bool)
    mula[P['nilai_3']:] = uji[P['nilai_3']:] & atas[P['nilai_2']:-1] & atas[1:-P['nilai_2']] & atas[:-P['nilai_3']]
    reset = ~naik | (c < P_)
    reset[:WARM] = True
    bil = np.zeros(n, int)
    b = 0
    for k in range(n):
        if reset[k]:
            b = 0
        elif mula[k]:
            b += 1
        bil[k] = b
    pantul = np.zeros(n, bool)
    kidx = np.full(n, -1)
    sudah = set()
    for i in range(1, n):
        if not (c[i] > c[i - 1] and c[i] > P_[i]):
            continue
        for k in range(i - 1, max(i - _p_i_tolak_6, -1), -1):
            if mula[k] and (c[k:i + 1] >= P_[k:i + 1]).all():
                if k not in sudah:
                    pantul[i] = True
                    kidx[i] = k
                    sudah.add(k)
                break
    return (naik, mula, bil, pantul, kidx, e20, e50, reset)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_14 = P['rma_atr_14']
    _p_a_kali_2 = P['a_kali_2']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        naik, mula, bil, pantul, kidx, e20, e50, reset = _kira(g, P=P)
        bk = np.where(kidx >= 0, bil[np.clip(kidx, 0, None)], 0)
        sig = naik & pantul & np.array([BIL_SYARAT(x) for x in bk])
        a = _rma_atr(g, n=_p_rma_atr_14, P=P)
        bm = g.open.shift(-1).fillna(g.close)
        g['_naik'] = naik
        g['_bil'] = bil
        g['_e20'] = e20
        g['_e50'] = e50
        g['_mula'] = mula
        g['sig'] = sig
        g['stop'] = bm - _p_a_kali_2 * a
        g['tgt'] = np.nan
        g['exitc'] = g.close < e50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

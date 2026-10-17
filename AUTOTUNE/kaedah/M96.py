# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M96.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'nilai_252': 252,
    'nilai_126': 126,
    'nilai_63': 63,
    's_bahagi_3': 3,
    'sqrt_252': 252,
    'c_ambang_0_05': 0.05,
    'k_ambang_8': 8,
    'atr_kali_3': 3,
    'k_ambang_20': 20,
    'c_kali_0_75': 0.75,
    'atr_14': 14,
    'shift_252': 252,
    'rolling_200': 200,
}
ID = 'M96'
NAMA = 'Momo India: Ranking Sharpe 3/6/12 bulan'
VARIAN = 'V1 Dikunci (+henti tutup-3xATR14)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = True
PERLU_BAR = 270

def _skor(c, *, P=PARAM):
    _p_nilai_252 = P['nilai_252']
    _p_nilai_126 = P['nilai_126']
    _p_nilai_63 = P['nilai_63']
    _p_sqrt_252 = P['sqrt_252']
    r = c.pct_change()
    s = 0
    for n in (_p_nilai_252, _p_nilai_126, _p_nilai_63):
        s = s + (c / c.shift(n) - 1) / (r.rolling(n).std() * np.sqrt(_p_sqrt_252))
    return s / P['s_bahagi_3']

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_c_ambang_0_05 = P['c_ambang_0_05']
    _p_k_ambang_8 = P['k_ambang_8']
    _p_atr_kali_3 = P['atr_kali_3']
    _p_k_ambang_20 = P['k_ambang_20']
    _p_c_kali_0_75 = P['c_kali_0_75']
    _p_atr_14 = P['atr_14']
    _p_shift_252 = P['shift_252']
    _p_rolling_200 = P['rolling_200']
    S = {}
    L = {}
    for t, g in fr.items():
        c = g.close
        lulus = (c >= _p_c_kali_0_75 * c.cummax()) & (c > c.rolling(_p_rolling_200).mean()) & (c / c.shift(_p_shift_252) - 1 > _p_c_ambang_0_05)
        S[t] = _skor(c, P=P)
        L[t] = lulus
    S = pd.DataFrame(S)
    L = pd.DataFrame(L).fillna(False).astype(bool)
    Sl = S.where(L & S.notna())
    ked = Sl.rank(axis=1, ascending=False, method='first')
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    hb = set(pd.Series(tarikh, tarikh).groupby(tarikh.to_period('M')).max())
    akhir = tarikh[-1]
    if (akhir + pd.offsets.BDay(1)).month == akhir.month:
        hb.discard(akhir)
    for t, g in fr.items():
        k = ked[t].reindex(g.index)
        lu = L[t].reindex(g.index).fillna(False).astype(bool)
        hbs = pd.Series(g.index.isin(list(hb)), g.index)
        g['_ked'] = k
        g['_lulus'] = lu
        g['_skor'] = S[t].reindex(g.index)
        g['sig'] = hbs & lu & (k <= _p_k_ambang_8)
        g['stop'] = g.close - _p_atr_kali_3 * atr(g, n=_p_atr_14)
        g['tgt'] = np.nan
        g['exitc'] = hbs & (~lu | k.isna() | (k > _p_k_ambang_20))
        g['rank'] = g['_skor']

def _hari_ke_rotasi(akhir):
    hb = akhir + pd.offsets.BMonthEnd(0)
    if hb == akhir:
        hb = akhir + pd.offsets.BMonthEnd(1)
    return (len(pd.bdate_range(akhir, hb)) - 1, hb)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'nilai_126': ('int', 63, 252),
    'nilai_63': ('int', 32, 126),
    's_bahagi_3': ('float', 1.5, 4.5),
    'c_ambang_0_05': ('float', 0.025, 0.075),
    'atr_kali_3': ('float', 1.5, 4.5),
    'c_kali_0_75': ('float', 0.375, 0.99),
    'atr_14': ('int', 7, 28),
    'rolling_200': ('int', 100, 400),
}
TALA = ['atr_kali_3', 'atr_14', 's_bahagi_3', 'c_ambang_0_05', 'c_kali_0_75', 'rolling_200']

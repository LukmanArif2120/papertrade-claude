# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M101.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'p': 5,
    'ptr_ambang_3': 3,
    'b_ambang_5': 5,
    'p_b_ambang_5_ambang_60': 60,
    'cc_ambang_5': 5,
    'p_cc_ambang_5_ambang_60': 60,
    'i_ambang_126': 126,
    'ptr_tolak_3': 3,
    'ptr_tolak_2': 2,
    'a_tolak_63': 63,
    'p_kali_2': 2,
    'lc_kali_0_99': 0.99,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M101'
NAMA = 'Bulkowski: Tiga lembah menaik'
VARIAN = 'V3 V1 + corak sambungan (tutup_a>tutup_a-63)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320
P_ = 5

def _corak(g, P_=P_, *, P=PARAM):
    """Per hari i: syarat persediaan (NAIK3, JARAK, sambungan), PUNCAK_i, PUNCAK lama (a sama, high a..i-2), low_c."""
    _p_p = P['p']
    _p_ptr_ambang_3 = P['ptr_ambang_3']
    _p_b_ambang_5 = P['b_ambang_5']
    _p_p_b_ambang_5_ambang_60 = P['p_b_ambang_5_ambang_60']
    _p_cc_ambang_5 = P['cc_ambang_5']
    _p_p_cc_ambang_5_ambang_60 = P['p_cc_ambang_5_ambang_60']
    _p_i_ambang_126 = P['i_ambang_126']
    _p_ptr_tolak_3 = P['ptr_tolak_3']
    _p_ptr_tolak_2 = P['ptr_tolak_2']
    _p_a_tolak_63 = P['a_tolak_63']
    lo = g.low.values.astype(float)
    hi = g.high.values.astype(float)
    c = g.close.values.astype(float)
    n = len(g)
    piv = (g.low == g.low.rolling(P['p_kali_2'] * P['p'] + 1, center=True).min()).values
    sedia_ = np.zeros(n, bool)
    pk = np.full(n, np.nan)
    pk_lama = np.full(n, np.nan)
    lc = np.full(n, np.nan)
    sam = np.zeros(n, bool)
    kp = np.nonzero(piv)[0]
    ptr = 0
    for i in range(1, n):
        while ptr < len(kp) and kp[ptr] + _p_p <= i - 1:
            ptr += 1
        if ptr < _p_ptr_ambang_3:
            continue
        a, b, cc = (kp[ptr - _p_ptr_tolak_3], kp[ptr - _p_ptr_tolak_2], kp[ptr - 1])
        naik3 = lo[a] < lo[b] < lo[cc] and lo[cc + 1:i + 1].min() > lo[cc]
        jarak = _p_b_ambang_5 <= b - a <= _p_p_b_ambang_5_ambang_60 and _p_cc_ambang_5 <= cc - b <= _p_p_cc_ambang_5_ambang_60 and (i - a <= _p_i_ambang_126)
        if not (naik3 and jarak):
            continue
        sedia_[i] = True
        pk[i] = hi[a:i].max()
        pk_lama[i] = hi[a:i - 1].max() if i - 1 > a else np.nan
        lc[i] = lo[cc]
        sam[i] = a - _p_a_tolak_63 >= 0 and c[a] > c[a - _p_a_tolak_63]
    idx = g.index
    return (pd.Series(sedia_, idx), pd.Series(pk, idx), pd.Series(pk_lama, idx), pd.Series(lc, idx), pd.Series(sam, idx))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_p = P['p']
    _p_lc_kali_0_99 = P['lc_kali_0_99']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        sd, pk, pkl, lc, sam = _corak(g, P_=_p_p, P=P)
        s50 = g.close.rolling(_p_rolling_50).mean()
        sah = (g.close > pk) & (g.close.shift(1) <= pkl)
        stop = _p_lc_kali_0_99 * lc
        sig = sd & sah & sam & (g.close > s50)
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_sd'] = sd & sam
        g['_pk'] = pk
        g['_lc'] = lc
        g['_s50'] = s50
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

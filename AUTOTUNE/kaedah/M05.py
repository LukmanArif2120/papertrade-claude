# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M05.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_10': 10,
    'len_ambang_2': 2,
    'p2_ambang_5': 5,
    'p_p2_ambang_5_ambang_40': 40,
    'q2_ambang_5': 5,
    'p_q2_ambang_5_ambang_40': 40,
    'rolling_200': 200,
    'range_3': 3,
    'i_tolak_3': 3,
    'n_tolak_3': 3,
    'nilai_2': 2,
    'i_ambang_15': 15,
    'ewm_span_12': 12,
    'ewm_span_26': 26,
    'l_kali_0_99': 0.99,
    't_tolak_3': 3,
    't_tambah_4': 4,
}
ID = 'M05'
NAMA = 'MACD Divergence + Pengesahan'
VARIAN = 'V3 V1+close>SMA200'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 220

def _kira(g, *, P=PARAM):
    _p_range_10 = P['range_10']
    _p_len_ambang_2 = P['len_ambang_2']
    _p_p2_ambang_5 = P['p2_ambang_5']
    _p_p_p2_ambang_5_ambang_40 = P['p_p2_ambang_5_ambang_40']
    _p_q2_ambang_5 = P['q2_ambang_5']
    _p_p_q2_ambang_5_ambang_40 = P['p_q2_ambang_5_ambang_40']
    _p_range_3 = P['range_3']
    _p_i_tolak_3 = P['i_tolak_3']
    _p_n_tolak_3 = P['n_tolak_3']
    _p_nilai_2 = P['nilai_2']
    _p_i_ambang_15 = P['i_ambang_15']
    _p_l_kali_0_99 = P['l_kali_0_99']
    _p_t_tolak_3 = P['t_tolak_3']
    _p_t_tambah_4 = P['t_tambah_4']
    h, l, c = (g.high.values, g.low.values, g.close.values)
    n = len(g)
    M = (g.close.ewm(span=P['ewm_span_12'], adjust=False).mean() - g.close.ewm(span=P['ewm_span_26'], adjust=False).mean()).values
    s200 = g.close.rolling(P['rolling_200']).mean().values
    pl = np.array([t for t in range(_p_range_3, n - _p_n_tolak_3) if l[t] == l[t - _p_t_tolak_3:t + _p_t_tambah_4].min()], dtype=int)
    ph = np.array([t for t in range(_p_range_3, n - _p_n_tolak_3) if h[t] == h[t - _p_t_tolak_3:t + _p_t_tambah_4].max()], dtype=int)
    sg = np.zeros(n, bool)
    st = np.full(n, np.nan)
    rk = np.zeros(n)
    ex = np.zeros(n, bool)
    hv = np.full(n, np.nan)
    p2low = np.full(n, np.nan)
    divok = np.zeros(n, bool)
    for i in range(_p_range_10, n):
        pv = pl[pl <= i - _p_i_tolak_3]
        if len(pv) >= _p_len_ambang_2:
            P1, P2 = (pv[-_p_nilai_2], pv[-1])
            if _p_p2_ambang_5 <= P2 - P1 <= _p_p_p2_ambang_5_ambang_40:
                Hh = h[P1:P2 + 1].max()
                if l[P2] < l[P1] and M[P2] > M[P1] and (i - P2 <= _p_i_ambang_15) and (l[P2 + 1:i + 1].min() > l[P2]):
                    divok[i] = True
                    hv[i] = Hh
                    p2low[i] = l[P2]
                    if c[i] > Hh and c[i - 1] <= Hh and (c[i] > s200[i]):
                        sg[i] = True
                        st[i] = _p_l_kali_0_99 * l[P2]
                        rk[i] = (M[P2] - M[P1]) / c[i]
        qv = ph[ph <= i - _p_i_tolak_3]
        if len(qv) >= _p_len_ambang_2:
            Q1, Q2 = (qv[-_p_nilai_2], qv[-1])
            if _p_q2_ambang_5 <= Q2 - Q1 <= _p_p_q2_ambang_5_ambang_40:
                Mm = l[Q1:Q2 + 1].min()
                if h[Q2] > h[Q1] and M[Q2] < M[Q1] and (c[i] < Mm) and (c[i - 1] >= Mm) and (i - Q2 <= _p_i_ambang_15):
                    ex[i] = True
    return (sg, st, rk, ex, divok, hv, p2low, s200)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    for g in fr.values():
        sg, st, rk, ex, divok, hv, p2low, s200 = _kira(g, P=P)
        stop = pd.Series(st, g.index)
        bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())
        g['_div'] = divok
        g['_H'] = hv
        g['_p2'] = p2low
        g['_s200'] = s200
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ex
        g['rank'] = rk

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

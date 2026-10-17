# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M06.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rank_kali_100': 100,
    'cl_kali_0_2': 0.2,
    'cl_kali_0_4': 0.4,
    'shift_252': 252,
    'shift_189': 189,
    'shift_63': 63,
    'shift_126': 126,
    'rsp_ambang_70': 70,
    'rolling_15': 15,
    'vola_kali_1_4': 1.4,
    'rolling_50': 50,
    'rolling_150': 150,
    'rolling_200': 200,
    'h_kali_0_75': 0.75,
    'piv_kali_1_05': 1.05,
    'l_kali_1_3': 1.3,
    'lb3_kali_0_99': 0.99,
    'bm_kali_0_92': 0.92,
    'shift_21': 21,
    'rolling_252': 252,
}
ID = 'M06'
NAMA = 'Minervini VCP Breakout'
VARIAN = 'V5 V1 tanpa VCP'
TMAX = None
WARM = 252
ADA_HENTI = True
SILANG = True
PERLU_BAR = 260

def _rsp(fr, *, P=PARAM):
    cl = pd.DataFrame({t: g.close for t, g in fr.items()})
    rs = P['cl_kali_0_4'] * (cl / cl.shift(P['shift_63']) - 1) + P['cl_kali_0_2'] * (cl / cl.shift(P['shift_126']) - 1) + P['cl_kali_0_2'] * (cl / cl.shift(P['shift_189']) - 1) + P['cl_kali_0_2'] * (cl / cl.shift(P['shift_252']) - 1)
    return rs.rank(axis=1, pct=True) * P['rank_kali_100']

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rsp_ambang_70 = P['rsp_ambang_70']
    _p_rolling_15 = P['rolling_15']
    _p_vola_kali_1_4 = P['vola_kali_1_4']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_150 = P['rolling_150']
    _p_rolling_200 = P['rolling_200']
    _p_h_kali_0_75 = P['h_kali_0_75']
    _p_piv_kali_1_05 = P['piv_kali_1_05']
    _p_l_kali_1_3 = P['l_kali_1_3']
    _p_lb3_kali_0_99 = P['lb3_kali_0_99']
    _p_bm_kali_0_92 = P['bm_kali_0_92']
    _p_shift_21 = P['shift_21']
    _p_rolling_252 = P['rolling_252']
    RSP = _rsp(fr, P=P)
    for t, g in fr.items():
        o, h, l, c, v = (g.open, g.high, g.low, g.close, g.volume)
        s50, s150, s200 = (c.rolling(_p_rolling_50).mean(), c.rolling(_p_rolling_150).mean(), c.rolling(_p_rolling_200).mean())
        rsp = RSP[t].reindex(g.index)
        TT = (c > s50) & (s50 > s150) & (s150 > s200) & (s200 > s200.shift(_p_shift_21)) & (c >= _p_l_kali_1_3 * l.rolling(_p_rolling_252).min()) & (c >= _p_h_kali_0_75 * h.rolling(_p_rolling_252).max()) & (rsp >= _p_rsp_ambang_70)
        VOLA = v.rolling(_p_rolling_50).mean().shift(1)
        PIV = h.shift(1).rolling(_p_rolling_15).max()
        LB3 = l.shift(1).rolling(_p_rolling_15).min()
        sig = TT & (c > PIV) & (c.shift() <= PIV) & (v >= _p_vola_kali_1_4 * VOLA)
        bm = o.shift(-1)
        stop = pd.concat([_p_lb3_kali_0_99 * LB3, _p_bm_kali_0_92 * bm], axis=1).max(axis=1)
        ok = (bm > stop) & (bm <= _p_piv_kali_1_05 * PIV) | bm.isna()
        g['_tt'] = TT.fillna(False)
        g['_piv'] = PIV
        g['_vola'] = VOLA
        g['_rsp'] = rsp
        g['sig'] = (sig & ok).fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = rsp.fillna(0)

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

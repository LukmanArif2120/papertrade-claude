# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M07.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_132': 132,
    'atrw_14': 14,
    'i_tolak_126': 126,
    'k_tolak_63': 63,
    'run_ambang_0_3': 0.3,
    'adr_ambang_0_04': 0.04,
    'rolling_10': 10,
    'rolling_20': 20,
    'rolling_50': 50,
    'adr_kali_3': 3,
    'i_tolak_5': 5,
    'i_tolak_6': 6,
    's10_kali_1_01': 1.01,
    'i_tolak_10': 10,
    'i_tolak_4': 4,
    'i_tolak_9': 9,
    'shift_126': 126,
}
ID = 'M07'
NAMA = 'Qullamaggie Breakout'
VARIAN = 'V11 V7 keluar close<SMA20'
TMAX = None
WARM = 130
ADA_HENTI = True
SILANG = False
PERLU_BAR = 140

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _mkt(idx, ix, *, P=PARAM):
    q = idx['QQQ'].close
    q10, q20 = (q.rolling(P['rolling_10']).mean(), q.rolling(P['rolling_20']).mean())
    m = (q10 > q20) & ((q10 > q10.shift()) | (q20 > q20.shift()))
    return m.reindex(ix).fillna(False).astype(bool).values

def _kira(g, MKT, *, P=PARAM):
    _p_range_132 = P['range_132']
    _p_i_tolak_126 = P['i_tolak_126']
    _p_k_tolak_63 = P['k_tolak_63']
    _p_run_ambang_0_3 = P['run_ambang_0_3']
    _p_adr_ambang_0_04 = P['adr_ambang_0_04']
    _p_adr_kali_3 = P['adr_kali_3']
    _p_i_tolak_5 = P['i_tolak_5']
    _p_i_tolak_6 = P['i_tolak_6']
    _p_s10_kali_1_01 = P['s10_kali_1_01']
    _p_i_tolak_10 = P['i_tolak_10']
    _p_i_tolak_4 = P['i_tolak_4']
    _p_i_tolak_9 = P['i_tolak_9']
    h, l, c, o = (g.high.values, g.low.values, g.close.values, g.open.values)
    n = len(g)
    s10 = g.close.rolling(P['rolling_10']).mean().values
    s20 = g.close.rolling(P['rolling_20']).mean().values
    s50 = g.close.rolling(P['rolling_50']).mean().values
    a14 = _atrw(g, n=P['atrw_14'], P=P).values
    ADR = ((g.high / g.low).rolling(P['rolling_20']).mean() - 1).values
    sg = np.zeros(n, bool)
    setup = np.zeros(n, bool)
    RHv = np.full(n, np.nan)
    for i in range(_p_range_132, n):
        k = i - _p_i_tolak_126 + int(np.argmax(h[i - _p_i_tolak_126:i - _p_i_tolak_4]))
        if k - _p_k_tolak_63 < 0:
            continue
        RUN = h[k] / l[k - _p_k_tolak_63:k + 1].min() - 1
        RH = h[i - _p_i_tolak_5:i].max()
        RL = l[i - _p_i_tolak_5:i].min()
        RHp = h[i - _p_i_tolak_6:i - 1].max()
        SURF = any((l[t] <= _p_s10_kali_1_01 * s10[t] and c[t] >= s50[t] for t in range(i - _p_i_tolak_10, i)))
        HL = RL > l[i - _p_i_tolak_10:i - _p_i_tolak_5].min()
        base = RUN >= _p_run_ambang_0_3 and s10[i] > s20[i] and (s20[i] > s20[i - _p_i_tolak_5]) and SURF and HL and (ADR[i] >= _p_adr_ambang_0_04) and ((RH - RL) / RL <= _p_adr_kali_3 * ADR[i]) and (c[i] > s50[i])
        if base and MKT[i] and (c[i] > RH) and (c[i - 1] <= RHp) and (c[i] - l[i] <= a14[i]):
            sg[i] = True
        if i == n - 1:
            RH2 = h[i - _p_i_tolak_4:i + 1].max()
            RL2 = l[i - _p_i_tolak_4:i + 1].min()
            SURF2 = any((l[t] <= _p_s10_kali_1_01 * s10[t] and c[t] >= s50[t] for t in range(i - _p_i_tolak_9, i + 1)))
            HL2 = RL2 > l[i - _p_i_tolak_9:i - _p_i_tolak_4].min()
            setup[i] = RUN >= _p_run_ambang_0_3 and s10[i] > s20[i] and SURF2 and HL2 and (ADR[i] >= _p_adr_ambang_0_04) and ((RH2 - RL2) / RL2 <= _p_adr_kali_3 * ADR[i]) and (c[i] > s50[i]) and (c[i] <= RH2)
            RHv[i] = RH2
    return (sg, setup, RHv, ADR, a14)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_126 = P['shift_126']
    _p_rolling_20 = P['rolling_20']
    for g in fr.values():
        MKT = _mkt(idx, g.index, P=P)
        sg, setup, RHv, ADR, a14 = _kira(g, MKT, P=P)
        stop = g.low.copy()
        bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())
        g['_setup'] = setup
        g['_rh'] = RHv
        g['_mkt'] = MKT
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < g.close.rolling(_p_rolling_20).mean()).fillna(False)
        g['rank'] = g.close / g.close.shift(_p_shift_126) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'atrw_14': ('int', 7, 28),
    'run_ambang_0_3': ('float', 0.15, 0.45),
    'adr_ambang_0_04': ('float', 0.02, 0.06),
    'rolling_10': ('int', 5, 20),
    'rolling_20': ('int', 10, 40),
    'rolling_50': ('int', 25, 100),
    'adr_kali_3': ('float', 1.5, 4.5),
    's10_kali_1_01': ('float', 0.505, 1.515),
    'shift_126': ('int', 63, 252),
}
TALA = ['rolling_20', 'run_ambang_0_3', 'adr_ambang_0_04', 'rolling_10', 'adr_kali_3', 's10_kali_1_01']

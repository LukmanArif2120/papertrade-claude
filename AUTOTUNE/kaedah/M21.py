# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M21.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'range_70': 70,
    'atr_14': 14,
    'c_ambang_1000000_0': 1000000.0,
    'i_tolak_63': 63,
    'run_ambang_0_3': 0.3,
    'o_ambang_0_05': 0.05,
    'c_ambang_0_75': 0.75,
    'adr_ambang_0_05': 0.05,
    'rolling_10': 10,
    'rolling_20': 20,
    'rolling_50': 50,
    'adr_kali_2_5': 2.5,
    'hk_kali_0_75': 0.75,
    'vol50_kali_3': 3,
    'max_0_04': 0.04,
    'vol50_kali_2': 2,
    'i_tolak_10': 10,
    'i_tolak_2': 2,
    'i_tolak_11': 11,
    'i_tolak_20': 20,
    'k_tolak_63': 63,
    'rolling_40': 40,
    'rolling_252': 252,
}
ID = 'M21'
NAMA = 'Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan)'
VARIAN = 'V5 V1 keluar close<SMA20'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300

def _persediaan(g, spy, *, P=PARAM):
    _p_range_70 = P['range_70']
    _p_i_tolak_63 = P['i_tolak_63']
    _p_run_ambang_0_3 = P['run_ambang_0_3']
    _p_o_ambang_0_05 = P['o_ambang_0_05']
    _p_c_ambang_0_75 = P['c_ambang_0_75']
    _p_adr_kali_2_5 = P['adr_kali_2_5']
    _p_hk_kali_0_75 = P['hk_kali_0_75']
    _p_vol50_kali_3 = P['vol50_kali_3']
    _p_max_0_04 = P['max_0_04']
    _p_vol50_kali_2 = P['vol50_kali_2']
    _p_i_tolak_10 = P['i_tolak_10']
    _p_i_tolak_2 = P['i_tolak_2']
    _p_i_tolak_11 = P['i_tolak_11']
    _p_i_tolak_20 = P['i_tolak_20']
    _p_k_tolak_63 = P['k_tolak_63']
    O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
    n = len(g)
    c, v = (g.close, g.volume)
    a14 = atr(g, P['atr_14']).values
    ADR = ((g.high / g.low).rolling(P['rolling_20']).mean() - 1).values
    U = ((c > 1) & (pd.Series(ADR, g.index) >= P['adr_ambang_0_05']) & ((c * v).rolling(P['rolling_20']).mean() >= P['c_ambang_1000000_0'])).values
    VOL50 = v.rolling(P['rolling_50']).mean().shift(1).values
    s10 = c.rolling(P['rolling_10']).mean().values
    s20 = c.rolling(P['rolling_20']).mean().values
    s50 = c.rolling(P['rolling_50']).mean().values
    sp = spy.reindex(g.index).ffill().values
    BOk = np.zeros(n, bool)
    EPk = np.zeros(n, bool)
    MCk = np.zeros(n, bool)
    for i in range(_p_range_70, n):
        if not U[i]:
            continue
        k = i - _p_i_tolak_63 + int(np.argmax(H[i - _p_i_tolak_63:i - _p_i_tolak_2]))
        hk = H[k]
        RUN = hk / L[max(0, k - _p_k_tolak_63):k + 1].min() - 1
        RH = H[i - _p_i_tolak_10:i].max()
        RL = L[i - _p_i_tolak_10:i].min()
        BO = RUN >= _p_run_ambang_0_3 and s10[i] > s20[i] and (C[i] > RH) and (C[i - 1] <= H[i - _p_i_tolak_11:i - 1].max()) and (C[i] - L[i] <= a14[i])
        BOk[i] = BO and (RH - RL) / RL <= _p_adr_kali_2_5 * ADR[i] and (C[i] > s50[i]) and (RL >= _p_hk_kali_0_75 * hk)
        H63 = H[i - _p_i_tolak_63:i].max()
        EP = O[i] / C[i - 1] - 1 >= _p_o_ambang_0_05 and V[i] >= _p_vol50_kali_3 * VOL50[i] and (O[i] > H63)
        EPk[i] = EP and C[i] > H63
        MC = sp[i] < sp[i - 1] and C[i] / C[i - 1] - 1 >= max(_p_max_0_04, ADR[i]) and (V[i] >= _p_vol50_kali_2 * VOL50[i]) and (C[i] > H[i - _p_i_tolak_20:i].max())
        MCk[i] = MC and H[i] > L[i] and ((C[i] - L[i]) / (H[i] - L[i]) >= _p_c_ambang_0_75)
    return (BOk, EPk, MCk, U, ADR)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_20 = P['rolling_20']
    _p_rolling_40 = P['rolling_40']
    _p_rolling_252 = P['rolling_252']
    spy = idx['SPY'].close
    for g in fr.values():
        BOk, EPk, MCk, U, ADR = _persediaan(g, spy, P=P)
        sig = pd.Series(BOk | EPk | MCk, g.index)
        lk = (g.open.shift(-1) <= g.low).fillna(False)
        sig = (sig & ~lk).fillna(False)
        S20 = g.close.rolling(_p_rolling_20).mean()
        RED1 = sig.shift(1, fill_value=False) & (g.close < g.open)
        g['_U'] = U
        g['_ADR'] = ADR
        g['sig'] = sig
        g['stop'] = g.low
        g['tgt'] = np.nan
        g['exitc'] = (g.close < S20) | RED1
        g['rank'] = g.volume.rolling(_p_rolling_40).mean() / g.volume.rolling(_p_rolling_252).mean()
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'atr_14': ('int', 7, 28),
    'run_ambang_0_3': ('float', 0.15, 0.45),
    'o_ambang_0_05': ('float', 0.025, 0.075),
    'c_ambang_0_75': ('float', 0.375, 0.99),
    'adr_ambang_0_05': ('float', 0.025, 0.075),
    'rolling_10': ('int', 5, 20),
    'rolling_20': ('int', 10, 40),
    'rolling_50': ('int', 25, 100),
    'adr_kali_2_5': ('float', 1.25, 3.75),
    'hk_kali_0_75': ('float', 0.375, 0.99),
    'vol50_kali_3': ('float', 1.5, 4.5),
    'max_0_04': ('float', 0.02, 0.06),
    'vol50_kali_2': ('float', 1.0, 3.0),
    'rolling_40': ('int', 20, 80),
}
TALA = ['rolling_20', 'rolling_50', 'atr_14', 'run_ambang_0_3', 'o_ambang_0_05', 'c_ambang_0_75']

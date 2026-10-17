# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M78.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'k_atr': 5,
    'weekday_ambang_4': 4,
    'rma_atr_100': 100,
    'open_kali_0_92': 0.92,
    'rolling_100': 100,
    'shift_20': 20,
    'rolling_21': 21,
    'dv21_ambang_15000000_0': 15000000.0,
    'rolling_19': 19,
    'r20_ambang_0_3': 0.3,
}
ID = 'M78'
NAMA = 'Alvarez Pecahan Mingguan DTAYS'
VARIAN = 'V2 V1 henti mengekor 5xATR100'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210
K_ATR = 5

def _rma_atr(g, n, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _hm(g, *, P=PARAM):
    ix = g.index
    minggu = ix.to_period('W-SUN')
    hm = pd.Series(minggu[:-1] != minggu[1:], index=ix[:-1]).reindex(ix)
    hm.iloc[-1] = ix[-1].weekday() == P['weekday_ambang_4']
    return hm.astype(bool)

def _exitc_ekor(g, warm, *, P=PARAM):
    """Replika urutan dagangan enjin untuk henti mengekor bergantung dagangan: tutup_j < TT_j - K x ATR100_j."""
    _p_k_atr = P['k_atr']
    o, l, c = (g.open.values, g.low.values, g.close.values)
    sig = g.sig.fillna(False).astype(bool).values
    st = g.stop.astype(float).values
    a = g._atr100.values
    n = len(g)
    ex = np.zeros(n, bool)
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        j = i + 1
        tt = -np.inf
        keluar = n - 1
        while j < n:
            if j > i + 1 and o[j] <= sp:
                keluar = j
                break
            if l[j] <= sp:
                keluar = j
                break
            tt = max(tt, c[j])
            if c[j] < tt - _p_k_atr * a[j] and j + 1 < n:
                ex[j] = True
                keluar = j + 1
                break
            j += 1
        i = keluar + 1
    return ex

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_100 = P['rma_atr_100']
    _p_open_kali_0_92 = P['open_kali_0_92']
    _p_shift_20 = P['shift_20']
    _p_rolling_21 = P['rolling_21']
    _p_dv21_ambang_15000000_0 = P['dv21_ambang_15000000_0']
    _p_rolling_19 = P['rolling_19']
    _p_r20_ambang_0_3 = P['r20_ambang_0_3']
    spy = idx['SPY'].close
    mkt_spy = spy > spy.rolling(P['rolling_100']).mean()
    for g in fr.values():
        c = g.close
        hm = _hm(g, P=P)
        tm = c[hm]
        high20 = tm >= tm.shift(1).rolling(_p_rolling_19).max()
        ret20 = tm / tm.shift(_p_shift_20) - 1
        H20 = high20.reindex(g.index).fillna(False).astype(bool)
        R20 = ret20.reindex(g.index)
        dv21 = (c * g.volume).rolling(_p_rolling_21).mean()
        mkt = mkt_spy.reindex(g.index, method='ffill').fillna(False).astype(bool)
        g['_hm'] = hm
        g['_ret20'] = R20
        g['_dv21'] = dv21
        g['_mkt'] = mkt
        g['_atr100'] = _rma_atr(g, _p_rma_atr_100, P=P)
        g['sig'] = hm & H20 & (R20 > _p_r20_ambang_0_3) & (dv21 > _p_dv21_ambang_15000000_0) & mkt
        g['stop'] = _p_open_kali_0_92 * g.open.shift(-1)
        g['tgt'] = np.nan
        g['rank'] = R20.fillna(0.0)
        g['exitc'] = _exitc_ekor(g, WARM, P=P)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M84.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'rank_kali_100': 100,
    'close_ambang_5': 5,
    'rma_atr_kali_3': 3,
    'rolling_50': 50,
    'p_ambang_90': 90,
    'rolling_21': 21,
    'rolling_200': 200,
    'rma_atr_14': 14,
    'pmad_ambang_90': 90,
}
ID = 'M84'
NAMA = 'Jarak purata bergerak MAD 21/200'
VARIAN = 'V5 V1 + SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = True
PERLU_BAR = 210

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _hb(dates, *, P=PARAM):
    """Hujung bulan daripada kalendar dagangan gabungan: hari berikutnya dalam bulan lain.
    Andaian saya: bagi tarikh terakhir data (hari esok belum diketahui), guna hari bekerja berikutnya (BDay,
    tanpa cuti umum) untuk menentukan sama ada hari ini hari dagangan terakhir bulan."""
    d = pd.DatetimeIndex(sorted(dates))
    nxt = pd.Series(d[1:].tolist() + [d[-1] + pd.offsets.BDay(1)], index=d)
    return pd.Series(nxt.dt.month.values != d.month, index=d)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_close_ambang_5 = P['close_ambang_5']
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_rolling_50 = P['rolling_50']
    _p_p_ambang_90 = P['p_ambang_90']
    _p_rolling_21 = P['rolling_21']
    _p_rolling_200 = P['rolling_200']
    _p_rma_atr_14 = P['rma_atr_14']
    dates = sorted(set().union(*[g.index for g in fr.values()]))
    hb = _hb(dates, P=P)
    mad = {}
    for t, g in fr.items():
        m = g.close.rolling(_p_rolling_21).mean() / g.close.rolling(_p_rolling_200).mean()
        mad[t] = m.where(g.close >= _p_close_ambang_5)
    M = pd.DataFrame(mad)
    P_ = M.rank(axis=1, pct=True) * P['rank_kali_100']
    for t, g in fr.items():
        s50 = g.close.rolling(_p_rolling_50).mean()
        des = (P_[t].reindex(g.index) >= _p_p_ambang_90).fillna(False)
        h = hb.reindex(g.index).fillna(False).astype(bool)
        m = g.close.rolling(_p_rolling_21).mean() / g.close.rolling(_p_rolling_200).mean()
        g['_mad'] = m
        g['_pmad'] = P_[t].reindex(g.index)
        g['_s50'] = s50
        g['_hb'] = h
        g['sig'] = h & des & (g.close > s50)
        g['stop'] = g.close - _p_rma_atr_kali_3 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['tgt'] = np.nan
        g['exitc'] = h & ~des | (g.close < s50)
        g['rank'] = m
    C = pd.DataFrame({t: g._mad.where((g._pmad >= P['pmad_ambang_90']) & (g.close > g._s50)) for t, g in fr.items()})
    K = C.rank(axis=1, ascending=False, method='first')
    for t, g in fr.items():
        g['_kd'] = K[t].reindex(g.index)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

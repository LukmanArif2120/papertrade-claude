# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M50.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'dayofweek_ambang_4': 4,
    'ewm_span_12': 12,
    'ewm_span_26': 26,
    'ewm_span_9': 9,
    'rolling_50': 50,
    'shift_63': 63,
    'ewm_span_2': 2,
}
ID = 'M50'
NAMA = 'Elder Triple Screen'
VARIAN = 'V2 V1 keluar tutup<SMA50 + tutup>SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _arus(g, *, P=PARAM):
    """ARUS_i = HISTM minggu siap w(i) > HISTM minggu sebelumnya (MACD 12/26/9 mingguan).
    Minggu kalendar Isnin-Ahad; tutup mingguan = tutup hari dagangan terakhir minggu itu."""
    wk = g.index.to_period('W-SUN')
    akhir = pd.Series(wk, g.index) != pd.Series(wk, g.index).shift(-1)
    akhir.iloc[-1] = g.index[-1].dayofweek == P['dayofweek_ambang_4']
    tm = g.close.groupby(wk).last()
    macd = tm.ewm(span=P['ewm_span_12'], adjust=False).mean() - tm.ewm(span=P['ewm_span_26'], adjust=False).mean()
    hist = macd - macd.ewm(span=P['ewm_span_9'], adjust=False).mean()
    naik = hist > hist.shift(1)
    pos = pd.Series(np.arange(len(tm)), tm.index)
    wpos = pos.reindex(wk).values
    wsiap = np.where(akhir.values, wpos, wpos - 1)
    nv = naik.values
    arus = np.array([bool(nv[k]) if k >= 0 else False for k in wsiap])
    return (pd.Series(arus, g.index), akhir)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    _p_ewm_span_2 = P['ewm_span_2']
    for g in fr.values():
        c = g.close
        arus, akhir = _arus(g, P=P)
        fi2 = ((c - c.shift()) * g.volume).ewm(span=_p_ewm_span_2, adjust=False).mean()
        undur = fi2.shift() < 0
        pecah = g.high > g.high.shift()
        s50 = c.rolling(_p_rolling_50).mean()
        sig = arus & undur & pecah & (c > s50)
        stop = pd.concat([g.low, g.low.shift()], axis=1).min(axis=1)
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_arus'] = arus
        g['_fi2'] = fi2
        g['_s50'] = s50
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M37.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'vol4_kali_2': 2,
    'rolling_30': 30,
    'rolling_10': 10,
    'rolling_26': 26,
    'rolling_4': 4,
    'shift_4': 4,
    'rolling_52': 52,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M37'
NAMA = 'Weinstein Peringkat 2'
VARIAN = 'V2 V1 keluar tutup harian<SMA50 + tutup>SMA50'
TMAX = None
WARM = 400
ADA_HENTI = True
SILANG = False
PERLU_BAR = 420

def _mingguan(g, spy, *, P=PARAM):
    wk = g.index.to_period('W-FRI')
    grp = pd.Series(g.index, index=g.index).groupby(wk)
    akhir = grp.transform('max')
    W = pd.DataFrame({'high': g.high.groupby(wk).max(), 'low': g.low.groupby(wk).min(), 'close': g.close.groupby(wk).last(), 'volume': g.volume.groupby(wk).sum(), 'tarikh': grp.max()})
    sp = spy.reindex(g.index).ffill()
    W['spy'] = sp.groupby(wk).last().values
    return (W, akhir)

def _isyarat_mingguan(W, *, P=PARAM):
    c = W.close
    s30 = c.rolling(P['rolling_30']).mean()
    s10 = c.rolling(P['rolling_10']).mean()
    ma_ok = (c > s30) & (s30 >= s30.shift(P['shift_4'])) & (s10 > s10.shift(1))
    r26 = W.high.shift(1).rolling(P['rolling_26']).max()
    pecah = (c > r26) & (c.shift(1) <= r26.shift(1))
    vol4 = W.volume.shift(1).rolling(P['rolling_4']).mean()
    vol_ok = W.volume >= P['vol4_kali_2'] * vol4
    rp = c / W.spy
    kr = rp / rp.rolling(P['rolling_52']).mean() - 1
    kr_ok = kr > 0
    stop = W.low.rolling(P['rolling_4']).min()
    return dict(s30=s30, s10=s10, ma_ok=ma_ok, r26=r26, pecah=pecah, vol4=vol4, vol_ok=vol_ok, kr=kr, kr_ok=kr_ok, stop=stop)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    spy = idx['SPY'].close
    for g in fr.values():
        W, akhir = _mingguan(g, spy, P=P)
        k = _isyarat_mingguan(W, P=P)
        sigw = (k['ma_ok'] & k['pecah'] & k['vol_ok'] & k['kr_ok']).fillna(False)
        tarikh = W.tarikh.values
        sig = pd.Series(False, g.index)
        stop = pd.Series(np.nan, g.index)
        sig.loc[tarikh] = sigw.values
        stop.loc[tarikh] = k['stop'].values
        s50 = g.close.rolling(_p_rolling_50).mean()
        sig = sig & (g.close > s50)
        bk = g.open.shift(-1)
        sig = sig & ((bk > stop) | bk.isna())
        g['_s50'] = s50
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < s50).fillna(False)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

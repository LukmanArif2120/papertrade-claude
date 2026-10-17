# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M41.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'n_bahagi_2': 2,
    'ema_sma_9': 9,
    'rint_bahagi_2': 2,
    'c_ambang_0_2': 0.2,
    'ema_sma_12': 12,
    'ema_sma_26': 26,
    'volume_kali_1_3': 1.3,
    'rolling_20': 20,
    'sumbu_ambang_0_5': 0.5,
    'rolling_6': 6,
    'rolling_10': 10,
    'saiz_ambang_0_2': 0.2,
    'saiz_ambang_0_05': 0.05,
    'weekday_ambang_4': 4,
    'shift_63': 63,
    'nilai_6': 6,
    'nilai_10': 10,
}
ID = 'M41'
NAMA = 'FW Penyatuan Mingguan'
VARIAN = 'V0 Sumber sahaja (tanpa had julat 25%)'
TMAX = None
WARM = 300
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320

def _ema_sma(x, n, *, P=PARAM):
    """EMA dimulakan dengan purata mudah n nilai pertama yang sah (kad)."""
    x = pd.Series(x, dtype=float)
    out = np.full(len(x), np.nan)
    v = x.values
    ok = np.flatnonzero(~np.isnan(v))
    if len(ok) < n:
        return pd.Series(out, x.index)
    s = ok[0]
    a = P['n_bahagi_2'] / (n + 1)
    out[s + n - 1] = v[s:s + n].mean()
    for k in range(s + n, len(v)):
        out[k] = a * v[k] + (1 - a) * out[k - 1]
    return pd.Series(out, x.index)

def _minggu(g, *, P=PARAM):
    k = g.index.to_period('W-SUN')
    gr = g.groupby(k)
    w = pd.DataFrame({'open': gr.open.first(), 'high': gr.high.max(), 'low': gr.low.min(), 'close': gr.close.last(), 'volume': gr.volume.sum(), 'tarikh': pd.Series(g.index, index=g.index).groupby(k).last()}).reset_index(drop=True)
    c = w.close
    w['sma20'] = c.rolling(P['rolling_20']).mean()
    w['macd'] = _ema_sma(c, P['ema_sma_12'], P=P) - _ema_sma(c, P['ema_sma_26'], P=P)
    w['isy'] = _ema_sma(w.macd, P['ema_sma_9'], P=P)
    w['rint'] = w.high.rolling(P['rolling_6']).max().shift(1)
    w['sok'] = w.low.rolling(P['rolling_6']).min().shift(1)
    saiz = c / c.shift() - 1
    t10 = c > c.rolling(P['rolling_10']).max().shift(1)
    jul = w.high - w.low
    sumbu = np.where(jul > 0, (w.high - np.maximum(w.open, c)) / jul.replace(0, np.nan), 1.0)
    w['henti'] = (w.rint + w.sok) / P['rint_bahagi_2']
    jarak = (c - w.henti) / c < P['c_ambang_0_2']
    volok = w.volume >= P['volume_kali_1_3'] * w.volume.shift()
    w['sig'] = (c > w.sma20) & (w.macd > w.isy) & (c > w.rint) & (saiz >= P['saiz_ambang_0_05']) & (saiz <= P['saiz_ambang_0_2']) & t10 & (pd.Series(sumbu) < P['sumbu_ambang_0_5']) & volok & jarak
    w['turun'] = (w.macd < w.isy) & (w.macd.shift() >= w.isy.shift())
    return w

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_weekday_ambang_4 = P['weekday_ambang_4']
    _p_shift_63 = P['shift_63']
    _p_nilai_6 = P['nilai_6']
    _p_nilai_10 = P['nilai_10']
    for g in fr.values():
        w = _minggu(g, P=P)
        ix = g.index
        n = len(g)
        pos = {d: i for i, d in enumerate(ix)}
        o, lo, c = (g.open.values, g.low.values, g.close.values)
        wk_of_day = np.searchsorted(w.tarikh.values, ix.values)
        sig = np.zeros(n, bool)
        stop = np.full(n, np.nan)
        exitc = np.zeros(n, bool)
        raw = {}
        for k in np.flatnonzero(w.sig.values):
            raw[pos[w.tarikh[k]]] = (k, w.henti[k])
        for i, (k, h) in raw.items():
            stop[i] = h
        turun = w.turun.values
        i = WARM
        while i < n - 1:
            if i not in raw or o[i + 1] <= raw[i][1]:
                i += 1
                continue
            wk, sp = raw[i]
            sig[i] = True
            xs = np.flatnonzero(turun[wk + 1:])
            paras = None
            mula = None
            if len(xs):
                x = wk + 1 + xs[0]
                paras = w.low[x]
                mula = pos[w.tarikh[x]] + 1
            j = i + 1
            keluar = None
            while j < n:
                ex = paras is not None and j >= mula and (c[j] < paras)
                if ex:
                    exitc[j] = True
                if j > i + 1 and o[j] <= sp:
                    keluar = j
                    break
                if lo[j] <= sp:
                    keluar = j
                    break
                if ex and j + 1 < n:
                    keluar = j + 1
                    break
                j += 1
            if keluar is None:
                break
            i = keluar + 1
        siap = ix[-1].weekday() == _p_weekday_ambang_4
        if n - 1 in raw and n - 1 >= WARM and siap:
            sig[n - 1] = True
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = exitc
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
        b = len(w) if siap else len(w) - 1
        ws = w.iloc[:b]
        g.attrs['_m41'] = dict(siap=siap, close=float(ws.close.iloc[-1]), sma20=float(ws.sma20.iloc[-1]), macd=float(ws.macd.iloc[-1]), isy=float(ws.isy.iloc[-1]), rint=float(ws.high.iloc[-_p_nilai_6:].max()), sok=float(ws.low.iloc[-_p_nilai_6:].min()), tutup10=float(ws.close.iloc[-_p_nilai_10:].max()), vol_lalu=float(ws.volume.iloc[-1]), tutup_lalu=float(ws.close.iloc[-1]))
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'ema_sma_9': ('int', 4, 18),
    'c_ambang_0_2': ('float', 0.1, 0.3),
    'ema_sma_12': ('int', 6, 24),
    'ema_sma_26': ('int', 13, 52),
    'volume_kali_1_3': ('float', 0.65, 1.95),
    'rolling_20': ('int', 10, 40),
    'sumbu_ambang_0_5': ('float', 0.25, 0.75),
    'rolling_6': ('int', 3, 12),
    'rolling_10': ('int', 5, 20),
    'saiz_ambang_0_2': ('float', 0.1, 0.3),
    'saiz_ambang_0_05': ('float', 0.025, 0.075),
    'shift_63': ('int', 32, 126),
}
TALA = ['rolling_6', 'ema_sma_9', 'c_ambang_0_2', 'ema_sma_12', 'ema_sma_26', 'volume_kali_1_3']

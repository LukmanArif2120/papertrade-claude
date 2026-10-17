# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M40.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'weekday_ambang_2': 2,
    'weekday_mod_7': 7,
    'weekday_tolak_2': 2,
    'n_bahagi_2': 2,
    'b_kuasa_2': 2,
    'x_kuasa_2': 2,
    'd_kuasa_2': 2,
    'b_kali_252': 252,
    'slot': 8,
    'skor_90': 90,
    'rma_atr_kali_3': 3,
    'nb_kali_0_2': 0.2,
    'rolling_100': 100,
    'rma_atr_20': 20,
    'rolling_90': 90,
    'loc_kali_0_2': 0.2,
    'c_ambang_0_15': 0.15,
}
ID = 'M40'
NAMA = 'Clenow Stocks on the Move'
VARIAN = 'V4 V1 tanpa penapis pasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = True
PERLU_BAR = 210
SLOT = 8
START = pd.Timestamp('2019-11-01')

def _rma_atr(g, n, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _skor(c, n=90, *, P=PARAM):
    y = np.log(c.values.astype(float))
    out = np.full(len(y), np.nan)
    if len(y) >= n:
        W = np.lib.stride_tricks.sliding_window_view(y, n)
        x = np.arange(n) - (n - 1) / P['n_bahagi_2']
        sxx = (x ** P['x_kuasa_2']).sum()
        ym = W.mean(axis=1, keepdims=True)
        d = W - ym
        b = (d * x).sum(axis=1) / sxx
        sst = (d ** P['d_kuasa_2']).sum(axis=1)
        ssr = b ** P['b_kuasa_2'] * sxx
        r2 = np.where(sst > 0, ssr / sst, 0.0)
        out[n - 1:] = (np.exp(b * P['b_kali_252']) - 1) * r2
    return pd.Series(out, c.index)

def _hari_r(dates, *, P=PARAM):
    d = pd.DatetimeIndex(sorted(dates))
    rab = d - pd.to_timedelta((d.weekday - P['weekday_tolak_2']) % P['weekday_mod_7'], unit='D')
    rab = rab.where(d.weekday >= P['weekday_ambang_2'], d + pd.to_timedelta(P['weekday_tolak_2'] - d.weekday, unit='D'))
    s = pd.Series(d, index=d)
    out = s[d >= rab].groupby(rab[d >= rab]).min()
    return pd.DatetimeIndex(out.values)

def _keluar(g, i, sp, ex, *, P=PARAM):
    o, l = (g.open.values, g.low.values)
    n = len(g)
    j = i + 1
    while j < n:
        if j > i + 1 and o[j] <= sp:
            return j
        if l[j] <= sp:
            return j
        if ex[j] and j + 1 < n:
            return j + 1
        j += 1
    return n - 1

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_slot = P['slot']
    _p_skor_90 = P['skor_90']
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_rolling_100 = P['rolling_100']
    _p_rma_atr_20 = P['rma_atr_20']
    _p_rolling_90 = P['rolling_90']
    _p_loc_kali_0_2 = P['loc_kali_0_2']
    _p_c_ambang_0_15 = P['c_ambang_0_15']
    sk = {}
    lay = {}
    st = {}
    for t, g in fr.items():
        c = g.close
        sk[t] = _skor(c, n=_p_skor_90, P=P)
        jur = (c.pct_change().abs() >= _p_c_ambang_0_15).astype(float).rolling(_p_rolling_90, min_periods=1).max().astype(bool)
        s100 = c.rolling(_p_rolling_100).mean()
        lay[t] = (c > s100) & ~jur
        st[t] = c - _p_rma_atr_kali_3 * _rma_atr(g, _p_rma_atr_20, P=P)
        g['_skor'] = sk[t]
        g['_lay'] = lay[t]
        g['_s100'] = s100
    SK = pd.DataFrame(sk)
    LY = pd.DataFrame(lay).fillna(False).astype(bool)
    ST = pd.DataFrame(st)
    RK = SK.rank(axis=1, ascending=False, method='first')
    NB = SK.notna().sum(axis=1)
    TOP = RK.le(np.floor(P['nb_kali_0_2'] * NB), axis=0)
    hr = _hari_r(SK.index, P=P)
    hrset = set(hr)
    EX = ~TOP | ~LY
    for t, g in fr.items():
        m = g.index.isin(hr)
        g['exitc'] = pd.Series(m, g.index) & EX[t].reindex(g.index).fillna(True)
    pos = {t: {d: i for i, d in enumerate(g.index)} for t, g in fr.items()}
    sig = {t: np.zeros(len(g), bool) for t, g in fr.items()}
    pegang = {}
    keluar_hari = {}
    for d in hr:
        nx = SK.index[SK.index.get_loc(d) + 1] if SK.index.get_loc(d) + 1 < len(SK.index) else None
        if nx is not None and nx < START:
            continue
        for t, x in list(pegang.items()):
            if nx is not None and x <= nx:
                keluar_hari[t] = x
                del pegang[t]
        kosong = _p_slot - len(pegang)
        if kosong <= 0:
            continue
        cal = SK.loc[d][TOP.loc[d] & LY.loc[d]].dropna().sort_values(ascending=False).index
        for t in cal:
            if kosong <= 0:
                break
            if t in pegang or keluar_hari.get(t) == nx or d not in pos[t]:
                continue
            g = fr[t]
            i = pos[t][d]
            if i < WARM:
                continue
            sp = ST.at[d, t]
            kosong -= 1
            if i + 1 < len(g) and g.open.values[i + 1] <= sp:
                continue
            sig[t][i] = True
            pegang[t] = g.index[_keluar(g, i, sp, g['exitc'].values, P=P)] if i + 1 < len(g) else pd.Timestamp.max
    dl = SK.index[-1]
    for t, g in fr.items():
        g['sig'] = sig[t]
        g['stop'] = ST[t].reindex(g.index)
        g['tgt'] = np.nan
        g['rank'] = g['_skor']
        g.attrs['_m40'] = dict(hr=dl in hrset, top=bool(TOP.at[dl, t]) if t in TOP else False, kd=int(RK.at[dl, t]) if not np.isnan(RK.at[dl, t]) else None, k=int(np.floor(_p_loc_kali_0_2 * NB.loc[dl])), pegang=t in pegang, slot_kosong=_p_slot - len(pegang))
    masih = {t for t, x in pegang.items() if x >= dl}
    calx = [t for t in SK.loc[dl][TOP.loc[dl] & LY.loc[dl]].dropna().sort_values(ascending=False).index if t not in masih and dl in pos[t] and (pos[t][dl] >= WARM)]
    for t, g in fr.items():
        g.attrs['_m40'].update(urutan=calx.index(t) + 1 if t in calx else None, kosong2=_p_slot - len(masih), masih=t in masih)

def _hari_ke_R(d):
    """Bilangan hari dagangan (hari bekerja; Andaian saya: cuti umum diabaikan) dari d ke hari R seterusnya (Rabu, > d)."""
    k = 0
    x = d
    while True:
        x = x + pd.offsets.BDay(1)
        k += 1
        if x.weekday() == 2:
            return k
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'skor_90': ('int', 45, 180),
    'rma_atr_kali_3': ('float', 1.5, 4.5),
    'nb_kali_0_2': ('float', 0.1, 0.3),
    'rma_atr_20': ('int', 10, 40),
    'rolling_90': ('int', 45, 180),
    'loc_kali_0_2': ('float', 0.1, 0.3),
    'c_ambang_0_15': ('float', 0.075, 0.225),
}
TALA = ['skor_90', 'rma_atr_kali_3', 'nb_kali_0_2', 'rma_atr_20', 'rolling_90', 'c_ambang_0_15']

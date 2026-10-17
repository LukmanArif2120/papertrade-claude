# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M38.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'weekday_ambang_4': 4,
    'n_sah': 3,
    'rolling_52': 52,
    'shift_63': 63,
}
ID = 'M38'
NAMA = 'Darvas Kotak'
VARIAN = 'V4 V1 atas bar mingguan'
TMAX = None
WARM = 265
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280
N_SAH = 3

def _minggu(g, *, P=PARAM):
    """Bar mingguan Isnin-Jumaat daripada data harian; tarikh = hari dagangan terakhir minggu itu."""
    k = g.index.to_period('W-FRI')
    w = pd.DataFrame({'high': g.high.groupby(k).max(), 'low': g.low.groupby(k).min(), 'close': g.close.groupby(k).last(), 'tarikh': pd.Series(g.index, index=g.index).groupby(k).last()})
    return w.reset_index(drop=True)

def _mesin(w, *, P=PARAM):
    """Mesin keadaan A/B/C atas bar mingguan. Pulangkan senarai isyarat (indeks minggu, T, B),
    senarai kotak siap (indeks minggu, B), dan keadaan akhir."""
    _p_n_sah = P['n_sah']
    h, l, c = (w.high.values, w.low.values, w.close.values)
    n = len(w)
    h52 = pd.Series(h).rolling(P['rolling_52']).max().shift(1).values
    st = 'IDLE'
    T = B = np.nan
    cnt = 0
    sig = []
    kotak = []
    for k in range(n):
        if st == 'IDLE':
            if not np.isnan(h52[k]) and h[k] > h52[k]:
                st, T, cnt = ('A', h[k], 0)
            continue
        if st == 'A':
            if h[k] > T:
                T, cnt = (h[k], 0)
            else:
                cnt += 1
                if cnt == _p_n_sah:
                    st, B, cnt = ('B0', np.nan, 0)
            continue
        if st == 'B0':
            if h[k] > T:
                st, T, cnt = ('A', h[k], 0)
            else:
                st, B, cnt = ('B', l[k], 0)
            continue
        if st == 'B':
            if h[k] > T:
                st, T, cnt = ('A', h[k], 0)
            elif l[k] < B:
                B, cnt = (l[k], 0)
            else:
                cnt += 1
                if cnt == _p_n_sah:
                    st = 'C'
                    kotak.append((k, B))
            continue
        if st == 'C':
            if c[k] > T:
                sig.append((k, T, B))
                st, T, cnt = ('A', h[k], 0)
            elif c[k] < B:
                st = 'IDLE'
                T = B = np.nan
    return (sig, kotak, dict(st=st, T=T, B=B, cnt=cnt))

def _isi(g, *, P=PARAM):
    w = _minggu(g, P=P)
    sigs, kotak, akhir = _mesin(w, P=P)
    ix = g.index
    n = len(g)
    pos = {d: i for i, d in enumerate(ix)}
    o, hi, lo = (g.open.values, g.high.values, g.low.values)
    wk_end = np.zeros(n, bool)
    wclose = np.full(n, np.nan)
    for d, cc in zip(w.tarikh, w.close):
        wk_end[pos[d]] = True
        wclose[pos[d]] = cc
    kotak_d = [(pos[w.tarikh[k]], b) for k, b in kotak]
    sig = np.zeros(n, bool)
    stop = np.full(n, np.nan)
    exitc = np.zeros(n, bool)
    raw = {pos[w.tarikh[k]]: B for k, T, B in sigs}
    for i, B in raw.items():
        stop[i] = B
    i = WARM
    while i < n - 1:
        if i not in raw or o[i + 1] <= raw[i]:
            i += 1
            continue
        sig[i] = True
        sp = raw[i]
        bs = sp
        j = i + 1
        kk = [x for x in kotak_d if x[0] > i]
        q = 0
        keluar = None
        while j < n:
            while q < len(kk) and kk[q][0] <= j:
                bs = max(bs, kk[q][1])
                q += 1
            ex = wk_end[j] and wclose[j] < bs
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
    if n - 1 in raw and n - 1 >= WARM and (ix[-1].weekday() == P['weekday_ambang_4']):
        sig[n - 1] = True
    return (sig, stop, exitc, w, akhir)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        sig, stop, exitc, w, akhir = _isi(g, P=P)
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = exitc
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
        g.attrs['_m38'] = akhir
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'n_sah': ('int', 2, 6),
    'rolling_52': ('int', 26, 104),
    'shift_63': ('int', 32, 126),
}
TALA = ['n_sah', 'rolling_52']

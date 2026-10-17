# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M26.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'j_tambah_11': 11,
    'l_kali_0_99': 0.99,
    'pivot_k_3': 3,
    'range_10': 10,
    'atrw_14': 14,
    'len_ambang_2': 2,
    'j_tolak_3': 3,
    'a_kali_0_25': 0.25,
    'l_tolak_1em12': 1e-12,
    'nilai_2': 2,
    'shift_63': 63,
}
ID = 'M26'
NAMA = 'Garis Trend Undur 3 Sentuhan + Pecahan'
VARIAN = 'V0 Sumber tulen (henti 0.99x low kotak, sasaran swing high kiri)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
COST = 0.001

def _atrw(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean().values

def _pivot(a, k, fn, *, P=PARAM):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]):
            p[t] = True
    return np.where(p)[0]
OPS = {'badan_sentuh': False, 'jauh_awal': True, 'win': 251}

def _sentuhan(g, mod=0, *, P=PARAM):
    """Senarai sentuhan j -> (a, b). Ikut Kad M26 seksyen 9."""
    _p_range_10 = P['range_10']
    _p_len_ambang_2 = P['len_ambang_2']
    _p_j_tolak_3 = P['j_tolak_3']
    _p_a_kali_0_25 = P['a_kali_0_25']
    _p_l_tolak_1em12 = P['l_tolak_1em12']
    _p_nilai_2 = P['nilai_2']
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g)
    A = _atrw(g, n=P['atrw_14'], P=P)
    blo = np.minimum(O, C)
    pl = _pivot(L, P['pivot_k_3'], np.min, P=P)
    ph = _pivot(H, P['pivot_k_3'], np.max, P=P)
    out = {}
    cache_b = -1
    cache = {}
    for j in range(_p_range_10, n):
        pv = pl[(pl <= j - _p_j_tolak_3) & (pl >= j - OPS['win'])]
        if len(pv) < _p_len_ambang_2:
            continue
        b = pv[-1]
        if b != cache_b:
            cache_b = b
            cache = {}
        a_ok = -1
        for a in pv[:-1][::-1]:
            if L[a] >= L[b]:
                continue
            st_ = cache.get(a)
            if st_ is None:
                t = np.arange(a, j + 1)
                v = bool(np.all(blo[a:j + 1] >= L[a] + (L[b] - L[a]) * (t - a) / (b - a) - _p_l_tolak_1em12))
            elif st_[1] is False:
                v = False
            else:
                lo = st_[0] + 1
                t = np.arange(lo, j + 1)
                v = bool(np.all(blo[lo:j + 1] >= L[a] + (L[b] - L[a]) * (t - a) / (b - a) - _p_l_tolak_1em12))
            cache[a] = (j, v)
            if v:
                a_ok = a
                break
        if a_ok < 0:
            continue
        a = a_ok
        hv = ph[(ph <= j - _p_j_tolak_3) & (ph >= j - OPS['win'])]
        if len(hv) < _p_len_ambang_2 or not H[hv[-1]] > H[hv[-_p_nilai_2]]:
            continue
        Lf = lambda t: L[a] + (L[b] - L[a]) * (t - a) / (b - a)
        if not L[j] <= Lf(j) + _p_a_kali_0_25 * A[j]:
            continue
        if OPS['badan_sentuh'] and blo[j] < Lf(j):
            continue
        tt = np.arange(b + 1, j)
        if len(tt) == 0:
            continue
        jauh = L[tt] > Lf(tt) + A[tt]
        if not jauh.any():
            continue
        tm = tt[np.where(jauh)[0][0 if OPS['jauh_awal'] else -1]]
        uu = np.arange(tm + 1, j)
        if len(uu) and np.any((L[uu] <= Lf(uu) + _p_a_kali_0_25 * A[uu]) & (blo[uu] >= Lf(uu) if OPS['badan_sentuh'] else True)):
            continue
        out[j] = (a, b)
    return out

def _isyarat(g, *, P=PARAM):
    _p_j_tambah_11 = P['j_tambah_11']
    _p_l_kali_0_99 = P['l_kali_0_99']
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g)
    blo = np.minimum(O, C)
    sen = _sentuhan(g, P=P)
    sig = np.zeros(n, bool)
    st = np.full(n, np.nan)
    tg = np.full(n, np.nan)
    jsig = np.full(n, -1)
    for j, (a, b) in sen.items():
        Lf = lambda t: L[a] + (L[b] - L[a]) * (t - a) / (b - a)
        if blo[j] < Lf(j):
            continue
        for i in range(j + 1, min(j + _p_j_tambah_11, n)):
            if blo[i] < Lf(i):
                break
            if C[i] > H[j:i].max():
                if jsig[i] < j:
                    sig[i] = True
                    jsig[i] = j
                    st[i] = _p_l_kali_0_99 * L[j:i + 1].min()
                    t_ = H[b:j + 1].max()
                    tg[i] = t_ if t_ > C[i] else np.nan
                break
    return (sig, st, tg, sen)

def _isi_tgt(g, sig, st, tgs, warm, *, P=PARAM):
    """Isi lajur tgt mengikut dagangan, meniru urutan enjin.trades() (enjin tidak diubah)."""
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g)
    tgt = np.full(n, np.nan)
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        tv = tgs[i]
        j = i + 1
        while j < n:
            tgt[j - 1] = tv
            if j > i + 1 and O[j] <= sp:
                break
            if L[j] <= sp:
                break
            if not np.isnan(tv):
                if j > i + 1 and O[j] >= tv:
                    break
                if j > i + 1 and H[j] >= tv:
                    break
            j += 1
        if j >= n:
            j = n - 1
        i = j + 1
    return tgt

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        sig, st, tgs, sen = _isyarat(g, P=P)
        on = g.open.shift(-1).values
        sig = sig & ~(on <= st)
        g['sig'] = sig
        g['stop'] = st
        g['tgt'] = _isi_tgt(g, sig, st, tgs, WARM, P=P)
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
        g.attrs['_sen'] = sen
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'l_kali_0_99': ('float', 0.495, 0.99),
    'pivot_k_3': ('int', 2, 6),
    'atrw_14': ('int', 7, 28),
    'shift_63': ('int', 32, 126),
}
TALA = ['pivot_k_3', 'l_kali_0_99', 'atrw_14']

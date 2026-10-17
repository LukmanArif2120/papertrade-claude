# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M13.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'win': 252,
    'k': 3,
    'len_ambang_2': 2,
    'nilai_2': 2,
    'shift_63': 63,
}
ID = 'M13'
NAMA = 'Garis Trend Action/Safety Line'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
K = 3
WIN = 252

def _pivot(a, k, fn, *, P=PARAM):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]):
            p[t] = True
    return np.where(p)[0]

def _garis(Y, piv, upper, *, P=PARAM):
    """Untuk setiap hari i: segmen terakhir kulit cembung (atas jika upper) atas bar [m, P],
    m = indeks ekstrem tetingkap (pertama jika seri), P = pivot disahkan terakhir (P <= i-K, P >= w0).
    Andaian saya (ikut laporan M13): tetingkap dipendekkan ke mula data bila sejarah < 252 hari.
    Pulang nilai garis pada i, indeks B, dan nilai ekstrem tetingkap (untuk garis naik mendatar)."""
    _p_win = P['win']
    _p_k = P['k']
    _p_len_ambang_2 = P['len_ambang_2']
    _p_nilai_2 = P['nilai_2']
    n = len(Y)
    val = np.full(n, np.nan)
    Bi = np.full(n, -1)
    ext = np.full(n, np.nan)
    nxt = np.full(n, np.nan)
    st = []
    cur_m = -1
    cur_P = -1
    pj = 0
    lastp = -1
    for i in range(n):
        w0 = max(0, i - _p_win + 1)
        seg = Y[w0:i + 1]
        m = w0 + (int(np.argmax(seg)) if upper else int(np.argmin(seg)))
        ext[i] = Y[m]
        while pj < len(piv) and piv[pj] <= i - _p_k:
            lastp = piv[pj]
            pj += 1
        if lastp < w0 or lastp <= m:
            continue
        P_ = lastp
        if m != cur_m or P_ < cur_P:
            st = []
            cur_m = m
            cur_P = m - 1
        for t in range(cur_P + 1, P_ + 1):
            y = Y[t]
            while len(st) >= _p_len_ambang_2:
                (t1, y1), (t2, y2) = (st[-_p_nilai_2], st[-1])
                cr = (t2 - t1) * (y - y1) - (y2 - y1) * (t - t1)
                if upper and cr >= 0 or (not upper and cr <= 0):
                    st.pop()
                else:
                    break
            st.append((t, y))
        cur_P = P_
        (A, ya), (B, yb) = (st[-_p_nilai_2], st[-1])
        val[i] = ya + (yb - ya) * (i - A) / (B - A)
        Bi[i] = B
        nxt[i] = ya + (yb - ya) * (i + 1 - A) / (B - A)
    _garis.nxt = nxt
    return (val, Bi, ext)

def _kira(g, *, P=PARAM):
    H, L, C = (g.high.values.astype(float), g.low.values.astype(float), g.close.values.astype(float))
    D, Bd, _ = _garis(H, _pivot(H, P['k'], np.max, P=P), True, P=P)
    _kira.Dn = _garis.nxt
    U, _, lmin = _garis(L, _pivot(L, P['k'], np.min, P=P), False, P=P)
    U = np.where(np.isnan(U), lmin, U)
    n = len(C)
    sg = np.zeros(n, bool)
    pecah = set()
    for i in range(n):
        if np.isnan(D[i]) or C[i] <= D[i]:
            continue
        if Bd[i] not in pecah:
            sg[i] = True
        pecah.add(Bd[i])
    return (sg, D, Bd, U, pecah)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        sg, D, Bd, U, pecah = _kira(g, P=P)
        stop = pd.Series(U, g.index)
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)
        g['_Dn'] = _kira.Dn
        g['_D'] = D
        g['_Bd'] = Bd
        g['_U'] = U
        g['_dipecah'] = [b in pecah and b >= 0 for b in Bd]
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < stop
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

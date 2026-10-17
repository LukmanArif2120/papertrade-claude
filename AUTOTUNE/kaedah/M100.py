# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M100.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'w': 40,
    'p_w_tambah_63': 63,
    'i_tolak_4': 4,
    'nl3_ambang_2': 2,
    'np_ambang_2': 2,
    'np_ambang_5': 5,
    'i_tolak_63': 63,
    'b_kali_1_03': 1.03,
    'rolling_7': 7,
    'np_ambang_3': 3,
    'nl4_ambang_2': 2,
    'nl4_ambang_3': 3,
    't_kali_0_98': 0.98,
    'shift_63': 63,
}
ID = 'M100'
NAMA = 'Bulkowski Segi Empat & Segi Tiga Menaik'
VARIAN = 'V0 Sumber tulen (proksi): sasaran T+tinggi, tiada exitc'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320
W = 40

def _corak(g, W=W, *, P=PARAM):
    """Pulangkan siri per hari i: T, B, SEGI4, SEGI3, LT, NP, NL3/NL4 (tetingkap i-W..i-1; pangsi k+3<=i-1)."""
    _p_w = P['w']
    _p_p_w_tambah_63 = P['p_w_tambah_63']
    _p_i_tolak_4 = P['i_tolak_4']
    _p_nl3_ambang_2 = P['nl3_ambang_2']
    _p_np_ambang_2 = P['np_ambang_2']
    _p_np_ambang_5 = P['np_ambang_5']
    _p_i_tolak_63 = P['i_tolak_63']
    _p_b_kali_1_03 = P['b_kali_1_03']
    _p_np_ambang_3 = P['np_ambang_3']
    _p_nl4_ambang_2 = P['nl4_ambang_2']
    _p_nl4_ambang_3 = P['nl4_ambang_3']
    _p_t_kali_0_98 = P['t_kali_0_98']
    h = g.high.values.astype(float)
    l = g.low.values.astype(float)
    c = g.close.values.astype(float)
    n = len(g)
    ph = (g.high == g.high.rolling(P['rolling_7'], center=True).max()).values
    pl = (g.low == g.low.rolling(P['rolling_7'], center=True).min()).values
    T = g.high.rolling(P['w']).max().shift(1).values
    B = g.low.rolling(P['w']).min().shift(1).values
    s4 = np.zeros(n, bool)
    s3 = np.zeros(n, bool)
    LT = np.full(n, np.nan)
    np_ = np.zeros(n, int)
    nl4 = np.zeros(n, int)
    nl3 = np.zeros(n, int)
    naik = np.zeros(n, bool)
    for i in range(_p_w + _p_p_w_tambah_63, n):
        a, b = (i - _p_w, i - _p_i_tolak_4)
        if b < a or np.isnan(T[i]):
            continue
        kh = np.nonzero(ph[a:b + 1])[0] + a
        kl = np.nonzero(pl[a:b + 1])[0] + a
        NP = int((h[kh] >= _p_t_kali_0_98 * T[i]).sum())
        NL4 = int((l[kl] <= _p_b_kali_1_03 * B[i]).sum())
        np_[i] = NP
        nl4[i] = NL4
        if len(kl):
            LT[i] = l[kl[-1]]
        tr = c[i - _p_w] > c[i - _p_w - _p_i_tolak_63]
        s4[i] = (NP >= _p_np_ambang_3 and NL4 >= _p_nl4_ambang_2 or (NP >= _p_np_ambang_2 and NL4 >= _p_nl4_ambang_3)) and tr
        NL3 = len(kl)
        nl3[i] = NL3
        mnk = NL3 >= _p_nl3_ambang_2 and bool(np.all(np.diff(l[kl]) > 0))
        naik[i] = mnk
        s3[i] = NP >= _p_np_ambang_2 and mnk and (NP + NL3 >= _p_np_ambang_5) and (l[kl[-1]] >= B[i] * _p_b_kali_1_03)
    idx = g.index
    return (pd.Series(T, idx), pd.Series(B, idx), pd.Series(s4, idx), pd.Series(s3, idx), pd.Series(LT, idx), pd.Series(np_, idx), pd.Series(nl4, idx), pd.Series(nl3, idx), pd.Series(naik, idx))

def _kunci_tgt(g, sig, st, tg0, warm=WARM, *, P=PARAM):
    o, h, l = (g.open.values, g.high.values, g.low.values)
    n = len(g)
    tg = pd.Series(tg0, g.index).where(pd.Series(sig, g.index)).ffill().values.copy()
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        t = tg0[i]
        j = i + 1
        while j < n:
            tg[j - 1] = t
            if j > i + 1 and o[j] <= sp:
                break
            if l[j] <= sp:
                break
            if not np.isnan(t) and (j > i + 1 and o[j] >= t or h[j] >= t):
                break
            j += 1
        if j < n:
            tg[j] = t
        i = j + 1
    return tg

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_w = P['w']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        T, B, s4, s3, LT, NP, NL4, NL3, naik = _corak(g, W=_p_w, P=P)
        pecah = (g.close > T) & (g.close.shift(1) <= T.shift(1))
        sig = pecah & (s4 | s3)
        langkau = (g.open.shift(-1) <= LT).fillna(False)
        sig = sig & ~langkau
        g['_T'] = T
        g['_B'] = B
        g['_s4'] = s4
        g['_s3'] = s3
        g['_NP'] = NP
        g['_NL4'] = NL4
        g['_NL3'] = NL3
        g['_naik'] = naik
        g['sig'] = sig
        g['stop'] = LT
        g['tgt'] = _kunci_tgt(g, sig.values, LT.values, (T + (T - B)).values, P=P)
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}

def _corak_esok(g, W=W):
    """Nilai corak untuk hari ESOK (i = n), logik sama seperti _corak (tetingkap n-W..n-1; pangsi k+3 <= n-1)."""
    h = g.high.values.astype(float)
    l = g.low.values.astype(float)
    c = g.close.values.astype(float)
    n = len(g)
    i = n
    if i < W + 63:
        return None
    ph = (g.high == g.high.rolling(7, center=True).max()).values
    pl = (g.low == g.low.rolling(7, center=True).min()).values
    T = h[i - W:i].max()
    B = l[i - W:i].min()
    a, b = (i - W, i - 4)
    kh = np.nonzero(ph[a:b + 1])[0] + a
    kl = np.nonzero(pl[a:b + 1])[0] + a
    NP = int((h[kh] >= 0.98 * T).sum())
    NL4 = int((l[kl] <= 1.03 * B).sum())
    tr = c[i - W] > c[i - W - 63]
    s4 = (NP >= 3 and NL4 >= 2 or (NP >= 2 and NL4 >= 3)) and tr
    NL3 = len(kl)
    mnk = NL3 >= 2 and bool(np.all(np.diff(l[kl]) > 0))
    s3 = NP >= 2 and mnk and (NP + NL3 >= 5) and (l[kl[-1]] >= B * 1.03)
    LT = l[kl[-1]] if len(kl) else np.nan
    return dict(T=T, B=B, s4=s4, s3=s3, NP=NP, NL4=NL4, NL3=NL3, LT=LT)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []

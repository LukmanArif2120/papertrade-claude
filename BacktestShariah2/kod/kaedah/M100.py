from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M100'
NAMA = 'Bulkowski Segi Empat & Segi Tiga Menaik'
VARIAN = 'V0 Sumber tulen (proksi): sasaran T+tinggi, tiada exitc'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320
W = 40


def _corak(g, W=W):
    """Pulangkan siri per hari i: T, B, SEGI4, SEGI3, LT, NP, NL3/NL4 (tetingkap i-W..i-1; pangsi k+3<=i-1)."""
    h = g.high.values.astype(float); l = g.low.values.astype(float); c = g.close.values.astype(float)
    n = len(g)
    ph = (g.high == g.high.rolling(7, center=True).max()).values
    pl = (g.low == g.low.rolling(7, center=True).min()).values
    T = g.high.rolling(W).max().shift(1).values
    B = g.low.rolling(W).min().shift(1).values
    s4 = np.zeros(n, bool); s3 = np.zeros(n, bool); LT = np.full(n, np.nan)
    np_ = np.zeros(n, int); nl4 = np.zeros(n, int); nl3 = np.zeros(n, int); naik = np.zeros(n, bool)
    for i in range(W + 63, n):
        a, b = i - W, i - 4          # k dalam [i-W, i-4]
        if b < a or np.isnan(T[i]):
            continue
        kh = np.nonzero(ph[a:b + 1])[0] + a
        kl = np.nonzero(pl[a:b + 1])[0] + a
        NP = int((h[kh] >= 0.98 * T[i]).sum())
        NL4 = int((l[kl] <= 1.03 * B[i]).sum())
        np_[i] = NP; nl4[i] = NL4
        if len(kl):
            LT[i] = l[kl[-1]]
        tr = c[i - W] > c[i - W - 63]
        s4[i] = ((NP >= 3 and NL4 >= 2) or (NP >= 2 and NL4 >= 3)) and tr
        NL3 = len(kl); nl3[i] = NL3
        mnk = NL3 >= 2 and bool(np.all(np.diff(l[kl]) > 0))
        naik[i] = mnk
        s3[i] = NP >= 2 and mnk and NP + NL3 >= 5 and l[kl[-1]] >= B[i] * 1.03
    idx = g.index
    return (pd.Series(T, idx), pd.Series(B, idx), pd.Series(s4, idx), pd.Series(s3, idx), pd.Series(LT, idx),
            pd.Series(np_, idx), pd.Series(nl4, idx), pd.Series(nl3, idx), pd.Series(naik, idx))


def _kunci_tgt(g, sig, st, tg0, warm=WARM):
    # Andaian (laporan M100 #3): sasaran dikunci pada nilai hari isyarat sepanjang dagangan.
    # Jalan dagangan sama seperti enjin supaya isyarat baharu semasa pegangan tidak mengubah sasaran.
    o, h, l = g.open.values, g.high.values, g.low.values
    n = len(g); tg = pd.Series(tg0, g.index).where(pd.Series(sig, g.index)).ffill().values.copy()
    i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf; t = tg0[i]
        j = i + 1
        while j < n:
            tg[j - 1] = t
            if j > i + 1 and o[j] <= sp: break
            if l[j] <= sp: break
            if not np.isnan(t) and ((j > i + 1 and o[j] >= t) or h[j] >= t): break
            j += 1
        if j < n: tg[j] = t
        i = j + 1
    return tg


def sedia(fr, idx):
    for g in fr.values():
        T, B, s4, s3, LT, NP, NL4, NL3, naik = _corak(g)
        pecah = (g.close > T) & (g.close.shift(1) <= T.shift(1))
        sig = pecah & (s4 | s3)
        # Kad: masuk dilangkau jika buka masuk <= stop
        langkau = (g.open.shift(-1) <= LT).fillna(False)
        sig = sig & ~langkau
        g['_T'] = T; g['_B'] = B; g['_s4'] = s4; g['_s3'] = s3; g['_NP'] = NP; g['_NL4'] = NL4; g['_NL3'] = NL3; g['_naik'] = naik
        g['sig'] = sig
        g['stop'] = LT
        # Andaian (laporan): sasaran T+(T-B) dikunci pada hari isyarat, ffill
        g['tgt'] = _kunci_tgt(g, sig.values, LT.values, (T + (T - B)).values)
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def _corak_esok(g, W=W):
    """Nilai corak untuk hari ESOK (i = n), logik sama seperti _corak (tetingkap n-W..n-1; pangsi k+3 <= n-1)."""
    h = g.high.values.astype(float); l = g.low.values.astype(float); c = g.close.values.astype(float)
    n = len(g); i = n
    if i < W + 63:
        return None
    ph = (g.high == g.high.rolling(7, center=True).max()).values
    pl = (g.low == g.low.rolling(7, center=True).min()).values
    T = h[i - W:i].max(); B = l[i - W:i].min()
    a, b = i - W, i - 4
    kh = np.nonzero(ph[a:b + 1])[0] + a
    kl = np.nonzero(pl[a:b + 1])[0] + a
    NP = int((h[kh] >= 0.98 * T).sum()); NL4 = int((l[kl] <= 1.03 * B).sum())
    tr = c[i - W] > c[i - W - 63]
    s4 = ((NP >= 3 and NL4 >= 2) or (NP >= 2 and NL4 >= 3)) and tr
    NL3 = len(kl)
    mnk = NL3 >= 2 and bool(np.all(np.diff(l[kl]) > 0))
    s3 = NP >= 2 and mnk and NP + NL3 >= 5 and l[kl[-1]] >= B * 1.03
    LT = l[kl[-1]] if len(kl) else np.nan
    return dict(T=T, B=B, s4=s4, s3=s3, NP=NP, NL4=NL4, NL3=NL3, LT=LT)


def hampir(g, idx):
    # Syarat entry V0 (3): (1) corak segi empat ATAU segi tiga menaik sah dalam tetingkap 40 hari esok;
    # (2) tutup hari ini <= paras atas hari ini (pecahan kali pertama); (3) PENCETUS: tutup esok > paras atas T (high tertinggi 40 hari)
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._T):
        return None
    if not (r.close <= r._T):                                 # syarat 2
        return None
    k = _corak_esok(g)
    if k is None or not (k['s4'] or k['s3']):                 # syarat 1
        return None
    paras = k['T']
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    jenis = 'segi empat' if k['s4'] else 'segi tiga menaik'
    tgt = paras + (paras - k['B'])
    return _hasil(f'Corak {jenis} sah dalam 40 hari ({k["NP"]} puncak pada paras rata); tutup hari ini belum melepasi paras atas',
                  f'Tutup esok > {paras:.2f} (high tertinggi 40 hari). Sasaran {tgt:.2f}; henti {k["LT"]:.2f} (lembah pangsi terakhir); '
                  f'masuk dibatalkan jika harga buka hari masuk <= henti',
                  'Pecah rintangan rata (tutup > T)', paras, jarak, 2, 3)

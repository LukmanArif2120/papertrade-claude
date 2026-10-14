from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M26'
NAMA = 'Garis Trend Undur 3 Sentuhan + Pecahan'
VARIAN = 'V0 Sumber tulen (henti 0.99x low kotak, sasaran swing high kiri)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
COST = 0.001


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean().values


def _pivot(a, k, fn):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]): p[t] = True
    return np.where(p)[0]


# Andaian saya (dipadankan dengan registry, 8164 sentuhan = laporan): j = sentuhan pertama selepas hari
# 'menjauh' PERTAMA sejak b; sentuhan hanya disemak pada low (badan disemak pada pencetus).
OPS = {'badan_sentuh': False, 'jauh_awal': True, 'win': 251}


def _sentuhan(g, mod=0):
    """Senarai sentuhan j -> (a, b). Ikut Kad M26 seksyen 9."""
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g); A = _atrw(g); blo = np.minimum(O, C)
    pl = _pivot(L, 3, np.min); ph = _pivot(H, 3, np.max)
    out = {}; cache_b = -1; cache = {}
    for j in range(10, n):
        pv = pl[(pl <= j - 3) & (pl >= j - OPS['win'])]
        if len(pv) < 2: continue
        b = pv[-1]
        if b != cache_b: cache_b = b; cache = {}
        a_ok = -1
        for a in pv[:-1][::-1]:
            if L[a] >= L[b]: continue
            st_ = cache.get(a)
            if st_ is None:
                t = np.arange(a, j + 1); v = bool(np.all(blo[a:j + 1] >= L[a] + (L[b] - L[a]) * (t - a) / (b - a) - 1e-12))
            elif st_[1] is False: v = False
            else:
                lo = st_[0] + 1; t = np.arange(lo, j + 1)
                v = bool(np.all(blo[lo:j + 1] >= L[a] + (L[b] - L[a]) * (t - a) / (b - a) - 1e-12))
            cache[a] = (j, v)
            if v: a_ok = a; break
        if a_ok < 0: continue
        a = a_ok
        hv = ph[(ph <= j - 3) & (ph >= j - OPS['win'])]
        if len(hv) < 2 or not H[hv[-1]] > H[hv[-2]]: continue
        Lf = lambda t: L[a] + (L[b] - L[a]) * (t - a) / (b - a)
        if not L[j] <= Lf(j) + 0.25 * A[j]: continue
        if OPS['badan_sentuh'] and blo[j] < Lf(j): continue
        tt = np.arange(b + 1, j)
        if len(tt) == 0: continue
        jauh = L[tt] > Lf(tt) + A[tt]
        if not jauh.any(): continue
        tm = tt[np.where(jauh)[0][0 if OPS['jauh_awal'] else -1]]
        uu = np.arange(tm + 1, j)
        if len(uu) and np.any((L[uu] <= Lf(uu) + 0.25 * A[uu]) & ((blo[uu] >= Lf(uu)) if OPS['badan_sentuh'] else True)): continue
        out[j] = (a, b)
    return out


def _isyarat(g):
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g); blo = np.minimum(O, C)
    sen = _sentuhan(g)
    sig = np.zeros(n, bool); st = np.full(n, np.nan); tg = np.full(n, np.nan); jsig = np.full(n, -1)
    for j, (a, b) in sen.items():
        Lf = lambda t: L[a] + (L[b] - L[a]) * (t - a) / (b - a)
        if blo[j] < Lf(j): continue
        for i in range(j + 1, min(j + 11, n)):
            if blo[i] < Lf(i): break
            if C[i] > H[j:i].max():
                if jsig[i] < j:  # Andaian saya (backtest): beberapa sentuhan hari sama -> guna sentuhan terkini
                    sig[i] = True; jsig[i] = j
                    st[i] = 0.99 * L[j:i + 1].min()
                    t_ = H[b:j + 1].max()
                    tg[i] = t_ if t_ > C[i] else np.nan
                break
    return sig, st, tg, sen


def _isi_tgt(g, sig, st, tgs, warm):
    """Isi lajur tgt mengikut dagangan, meniru urutan enjin.trades() (enjin tidak diubah)."""
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g); tgt = np.full(n, np.nan); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf; tv = tgs[i]
        j = i + 1
        while j < n:
            tgt[j - 1] = tv
            if j > i + 1 and O[j] <= sp: break
            if L[j] <= sp: break
            if not np.isnan(tv):
                if j > i + 1 and O[j] >= tv: break
                if j > i + 1 and H[j] >= tv: break
            j += 1
        if j >= n: j = n - 1
        i = j + 1
    return tgt


def sedia(fr, idx):
    for g in fr.values():
        sig, st, tgs, sen = _isyarat(g)
        on = g.open.shift(-1).values
        sig = sig & ~(on <= st)                       # langkau buka masuk <= henti
        g['sig'] = sig
        g['stop'] = st
        g['tgt'] = _isi_tgt(g, sig, st, tgs, WARM)
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(63) - 1
        # untuk hampir(): sentuhan aktif dalam 10 hari tanpa pecahan
        g.attrs['_sen'] = sen


def hampir(g, idx):
    # Piawaian ketat: syarat entry V0 = (1) garis naik sah (a, b) dengan badan lilin di atas garis,
    # (2) dua swing high menaik, (3) harga menjauh >= 1 ATR dari garis, (4) sentuhan j dalam 10 hari
    # (esok <= j+10), (5) badan lilin kekal atas garis sejak j dan tiada pecahan sebelum ini,
    # (6) PENCETUS: tutup > high kotak (max high j..hari ini).
    r = g.iloc[-1]
    if bool(r.sig): return None
    sen = g.attrs.get('_sen')
    if sen is None: sen = _sentuhan(g)
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g); blo = np.minimum(O, C)
    for j in sorted(sen, reverse=True):
        if j < n - 10: break                      # esok (indeks n) mesti <= j + 10
        a, b = sen[j]
        Lf = lambda t: L[a] + (L[b] - L[a]) * (t - a) / (b - a)
        tt = np.arange(j, n)
        if np.any(blo[tt] < Lf(tt)): continue
        if any(C[i] > H[j:i].max() for i in range(j + 1, n)): continue   # pecahan sudah berlaku
        kotak = H[j:n].max()
        jarak = (kotak - C[-1]) / C[-1] * 100
        # Andaian saya: jarak = 0 (tutup = high kotak) masih belum isyarat (perlu tutup > kotak), maka diterima
        if not (0 <= jarak <= 2.0): return None
        return {'sebab': f'Garis trend naik sah (badan lilin di atas garis); swing high menaik; harga pernah menjauh >= 1 ATR; sentuhan semula {n-1-j} hari lalu; badan kekal atas garis ({Lf(n-1):.2f}) tanpa pecahan',
                'syarat_beli': f'Tutup esok > {kotak:.2f} (high kotak sejak sentuhan) dan badan lilin esok >= {Lf(n):.2f} (garis); tetingkap tinggal {10-(n-1-j)} hari; henti 0.99 x {L[j:n].min():.2f}',
                'pencetus': 'tutup > high kotak', 'paras': round(float(kotak), 4), 'jarak_pct': round(jarak, 2),
                'syarat_dipenuhi': '5/6', 'skor': round(1 - jarak / 2, 3)}
    return None

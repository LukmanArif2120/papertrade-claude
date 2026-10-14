from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M27'
NAMA = 'Price Action 4 Tiang'
VARIAN = 'V2 Persediaan A sahaja (flip & hold)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 270


def _pivot(a, k, fn):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]): p[t] = True
    return np.where(p)[0]


def _flip(g):
    """Untuk setiap hari b: senarai paras L (harga PH dalam P(b), TOUCH>=2) dengan close[b-1] <= L < close[b]."""
    H, L, C = [g[k].values.astype(float) for k in ['high', 'low', 'close']]
    n = len(g); a14 = atr(g, 14).values
    ph = _pivot(H, 3, np.max); pl = _pivot(L, 3, np.min)
    pt = np.r_[ph, pl]; pp = np.r_[H[ph], L[pl]]; isph = np.r_[np.ones(len(ph), bool), np.zeros(len(pl), bool)]
    o = np.argsort(pt, kind='stable'); pt, pp, isph = pt[o], pp[o], isph[o]
    fl = {}
    for b in range(1, n):
        if np.isnan(a14[b]): continue
        lo, hi = C[b - 1], C[b]
        if not hi > lo: continue
        msk = (pt >= b - 250) & (pt <= b - 4)
        cand = pp[msk & isph]
        cand = cand[(cand >= lo) & (cand < hi)]
        if not len(cand): continue
        allp = pp[msk]
        ok = [v for v in cand if np.sum(np.abs(allp - v) <= 0.5 * a14[b]) >= 2]
        if ok: fl[b] = np.array(ok)
    return fl, a14


def sedia(fr, idx):
    qqq = idx['QQQ'].close
    for g in fr.values():
        O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
        n = len(g)
        q = qqq.reindex(g.index).ffill(); mkt = (q > q.rolling(50).mean()).values
        up = (g.close > g.close.shift()).values
        fl, a14 = _flip(g)
        sgA = np.zeros(n, bool); Ls = np.full(n, np.nan)
        hold = np.zeros(n, bool); Lh = np.full(n, np.nan)   # untuk hampir(): paras flip yang masih bertahan
        for i in range(5, n):
            best = np.nan; bh = np.nan
            for b in range(max(1, i - 15), i):
                if b not in fl: continue
                mn = C[b:i + 1].min()
                for Lv in fl[b]:
                    if mn > Lv:
                        if np.isnan(bh) or Lv > bh: bh = Lv
                        if L[i] <= Lv + 0.5 * a14[i] and C[i] > Lv and (np.isnan(best) or Lv > best): best = Lv
            if not np.isnan(bh): hold[i] = True; Lh[i] = bh
            ext = up[i - 4:i + 1].all()
            if not np.isnan(best) and mkt[i] and not ext:
                sgA[i] = True; Ls[i] = best
        stop = Ls - a14
        Lff = pd.Series(Ls).ffill().values           # Andaian saya (backtest): Lff ikut isyarat selepas penapis, sebelum langkau
        on = g.open.shift(-1).values
        sig = sgA & ~(on <= stop)
        s20 = g.close.rolling(20).mean().values
        # Untuk hampir(): paras flip yang sah untuk tetingkap ESOK (b dalam [i-14, i]) pada bar terakhir
        Le = np.nan; i = n - 1
        for b in range(max(1, i - 14), i + 1):
            if b not in fl: continue
            mn = C[b:i + 1].min()
            for Lv in fl[b]:
                if mn > Lv and (np.isnan(Le) or Lv > Le): Le = Lv
        g['_Le'] = np.r_[np.full(n - 1, np.nan), [Le]] if n else []
        g['_up4'] = pd.Series(up, g.index).rolling(4).sum().eq(4).values
        g['_hold'] = hold; g['_Lh'] = Lh; g['_mkt'] = mkt; g['_a14'] = a14
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (C < Lff) | (C < s20)
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Piawaian ketat: syarat entry V2 = (1) paras rintangan PH (>=2 sentuhan) dipecah tutup dalam 15 hari
    # (tetingkap esok: b dalam [hari ini-14, hari ini]), (2) tiada tutup <= paras sejak pecahan,
    # (3) QQQ > SMA50, (4) bukan 5 tutup naik berturut,
    # (5) PENCETUS uji semula: low <= paras + 0.5 x ATR14 dan tutup > paras.
    r = g.iloc[-1]
    if bool(r.sig) or pd.isna(r._Le) or not bool(r._mkt):
        return None
    Lv = float(r._Le); a = float(r._a14); c = float(r.close)
    zon = Lv + 0.5 * a      # Andaian saya: ATR14 esok dianggarkan = ATR14 hari ini
    # Pencetus ialah undur ke zon: jarak = (tutup - zon)/tutup x 100 (arah ke bawah)
    jarak = (c - zon) / c * 100
    # Andaian saya: tutup sudah dalam zon (jarak <= 0) -> jarak 0 (hanya perlu low esok <= zon dan tutup > paras)
    jarak = max(jarak, 0.0)
    if jarak > 2.0:
        return None
    ext = bool(r._up4)
    return {'sebab': f'Rintangan {Lv:.2f} (>=2 sentuhan) dipecah tutup dalam 15 hari dan bertahan (tiada tutup bawah paras); QQQ > SMA50' +
                     ('' if ext else '; belum 5 tutup naik berturut'),
            'syarat_beli': f'Esok: low <= {zon:.2f} (paras + 0.5xATR) dan tutup > {Lv:.2f}' +
                           (f'; tutup esok <= {c:.2f} (elak 5 tutup naik berturut)' if ext else '') +
                           f'; henti {Lv - a:.2f}',
            'pencetus': 'uji semula paras', 'paras': round(zon, 4), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '4/5', 'skor': round(1 - jarak / 2, 3)}

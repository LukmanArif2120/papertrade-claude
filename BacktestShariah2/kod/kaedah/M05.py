from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M05'
NAMA = 'MACD Divergence + Pengesahan'
VARIAN = 'V3 V1+close>SMA200'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 220


def _kira(g):
    h, l, c = g.high.values, g.low.values, g.close.values
    n = len(g)
    M = (g.close.ewm(span=12, adjust=False).mean() - g.close.ewm(span=26, adjust=False).mean()).values
    s200 = g.close.rolling(200).mean().values
    # pivot k=3; nilai sama dikira pivot (ikut kod finalis_v1)
    pl = np.array([t for t in range(3, n - 3) if l[t] == l[t - 3:t + 4].min()], dtype=int)
    ph = np.array([t for t in range(3, n - 3) if h[t] == h[t - 3:t + 4].max()], dtype=int)
    sg = np.zeros(n, bool); st = np.full(n, np.nan); rk = np.zeros(n); ex = np.zeros(n, bool)
    hv = np.full(n, np.nan); p2low = np.full(n, np.nan); divok = np.zeros(n, bool)
    for i in range(10, n):
        pv = pl[pl <= i - 3]
        if len(pv) >= 2:
            P1, P2 = pv[-2], pv[-1]
            if 5 <= P2 - P1 <= 40:
                Hh = h[P1:P2 + 1].max()
                if l[P2] < l[P1] and M[P2] > M[P1] and i - P2 <= 15 and l[P2 + 1:i + 1].min() > l[P2]:
                    divok[i] = True; hv[i] = Hh; p2low[i] = l[P2]
                    if c[i] > Hh and c[i - 1] <= Hh and c[i] > s200[i]:
                        sg[i] = True; st[i] = 0.99 * l[P2]; rk[i] = (M[P2] - M[P1]) / c[i]
        qv = ph[ph <= i - 3]
        if len(qv) >= 2:
            Q1, Q2 = qv[-2], qv[-1]
            if 5 <= Q2 - Q1 <= 40:
                Mm = l[Q1:Q2 + 1].min()
                if h[Q2] > h[Q1] and M[Q2] < M[Q1] and c[i] < Mm and c[i - 1] >= Mm and i - Q2 <= 15:
                    ex[i] = True
    return sg, st, rk, ex, divok, hv, p2low, s200


def sedia(fr, idx):
    for g in fr.values():
        sg, st, rk, ex, divok, hv, p2low, s200 = _kira(g)
        stop = pd.Series(st, g.index); bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())     # langkau jika buka_masuk <= henti
        g['_div'] = divok; g['_H'] = hv; g['_p2'] = p2low; g['_s200'] = s200
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ex
        g['rank'] = rk



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V3 (N=6), untuk bar esok i: [1] divergence: low_P2 < low_P1 & MACD_P2 > MACD_P1 (pivot k=3, jarak 5-40)
       [2] i - P2 <= 15 [3] tiada low baharu selepas P2 [4] tutup > SMA200 [5] tutup semalam <= H
       [6] PENCETUS: tutup > H (puncak antara P1-P2)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s200) or len(g) < 220:
        return None
    if not (r.close > r._s200):
        return None
    h, l, c = g.high.values, g.low.values, g.close.values
    n = len(g)
    e12 = g.close.ewm(span=12, adjust=False).mean(); e26 = g.close.ewm(span=26, adjust=False).mean()
    M = (e12 - e26).values
    pl0 = [t for t in range(max(3, n - 120), n - 3) if l[t] == l[t - 3:t + 4].min()]   # pivot tidak bergantung bar esok
    w199 = c[-199:]
    def ok(x):
        # Andaian saya: bar esok high = low = tutup esok x
        ll = np.append(l, x); i = n
        pl = pl0 + ([n - 3] if ll[n - 3] == ll[n - 6:n + 1].min() else [])
        if len(pl) < 2: return None
        P1, P2 = pl[-2], pl[-1]
        if not (5 <= P2 - P1 <= 40): return None
        Hh = h[P1:P2 + 1].max()
        if not (l[P2] < l[P1] and M[P2] > M[P1] and i - P2 <= 15 and ll[P2 + 1:i + 1].min() > l[P2]): return None
        return (Hh, P1, P2, x > Hh and c[-1] <= Hh and x > np.append(w199, x).mean())
    c0 = float(c[-1]); hi = c0 * 1.02
    z = ok(hi)
    if not z or not z[3]:
        return None
    lo = c0
    zl = ok(lo)
    if zl and zl[3]:
        paras = lo
    else:
        for _ in range(50):
            m = (lo + hi) / 2; zm = ok(m)
            lo, hi = (lo, m) if (zm and zm[3]) else (m, hi)
        paras = hi
    Hh, P1, P2, _ = ok(paras * (1 + 1e-9))
    jarak = max(0.0, (paras - c0) / c0 * 100)
    return _hasil(f'Divergence menaik MACD: low P2 {l[P2]:.2f} < low P1 {l[P1]:.2f}, MACD P2 lebih tinggi; tiada low baharu selepas P2; tutup > SMA200 ({r._s200:.2f}); tutup <= H',
                  f'Tutup esok > {paras:.2f} (puncak antara P1-P2 = {Hh:.2f}, dan kekal > SMA200) dalam {15-(n-P2)} hari lagi; langkau jika buka esok <= henti {0.99*l[P2]:.2f}',
                  'Tutup > H', paras, jarak, 5, 6)

from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M104'
NAMA = 'High Tight Flag / Power Play'
VARIAN = 'V2 V1 + tiang >=50%'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
TIANG_MIN = 0.50
L_MIN, L_MAX = 10, 30


def _bendera(g):
    """Per hari i: PUNCAK, L, TIANG, RENDAH_REHAT, DALAM, sah_dasar (Kad + laporan Andaian #2)."""
    h = g.high.values.astype(float); l = g.low.values.astype(float)
    n = len(g)
    pk = np.full(n, np.nan); L = np.zeros(n, int); tiang = np.full(n, np.nan)
    rr = np.full(n, np.nan); dalam = np.full(n, np.nan)
    for i in range(41, n):
        a = max(0, i - 30)
        w = h[a:i]
        p = a + (len(w) - 1 - int(np.argmax(w[::-1])))   # seri: hari terkini
        if p - 40 < 0:
            continue
        das = l[p - 40:p].min()
        if not das <= l[p]:
            continue
        pk[i] = h[p]; L[i] = i - p; tiang[i] = h[p] / das - 1
        if i - 1 >= p + 1:
            rr[i] = l[p + 1:i].min(); dalam[i] = 1 - rr[i] / h[p]
    idx = g.index
    return (pd.Series(pk, idx), pd.Series(L, idx), pd.Series(tiang, idx), pd.Series(rr, idx), pd.Series(dalam, idx))


def sedia(fr, idx):
    for g in fr.values():
        pk, L, tiang, rr, dalam = _bendera(g)
        vol50 = g.volume.rolling(50).mean().shift(1)
        s50 = g.close.rolling(50).mean()
        sd = (tiang >= TIANG_MIN) & (L >= L_MIN) & (L <= L_MAX) & (dalam <= 0.20)
        sig = sd & (g.close > pk) & (g.volume >= 1.5 * vol50)
        g['_sd'] = sd; g['_pk'] = pk; g['_L'] = L; g['_tiang'] = tiang; g['_rr'] = rr; g['_dalam'] = dalam; g['_vol50'] = vol50
        g['sig'] = sig
        g['stop'] = np.maximum(rr * 0.99, g.close * 0.88)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = tiang.fillna(-1e9)


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V2 (4): (1) TIANG >= 50%; (2) panjang rehat L 10-30 hari; (3) kedalaman rehat <= 20%;
    # (4) PENCETUS: tutup > PUNCAK dengan volum >= 1.5 x purata volum 50 hari (dinilai untuk hari ESOK)
    r = g.iloc[-1]
    if bool(r.sig):
        return None
    h = g.high.values; l = g.low.values; n = len(g)
    i = n                    # hari esok
    if i < 41:
        return None
    a = max(0, i - 30); w = h[a:i]
    p = a + (len(w) - 1 - int(np.argmax(w[::-1])))
    if p - 40 < 0:
        return None
    das = l[p - 40:p].min()
    if not das <= l[p]:
        return None
    PK = h[p]; Lx = i - p; tg = PK / das - 1
    if tg < TIANG_MIN:                                  # 1
        return None
    if Lx < L_MIN or Lx > L_MAX:                        # 2
        return None
    rrx = l[p + 1:i].min(); dl = 1 - rrx / PK
    if dl > 0.20:                                       # 3
        return None
    jarak = (PK - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    vol50 = g.volume.iloc[-50:].mean()
    return _hasil(f'Tiang naik {tg*100:.0f}% (>= 50%); rehat {Lx} hari dari puncak pada esok (10-30); kedalaman rehat {dl*100:.1f}% (<= 20%)',
                  f'Tutup esok > {PK:.2f} (puncak bendera) DAN volum esok >= {1.5*vol50:,.0f} (1.5 x purata 50 hari); '
                  f'henti = maks(0.99 x {rrx:.2f}, 0.88 x tutup isyarat)',
                  'Pecah puncak bendera dengan volum', PK, jarak, 3, 4)

from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M55'
NAMA = 'Guppy GMMA'
VARIAN = 'V4 Undur ke kumpulan panjang lalu lantun (Persediaan 2)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

PEND = [3, 5, 8, 10, 12, 15]
PANJ = [30, 35, 40, 45, 50, 60]


def _gmma(c):
    P = pd.concat([c.ewm(span=n, adjust=False).mean() for n in PEND], axis=1)
    J = pd.concat([c.ewm(span=n, adjust=False).mean() for n in PANJ], axis=1)
    J.columns = PANJ; P.columns = PEND
    return P, J


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        P, J = _gmma(c)
        pp = P.mean(axis=1); pj = J.mean(axis=1); jmax = J.max(axis=1)
        e15 = P[15]; e30 = J[30]; e60 = J[60]
        sentuh = (g.low <= jmax).astype(int)
        sentuh3 = sentuh.shift(1).rolling(3).sum() >= 1          # wujud k dalam [i-3, i-1]
        asas = (e30 > e60) & (e60 > e60.shift(10)) & (pp > pj)
        undur = asas & sentuh3 & (c > e15) & (c.shift() <= e15.shift())
        stop = g.low.rolling(4).min()
        bo = g.open.shift(-1)
        g['sig'] = (undur & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pp < pj
        g['rank'] = c / c.shift(63) - 1
        g['_asas'] = asas; g['_sentuh3b'] = sentuh.rolling(3).sum() >= 1   # sentuhan dalam [i-2, i]
        g['_e15'] = e15; g['_jmax'] = jmax


def hampir(g, idx):
    # Syarat entry V4 Persediaan 2 (N=6): (1) EMA30 > EMA60; (2) EMA60 > EMA60 10 hari lalu; (3) purata
    # kumpulan pendek > purata kumpulan panjang; (4) low menyentuh EMA tertinggi kumpulan panjang dalam
    # 3 hari sebelum isyarat; (5) tutup semalam <= EMA15 semalam; (6) PENCETUS: tutup > EMA15.
    # Hampir: (1)-(3) benar hari ini dan esok (pada tutup = paras), sentuhan dalam [hari ini-2, hari ini],
    # tutup hari ini <= EMA15. EMA15 esok = a.C + (1-a).EMA15 => C > EMA15 esok <=> C > EMA15 hari ini.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._asas) or not bool(r._sentuh3b) or not (r.close <= r._e15):
        return None
    paras = float(r._e15); c0 = float(r.close)
    jarak = (paras - c0) / c0 * 100
    if not (0 < jarak <= 2.0):
        return None
    # Semak asas esok pada C = paras
    c2 = pd.concat([g.close, pd.Series([paras])], ignore_index=True)
    P, J = _gmma(c2)
    e60 = J[60]
    if not (J[30].iloc[-1] > e60.iloc[-1] and e60.iloc[-1] > e60.iloc[-11] and P.mean(axis=1).iloc[-1] > J.mean(axis=1).iloc[-1]):
        return None
    henti = float(g.low.iloc[-3:].min())
    return {'sebab': f'EMA30 > EMA60; EMA60 menaik 10 hari; purata EMA pendek > purata EMA panjang; low menyentuh kumpulan panjang ({r._jmax:.2f}) dalam 3 hari; tutup <= EMA15',
            'syarat_beli': f'Tutup esok > {paras:.2f} (EMA15); henti low terendah 4 hari (min({henti:.2f}, low esok))',
            'pencetus': 'Tutup > EMA15 (lantun)', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '5/6', 'skor': float(round(1 - jarak / 2, 3))}

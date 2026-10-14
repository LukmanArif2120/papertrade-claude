from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M29'
NAMA = 'EMA3 + RSI75 + Stokastik'
VARIAN = 'V4 V1 EMA 50/110/250'
TMAX = None
WARM = 300
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320

P1, P2, P3 = 50, 110, 250


def _komponen(g):
    c, h, l = g.close, g.high, g.low
    ema = lambda k: c.ewm(span=k, adjust=False).mean()
    e1, e2, e3 = ema(P1), ema(P2), ema(P3)
    r75 = rsi(c, 75)
    fk = 100 * (c - l.rolling(14).min()) / (h.rolling(14).max() - l.rolling(14).min())
    K = fk.rolling(3).mean(); D = K.rolling(3).mean()
    # Zon = EMA paling dalam yang disentuh (low <= EMA) dalam i-5..i (6 hari)
    z = pd.Series(np.nan, g.index)
    for ee in (e1, e2, e3):  # tulis dari cetek ke dalam; yang terdalam menang
        sentuh = (l - ee).rolling(6).min() <= 0
        z = z.where(~sentuh, ee)
    susun = (e1 > e2) & (e2 > e3) & (e1 > e1.shift(5)) & (e2 > e2.shift(5)) & (e3 > e3.shift(5))
    return e1, e2, e3, r75, K, D, z, susun


def sedia(fr, idx):
    for g in fr.values():
        o, c = g.open, g.close
        e1, e2, e3, r75, K, D, z, susun = _komponen(g)
        silang = (K.shift() <= D.shift()) & (K > D)
        k20 = K.rolling(6).min() < 20
        sig = susun & (r75 > 50) & z.notna() & (c > e3) & k20 & silang
        stop = 0.99 * z
        sig = sig & ~(o.shift(-1) <= stop)
        g['_pers'] = (susun & (r75 > 50) & z.notna() & (c > e3)).fillna(False)
        g['_e1'] = e1; g['_e2'] = e2; g['_e3'] = e3
        g['_k20'] = k20.fillna(False); g['_K'] = K; g['_D'] = D; g['_z'] = z
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ((c < e3) | (r75 < 50)).fillna(False)
        g['rank'] = r75


def hampir(g, idx):
    # Piawaian ketat: syarat entry V4 = (1) EMA50 > EMA110 > EMA250, (2) ketiga-tiga EMA menaik 5 hari,
    # (3) RSI75 > 50, (4) zon EMA disentuh dalam 6 hari (tetingkap esok), (5) tutup > EMA250,
    # (6) %K < 20 dalam 6 hari (tetingkap esok), (7) PENCETUS: %K silang ke atas %D.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._pers):
        return None
    K = g._K.values; D = g._D.values
    if not (K[-1] <= D[-1]):                     # silang esok perlukan %K hari ini <= %D
        return None
    if not (np.nanmin(K[-5:]) < 20):             # tetingkap esok i-4..i (+esok)
        return None
    lo = g.low.values[-5:]
    z = None
    for k in ('_e1', '_e2', '_e3'):              # cetek -> dalam; yang terdalam menang
        if np.min(lo - g[k].values[-5:]) <= 0: z = float(g[k].iloc[-1])
    if z is None:
        return None
    # Andaian saya: high = low = tutup esok; EMA esok = nilai hari ini
    h13 = g.high.values[-13:].max(); l13 = g.low.values[-13:].min()
    c = float(r.close)
    fk = 100 * (g.close - g.low.rolling(14).min()) / (g.high.rolling(14).max() - g.low.rolling(14).min())
    perlu = 1.5 * (K[-2] + K[-1]) - fk.iloc[-2] - fk.iloc[-1]   # fastK esok mesti > nilai ini
    if not np.isfinite(perlu) or perlu >= 100 or not h13 > l13:
        return None
    cstar = max(l13 + max(perlu, 0) / 100 * (h13 - l13), float(r._e3))   # juga mesti kekal > EMA250
    jarak = max((cstar - c) / c * 100, 0.0)     # Andaian saya: paras di bawah tutup -> jarak 0
    if jarak > 2.0:
        return None
    return {'sebab': f'EMA{P1} > EMA{P2} > EMA{P3}, semua menaik; RSI75 > 50; harga undur menyentuh zon EMA {z:.2f}; tutup > EMA{P3}; %K < 20 dalam 6 hari (%K={K[-1]:.1f})',
            'syarat_beli': f'Tutup esok > {cstar:.2f} supaya %K silang ke atas %D; henti 0.99 x {z:.2f}',
            'pencetus': 'silang stokastik', 'paras': round(cstar, 4), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '6/7', 'skor': round(1 - jarak / 2, 3)}

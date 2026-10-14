from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M02'
NAMA = 'MACD + SMA200'
VARIAN = 'V5 V1+sasaran 3R'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

_R = 3.0


def _isi_tgt(g, sig, st):
    """Sasaran tetap = buka_masuk + 3 x (buka_masuk - henti), diisi sepanjang tempoh dagangan.
       Simulasi meniru gelung enjin.trades (tmax=TMAX, warm=WARM) supaya lajur tgt betul bagi setiap dagangan.
       Hanya buka hari i+1 (harga pesanan) diguna; isyarat sendiri tiada pandang ke hadapan."""
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g); tg = np.full(n, np.nan); i = WARM
    while i < n - 1:
        if not sig[i]: i += 1; continue
        e = o[i + 1]; sp = st[i]; tf = e + _R * (e - sp)
        j = i + 1; x = None
        while j < n:
            tg[j - 1] = tf
            if j > i + 1 and o[j] <= sp: x = 1; break
            if l[j] <= sp: x = 1; break
            if j > i + 1:
                if o[j] >= tf: x = 1; break
                if h[j] >= tf: x = 1; break
            if TMAX and (j - i) >= TMAX: x = 1; break
            j += 1
        if x is None: j = n - 1
        i = j + 1
    return tg


def sedia(fr, idx):
    for g in fr.values():
        c, o = g.close, g.open
        s200 = c.rolling(200).mean()
        m = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
        s = m.ewm(span=9, adjust=False).mean()
        stop = 0.99 * s200
        sig = (c > s200) & (m < 0) & (s < 0) & (m.shift() <= s.shift()) & (m > s)
        # langkau jika buka_masuk <= henti (bar terakhir: buka esok belum diketahui -> dikekalkan)
        bm = o.shift(-1)
        sig = (sig & ((bm > stop) | bm.isna())).fillna(False)
        g['_m'] = m; g['_s'] = s; g['_s200'] = s200
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _isi_tgt(g, sig.values, stop.values)
        g['exitc'] = False
        g['rank'] = c / c.shift(63) - 1



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V5 (N=5): [1] tutup > SMA200 [2] MACD < 0 [3] isyarat < 0
       [4] MACD semalam <= isyarat semalam [5] PENCETUS: MACD silang ke atas isyarat (MACD > isyarat).
       Untuk esok: [4] = MACD hari ini <= isyarat hari ini. Paras = tutup esok minimum untuk silang (algebra EMA)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s200) or len(g) < 210:
        return None
    if not (r.close > r._s200 and r._m < 0 and r._s < 0 and r._m <= r._s):
        return None
    c = g.close
    e12 = c.ewm(span=12, adjust=False).mean().iloc[-1]; e26 = c.ewm(span=26, adjust=False).mean().iloc[-1]
    a12, a26, a9 = 2 / 13, 2 / 27, 2 / 10
    cx = float((r._s - (1 - a12) * e12 + (1 - a26) * e26) / (a12 - a26))   # MACD esok = isyarat hari ini <=> silang
    c0 = float(r.close); w199 = c.values[-199:]
    def lain(x):          # syarat [1][2][3] dinilai pada tutup esok x
        m = (e12 + a12 * (x - e12)) - (e26 + a26 * (x - e26)); s = r._s + a9 * (m - r._s)
        return x > np.append(w199, x).mean() and m < 0 and s < 0
    xs = max(cx, c0 * 0.98) * (1 + 1e-7)
    if not lain(xs):
        return None       # silang esok akan berlaku di atas sifar / di bawah SMA200 -> bukan persediaan sah
    jarak = (cx - c0) / c0 * 100
    if jarak > 2.0:
        return None
    # Andaian saya: jika paras silang <= tutup semasa, jarak_pct = 0 (silang berlaku walaupun harga tidak naik)
    jarak = max(0.0, jarak)
    return _hasil(f'Tutup > SMA200 ({r._s200:.2f}); MACD ({r._m:.3f}) dan isyarat ({r._s:.3f}) di bawah sifar; MACD masih <= isyarat',
                  f'Tutup esok > {cx:.2f} (MACD silang naik garisan isyarat di bawah sifar)', 'Silang MACD naik', cx, jarak, 4, 5)

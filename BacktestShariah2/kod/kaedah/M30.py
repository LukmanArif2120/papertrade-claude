from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M30'
NAMA = 'BB Free Bar + Himpitan 50/2.5'
VARIAN = 'V3 V1 tetapi BB20/2'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 200


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        bm = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0)
        bbu = bm + 2 * sd; bw = 4 * sd / bm
        sqz = (bw <= bw.rolling(126).quantile(0.2))
        sq = sqz.shift(1).rolling(10).max() == 1            # himpitan dalam i-10..i-1
        dec = c >= bbu + 0.5 * _atrw(g)                     # tutup tegas
        dec_lalu = dec.shift(1).rolling(10).max() == 1
        hh20 = h.shift(1).rolling(20).max()
        sig = sq & dec & ~dec_lalu & (c > hh20)
        stop = 0.99 * l.rolling(11).min()
        # Langkau jika buka esok <= henti (sama seperti backtest). Pada bar terakhir buka esok belum wujud -> tidak dilangkau.
        sig = sig & ~(o.shift(-1) <= stop)
        g['_sqz'] = sqz; g['_dec'] = dec
        g['_sq'] = sq; g['_bbu'] = bbu; g['_dec_lalu'] = dec_lalu; g['_hh20'] = hh20; g['_atrw'] = _atrw(g)
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < c.rolling(50).mean()).fillna(False)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    # Piawaian ketat: syarat entry V3 = (1) himpitan BB(20,2) dalam 10 hari (tetingkap esok),
    # (2) tiada tutup tegas dalam 10 hari (tetingkap esok), (3) PENCETUS: tutup >= BBU + 0.5 x ATR14
    # DAN tutup > high 20 hari (kedua-duanya paras harga; digabung sebagai satu pencetus).
    r = g.iloc[-1]
    if bool(r.sig):
        return None
    if not bool(g._sqz.iloc[-10:].fillna(False).astype(bool).any()) or bool(g._dec.iloc[-10:].fillna(False).astype(bool).any()):
        return None
    w = g.close.values[-19:].astype(float); c0 = float(r.close); a0 = float(r._atrw)
    if len(w) < 19 or not np.isfinite(a0):
        return None
    hh = float(g.high.iloc[-20:].max())            # high 20 hari untuk esok
    # Andaian saya: high = low = tutup esok, maka TR esok = |tutup esok - tutup hari ini| (ATR Wilder)
    def f(C):
        x = np.r_[w, C]
        return C - (x.mean() + 2 * x.std() + 0.5 * (a0 + (abs(C - c0) - a0) / 14))
    lo, hi = c0 * 0.5, c0 * 3.0
    if f(hi) < 0: return None
    for _ in range(60):
        m = (lo + hi) / 2
        if f(m) >= 0: hi = m
        else: lo = m
    cbb = hi
    paras = max(cbb, hh)
    jarak = (paras - c0) / c0 * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': 'Himpitan BB(20,2) dalam 10 hari (lebar band <= persentil 20% 126 hari); tiada tutup tegas dalam 10 hari',
            'syarat_beli': f'Tutup esok >= {cbb:.2f} (band atas + 0.5xATR14) dan > {hh:.2f} (high 20 hari)',
            'pencetus': 'tutup tegas + pecah high 20 hari', 'paras': round(paras, 4), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '2/3', 'skor': round(1 - jarak / 2, 3)}

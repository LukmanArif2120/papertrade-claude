from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M04'
NAMA = 'BB Squeeze Breakout'
VARIAN = 'U2 asas V2 + E1 volume>=1.5xSMA20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        bm = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0); BBU = bm + 2 * sd; BW = 4 * sd / bm
        s50 = c.rolling(50).mean()
        # himpitan: BW <= persentil 20% BW 126 hari, berlaku dalam i-10..i-1 (ikut kod finalis_v1)
        sqk = (BW <= BW.rolling(126).quantile(0.2))
        sq = sqk.shift(1).rolling(10).max() == 1
        vs20 = v.rolling(20).mean()
        stop = 0.99 * l.rolling(11).min()
        sig = sq & (c > BBU) & (c.shift() <= BBU.shift()) & (v >= 1.5 * vs20)   # U2: volume >= 1.5 x SMA20
        bmk = o.shift(-1)
        sig = sig & ((bmk > stop) | bmk.isna())                               # langkau jika buka_masuk <= henti
        g['_sq'] = sq; g['_bbu'] = BBU; g['_vs20'] = vs20
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(63) - 1



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry U2 (N=3), untuk bar esok: [1] himpitan BB (BW <= persentil 20% 126 hari) dalam 10 hari terakhir
       [2] tutup hari ini <= band atas [3] PENCETUS: tutup esok > band atas BB(20,2) DENGAN volume >= 1.5 x SMA20 volume."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._bbu) or len(g) < 150:
        return None
    c = g.close; sd = c.rolling(20).std(ddof=0); BW = 4 * sd / c.rolling(20).mean()
    if not bool((BW <= BW.rolling(126).quantile(0.2)).iloc[-10:].any()) or r.close > r._bbu:
        return None
    w19 = c.values[-19:]; c0 = float(r.close)
    def bbu(x):
        w = np.append(w19, x); return w.mean() + 2 * w.std()
    lo, hi = c0, c0 * 1.02
    if hi <= bbu(hi):
        return None
    if lo > bbu(lo):
        paras = lo
    else:
        for _ in range(50):
            m = (lo + hi) / 2
            lo, hi = (lo, m) if m > bbu(m) else (m, hi)
        paras = hi
    jarak = (paras - c0) / c0 * 100
    vmin = 1.5 * g.volume.values[-19:].sum() / 18.5          # v >= 1.5 x (jumlah 19 hari + v)/20
    return _hasil(f'Himpitan Bollinger dalam 10 hari terakhir; tutup {c0:.2f} masih <= band atas {r._bbu:.2f}',
                  f'Tutup esok > {paras:.2f} (band atas BB20 termasuk tutup esok) DAN volume esok >= {vmin:,.0f} (1.5 x SMA20 volume)',
                  'Pecah band atas + volume', paras, jarak, 2, 3)

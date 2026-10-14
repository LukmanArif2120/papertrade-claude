from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M70'
NAMA = 'Pecahan Hari Dalam'
VARIAN = 'V5 V1 masuk awal tanpa pengesahan'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        e10 = c.ewm(span=10, adjust=False).mean(); e21 = c.ewm(span=21, adjust=False).mean()
        s50 = c.rolling(50).mean(); s200 = c.rolling(200).mean()
        dalam = (g.high < g.high.shift()) & (g.low > g.low.shift()) & (g.high > g.low)
        atasma = (c > e10) & (c > e21) & (c > s50) & (c > s200)
        stop = g.low.copy()
        # Langkau jika buka masuk (buka i+1) <= henti; pada bar terakhir buka esok belum diketahui -> isyarat dikekalkan
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_dalam'] = dalam; g['_atasma'] = atasma
        g['_e10'] = e10; g['_e21'] = e21; g['_s50'] = s50; g['_s200'] = s200
        g['sig'] = dalam & atasma & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V5 (N=5): tutup > EMA10, tutup > EMA21, tutup > SMA50, tutup > SMA200, hari dalam (PENCETUS).
    # Pencetus corak satu hari (hari dalam) -> jarak_pct = None.
    r = g.iloc[-1]
    if bool(r.sig):
        return None
    if not (r.close > r._e10 and r.close > r._e21 and r.close > r._s50 and r.close > r._s200):
        return None
    if not (r.high > r.low):
        return None
    c = g.close.values.astype(float)
    if len(c) < 200:
        return None
    # Tutup minimum esok supaya kekal di atas keempat-empat purata (purata esok termasuk tutup esok):
    # EMA: x > EMA hari ini; SMA50: x > purata 49 tutup terakhir; SMA200: x > purata 199 tutup terakhir.
    pmin = max(r._e10, r._e21, c[-49:].mean(), c[-199:].mean())
    # Hari dalam esok memerlukan tutup esok < high hari ini; jika pmin >= high hari ini, pencetus mustahil esok.
    if pmin >= r.high:
        return None
    # Andaian saya: langkau (buka lusa <= low hari dalam) bukan syarat isyarat pada bar terakhir, jadi tidak dikira.
    return {'sebab': 'Tutup di atas EMA10, EMA21, SMA50 dan SMA200 (4/4 penapis purata dipenuhi); hari ini bukan hari dalam',
            'syarat_beli': f'Esok mesti hari dalam: high < {r.high:.2f} dan low > {r.low:.2f}, dengan tutup > {pmin:.2f} '
                           f'(kekal atas 4 purata); masuk buka lusa, henti = low hari dalam',
            'pencetus': 'hari dalam', 'paras': None, 'jarak_pct': None,
            'syarat_dipenuhi': '4/5', 'skor': 0.9}

from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M51'
NAMA = "O'Neil Cawan & Pemegang"
VARIAN = 'V3 V1 kedalaman cawan 12-50%'
TMAX = None
WARM = 480
ADA_HENTI = True
SILANG = False
PERLU_BAR = 482
DALAM_MAX = 0.50          # V3


def _corak(g, i):
    """Pulangkan dict geometri cawan & pemegang pada hari i (tanpa syarat PECAH), atau None."""
    h = g.high.values; l = g.low.values
    if i < 475:
        return None
    w = h[i - 25:i - 4]                       # [i-25, i-5]
    r = i - 25 + (len(w) - 1 - np.argmax(w[::-1]))   # seri: paling lewat
    piv = h[r]
    if r + 1 <= i - 1 and h[r + 1:i].max() > piv:
        return None
    rp = l[r + 1:i].min()
    wl = h[r - 320:r - 29]                    # [r-320, r-30]
    lft = r - 320 + (len(wl) - 1 - np.argmax(wl[::-1]))
    kiri = h[lft]; panjang = i - lft
    dasar = l[lft:r + 1].min(); dc = 1 - dasar / kiri
    if lft - 130 < 0:
        return None
    naik = kiri / l[lft - 130:lft].min() - 1
    lompang = h[r - 29:r].max() <= piv
    cawan = (35 <= panjang <= 325) and (0.12 <= dc <= DALAM_MAX) and naik >= 0.30 and \
            (0.90 * kiri <= piv <= 1.05 * kiri) and lompang
    pem = (1 - rp / piv) <= 0.12 and rp >= (kiri + dasar) / 2
    return dict(cawan=cawan, pem=pem, piv=piv, rp=rp, kiri=kiri, dasar=dasar, dc=dc)


def sedia(fr, idx):
    for g in fr.values():
        c = g.close; n = len(g)
        s50 = c.rolling(50).mean()
        vol50 = g.volume.rolling(50).mean().shift(1)
        cv = c.values; vv = g.volume.values; v50 = vol50.values; s = s50.values
        sig = np.zeros(n, bool); piv = np.full(n, np.nan)
        for i in range(475, n):
            # Prapenapis murah: tutup melepasi high tertinggi 25..5 hari lalu buat kali pertama
            if not (cv[i] > s[i]) or not (vv[i] >= 1.4 * v50[i]):
                continue
            k = _corak(g, i)
            if k is None:
                continue
            p = k['piv']
            pecah = cv[i] > p and cv[i - 1] <= p and cv[i] <= 1.05 * p
            if k['cawan'] and k['pem'] and pecah:
                sig[i] = True; piv[i] = p
        g['sig'] = sig
        # Henti 0.92 x buka masuk (buka hari i+1). Ditulis pada hari isyarat i; tidak pandang ke hadapan
        # untuk isyarat (henti hanya terpakai selepas masuk). Bar terakhir: belum diketahui -> anggaran 0.92 x tutup.
        bo = g.open.shift(-1)
        g['stop'] = (0.92 * bo).fillna(0.92 * c)
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(63) - 1
        g['_s50'] = s50; g['_vol50'] = vol50


def hampir(g, idx):
    # Syarat entry V3 (N=4): (1) cawan sah (panjang 35-325 hari, dalam 12-50%, naik >= 30% sebelum, pangsi
    # 0.90-1.05 x bibir kiri, tiada high > pangsi dalam 29 hari sebelum pangsi); (2) pemegang sah (<= 12%,
    # low di separuh atas cawan); (3) tutup > SMA50; (4) PENCETUS: tutup > pangsi buat kali pertama
    # (tutup semalam <= pangsi, tutup <= 1.05 x pangsi) dengan volum >= 1.4 x purata volum 50 hari.
    # Geometri dinilai untuk bar ESOK (_corak tidak guna data bar i itu sendiri, jadi boleh dikira hari ini).
    r = g.iloc[-1]
    n = len(g)
    if bool(r.sig) or n < 482 or not (r.close > r._s50):
        return None
    g2 = pd.concat([g[['high', 'low']], pd.DataFrame({'high': [r.close], 'low': [r.close]})], ignore_index=True)
    k = _corak(g2, n)
    if k is None or not (k['cawan'] and k['pem']):
        return None
    p = float(k['piv'])
    if r.close > p:          # syarat tutup semalam <= pangsi
        return None
    s50_esok = float(g.close.iloc[-49:].mean())
    paras = max(p, s50_esok)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    vmin = 1.4 * float(g.volume.iloc[-50:].mean())
    return {'sebab': f'Cawan sedalam {k["dc"]*100:.0f}% sah; pemegang (low {k["rp"]:.2f}) di separuh atas sah; tutup > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} (pangsi) dan <= {1.05*p:.2f}, dengan volum esok >= {vmin:,.0f} (1.4 x purata 50 hari); henti 8% bawah harga masuk',
            'pencetus': 'Pecah pangsi dengan volum', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 3))}

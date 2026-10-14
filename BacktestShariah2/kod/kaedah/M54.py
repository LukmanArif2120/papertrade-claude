from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M54'
NAMA = 'IBD Power Trend'
VARIAN = 'V4 V1 sig=PT benar & tutup>high 20 hari'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _pt(g):
    e21 = g.close.ewm(span=21, adjust=False).mean(); s50 = g.close.rolling(50).mean()
    k1 = (g.low > e21).astype(int).rolling(10).sum() == 10
    k2 = (e21 > s50).astype(int).rolling(5).sum() == 5
    k3 = s50 > s50.shift(5); k4 = g.close > g.close.shift()
    mula_ok = (k1 & k2 & k3 & k4).values; tamat = (e21 < s50).values
    pt = np.zeros(len(g), bool)
    for i in range(1, len(g)):
        if not pt[i - 1] and mula_ok[i]: pt[i] = True
        elif tamat[i]: pt[i] = False
        else: pt[i] = pt[i - 1]
    return pd.Series(pt, g.index), e21, s50


def sedia(fr, idx):
    for g in fr.values():
        pt, e21, s50 = _pt(g)
        hh20 = g.high.rolling(20).max().shift(1)
        g['_pt'] = pt; g['_hh20'] = hh20
        g['sig'] = pt & (g.close > hh20)
        g['stop'] = g.close - 2 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = e21 < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V4 (N=2): (1) Power Trend aktif (mula: low > EMA21 10 hari, EMA21 > SMA50 5 hari,
    # SMA50 naik berbanding 5 hari lalu, tutup naik; tamat bila EMA21 < SMA50); (2) PENCETUS: tutup > high 20 hari.
    # Hampir: PT aktif hari ini dan kekal aktif esok pada tutup = paras; tutup esok perlu > high 20 hari
    # (tetingkap esok = 20 bar terakhir termasuk hari ini).
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._pt):
        return None
    paras = float(g.high.iloc[-20:].max())
    c0 = float(r.close)
    jarak = (paras - c0) / c0 * 100
    if not (0 < jarak <= 2.0):
        return None
    a = 2 / 22
    e21 = g.close.ewm(span=21, adjust=False).mean().iloc[-1]
    e21_esok = a * paras + (1 - a) * e21
    s50_esok = (g.close.iloc[-49:].sum() + paras) / 50
    if e21_esok < s50_esok:
        return None
    return {'sebab': f'Power Trend aktif (EMA21 {e21:.2f} > SMA50, belum tamat); harga {jarak:.1f}% di bawah high 20 hari',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high 20 hari) sementara Power Trend masih aktif',
            'pencetus': 'Tutup > high 20 hari', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '1/2', 'skor': float(round(1 - jarak / 2, 3))}

from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M46'
NAMA = 'Jurang Naik Boleh Beli (Buyable Gap Up)'
VARIAN = 'V2 V1 dengan jurang ketat (low>high semalam+0.75xATR40)'
TMAX = None
WARM = 231
ADA_HENTI = True
SILANG = False
PERLU_BAR = 240


def _asas(g):
    c = g.close
    a40 = atr(g, 40)                       # purata mudah TR 40 hari (laporan)
    vol50 = g.volume.rolling(50).mean().shift(1)
    s200 = c.rolling(200).mean(); s50 = c.rolling(50).mean()
    aliran = (c.shift() > s200.shift()) & (s200.shift() > s200.shift(31))
    return a40, vol50, s50, aliran


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        a40, vol50, s50, aliran = _asas(g)
        ketat = g.low > g.high.shift() + 0.75 * a40.shift()
        taktutup = g.low > c.shift()
        volum = g.volume >= 1.5 * vol50
        sig = ketat & taktutup & volum & aliran & (c > s50)
        stop = g.low
        # Langkau jika buka masuk <= henti (spec). Bar terakhir: buka esok belum diketahui
        g['sig'] = sig & ~(g.open.shift(-1) <= stop)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(63) - 1
        g['_a40'] = a40; g['_vol50'] = vol50; g['_s50'] = s50; g['_aliran'] = aliran


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2, N=4, dinilai untuk isyarat esok:
    1 tutup hari ini > SMA200 hari ini; 2 SMA200 hari ini > SMA200 30 hari dagangan lalu; 3 tutup > SMA50;
    4 PENCETUS (jurang ketat esok): low esok > high hari ini + 0.75 x ATR40 hari ini, low esok > tutup hari ini,
      volum esok >= 1.5 x purata volum 50 hari (hingga hari ini)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._a40) or np.isnan(r._s50) or len(g) < 232:
        return None
    c = g.close; s200 = c.rolling(200).mean()
    if not (r.close > s200.iloc[-1]):
        return None
    if not (s200.iloc[-1] > s200.iloc[-31]):
        return None
    # Andaian saya: syarat tutup > SMA50 (hari isyarat) disemak pada tutup hari ini
    if not (r.close > r._s50):
        return None
    paras = max(r.high + 0.75 * r._a40, r.close)
    vmin = 1.5 * g.volume.iloc[-50:].mean()
    # Andaian saya: jurang diukur sebagai paras harga (low esok mesti melepasi paras), jadi jarak = (paras − tutup)/tutup
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Tutup > SMA200 ({s200.iloc[-1]:.2f}); SMA200 menaik berbanding 30 hari lalu; tutup > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Esok: low > {paras:.2f} (high hari ini + 0.75 × ATR40; jurang tidak ditutup sepanjang hari), volum esok >= {vmin:,.0f}, tutup esok > SMA50; beli buka lusa; henti low hari jurang',
            'pencetus': 'Jurang naik ketat + volum', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}

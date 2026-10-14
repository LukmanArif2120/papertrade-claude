from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M48'
NAMA = 'Cooper 1-2-3-4'
VARIAN = 'V3 V1 henti low hari 3 - 1xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _wilder(g, n=14):
    h, l, c = g.high, g.low, g.close
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    up = h.diff(); dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), g.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), g.index)
    a = 1 / n
    atr_ = tr.ewm(alpha=a, adjust=False).mean()
    pdi = 100 * pdm.ewm(alpha=a, adjust=False).mean() / atr_
    mdi = 100 * mdm.ewm(alpha=a, adjust=False).mean() / atr_
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=a, adjust=False).mean(), pdi, mdi, atr_


def _undur(g):
    """Bagi tiga hari berakhir hari k: setiap hari RENDAH atau DALAM, >=2 RENDAH."""
    rendah = g.low < g.low.shift()
    dalam = (g.high <= g.high.shift()) & (g.low >= g.low.shift())
    ok = (rendah | dalam).astype(int).rolling(3).sum() == 3
    nr = rendah.astype(int).rolling(3).sum() >= 2
    return ok & nr


def sedia(fr, idx):
    for g in fr.values():
        adx, pdi, mdi, a14 = _wilder(g)
        s50 = g.close.rolling(50).mean()
        kuat = (adx >= 30) & (pdi > mdi)                 # dinilai pada hari ketiga (i-1)
        und = _undur(g)                                   # tiga hari berakhir hari ketiga
        setup = kuat & und                                # pada hari ketiga
        cetus = g.close > g.high.shift() + 0.125
        sig = setup.shift(1, fill_value=False) & cetus & (g.close > s50)
        stop = g.low.shift() - a14                        # V3: low hari 3 - 1 x ATR14 Wilder hari isyarat
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1
        g['_setup'] = setup; g['_s50'] = s50; g['_adx'] = adx; g['_a14'] = a14


def hampir(g, idx):
    # Syarat entry V3 (N=5): (1) ADX14 >= 30 pada hari ketiga; (2) +DI > -DI; (3) undur tiga hari
    # (setiap hari low lebih rendah atau hari dalam, >= 2 low lebih rendah) berakhir hari ketiga;
    # (4) tutup hari isyarat > SMA50; (5) PENCETUS: tutup hari isyarat > high hari ketiga + 0.125.
    # Hampir: hari ini = hari ketiga sah (1-3) dan tutup hari ini > SMA50 (4); pencetus esok.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._setup) or not (r.close > r._s50):
        return None
    # SMA50 esok = (jumlah 49 tutup terakhir + C)/50; C > SMA50 esok <=> C > purata 49 tutup terakhir
    s50_esok = float(g.close.iloc[-49:].mean())
    paras = max(float(r.high) + 0.125, s50_esok)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'ADX14 {r._adx:.1f} >= 30; +DI > -DI; undur tiga hari lengkap hari ini; tutup > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high hari ini {r.high:.2f} + 0.125, dan atas SMA50 esok); henti {r.low - r._a14:.2f} (low hari ini - 1 x ATR14)',
            'pencetus': 'Tutup > high hari ketiga + 0.125', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 3))}

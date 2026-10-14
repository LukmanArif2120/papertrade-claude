from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M91'
NAMA = 'Stochastic Pop (Bernstein/Steckler)'
VARIAN = 'V2 V1 + tutup>HH20 (pecah keluar)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280


def _sto(g, n):
    ll = g.low.rolling(n).min(); hh = g.high.rolling(n).max()
    d = hh - ll
    k = (100 * (g.close - ll) / d.replace(0, np.nan)).where(d != 0, 50.0)
    k[ll.isna()] = np.nan
    return k.rolling(3).mean()


def _adx(g, n=14):
    # Andaian saya (ikut laporan): pelicinan Wilder sebagai EMA alpha 1/14, tanpa permulaan jumlah 14 hari.
    h, l, c = g.high, g.low, g.close
    up = h.diff(); dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), g.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), g.index)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a = 1 / n
    atr_ = tr.ewm(alpha=a, adjust=False).mean()
    pdi = 100 * pdm.ewm(alpha=a, adjust=False).mean() / atr_
    mdi = 100 * mdm.ewm(alpha=a, adjust=False).mean() / atr_
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=a, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        s14 = _sto(g, 14); s70 = _sto(g, 70); adx = _adx(g)
        v250 = g.volume.rolling(250).mean().shift(1)
        hh20 = g.high.rolling(20).max().shift(1)
        pop = (s14 > 80) & (s14.shift() <= 80)
        g['_s14'] = s14; g['_s70'] = s70; g['_adx'] = adx; g['_v250'] = v250; g['_hh20'] = hh20
        g['sig'] = pop & (s70 > 50) & (adx < 20) & (g.volume > v250) & (g.close > hh20)
        g['stop'] = g.low.rolling(10).min()
        g['tgt'] = np.nan
        g['exitc'] = s14 < 50
        g['rank'] = g.close / g.close.shift(63) - 1


def _cari_paras(g, idx, ekor, bawah=-0.05, atas=0.02, vol=None):
    """Tutup esok minimum (dalam julat tutup*(1+bawah)..tutup*(1+atas)) yang menjadikan sig bar esok benar,
    dengan menjalankan sedia() asal pada ekor data + satu bar esok rekaan.
    Andaian saya: bar esok open=high=low=close=C; volum esok = `vol` jika diberi, jika tidak purata volum 10 hari."""
    c0 = float(g.close.iloc[-1])
    asas = g[['open', 'high', 'low', 'close', 'volume', 'turnover']].iloc[-ekor:].astype(float)
    v = float(asas.volume.iloc[-10:].mean()) if vol is None else float(vol)
    esok = asas.index[-1] + pd.offsets.BDay(1)

    def cuba(C):
        b = asas.copy()
        b.loc[esok] = [C, C, C, C, v, C * v]
        d = {'x': b}; sedia(d, {})
        return bool(d['x'].sig.iloc[-1])

    grid = np.round(np.arange(bawah, atas + 1e-9, 0.0025), 6)
    sebelum = None
    for p in grid:
        if cuba(c0 * (1 + p)):
            if sebelum is None:
                return c0 * (1 + p)
            lo, hi = c0 * (1 + sebelum), c0 * (1 + p)
            for _ in range(18):
                m = (lo + hi) / 2
                if cuba(m): hi = m
                else: lo = m
            return hi
        sebelum = p
    return None


def _jarak(paras, tutup):
    # Jarak mentah; pemanggil menolak jarak <= 0 (piawaian: 0 < jarak <= 2.0).
    return (paras - tutup) / tutup * 100


def hampir(g, idx):
    # Syarat entry V2 (laporan M91 + spec): N = 4
    #   1. STO70 > 50   2. ADX14 < 20   3. STO14 <= 80 pada bar akhir (prasyarat "pop" = lintasan ke atas 80)
    #   4. PENCETUS: tutup esok > high 20 hari DAN STO14 melintas atas 80 DAN volum esok > purata volum 250 hari
    # Andaian saya: harga pencetus dicari dengan volum esok dianggap cukup (2 x VOL250); volum minimum dinyatakan berasingan.
    r = g.iloc[-1]
    if bool(r.sig) or any(np.isnan([r._s14, r._s70, r._adx, r._hh20, r._v250])):
        return None
    if not (r._s70 > 50 and r._adx < 20 and r._s14 <= 80):
        return None
    hh20_esok = float(g.high.iloc[-20:].max())
    if (hh20_esok - r.close) / r.close * 100 > 2.0:
        return None
    paras = _cari_paras(g, idx, ekor=600, vol=2 * float(r._v250))
    if paras is None:
        return None
    j = _jarak(paras, float(r.close))
    if not (0 < j <= 2.0):
        return None
    vmin = float(g.volume.iloc[-250:].mean())
    return {'sebab': f'STO70 {r._s70:.0f} > 50; ADX14 {r._adx:.1f} < 20 (penyatuan); STO14 {r._s14:.0f} belum melepasi 80',
            'syarat_beli': f'Tutup esok > {paras:.2f} (pecah high 20 hari {hh20_esok:.2f} dan STO14 melintas ke atas 80) dengan volum esok > {vmin:,.0f} (purata 250 hari) dan ADX14 kekal < 20',
            'pencetus': 'Pecah HH20 + STO14 > 80 + volum', 'paras': round(float(paras), 2), 'jarak_pct': round(float(j), 2),
            'syarat_dipenuhi': '3/4', 'skor': round(float(1 - j / 2), 3)}

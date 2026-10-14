from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M82'
NAMA = 'Arthur Hill Rotasi Sasaran 10%'
VARIAN = 'V0 Sumber tulen (sasaran 10% tutup / EMA25<EMA125, tiada henti)'
TMAX = None
WARM = 250
ADA_HENTI = False
SILANG = False
PERLU_BAR = 260


def _exitc(g, sig, tren_turun, warm):
    """Andaian saya: CAPAI10 (tutup_j >= 1.10 x buka_masuk) bergantung pada harga masuk dagangan,
    jadi jujukan dagangan enjin (tiada henti) disimulasi di sini dan exitc ditanda pada hari j
    (jual buka j+1, sama seperti enjin). Tiada pandang ke hadapan: hanya guna data <= j."""
    o, c = g.open.values, g.close.values; n = len(g)
    ex = tren_turun.copy(); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        e = o[i + 1]; j = i + 1; jx = n - 1
        while j < n:
            if (c[j] >= 1.10 * e or tren_turun[j]) and j + 1 < n:
                ex[j] = True; jx = j + 1; break
            j += 1
        i = jx + 1
    return ex


def sedia(fr, idx):
    spy = idx['SPY'].close
    pas = spy.ewm(span=50, adjust=False).mean() > spy.ewm(span=200, adjust=False).mean()
    for g in fr.values():
        c = g.close
        e25 = c.ewm(span=25, adjust=False).mean(); e125 = c.ewm(span=125, adjust=False).mean()
        roc65 = c / c.shift(65) - 1
        sma20 = c.rolling(20).mean()
        sd250 = c.rolling(250).std(ddof=0)
        vol250 = g.volume.rolling(250).mean()
        layak = (e25 > e125) & (roc65 < 1.0) & (sma20 > 10) & (sd250 / sma20 * 100 < 20) & (sma20 * vol250 > 5_000_000)
        mkt = pas.reindex(g.index, method='ffill').fillna(False).astype(bool)
        sig = (layak & mkt).fillna(False)
        turun = (e25 < e125).values
        g['_e25'] = e25; g['_e125'] = e125; g['_roc65'] = roc65; g['_vr'] = sd250 / sma20 * 100
        g['_cair'] = (sma20 > 10) & (sma20 * vol250 > 5_000_000); g['_mkt'] = mkt
        g['sig'] = sig
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = _exitc(g, sig.values, turun, WARM)
        g['rank'] = c / c.shift(125) - 1


def hampir(g, idx):
    """Syarat entry V0 (sig): (1) SPY EMA50 > EMA200; (2) ROC65 < 100%; (3) SMA20 > 10;
    (4) SD250/SMA20 < 20%; (5) SMA20 x purata volum 250h > 5 juta; (6) EMA25 > EMA125 (pencetus). N = 6."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._e125) or np.isnan(r._vr):
        return None
    if not (bool(r._mkt) and bool(r._cair) and r._vr < 20 and r._roc65 < 1.0):
        return None
    # EMA esok: e' = a*c + (1-a)*e. Silang: c > [(1-a125)e125 - (1-a25)e25] / (a25 - a125)
    a25, a125 = 2 / 26, 2 / 126
    paras = ((1 - a125) * r._e125 - (1 - a25) * r._e25) / (a25 - a125)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'SPY EMA50 > EMA200; ROC65 < 100%; SMA20 > 10; kemeruapan < 20%; kecairan lulus; EMA25 ({r._e25:.2f}) di bawah EMA125 ({r._e125:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya EMA25 menyilang ke atas EMA125',
            'pencetus': 'Silang EMA25 > EMA125', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '5/6', 'skor': float(round(1 - jarak / 2, 2))}

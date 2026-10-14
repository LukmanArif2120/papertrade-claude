from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M47'
NAMA = 'Holy Grail Raschke'
VARIAN = 'V3 V1 tanpa syarat ADX naik'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _adx(g, n=14):
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
    return dx.ewm(alpha=a, adjust=False).mean(), pdi, mdi


def _tgt_tetap(g, sig, stop, tgt_isyarat, warm):
    """Cerminkan gelung trades() enjin supaya lajur tgt kekal pada nilai hari isyarat
    sepanjang dagangan (laporan M47: sasaran dikunci pada hari isyarat). Enjin tidak diubah."""
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g); tg = np.full(n, np.nan); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        T = tgt_isyarat[i]; sp = stop[i] if not np.isnan(stop[i]) else -np.inf
        j = i + 1
        while j < n:
            if j > i + 1 and o[j] <= sp: break
            if l[j] <= sp: break
            if not np.isnan(T) and j > i + 1:
                if o[j] >= T or h[j] >= T: break
            j += 1
        tg[i:min(j, n - 1) + 1] = T
        if j >= n: j = n - 1
        i = j + 1
    return tg


def sedia(fr, idx):
    for g in fr.values():
        adx, pdi, mdi = _adx(g)
        e20 = g.close.ewm(span=20, adjust=False).mean()
        kuat = adx > 30                          # V3: tanpa syarat ADX naik
        arah = pdi > mdi
        sentuh = (g.low <= e20) & (g.close.shift() > e20.shift())
        setup = kuat & arah & sentuh             # pada hari sentuhan (i-1)
        cetus = g.close > g.high.shift()
        puncak = g.high.rolling(20).max().shift(1)
        stop = g.low.shift()
        sig = setup.shift(1, fill_value=False) & cetus
        # Langkau jika buka masuk <= henti atau >= sasaran (kad). Bar terakhir: buka esok belum diketahui
        bo = g.open.shift(-1)
        sig = sig & ~((bo <= stop) | (bo >= puncak))
        sig = sig.fillna(False).astype(bool)
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _tgt_tetap(g, sig.values, stop.values.astype(float), puncak.values.astype(float), WARM)
        # Bar terakhir: sasaran isyarat hari ini
        if sig.iloc[-1]: g.iloc[-1, g.columns.get_loc('tgt')] = puncak.iloc[-1]
        g['exitc'] = False
        g['rank'] = g.close / g.close.shift(63) - 1
        g['_setup'] = setup; g['_e20'] = e20; g['_adx'] = adx; g['_puncak'] = puncak


def hampir(g, idx):
    # Syarat entry V3 (N=4): (1) ADX14 > 30 pada hari sentuhan; (2) +DI > -DI; (3) hari sentuhan:
    # low <= EMA20 dan tutup semalam > EMA20 semalam; (4) PENCETUS: tutup hari isyarat > high hari sentuhan.
    # Hampir: hari ini = hari sentuhan sah (1-3 dipenuhi), pencetus esok: tutup > high hari ini.
    # Andaian saya: penapis buka (buka masuk > henti dan < sasaran) tidak boleh dinilai sebelum buka; dinyatakan sahaja.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._setup):
        return None
    paras = float(r.high)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    sasaran = float(g.high.iloc[-20:].max())
    return {'sebab': f'ADX14 {r._adx:.1f} > 30; +DI > -DI; harga undur menyentuh EMA20 ({r._e20:.2f}) hari ini selepas tutup semalam di atas EMA20',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high hari sentuhan); masuk buka lusa hanya jika buka > {r.low:.2f} (henti) dan < {sasaran:.2f} (sasaran high 20 hari)',
            'pencetus': 'Tutup > high hari sentuhan', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 3))}

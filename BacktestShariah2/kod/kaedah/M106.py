from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M106'
NAMA = 'DMI Wilder'
VARIAN = 'V5 V1 dengan henti tutup-2xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _w14(x, n=14, start=1):
    # Pelicinan Wilder: nilai pertama = jumlah n nilai pertama (mula indeks `start`), kemudian lama - lama/n + semasa
    out = np.full(len(x), np.nan)
    if len(x) < start + n: return out
    out[start + n - 1] = x[start:start + n].sum()
    for i in range(start + n, len(x)):
        out[i] = out[i - 1] - out[i - 1] / n + x[i]
    return out


def _dmi(g, n=14):
    h, l, c = g.high.values, g.low.values, g.close.values
    tr = pd.concat([g.high - g.low, (g.high - g.close.shift()).abs(), (g.low - g.close.shift()).abs()], axis=1).max(axis=1).values
    up = np.r_[np.nan, h[1:] - h[:-1]]; dn = np.r_[np.nan, l[:-1] - l[1:]]
    pdm = np.where((up > dn) & (up > 0), up, 0.0); ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    # Andaian saya: pelicinan bermula indeks 1 (hari pertama ada DM)
    wtr, wp, wn = _w14(tr, n), _w14(pdm, n), _w14(ndm, n)
    with np.errstate(invalid='ignore', divide='ignore'):
        pdi = 100 * wp / wtr; ndi = 100 * wn / wtr
        dx = 100 * np.abs(pdi - ndi) / (pdi + ndi)
    adx = np.full(len(c), np.nan); f = n  # DX pertama sah pada indeks n
    if len(c) >= f + n:
        adx[f + n - 1] = np.nanmean(dx[f:f + n])
        for i in range(f + n, len(c)):
            adx[i] = (13 * adx[i - 1] + dx[i]) / 14
    atr14 = wtr / n
    return pd.Series(pdi, g.index), pd.Series(ndi, g.index), pd.Series(adx, g.index), pd.Series(atr14, g.index)


def sedia(fr, idx):
    for g in fr.values():
        pdi, ndi, adx, a14 = _dmi(g)
        silang = (pdi > ndi) & (pdi.shift() <= ndi.shift())
        stop = g.close - 2 * a14
        langkau = (g.open.shift(-1) <= stop).fillna(False)   # Andaian laporan: langkau jika buka masuk <= henti
        g['_pdi'] = pdi; g['_ndi'] = ndi; g['_adx'] = adx
        g['sig'] = silang & (adx > 25) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ndi > pdi
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def _di_esok(wtr, wp, wn, adx, h0, l0, c0, x, n=14):
    # Andaian saya: bar esok high = low = tutup = x (ikut arahan); pelicinan Wilder satu langkah
    up = x - h0; dn = l0 - x
    pdm = up if (up > dn and up > 0) else 0.0
    ndm = dn if (dn > up and dn > 0) else 0.0
    tr = max(0.0, abs(x - c0))
    wtr1 = wtr - wtr / n + tr; wp1 = wp - wp / n + pdm; wn1 = wn - wn / n + ndm
    pdi = 100 * wp1 / wtr1; ndi = 100 * wn1 / wtr1
    dx = 100 * abs(pdi - ndi) / (pdi + ndi) if pdi + ndi > 0 else 0.0
    return pdi, ndi, (13 * adx + dx) / 14


def hampir(g, idx):
    # Syarat entry V5 (3): (1) ADX14 > 25; (2) +DI <= -DI hari ini (belum silang);
    # (3) PENCETUS: +DI memotong ke atas -DI pada tutup esok, dengan ADX esok > 25
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._adx) or np.isnan(r._pdi) or np.isnan(r._ndi):
        return None
    if not (r._adx > 25):                               # 1
        return None
    if not (r._pdi <= r._ndi):                          # 2
        return None
    pdi, ndi, adx, a14 = _dmi(g)
    wtr = a14.iloc[-1] * 14; wp = pdi.iloc[-1] * wtr / 100; wn = ndi.iloc[-1] * wtr / 100
    h0, l0, c0 = float(r.high), float(r.low), float(r.close)
    ok = lambda x: (lambda t: t[0] > t[1] and t[2] > 25)(_di_esok(wtr, wp, wn, r._adx, h0, l0, c0, x))
    hi = c0 * 1.021
    if not ok(hi):                                      # tidak tercapai dalam 2%
        return None
    lo = max(h0, c0)                                    # bawah high hari ini +DM = 0, silang mustahil
    if ok(lo):
        paras = lo
    else:
        for _ in range(60):
            m = (lo + hi) / 2
            if ok(m): hi = m
            else: lo = m
        paras = hi
    jarak = (paras - c0) / c0 * 100
    if not (0 < jarak <= 2.0):
        return None
    return _hasil(f'ADX14 {r._adx:.1f} (> 25); +DI {r._pdi:.1f} masih di bawah -DI {r._ndi:.1f}',
                  f'Tutup esok > {paras:.2f} (anggaran: +DI memotong ke atas -DI dengan ADX kekal > 25, andaian high = low = tutup esok); '
                  f'henti = tutup isyarat - 2 x ATR14; masuk dibatalkan jika harga buka hari masuk <= henti',
                  'Silang +DI/-DI', paras, jarak, 2, 3)

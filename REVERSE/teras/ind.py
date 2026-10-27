"""Bateri indikator REVERSE. Tetapan standard sahaja; tiada penalaan.

Semua lajur hari t hanya menggunakan data hingga tutup hari t (lihat REVERSE/semak_hadapan.py).
Input: DataFrame indeks 'date' dengan lajur open, high, low, close, volume, turnover.
"""
import numpy as np
import pandas as pd

EPS = 1e-12


# ---------- pembantu ----------
def _wilder(s, n):
    """Pelicinan Wilder (RMA) dengan nilai awal = purata n pertama."""
    a = s.to_numpy(dtype='float64')
    out = np.full(a.size, np.nan)
    if a.size < n:
        return pd.Series(out, index=s.index)
    awal = np.nanmean(a[:n])
    out[n - 1] = awal
    for i in range(n, a.size):
        x = a[i]
        if not np.isfinite(x):
            x = 0.0
        out[i] = (out[i - 1] * (n - 1) + x) / n
    return pd.Series(out, index=s.index)


def _ema(s, n):
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def _pct(a, b):
    """Jarak % a dari b."""
    return (a / b.replace(0, np.nan) - 1.0) * 100.0


def _hari_sejak(cond):
    """Bilangan hari sejak cond terakhir True (0 jika hari ini True); NaN jika belum pernah."""
    c = cond.to_numpy(dtype=bool)
    out = np.full(c.size, np.nan)
    akhir = -1
    for i in range(c.size):
        if c[i]:
            akhir = i
        if akhir >= 0:
            out[i] = i - akhir
    return pd.Series(out, index=cond.index)


def _supertrend(h, l, c, atr, mult=3.0):
    """Arah Supertrend(10,3): +1 menaik, -1 menurun."""
    hl2 = ((h + l) / 2.0).to_numpy('float64')
    a = atr.to_numpy('float64')
    cc = c.to_numpy('float64')
    n = cc.size
    arah = np.full(n, np.nan)
    atas = hl2 + mult * a
    bawah = hl2 - mult * a
    fa, fb, d = np.nan, np.nan, 1
    for i in range(n):
        if not np.isfinite(a[i]):
            continue
        if not np.isfinite(fa):
            fa, fb, d = atas[i], bawah[i], 1
            arah[i] = d
            continue
        fa = min(atas[i], fa) if cc[i - 1] <= fa else atas[i]
        fb = max(bawah[i], fb) if cc[i - 1] >= fb else bawah[i]
        if d == 1 and cc[i] < fb:
            d = -1
        elif d == -1 and cc[i] > fa:
            d = 1
        arah[i] = d
    return pd.Series(arah, index=c.index)


def _psar(h, l, af0=0.02, afm=0.2, afs=0.02):
    """Arah PSAR: +1 jika PSAR di bawah harga (menaik), -1 jika di atas."""
    hh = h.to_numpy('float64')
    ll = l.to_numpy('float64')
    n = hh.size
    arah = np.full(n, np.nan)
    if n < 2:
        return pd.Series(arah, index=h.index)
    naik = hh[1] >= hh[0]
    sar = ll[0] if naik else hh[0]
    ep = hh[0] if naik else ll[0]
    af = af0
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if naik:
            if ll[i] < sar:
                naik, sar, ep, af = False, ep, ll[i], af0
            else:
                if hh[i] > ep:
                    ep, af = hh[i], min(af + afs, afm)
                sar = min(sar, ll[i - 1], ll[i])
        else:
            if hh[i] > sar:
                naik, sar, ep, af = True, ep, hh[i], af0
            else:
                if ll[i] < ep:
                    ep, af = ll[i], min(af + afs, afm)
                sar = max(sar, hh[i - 1], hh[i])
        arah[i] = 1 if naik else -1
    return pd.Series(arah, index=h.index)


# ---------- bateri utama ----------
def kira(g, spy=None, sektor_idx=None):
    """Pulangkan DataFrame indikator sejajar g.index.

    g        : DataFrame OHLCV ticker (indeks tarikh menaik).
    spy      : Series tutup SPY sejajar (untuk RS); None -> lajur RS NaN.
    sektor_idx: Series indeks sektor (tutup) sejajar; None -> lajur sektor NaN.
    """
    o, h, l, c, v = (g['open'], g['high'], g['low'], g['close'], g['volume'])
    d = pd.DataFrame(index=g.index)
    d['tutup'] = c
    d['buka'] = o

    # --- moving average ---
    ema9, ema21 = _ema(c, 9), _ema(c, 21)
    ma50 = c.rolling(50, min_periods=50).mean()
    ma150 = c.rolling(150, min_periods=150).mean()
    ma200 = c.rolling(200, min_periods=200).mean()
    d['ema9'], d['ema21'], d['ma50'], d['ma150'], d['ma200'] = ema9, ema21, ma50, ma150, ma200
    d['j_ema9'] = _pct(c, ema9)
    d['j_ema21'] = _pct(c, ema21)
    d['j_ma50'] = _pct(c, ma50)
    d['j_ma150'] = _pct(c, ma150)
    d['j_ma200'] = _pct(c, ma200)
    d['cerun_ema21'] = _pct(ema21, ema21.shift(10))
    d['cerun_ma50'] = _pct(ma50, ma50.shift(10))
    d['cerun_ma200'] = _pct(ma200, ma200.shift(10))
    d['lapis'] = ((ema9 > ema21).astype('float64') + (ema21 > ma50) + (ma50 > ma150) + (ma150 > ma200))
    d.loc[ma200.isna(), 'lapis'] = np.nan
    gc = (ma50 > ma200) & (ma50.shift(1) <= ma200.shift(1))
    d['hari_gc'] = _hari_sejak(gc)

    # --- momentum ---
    delta = c.diff()
    naik_w = _wilder(delta.clip(lower=0), 14)
    turun_w = _wilder((-delta).clip(lower=0), 14)
    rs = naik_w / (turun_w + EPS)
    d['rsi14'] = 100.0 - 100.0 / (1.0 + rs)
    n2 = _wilder(delta.clip(lower=0), 2)
    t2 = _wilder((-delta).clip(lower=0), 2)
    d['rsi2'] = 100.0 - 100.0 / (1.0 + n2 / (t2 + EPS))
    d['rsi_lintas50'] = ((d['rsi14'] > 50) & (d['rsi14'].shift(1) <= 50)).astype('float64')
    d['rsi_lintas60'] = ((d['rsi14'] > 60) & (d['rsi14'].shift(1) <= 60)).astype('float64')
    macd = _ema(c, 12) - _ema(c, 26)
    macd_sig = _ema(macd, 9)
    d['macd'], d['macd_sig'] = macd, macd_sig
    d['macd_hist'] = macd - macd_sig
    xm = (macd > macd_sig) & (macd.shift(1) <= macd_sig.shift(1))
    d['macd_cross'] = xm.astype('float64')
    d['hari_macd_cross'] = _hari_sejak(xm)
    d['macd_atas0'] = (macd > 0).astype('float64')
    ll14 = l.rolling(14, min_periods=14).min()
    hh14 = h.rolling(14, min_periods=14).max()
    stk = (c - ll14) / ((hh14 - ll14) + EPS) * 100.0
    d['stoch_k'] = stk
    d['stoch_d'] = stk.rolling(3, min_periods=3).mean()
    d['roc20'] = _pct(c, c.shift(20))
    d['roc60'] = _pct(c, c.shift(60))
    # ADX(14)
    up = h.diff()
    dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=c.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=c.index)
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    atr14 = _wilder(tr, 14)
    pdi = 100.0 * _wilder(pdm, 14) / (atr14 + EPS)
    mdi = 100.0 * _wilder(mdm, 14) / (atr14 + EPS)
    d['pdi'], d['mdi'] = pdi, mdi
    d['adx14'] = _wilder((100.0 * (pdi - mdi).abs() / (pdi + mdi + EPS)).fillna(0.0), 14)
    d['willr14'] = -100.0 * (hh14 - c) / ((hh14 - ll14) + EPS)
    tp = (h + l + c) / 3.0
    sma_tp = tp.rolling(20, min_periods=20).mean()
    md = (tp - sma_tp).abs().rolling(20, min_periods=20).mean()
    d['cci20'] = (tp - sma_tp) / (0.015 * md + EPS)

    # --- volatiliti ---
    d['atr14'] = atr14
    d['atr_pct'] = atr14 / (c + EPS) * 100.0
    d['nisbah_atr'] = atr14 / (_wilder(tr, 50) + EPS)
    m20 = c.rolling(20, min_periods=20).mean()
    s20 = c.rolling(20, min_periods=20).std(ddof=0)
    bb_a, bb_b = m20 + 2 * s20, m20 - 2 * s20
    d['bb_lebar'] = (bb_a - bb_b) / (m20 + EPS) * 100.0
    d['bb_pctb'] = (c - bb_b) / ((bb_a - bb_b) + EPS) * 100.0
    d['bb_squeeze'] = (d['bb_lebar'] <= d['bb_lebar'].rolling(120, min_periods=120).min() + EPS).astype('float64')
    d.loc[d['bb_lebar'].rolling(120, min_periods=120).min().isna(), 'bb_squeeze'] = np.nan
    ema20 = _ema(c, 20)
    d['kelt_pos'] = (c - ema20) / (2 * atr14 + EPS)
    d['julat10'] = (h.rolling(10, min_periods=10).max() - l.rolling(10, min_periods=10).min()) / (c + EPS) * 100.0
    d['julat20'] = (h.rolling(20, min_periods=20).max() - l.rolling(20, min_periods=20).min()) / (c + EPS) * 100.0

    # --- volum & aliran wang ---
    v50 = v.rolling(50, min_periods=50).mean()
    d['vol_n50'] = v / (v50 + EPS)
    d['vol_n50_5h'] = v.rolling(5, min_periods=5).mean() / (v50 + EPS)
    arah = np.sign(c.diff().fillna(0.0))
    obv = (arah * v).cumsum()
    d['obv_tinggi_baru'] = ((obv >= obv.rolling(50, min_periods=50).max() - EPS)
                            & (c < c.rolling(50, min_periods=50).max() - EPS)).astype('float64')
    mfv = (((c - l) - (h - c)) / ((h - l) + EPS)) * v
    ad = mfv.cumsum()
    d['ad_tinggi_baru'] = ((ad >= ad.rolling(50, min_periods=50).max() - EPS)
                           & (c < c.rolling(50, min_periods=50).max() - EPS)).astype('float64')
    vn = pd.Series(np.where(arah > 0, v, 0.0), index=c.index).rolling(20, min_periods=20).sum()
    vt = pd.Series(np.where(arah < 0, v, 0.0), index=c.index).rolling(20, min_periods=20).sum()
    d['vol_naik_turun20'] = vn / (vt + EPS)
    pmf = pd.Series(np.where(tp.diff() > 0, tp * v, 0.0), index=c.index).rolling(14, min_periods=14).sum()
    nmf = pd.Series(np.where(tp.diff() < 0, tp * v, 0.0), index=c.index).rolling(14, min_periods=14).sum()
    d['mfi14'] = 100.0 - 100.0 / (1.0 + pmf / (nmf + EPS))
    d['cmf20'] = mfv.rolling(20, min_periods=20).sum() / (v.rolling(20, min_periods=20).sum() + EPS)

    # --- trend lain ---
    d['supertrend'] = _supertrend(h, l, c, atr14)
    d['psar_arah'] = _psar(h, l)
    tenkan = (h.rolling(9, min_periods=9).max() + l.rolling(9, min_periods=9).min()) / 2.0
    kijun = (h.rolling(26, min_periods=26).max() + l.rolling(26, min_periods=26).min()) / 2.0
    sa = ((tenkan + kijun) / 2.0).shift(26)
    sb = ((h.rolling(52, min_periods=52).max() + l.rolling(52, min_periods=52).min()) / 2.0).shift(26)
    d['atas_awan'] = ((c > sa) & (c > sb)).astype('float64')
    d.loc[sb.isna(), 'atas_awan'] = np.nan
    d['tenkan_atas'] = (tenkan > kijun).astype('float64')
    d.loc[kijun.isna(), 'tenkan_atas'] = np.nan
    dc20 = h.rolling(20, min_periods=20).max().shift(1)
    dc55 = h.rolling(55, min_periods=55).max().shift(1)
    d['donchian20'] = (c > dc20).astype('float64')
    d.loc[dc20.isna(), 'donchian20'] = np.nan
    d['donchian55'] = (c > dc55).astype('float64')
    d.loc[dc55.isna(), 'donchian55'] = np.nan

    # --- corak harga ---
    d['inside_day'] = ((h < h.shift(1)) & (l > l.shift(1))).astype('float64')
    d['outside_day'] = ((h > h.shift(1)) & (l < l.shift(1))).astype('float64')
    jr = h - l
    d['nr7'] = (jr <= jr.rolling(7, min_periods=7).min() + EPS).astype('float64')
    d.loc[jr.rolling(7, min_periods=7).min().isna(), 'nr7'] = np.nan
    badan = (c - o).abs()
    d['hammer'] = (((np.minimum(o, c) - l) >= 2 * badan) & ((h - np.maximum(o, c)) <= badan)
                   & (jr > 0)).astype('float64')
    d['bullish_engulfing'] = ((c > o) & (c.shift(1) < o.shift(1)) & (c >= o.shift(1))
                              & (o <= c.shift(1))).astype('float64')
    turun_v = pd.Series(np.where(c.diff() < 0, v, np.nan), index=c.index)
    maks_turun10 = turun_v.rolling(10, min_periods=1).max()
    d['pocket_pivot'] = ((c > c.shift(1)) & (v >= maks_turun10) & (c > ema21)).astype('float64')
    d.loc[ema21.isna(), 'pocket_pivot'] = np.nan
    d['vcp'] = ((d['julat20'] <= 0.6 * d['julat20'].shift(40)) & (c > ma50)).astype('float64')
    d.loc[ma50.isna() | d['julat20'].shift(40).isna(), 'vcp'] = np.nan
    d['gap_and_go'] = ((o > h.shift(1) * 1.02) & (c > o) & (d['vol_n50'] >= 1.5)).astype('float64')
    d.loc[v50.isna(), 'gap_and_go'] = np.nan
    t52 = c.rolling(252, min_periods=252).max()
    r52 = c.rolling(252, min_periods=252).min()
    d['breakout_52w'] = (c >= t52 - EPS).astype('float64')
    d.loc[t52.isna(), 'breakout_52w'] = np.nan
    asas = c.rolling(60, min_periods=60).max().shift(1)
    ketat = d['julat20'].shift(1) <= d['julat20'].rolling(120, min_periods=120).quantile(0.30).shift(1)
    d['breakout_asas'] = ((c > asas) & ketat).astype('float64')
    d.loc[asas.isna(), 'breakout_asas'] = np.nan
    d['ema_crossback'] = ((c > ema21) & (c.shift(1) <= ema21.shift(1)) & (d['cerun_ma50'] > 0)).astype('float64')
    d.loc[ma50.isna(), 'ema_crossback'] = np.nan

    # --- kekuatan relatif ---
    d['j_52w_tinggi'] = _pct(c, t52)
    d['j_52w_rendah'] = _pct(c, r52)
    if spy is not None:
        s = spy.reindex(g.index)
        d['rs_spy_3b'] = _pct(c, c.shift(63)) - _pct(s, s.shift(63))
        d['rs_spy_6b'] = _pct(c, c.shift(126)) - _pct(s, s.shift(126))
        d['rs_spy_12b'] = _pct(c, c.shift(252)) - _pct(s, s.shift(252))
        garis = c / (s + EPS)
        d['garis_rs_tinggi'] = (garis >= garis.rolling(252, min_periods=252).max() - EPS).astype('float64')
        d.loc[garis.rolling(252, min_periods=252).max().isna(), 'garis_rs_tinggi'] = np.nan
    else:
        for k in ('rs_spy_3b', 'rs_spy_6b', 'rs_spy_12b', 'garis_rs_tinggi'):
            d[k] = np.nan
    if sektor_idx is not None:
        si = sektor_idx.reindex(g.index)
        d['sektor_1b'] = _pct(si, si.shift(21))
        d['sektor_atas_ma50'] = (si > si.rolling(50, min_periods=50).mean()).astype('float64')
        d.loc[si.rolling(50, min_periods=50).mean().isna(), 'sektor_atas_ma50'] = np.nan
    else:
        d['sektor_1b'] = np.nan
        d['sektor_atas_ma50'] = np.nan
    return d


def kira_indeks(ix):
    """Lajur konteks pasaran daripada tutup SPY/QQQ: {'spy_ma50','spy_ma200','qqq_ma50','qqq_ma200',
    'spy_cerun_ma50'} sebagai DataFrame indeks tarikh."""
    out = {}
    for nama, c in ix.items():
        p = nama.lower()
        ma50 = c.rolling(50, min_periods=50).mean()
        ma200 = c.rolling(200, min_periods=200).mean()
        out[f'{p}_ma50'] = (c > ma50).astype('float64')
        out[f'{p}_ma200'] = (c > ma200).astype('float64')
        out[f'{p}_cerun_ma50'] = _pct(ma50, ma50.shift(10))
    return pd.DataFrame(out)

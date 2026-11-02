"""Pembantu dikongsi bagi kaedah Nxx (kombinasi indikator REVERSE).

PERATURAN WAJIB: formula di sini ialah salinan **verbatim** daripada `REVERSE/teras/ind.py`
dan `REVERSE/step18_nxx.py`, bukan daripada `enjin.rsi`/`enjin.atr`. Sebabnya:

  * `enjin.rsi` guna `ewm(alpha=1/n, adjust=False)` tanpa benih purata-n;
  * `enjin.atr` guna `rolling(n).mean()` (purata mudah), bukan pelicinan Wilder.

Kedua-duanya BERBEZA daripada `_wilder` kajian. Kalau kaedah Nxx memakai pembantu enjin,
jejak hadapan akan mengukur peraturan yang bukan peraturan yang dikaji, dan kesemua nombor
`REVERSE/silang_akhir.csv` tidak lagi terpakai. `ujian/test_nxx_sepadan.py` membandingkan
keluaran fail ini dengan `REVERSE/teras/ind.py` pada harga sebenar dan GAGAL jika terpesong.

Rujukan nombor (REVERSE/silang_akhir.csv, 2 tingkap, BH-FDR, gate0-gate3 LULUS):
  GB02_atau3 x X13 -> jangkaan tahan +8.541%, lift +4.191/+1.818, menang 64.2%,
  n 195,681, p 0.0068, tanpa5 +2.858% (POSITIF - tidak bergantung ekor kanan).
"""
import numpy as np
import pandas as pd

EPS = 1e-12                 # ind.py:9
IMBAS = 126                 # step19_nxx_keluar.py:29 - ufuk keluar kajian = TMAX


def _wilder(s, n):
    """Pelicinan Wilder (RMA) dengan nilai awal = purata n pertama. ind.py:13."""
    a = s.to_numpy(dtype='float64')
    out = np.full(a.size, np.nan)
    if a.size < n:
        return pd.Series(out, index=s.index)
    out[n - 1] = np.nanmean(a[:n])
    for i in range(n, a.size):
        x = a[i]
        if not np.isfinite(x):
            x = 0.0
        out[i] = (out[i - 1] * (n - 1) + x) / n
    return pd.Series(out, index=s.index)


def _ema(s, n):
    """ind.py:29."""
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def _supertrend(h, l, c, atr, mult=3.0):
    """Arah Supertrend(10,3): +1 menaik, -1 menurun. ind.py:_supertrend verbatim."""
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
    """Arah PSAR: +1 jika PSAR di bawah harga, -1 jika di atas. ind.py:_psar verbatim."""
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


def indikator(g):
    """Lajur yang N19/N20/N37/N115 dan keluar X13 perlukan, formula kajian verbatim."""
    o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
    d = pd.DataFrame(index=g.index)

    # rsi14 - ind.py:143-147
    delta = c.diff()
    naik_w = _wilder(delta.clip(lower=0), 14)
    turun_w = _wilder((-delta).clip(lower=0), 14)
    d['rsi14'] = 100.0 - 100.0 / (1.0 + naik_w / (turun_w + EPS))

    # rsi2 - ind.py:148-150 (Connors; N16 memerlukannya)
    n2 = _wilder(delta.clip(lower=0), 2)
    t2 = _wilder((-delta).clip(lower=0), 2)
    d['rsi2'] = 100.0 - 100.0 / (1.0 + n2 / (t2 + EPS))

    # adx14 - ind.py:168-178
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=c.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=c.index)
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    atr14 = _wilder(tr, 14)
    pdi = 100.0 * _wilder(pdm, 14) / (atr14 + EPS)
    mdi = 100.0 * _wilder(mdm, 14) / (atr14 + EPS)
    d['adx14'] = _wilder((100.0 * (pdi - mdi).abs() / (pdi + mdi + EPS)).fillna(0.0), 14)

    # bb_pctb - ind.py:189-193
    m20 = c.rolling(20, min_periods=20).mean()
    s20 = c.rolling(20, min_periods=20).std(ddof=0)
    bb_a, bb_b = m20 + 2 * s20, m20 - 2 * s20
    d['bb_pctb'] = (c - bb_b) / ((bb_a - bb_b) + EPS) * 100.0

    # ema20 + sentuh_ema20 - ind.py:196, step18_nxx.py:72
    d['ema20'] = _ema(c, 20)
    d['sentuh_ema20'] = l <= d['ema20']

    # vol_n50 - ind.py:202-203
    v50 = v.rolling(50, min_periods=50).mean()
    d['vol_n50'] = v / (v50 + EPS)

    # gap_and_go - ind.py:256-257
    gg = (o > h.shift(1) * 1.02) & (c > o) & (d['vol_n50'] >= 1.5)
    d['gap_and_go'] = gg.astype('float64')
    d.loc[v50.isna(), 'gap_and_go'] = np.nan

    # purata bergerak - ind.py:124-127
    d['ema21'] = _ema(c, 21)
    d['ma20'], d['sd20'] = m20, s20
    for n in (50, 150, 200):
        d[f'ma{n}'] = c.rolling(n, min_periods=n).mean()

    # supertrend(10,3) - ind.py:222
    d['supertrend'] = _supertrend(h, l, c, atr14)

    # donchian55 - ind.py:233-237
    dc55 = h.rolling(55, min_periods=55).max().shift(1)
    d['donchian55'] = (c > dc55).astype('float64')
    d.loc[dc55.isna(), 'donchian55'] = np.nan

    # inside_day + nr7 - ind.py:240-243
    d['inside_day'] = ((h < h.shift(1)) & (l > l.shift(1))).astype('float64')
    jr = h - l
    d['nr7'] = (jr <= jr.rolling(7, min_periods=7).min() + EPS).astype('float64')
    d.loc[jr.rolling(7, min_periods=7).min().isna(), 'nr7'] = np.nan

    # julat20 - ind.py:199
    d['julat20'] = ((h.rolling(20, min_periods=20).max()
                     - l.rolling(20, min_periods=20).min()) / (c + EPS) * 100.0)

    # mdi - ind.py:177 (N28)
    d['mdi'] = mdi

    # julat10 - ind.py:198
    d['julat10'] = ((h.rolling(10, min_periods=10).max()
                     - l.rolling(10, min_periods=10).min()) / (c + EPS) * 100.0)

    # obv_tinggi_baru - ind.py:205-208
    arah = np.sign(c.diff().fillna(0.0))
    obv = (arah * v).cumsum()
    d['obv_tinggi_baru'] = ((obv >= obv.rolling(50, min_periods=50).max() - EPS)
                            & (c < c.rolling(50, min_periods=50).max() - EPS)
                            ).astype('float64')

    # pocket_pivot - ind.py:250-253
    turun_v = pd.Series(np.where(c.diff() < 0, v, np.nan), index=c.index)
    maks_turun10 = turun_v.rolling(10, min_periods=1).max()
    d['pocket_pivot'] = ((c > c.shift(1)) & (v >= maks_turun10)
                         & (c > d['ema21'])).astype('float64')
    d.loc[d['ema21'].isna(), 'pocket_pivot'] = np.nan

    # vcp - ind.py:254-255
    d['vcp'] = ((d['julat20'] <= 0.6 * d['julat20'].shift(40))
                & (c > d['ma50'])).astype('float64')
    d.loc[d['ma50'].isna() | d['julat20'].shift(40).isna(), 'vcp'] = np.nan

    # j_52w_tinggi - ind.py:258,270
    t52 = c.rolling(252, min_periods=252).max()
    d['j_52w_tinggi'] = (c / t52.replace(0, np.nan) - 1.0) * 100.0

    # purata bergerak tambahan - ind.py:124-128, step18.tambahan:54-56
    d['ema9'] = _ema(c, 9)
    d['ema10'] = _ema(c, 10)
    d['ema50'] = _ema(c, 50)
    d['ma10'] = c.rolling(10).mean()
    d['atr14'] = atr14
    d['j_ma200'] = (c / d['ma200'].replace(0, np.nan) - 1.0) * 100.0
    d['cerun_ema21'] = (d['ema21'] / d['ema21'].shift(10).replace(0, np.nan) - 1.0) * 100.0

    # macd - ind.py:153-155
    macd = _ema(c, 12) - _ema(c, 26)
    d['macd'] = macd
    d['macd_sig'] = _ema(macd, 9)

    # bb_squeeze - ind.py:191-195
    bb_lebar = (bb_a - bb_b) / (m20 + EPS) * 100.0
    d['bb_squeeze'] = (bb_lebar <= bb_lebar.rolling(120, min_periods=120).min()
                       + EPS).astype('float64')
    d.loc[bb_lebar.rolling(120, min_periods=120).min().isna(), 'bb_squeeze'] = np.nan

    # cmf20 - ind.py:219 (mfv = ind.py:216)
    mfv = (((c - l) - (h - c)) / ((h - l) + EPS)) * v
    d['cmf20'] = (mfv.rolling(20, min_periods=20).sum()
                  / (v.rolling(20, min_periods=20).sum() + EPS))

    # psar + ichimoku + donchian20 - ind.py:223-235
    d['psar_arah'] = _psar(h, l)
    tenkan = (h.rolling(9, min_periods=9).max() + l.rolling(9, min_periods=9).min()) / 2.0
    kijun = (h.rolling(26, min_periods=26).max() + l.rolling(26, min_periods=26).min()) / 2.0
    sa = ((tenkan + kijun) / 2.0).shift(26)
    sb = ((h.rolling(52, min_periods=52).max()
           + l.rolling(52, min_periods=52).min()) / 2.0).shift(26)
    d['atas_awan'] = ((c > sa) & (c > sb)).astype('float64')
    d.loc[sb.isna(), 'atas_awan'] = np.nan
    d['tenkan_atas'] = (tenkan > kijun).astype('float64')
    d.loc[kijun.isna(), 'tenkan_atas'] = np.nan
    dc20 = h.rolling(20, min_periods=20).max().shift(1)
    d['donchian20'] = (c > dc20).astype('float64')
    d.loc[dc20.isna(), 'donchian20'] = np.nan

    # bullish_engulfing - ind.py:248-249
    d['bullish_engulfing'] = ((c > o) & (c.shift(1) < o.shift(1)) & (c >= o.shift(1))
                              & (o <= c.shift(1))).astype('float64')

    # breakout_52w - ind.py:258-260
    t52c = c.rolling(252, min_periods=252).max()
    d['breakout_52w'] = (c >= t52c - EPS).astype('float64')

    # step18.tambahan:60-67
    d['tinggi_sepanjang'] = c.cummax().shift(1)
    d['tinggi_52w'] = h.rolling(252, min_periods=200).max().shift(1)
    julat = (h - l).replace(0, np.nan)
    d['pos_buka'] = (o - l) / julat
    d['pos_tutup'] = (c - l) / julat

    # step18_nxx.tambahan: tinggi20, gap, turun_4d5
    d['tinggi20'] = h.rolling(20).max().shift(1)
    d['gap'] = o / c.shift(1) - 1.0
    d['turun_4d5'] = (c < c.shift(1)).rolling(5).sum() >= 4

    return d


def _b(s):
    """Siri boolean tanpa NaN (NaN -> False), seperti `topeng()` kajian."""
    return s.fillna(False).astype(bool) if s.dtype == object else s.astype('float64').fillna(0.0) > 0.5


# ---------- topeng MASUK (step18_nxx.py:196,197,210,253) ----------
def n19(f):
    """Bawah jalur BB + RSI<30 (LuxAlgo). bb_pctb < 0 DAN rsi14 < 30."""
    return (f.bb_pctb < 0) & (f.rsi14 < 30)


def n20(f):
    """Kembali masuk jalur + RSI silang 30. bb_pctb[-1] < 0 DAN bb_pctb > 0 DAN rsi14 silang naik 30."""
    return (f.bb_pctb.shift(1) < 0) & (f.bb_pctb > 0) & (f.rsi14 > 30) & (f.rsi14.shift(1) <= 30)


def n37(f):
    """Gap and go. open > tinggi[-1] x 1.02 DAN tutup > open DAN vol_n50 >= 1.5."""
    return f.gap_and_go > 0


def n115(f, g):
    """Holy Grail (Raschke). adx14 > 30 DAN rendah menyentuh ema20 DAN tutup > tinggi[-1]."""
    return (f.adx14 > 30) & f.sentuh_ema20 & (g.close > g.high.shift(1))


def n16(f):
    """RSI2 < 10 tanpa penapis (Connors). `nxx.csv`: gate2 LULUS pada X2."""
    return f.rsi2 < 10


def n17(f):
    """RSI14 silang naik 30. `nxx.csv`: gate2 LULUS pada X2, lift +0.870/+1.264."""
    return (f.rsi14 > 30) & (f.rsi14.shift(1) <= 30)


def n75(f):
    """RSI14 < 40 tanpa penapis. `nxx.csv`: gate2 LULUS pada TIGA keluar (X2/X3/X4),
    dan jangkaan mutlak tertinggi antara semua topeng MASUK tunggal (+4.181% pada X3)."""
    return f.rsi14 < 40


# ---------- 7 topeng yang melepasi gate1 (lift positif dua tingkap) ----------
def n42(f, g):
    """Lonjakan volum + tutup naik. `vol_n50 >= 2.0 DAN tutup > tutup[-1]`."""
    return (f.vol_n50 >= 2.0) & (g.close > g.close.shift(1))


def n73(f, g):
    """Bawah jalur BB tanpa penapis RSI. SUPERSET tepat `N19` — menguji sama ada
    penapis `rsi14 < 30` menambah apa-apa (Jaccard N19/N73 ~0.30 = N19 subset N73)."""
    return g.close < (f.ma20 - 2.0 * f.sd20)


def n119(g):
    """Tiga tutup menurun berturut. `tutup[-2] > tutup[-1] DAN tutup[-1] > tutup`."""
    c = g.close
    return (c.shift(2) > c.shift(1)) & (c.shift(1) > c)


def n49(f):
    """Julat tersempit 7 hari DAN hari dalam. `nr7 DAN inside_day`."""
    return (f.nr7 > 0) & (f.inside_day > 0)


def n118(f, g):
    """Atas MA200 tetapi 4 daripada 5 sesi terakhir menurun."""
    return (g.close > f.ma200) & f.turun_4d5


def n46(f, g):
    """Undur ke EMA21 lalu pecah tinggi semalam."""
    return (g.low.shift(1) <= f.ema21.shift(1)) & (g.close > g.high.shift(1))


def n15(f, g):
    """RSI2 < 10 DAN atas MA200 (Connors dengan penapis trend)."""
    return (f.rsi2 < 10) & (g.close > f.ma200)


# ---------- 4 KAWALAN NEGATIF: lift tahan diukur NEGATIF, satu setiap keluarga gagal ----------
def n76(f, g):
    """KAWALAN `MA` (lift tahan −0.641). `tutup > ma50`."""
    return g.close > f.ma50


def n22(f):
    """`bb_pctb > 100 DAN rsi14 > 50` — tutup di ATAS jalur atas BB dengan momentum."""
    return (f.bb_pctb > 100) & (f.rsi14 > 50)


def n24(f):
    """KAWALAN `TREND` (lift tahan −0.161). `supertrend > 0 DAN adx14 > 20`."""
    return (f.supertrend > 0) & (f.adx14 > 20)


def n31(f):
    """KAWALAN `PECAH` (lift tahan −1.590). Pecah Donchian 55 hari."""
    return f.donchian55 > 0


def n62(f, g):
    """KAWALAN `POLA` (lift tahan −2.651, PALING BURUK dalam 65 dan satu-satunya dengan
    jangkaan mutlak negatif). `julat20 <= 0.08 x tutup DAN tutup > tinggi20[-1]`."""
    return (f.julat20 <= 0.08 * g.close) & (g.close > f.tinggi20)


# ---------- kes SOALAN REJIM: gagal gate1, dijejak dengan sengaja ----------
def n124(f):
    """Gap 8% + volum 2x. Lift tahan **+7.066** = TERTINGGI antara 65 topeng, hampir 2x
    `N19` — tetapi lift LATIH negatif, jadi ia GAGAL gate1 pradaftar.

    Dijejak bukan kerana ia dijangka berjaya, tetapi kerana jejak hadapan boleh membezakan
    dua tafsiran yang kajian tidak boleh: (a) peraturan gagal yang bernasib baik dalam
    2020-2025, atau (b) peraturan yang hanya berfungsi dalam rejim selepas 2020. Keputusan
    memasukkannya dibuat dengan mata terbuka bahawa ia gagal gate.
    """
    return (f.gap >= 0.08) & (f.vol_n50 >= 2.0)


def gb02_atau3(f, g):
    """KESATUAN N19 u N37 u N115 - konfigurasi yang melepasi KESEMUA empat gate."""
    return n19(f) | n37(f) | n115(f, g)


# ---------- 12 topeng tambahan bagi senarai grid penuh (step18_nxx.topeng verbatim) ----------
def n06(f, g):
    """`ma50` silang naik `ma200`."""
    return (f.ma50 > f.ma200) & (f.ma50.shift(1) <= f.ma200.shift(1))


def n25(f, g):
    """`supertrend > 0 DAN tutup > ema20 DAN adx14 > 23`."""
    return (f.supertrend > 0) & (g.close > f.ema20) & (f.adx14 > 23)


def n28(f):
    """`adx14 > 25 DAN mdi < adx14`."""
    return (f.adx14 > 25) & (f.mdi < f.adx14)


def n36(f):
    """`pocket_pivot` (volum > volum turun maks 10 hari, tutup naik, atas ema21)."""
    return f.pocket_pivot > 0


def n38(f):
    """`vcp` — julat20 <= 0.6x julat20[-40] DAN tutup > ma50."""
    return f.vcp > 0


def n40(f, g):
    """`obv_tinggi_baru DAN tutup > ma50`."""
    return (f.obv_tinggi_baru > 0) & (g.close > f.ma50)


def n50(f, g):
    """`julat10 < 0.5 x julat20 DAN vol_n50 >= 1.5 DAN tutup > tinggi[-1]`."""
    return ((f.julat10 < 0.5 * f.julat20) & (f.vol_n50 >= 1.5)
            & (g.close > g.high.shift(1)))


def n53(f):
    """`supertrend > 0 DAN adx14 > 25`."""
    return (f.supertrend > 0) & (f.adx14 > 25)


def n55(f):
    """`bb_pctb < 20 DAN rsi14 > 40 DAN adx14 > 20`."""
    return (f.bb_pctb < 20) & (f.rsi14 > 40) & (f.adx14 > 20)


def n56(f):
    """`rsi14 > 50 DAN adx14 > 20`."""
    return (f.rsi14 > 50) & (f.adx14 > 20)


def n64(f):
    """`gap_and_go DAN vol_n50 >= 2.0`."""
    return (f.gap_and_go > 0) & (f.vol_n50 >= 2.0)


def n65(f):
    """`gap_and_go DAN vol_n50 >= 1.5 DAN j_52w_tinggi >= -5%`."""
    return (f.gap_and_go > 0) & (f.vol_n50 >= 1.5) & (f.j_52w_tinggi >= -5.0)


# ---------- 21 topeng tambahan bagi senarai 95 (step18_nxx.topeng verbatim) ----------
def n07(f, g):
    """Hari PERTAMA `ma10 > ma20 > ma50`."""
    t = (f.ma10 > f.ma20) & (f.ma20 > f.ma50)
    lalu = (f.ma10.shift(1) > f.ma20.shift(1)) & (f.ma20.shift(1) > f.ma50.shift(1))
    return t & ~lalu


def n08(f, g):
    """`tutup > ema20 DAN (tutup - ema20) <= 1.5 x atr14`."""
    return (g.close > f.ema20) & ((g.close - f.ema20) <= 1.5 * f.atr14)


def n09(f, g):
    """`tutup > ema10 DAN tutup[-1] < ema10[-1] DAN tutup > ema50`."""
    return ((g.close > f.ema10) & (g.close.shift(1) < f.ema10.shift(1))
            & (g.close > f.ema50))


def n27(f):
    """`atas_awan DAN tenkan_atas` (Ichimoku)."""
    return (f.atas_awan > 0) & (f.tenkan_atas > 0)


def n29(f, g):
    """`psar_arah > 0 DAN tutup > ma50`."""
    return (f.psar_arah > 0) & (g.close > f.ma50)


def n33(f):
    """`donchian20 pecah DAN j_ma200 > 0`."""
    return (f.donchian20 > 0) & (f.j_ma200 > 0)


def n35(f):
    """`breakout_52w`."""
    return f.breakout_52w > 0


def n39(f):
    """`nr7[-1] DAN donchian20`."""
    return (f.nr7.shift(1) > 0) & (f.donchian20 > 0)


def n41(f, g):
    """`cmf20 > 0 DAN tutup > ema20`."""
    return (f.cmf20 > 0) & (g.close > f.ema20)


def n43(f, g):
    """`tutup[-1] < ema9[-1] DAN tutup > ema9 DAN tutup > ma50`."""
    return ((g.close.shift(1) < f.ema9.shift(1)) & (g.close > f.ema9)
            & (g.close > f.ma50))


def n45(f, g):
    """`tutup > ema21 DAN cerun_ema21 > 0 DAN julat10 < julat20`."""
    return (g.close > f.ema21) & (f.cerun_ema21 > 0) & (f.julat10 < f.julat20)


def n47(f, g):
    """`nr7 DAN ema9 > ema21 DAN tutup > ema21`."""
    return (f.nr7 > 0) & (f.ema9 > f.ema21) & (g.close > f.ema21)


def n48(f, g):
    """`inside_day[-1] DAN tutup > tinggi[-1]`."""
    return (f.inside_day.shift(1) > 0) & (g.close > g.high.shift(1))


def n51(f):
    """`bb_squeeze DAN supertrend > 0`."""
    return (f.bb_squeeze > 0) & (f.supertrend > 0)


def n54(f):
    """`supertrend > 0 DAN rsi14 > 50`."""
    return (f.supertrend > 0) & (f.rsi14 > 50)


def n57(f, g):
    """`adx14 > 20 DAN adx14[-1] <= 20 DAN tutup > ma50`."""
    return (f.adx14 > 20) & (f.adx14.shift(1) <= 20) & (g.close > f.ma50)


def n66(f, g):
    """`tutup > 1.01 x tinggi_52w[-1]`."""
    return g.close > 1.01 * f.tinggi_52w


def n68(f, g):
    """`bullish_engulfing DAN tutup > ema21`."""
    return (f.bullish_engulfing > 0) & (g.close > f.ema21)


def n74(f):
    """`macd > macd_sig`."""
    return f.macd > f.macd_sig


def n80(f, g):
    """`tutup >= tutup tertinggi sepanjang masa`."""
    return g.close >= f.tinggi_sepanjang


def n113(f):
    """Buka dalam 20% BAWAH julat hari DAN tutup dalam 20% ATAS julat."""
    return (f.pos_buka <= 0.2) & (f.pos_tutup >= 0.8)


# ---------- keluar (lorong 1) ----------
def x13(f):
    """X13 - keluar bila rsi14 > 70; enjin menjual pada buka esok. Keluar TERBAIK diukur
    (asas +4.350%), dan satu-satunya yang asasnya POSITIF selepas buang 5% teratas."""
    return f.rsi14 > 70


def u14(g):
    """`U14` momentum 12-1 bulan = C[-21] / C[-252] - 1. step27_keluar_portfolio.py:56.

    Dipakai sebagai `rank` kerana `harian_c.MAKS_KAEDAH` mengehadkan 10 isyarat baharu
    setiap kaedah setiap imbasan dan memilih ikut `rank`. Dengan `rank = 0` pemilihan
    antara isyarat menjadi **sewenang-wenang**, dan `KEPEKATAN_BENIH.md` mengukur hingar
    pemilihan susunan sewenang-wenang pada **17.3 mata peratus setahun** pada 8 slot.
    `SISTEM.md` mengukur bahawa memeringkat ikut skor objektif BERTERUSAN memberi sebaran
    benih **0.00**, jadi pemeringkat berterusan menghapuskan hingar itu.

    `U14` dipilih kerana (a) ia pemeringkat paling KERAP antara pemenang `E6a` dan (b) ia
    boleh dikira daripada harga sahaja.

    **DUA PEMBETULAN 1 Nov 2026** (`REVERSE/AUDIT_JEJAK_N.md`), kedua-duanya disahkan terhadap
    CSV sumber:

    1. Dakwaan asal "setiap pemenang `E6a` memakai U14" (dalam `HIERARKI.md` dan
       `SPEC_JEJAK_N.md`) **SALAH**. 19 pemenang terbahagi **U14 11 · U01 8 · U02 0** — jadi
       **8 daripada 19 memakai `U01` yang RAWAK**, dan kelebihan U14 atas susunan rawak dalam
       E6 jauh lebih kecil daripada yang dinyatakan.
    2. Perbandingan "`U02` ... 16.12 lawan 11.93 pada 8 slot" membandingkan **DUA MASUK
       BERBEZA** (16.12 = `GB02_atau3,8,X13,U02`; 11.93 = `GB02_atau4,8,X13,U01`). Bagi masuk
       yang SAMA (`GB02_atau3,8,X13`): U02 16.12 · U01 9.40 · U08 8.83. Dan `U14` **tiada
       dalam `portfolio_n_ringkas.csv` sama sekali** — lajur urutan hanya U01/U02/U08, jadi
       pemeringkat yang sebenarnya dipasang di sini **tidak pernah diuji pada peringkat
       portfolio bagi mana-mana masuk Nxx**.

    Sebab tinggal untuk memakai U14 kekal sah tetapi lebih sempit: ia skor BERTERUSAN (jadi ia
    menghapuskan hingar pemilihan 17.3 mata/tahun yang susunan sewenang-wenang suntik) dan ia
    boleh dikira daripada harga sahaja. Itu sahaja. Ia BUKAN "pemeringkat terbaik yang diukur".
    """
    c = g.close
    s = c.shift(21) / c.shift(252) - 1.0
    return s.replace([np.inf, -np.inf], np.nan).fillna(-9e9)


def x14(f):
    """`X14` — keluar bila `rsi14` silang naik 50. step19:124 verbatim."""
    return (f.rsi14 > 50) & (f.rsi14.shift(1) <= 50)


def x16(f):
    """`X16` — keluar bila supertrend berbalik (`supertrend <= 0`). step19:127."""
    return f.supertrend <= 0


def x17(f):
    """`X17` — keluar bila `adx14 < 20`. step19:128."""
    return f.adx14 < 20


def x36(f, g):
    """`X36` — keluar selepas DUA tutup berturut di bawah `ma50`. step19:142-143."""
    b = g.close < f.ma50
    return b & b.shift(1).fillna(False)


KELUAR_FN = {'X13': lambda f, g: x13(f), 'X14': lambda f, g: x14(f),
             'X16': lambda f, g: x16(f), 'X17': lambda f, g: x17(f),
             'X36': lambda f, g: x36(f, g),
             # X15 = Chandelier mengekor. Enjin v1.2 membaca `stop` SEKALI pada bar
             # isyarat (enjin.py:31 `sp = st[i]`), jadi henti MENGEKOR tidak boleh
             # dilaksanakan sebagai lorong 1 — diuji dan disahkan. Tetapi lorong 2 repo
             # IALAH X15, dan ia berjalan automatik pada setiap posisi. Jadi kohort X15
             # dikod TANPA keluar kaedah dan lorong 2 ialah keluarnya.
             'X15': None}


# Peta nama topeng -> fungsi, supaya `ujian/test_nxx_sepadan.py` boleh menguji pariti
# SETIAP topeng terhadap `step18_nxx.topeng()` tanpa transkripsi tangan (audit F6).
TOPENG_FN = {
    'N06': lambda f, g: n06(f, g),
    'N07': lambda f, g: n07(f, g),
    'N08': lambda f, g: n08(f, g),
    'N09': lambda f, g: n09(f, g),
    'N16': lambda f, g: n16(f),
    'N19': lambda f, g: n19(f),
    'N22': lambda f, g: n22(f),
    'N24': lambda f, g: n24(f),
    'N25': lambda f, g: n25(f, g),
    'N27': lambda f, g: n27(f),
    'N28': lambda f, g: n28(f),
    'N29': lambda f, g: n29(f, g),
    'N31': lambda f, g: n31(f),
    'N33': lambda f, g: n33(f),
    'N35': lambda f, g: n35(f),
    'N36': lambda f, g: n36(f),
    'N37': lambda f, g: n37(f),
    'N38': lambda f, g: n38(f),
    'N39': lambda f, g: n39(f),
    'N40': lambda f, g: n40(f, g),
    'N41': lambda f, g: n41(f, g),
    'N42': lambda f, g: n42(f, g),
    'N43': lambda f, g: n43(f, g),
    'N45': lambda f, g: n45(f, g),
    'N47': lambda f, g: n47(f, g),
    'N48': lambda f, g: n48(f, g),
    'N50': lambda f, g: n50(f, g),
    'N51': lambda f, g: n51(f),
    'N53': lambda f, g: n53(f),
    'N54': lambda f, g: n54(f),
    'N55': lambda f, g: n55(f),
    'N56': lambda f, g: n56(f),
    'N57': lambda f, g: n57(f, g),
    'N64': lambda f, g: n64(f),
    'N65': lambda f, g: n65(f),
    'N66': lambda f, g: n66(f, g),
    'N68': lambda f, g: n68(f, g),
    'N73': lambda f, g: n73(f, g),
    'N74': lambda f, g: n74(f),
    'N75': lambda f, g: n75(f),
    'N76': lambda f, g: n76(f, g),
    'N80': lambda f, g: n80(f, g),
    'N113': lambda f, g: n113(f),
    'N119': lambda f, g: n119(g),
    'N124': lambda f, g: n124(f),
}


def pasang(g, masuk, f=None, nama_rank=None, keluar='X13'):
    """Tulis lajur enjin v1.2. TIADA henti dan TIADA sasaran dengan sengaja:

    * `stop = NaN` -> `enjin.trades` guna `sp = -inf`, jadi kecacatan henti hari-0
      (`REVERSE/KOLAM_EKOR.md` §4a: 421/1,770 posisi, menang 0.00%) **tidak boleh berlaku**;
    * `tgt = NaN` -> tiada sasaran untung, kerana `KOMBINASI.md` mengukur sasaran 1xATR
      menukar asas +2.595% menjadi -0.281%.

    Lorong 2 repo (Chandelier tutup 4xATR14) = `X15` kajian dan berjalan automatik pada
    setiap posisi, jadi X13 dan X15 terukur BERSEBELAHAN tanpa kod tambahan.

    `rank` = `u14()` dan BUKAN 0.0 — lihat `u14` untuk sebabnya (hingar pemilihan 17.3
    mata/tahun kalau susunan sewenang-wenang).
    """
    if f is None:                      # pemanggil biasanya sudah mengiranya;
        f = indikator(g)               # `indikator()` ialah kos CPU termahal saluran
    g['sig'] = masuk.fillna(False).astype(bool)
    g['stop'] = np.nan
    g['tgt'] = np.nan
    fn = KELUAR_FN[keluar]
    g['exitc'] = (pd.Series(False, index=g.index) if fn is None
                  else fn(f, g).fillna(False).astype(bool))
    g['rank'] = u14(g) if nama_rank is None else f[nama_rank].fillna(-9e9).astype('float64')
    return f
    return f


def hampir_syarat(syarat, n_bar, cukup):
    """Watchlist "hampir" generik bagi kaedah Nxx.

    `syarat` = senarai (label, dipenuhi, jarak_unit) bagi bar TERAKHIR. Jarak dalam unit
    indikator sendiri (mata RSI, mata %b, mata ADX) kerana peraturan Nxx ialah ambang
    indikator, bukan paras harga: melaporkan "paras harga" akan mengandaikan hubungan
    harga->indikator yang tidak linear, jadi `paras` dibiar None dengan sengaja.
    """
    if n_bar < cukup:
        return None
    ok = [s for s in syarat if s[1]]
    belum = [s for s in syarat if not s[1]]
    if not belum or not ok:                 # semua sudah (= sig) atau semua belum (terlalu jauh)
        return None
    jarak = [s[2] for s in belum if s[2] is not None]
    j = float(min(jarak)) if jarak else None
    return {'sebab': ' DAN '.join(s[0] for s in ok) + ' sudah',
            'syarat_beli': ' DAN '.join(s[0] for s in syarat),
            'pencetus': ' DAN '.join(s[0] for s in belum),
            'paras': None,
            'jarak_pct': j,
            'syarat_dipenuhi': f'{len(ok)}/{len(syarat)}',
            'skor': 0.5 if j is None else round(float(max(0.0, 1.0 - j / 20.0)), 3)}

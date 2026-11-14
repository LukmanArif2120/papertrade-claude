"""Carian setup CS01 — atom: pencetus, penapis dan atom keluar (pradaftar `kajian/SPEC_CARIAN_SETUP.md`).

Semua nilai bar i hanya memakai data <= i (tiada pandang ke hadapan; diuji `ujian/test_carian_setup.py`).
Isyarat dikira pada TUTUP bar i; pembelian berlaku pada BUKA bar i+1 (lihat `cs_teras.py`).
Senarai PENCETUS, PENAPIS dan KELUAR di bawah ialah sebahagian daripada pradaftar: jangan ubah tanpa pindaan
bertarikh pada spec.
"""
import numpy as np
import pandas as pd

BENIH = 20261113
TMAX = 20                     # sesi pegang maksimum (sesi 1 = hari beli)
KOS = 0.005                   # kos pusingan
PEGANG_MIN = 3                # pindaan 14 Nov 2026 (p): indikator keluar hanya menjual mulai buka sesi ke-4
HENTI = ['H1 -8%', 'H2 -10%', 'H3 3xATR14', 'H4 4xATR14']

PENCETUS = [
    'P01 MACD silang naik', 'P02 MACD silang naik bawah sifar', 'P03 MACD silang naik atas sifar',
    'P04 MA5 silang atas MA20', 'P05 MA10 silang atas MA20', 'P06 MA10 silang atas MA50',
    'P07 MA20 silang atas MA50', 'P08 MA50 silang atas MA200', 'P09 tutup silang atas MA20',
    'P10 tutup silang atas MA50', 'P11 tutup silang atas MA200', 'P12 RSI14 silang atas 50',
    'P13 RSI14 silang atas 60', 'P14 RSI14 silang atas 30', 'P15 RSI2<10 atas MA200', 'P16 RSI2<5 atas MA200',
    'P17 pecah atas Keltner', 'P18 pecah atas jalur atas Bollinger', 'P19 bawah jalur bawah Bollinger + RSI14<30',
    'P20 squeeze lepas ke atas', 'P21 Supertrend bertukar naik', 'P22 ADX silang atas 25 & +DI>-DI',
    'P23 Ichimoku pecah atas awan', 'P24 Stochastic silang naik dari bawah 20', 'P25 pecah tinggi 20 hari',
    'P26 pecah tinggi 55 hari', 'P27 pecah tinggi 126 hari', 'P28 pecah tinggi 252 hari',
    'P29 Holy Grail (ADX>30, undur EMA20, tutup > tinggi semalam)', 'P30 gap and go', 'P31 episodic pivot',
    'P32 lonjakan >=4% + volum 2x', 'P33 lonjakan selepas tidur (julat 60 hari <=30%)',
    'P34 pecah tapak 3 bulan + volum', 'P35 pecah tinggi 6 bulan + volum',
    'P36 tinggi 52 minggu pertama selepas 6 bulan', 'P37 Stage 1->2 (silang MA150 mendatar + volum)',
    'P38 bangkit dari jatuh (silang MA50 + volum)', 'P39 volum kering kemudian meletup', 'P40 pocket pivot',
    'P41 squeeze panjang lepas + volum', 'P42 VCP', 'P43 Qullamaggie', 'P44 RS baru masuk 10% teratas',
    'P45 pemimpin undur ke MA20', "P46 O'Neil pecah 50 hari + volum + RS", 'P47 undur ke MA50 yang naik',
    'P48 EMA crossback', 'P49 pecah tinggi hari gap',
]
PENAPIS = [
    'F01 tutup > MA20', 'F02 tutup > MA50', 'F03 tutup > MA200', 'F04 MA20 > MA50', 'F05 MA50 > MA200',
    'F06 MA50 naik (lawan 20 bar lalu)', 'F07 templat trend Minervini', 'F08 RSI14 > 50', 'F09 RSI14 > 60',
    'F10 RSI14 < 40', 'F11 MACD > isyarat', 'F12 MACD > 0', 'F13 ADX > 25', 'F14 ADX < 20', 'F15 Supertrend naik',
    'F16 RS >= 70', 'F17 RS >= 90', 'F18 dalam 15% dari puncak 52 minggu', 'F19 dalam 5% dari puncak 52 minggu',
    'F20 >= 30% di bawah puncak 52 minggu', 'F21 volum hari isyarat >= 1.5x purata 50',
    'F22 volum 10 hari > volum 50 hari', 'F23 ATR% >= 4', 'F24 ATR% <= 2.5', 'F25 squeeze hidup',
    'F26 rejim QQQ ON', 'F27 rejim QQQ OFF', 'F28 SPY > SMA200', 'F29 tutup dalam 25% teratas julat hari',
    'F30 hari naik (tutup > buka)',
]
KELUAR = [
    'X01 tutup < MA10', 'X02 tutup < MA20', 'X03 tutup < MA50', 'X04 tutup < EMA10', 'X05 tutup < EMA20',
    'X06 dua tutup berturut < MA10', 'X07 dua tutup berturut < MA20', 'X08 MA10 < MA20', 'X09 MACD < isyarat',
    'X10 histogram MACD turun 3 hari', 'X11 RSI14 < 50', 'X12 RSI14 silang turun bawah 70', 'X13 RSI14 > 80',
    'X14 Supertrend turun', 'X15 tutup < rendah 3 hari', 'X16 tutup < rendah 5 hari', 'X17 tutup < rendah 10 hari',
    'X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli)', 'X19 Chandelier 2xATR14',
    'X20 tutup < 92% tutup tertinggi sejak beli', 'X21 Stochastic silang turun di atas 80',
    'X22 hari turun dengan volum >= 1.5x', 'X23 tutup < buka dan < rendah semalam', 'X24 +DI < -DI',
]
LALUAN = {17: ('chand', 3.0), 18: ('chand', 2.0), 19: ('ekor', 0.92)}   # atom yang bergantung pada laluan sejak beli
TEMPOH = {
    '431': (('Latih', 20200102, 20230630), ('Sah', 20230703, 20260828)),
    'kunci': (('K1', 20100104, 20191231), ('K2', 20200102, 20260828)),
    # CS02 (pindaan 13 Nov 2026 (b)): kumpulan A = cari, kumpulan B = Kunci; K3 = tempoh yang tidak dipakai carian
    'A': (('E1', 20100104, 20191231), ('E2', 20200102, 20241231)),
    'B': (('K1', 20100104, 20191231), ('K2', 20200102, 20241231), ('K3', 20250102, 20260828)),
    # jejak hadapan kohort F (pindaan 13 Nov 2026 (f)): hanya isyarat pada atau selepas 2026-11-13
    'hadapan': (('H', 20261113, 20991231),),
}


def _wilder(s, n):
    return s.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def _silang(a, b):
    return (a > b) & (a.shift() <= b.shift())


def _dulu(s, k=1):
    """Nilai boolean k bar lalu (False jika tiada)."""
    return s.astype(bool).shift(k, fill_value=False)


def _supertrend(h, l, c, atr, m=3.0):
    n = len(c)
    arah = np.ones(n)
    hl = (h + l) / 2
    ub, lb = hl + m * atr, hl - m * atr
    fu, fl = ub.copy(), lb.copy()
    for i in range(1, n):
        if np.isnan(atr[i - 1]) or np.isnan(atr[i]):
            continue
        fu[i] = ub[i] if (ub[i] < fu[i - 1] or c[i - 1] > fu[i - 1]) else fu[i - 1]
        fl[i] = lb[i] if (lb[i] > fl[i - 1] or c[i - 1] < fl[i - 1]) else fl[i - 1]
        arah[i] = 1 if c[i] > fu[i - 1] else (-1 if c[i] < fl[i - 1] else arah[i - 1])
    return arah


def indikator(g, rs, qqq_on, spy_atas):
    """g: DataFrame satu saham (open high low close volume). rs/qqq_on/spy_atas: Series sejajar g.index.
    Pulangkan (pencetus, penapis, keluar, atr14): tiga dict nama -> ndarray bool, dan ndarray ATR14."""
    o_, h_, l_, c_, v_ = g.open, g.high, g.low, g.close, g.volume.astype(float)
    pc = c_.shift()
    tr = pd.concat([h_ - l_, (h_ - pc).abs(), (l_ - pc).abs()], axis=1).max(axis=1)
    atr14, atr10, atr20 = _wilder(tr, 14), _wilder(tr, 10), tr.rolling(20).mean()
    dl = c_.diff()

    def rsi(n):
        return 100 - 100 / (1 + _wilder(dl.clip(lower=0), n) / _wilder((-dl).clip(lower=0), n).replace(0, np.nan))

    rsi14, rsi2 = rsi(14), rsi(2)
    um, dm = h_.diff(), -l_.diff()
    pdm = pd.Series(np.where((um > dm) & (um > 0), um, 0.0), index=g.index)
    ndm = pd.Series(np.where((dm > um) & (dm > 0), dm, 0.0), index=g.index)
    pdi, ndi = 100 * _wilder(pdm, 14) / atr14, 100 * _wilder(ndm, 14) / atr14
    adx = _wilder(100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan), 14)
    ma = {n: c_.rolling(n).mean() for n in (5, 10, 20, 50, 150, 200)}

    def ema(n):
        return c_.ewm(span=n, adjust=False, min_periods=n).mean()

    ema10, ema20 = ema(10), ema(20)
    macd = ema(12) - ema(26)
    sig = macd.ewm(span=9, adjust=False).mean()
    hist = macd - sig
    sd20 = c_.rolling(20).std(ddof=0)
    bb_a, bb_b = ma[20] + 2 * sd20, ma[20] - 2 * sd20

    def hh(n):                                  # tinggi n bar SEBELUM hari ini
        return h_.rolling(n).max().shift(1)

    def ll(n):
        return l_.rolling(n).min().shift(1)

    h252, l252 = h_.rolling(252).max(), l_.rolling(252).min()
    v50 = v_.rolling(50).mean().shift(1)
    vr = v_ / v50.replace(0, np.nan)
    ret1, gap = c_ / pc - 1, o_ / pc - 1
    pos = (c_ - l_) / (h_ - l_).replace(0, np.nan)
    kc_atas = ema20 + 2 * atr20
    sq_on = (bb_a < ma[20] + 1.5 * atr20) & (bb_b > ma[20] - 1.5 * atr20)
    mom = c_ - ((h_.rolling(20).max() + l_.rolling(20).min()) / 2 + ma[20]) / 2
    sq_lepas = (~sq_on) & _dulu(sq_on) & (mom > 0)
    st = pd.Series(_supertrend(h_.to_numpy(float), l_.to_numpy(float), c_.to_numpy(float), atr10.to_numpy(float)),
                   index=g.index)
    tenkan = (h_.rolling(9).max() + l_.rolling(9).min()) / 2
    kijun = (h_.rolling(26).max() + l_.rolling(26).min()) / 2
    awan = pd.concat([((tenkan + kijun) / 2).shift(26),
                      ((h_.rolling(52).max() + l_.rolling(52).min()) / 2).shift(26)], axis=1).max(axis=1)
    stk = 100 * (c_ - l_.rolling(14).min()) / (h_.rolling(14).max() - l_.rolling(14).min()).replace(0, np.nan)
    sk = stk.rolling(3).mean()
    sdd = sk.rolling(3).mean()
    templat = ((c_ > ma[50]) & (ma[50] > ma[150]) & (ma[150] > ma[200]) & (ma[200] > ma[200].shift(20))
               & (c_ >= 0.75 * h252) & (c_ >= 1.3 * l252))
    julat60 = hh(60) / ll(60) - 1
    v10 = v_.rolling(10).mean()
    kering = v10 <= v10.rolling(60).min() * 1.05
    turun_v = v_.where(c_ < pc, 0.0).rolling(10).max().shift(1)
    baru252 = h_ >= h252
    gapday = (gap >= 0.05) & (vr >= 2)
    gh = h_.where(gapday).ffill(limit=10)
    bwh50, bwh150 = (c_ < ma[50]).astype(float), (c_ < ma[150]).astype(float)
    lonjak = (ret1 >= 0.04) & (vr >= 2) & (pos >= 0.75)
    k = lambda x: pd.Series(float(x), index=g.index)

    P = {
        'P01': _silang(macd, sig), 'P02': _silang(macd, sig) & (macd < 0), 'P03': _silang(macd, sig) & (macd > 0),
        'P04': _silang(ma[5], ma[20]), 'P05': _silang(ma[10], ma[20]), 'P06': _silang(ma[10], ma[50]),
        'P07': _silang(ma[20], ma[50]), 'P08': _silang(ma[50], ma[200]), 'P09': _silang(c_, ma[20]),
        'P10': _silang(c_, ma[50]), 'P11': _silang(c_, ma[200]), 'P12': _silang(rsi14, k(50)),
        'P13': _silang(rsi14, k(60)), 'P14': _silang(rsi14, k(30)), 'P15': (rsi2 < 10) & (c_ > ma[200]),
        'P16': (rsi2 < 5) & (c_ > ma[200]), 'P17': _silang(c_, kc_atas), 'P18': _silang(c_, bb_a),
        'P19': (c_ < bb_b) & (rsi14 < 30), 'P20': sq_lepas, 'P21': (st > 0) & (st.shift() < 0),
        'P22': _silang(adx, k(25)) & (pdi > ndi), 'P23': _silang(c_, awan) & (tenkan > kijun),
        'P24': _silang(sk, sdd) & (sk.shift() < 20), 'P25': c_ > hh(20), 'P26': c_ > hh(55), 'P27': c_ > hh(126),
        'P28': c_ > hh(252), 'P29': (adx > 30) & (l_ <= ema20) & (c_ > h_.shift(1)),
        'P30': (o_ > h_.shift(1) * 1.02) & (c_ > o_) & (vr >= 1.5), 'P31': (gap >= 0.08) & (vr >= 3) & (c_ >= o_),
        'P32': lonjak, 'P33': lonjak & (julat60 <= 0.30),
        'P34': (c_ > hh(60)) & (julat60 <= 0.35) & (vr >= 1.5), 'P35': (c_ > hh(126)) & (vr >= 1.5),
        'P36': baru252 & ~(_dulu(baru252).astype(float).rolling(126).max().fillna(0) > 0),
        'P37': (_silang(c_, ma[150]) & ((ma[150] / ma[150].shift(20) - 1).abs() <= 0.02) & (vr >= 1.5)
                & (bwh150.shift(1).rolling(100).mean() >= 0.5)),
        'P38': ((c_ <= 0.7 * h252) & _silang(c_, ma[50]) & (bwh50.shift(1).rolling(50).mean() >= 0.8)
                & (vr >= 1.5)),
        'P39': (_dulu(kering).astype(float).rolling(10).max().fillna(0) > 0) & (vr >= 2) & (ret1 >= 0.02),
        'P40': (c_ > pc) & (v_ > turun_v) & (c_ > ma[50]) & (c_ <= 1.05 * ma[10]),
        'P41': sq_lepas & (sq_on.astype(float).shift(1).rolling(20).sum() >= 15) & (vr >= 1.5),
        'P42': _dulu(templat) & ((hh(10) / ll(10) - 1) <= 0.10) & (c_ > hh(10)) & (vr >= 1.5),
        'P43': (((c_.shift(10) / c_.shift(50) - 1) >= 0.30) & ((hh(10) / ll(10) - 1) <= 0.15) & (c_ > hh(10))
                & (vr >= 1.5) & (c_ > ma[20])),
        'P44': (rs >= 90) & (rs.shift(1) < 90) & (c_ > ma[50]),
        'P45': ((rs >= 80) & (c_ >= 0.85 * h252) & (ma[50] > ma[50].shift(20)) & (l_ <= ma[20]) & (c_ > ma[20])
                & (c_ > o_)),
        'P46': (c_ > hh(50)) & (vr >= 1.5) & (rs >= 80) & (c_ > ma[200]),
        'P47': (ma[50] > ma[50].shift(20)) & (c_ > ma[200]) & (l_ <= ma[50] * 1.01) & (c_ > ma[50]) & (c_ > pc),
        'P48': (ma[10] > ma[20]) & (ma[20] > ma[50]) & (l_ <= ema20) & (c_ > ema20) & (c_ > o_),
        'P49': (c_ > gh) & (pc <= gh.shift(1)) & ~gapday & gh.notna(),
    }
    atrp = atr14 / c_ * 100
    F = {
        'F01': c_ > ma[20], 'F02': c_ > ma[50], 'F03': c_ > ma[200], 'F04': ma[20] > ma[50], 'F05': ma[50] > ma[200],
        'F06': ma[50] > ma[50].shift(20), 'F07': templat, 'F08': rsi14 > 50, 'F09': rsi14 > 60, 'F10': rsi14 < 40,
        'F11': macd > sig, 'F12': macd > 0, 'F13': adx > 25, 'F14': adx < 20, 'F15': st > 0, 'F16': rs >= 70,
        'F17': rs >= 90, 'F18': c_ >= 0.85 * h252, 'F19': c_ >= 0.95 * h252, 'F20': c_ <= 0.70 * h252,
        'F21': vr >= 1.5, 'F22': v10 > v_.rolling(50).mean(), 'F23': atrp >= 4, 'F24': atrp <= 2.5, 'F25': sq_on,
        'F26': qqq_on == 1, 'F27': qqq_on == 0, 'F28': spy_atas == 1, 'F29': pos >= 0.75, 'F30': c_ > o_,
    }
    x_ma10, x_ma20 = c_ < ma[10], c_ < ma[20]
    hist_turun = hist < hist.shift(1)
    X = {
        'X01': x_ma10, 'X02': x_ma20, 'X03': c_ < ma[50], 'X04': c_ < ema10, 'X05': c_ < ema20,
        'X06': x_ma10 & _dulu(x_ma10), 'X07': x_ma20 & _dulu(x_ma20), 'X08': ma[10] < ma[20], 'X09': macd < sig,
        'X10': hist_turun & _dulu(hist_turun) & _dulu(hist_turun, 2), 'X11': rsi14 < 50,
        'X12': (rsi14 < 70) & (rsi14.shift(1) >= 70), 'X13': rsi14 > 80, 'X14': st < 0, 'X15': c_ < ll(3),
        'X16': c_ < ll(5), 'X17': c_ < ll(10), 'X18': k(0) > 1, 'X19': k(0) > 1, 'X20': k(0) > 1,
        'X21': (sk < sdd) & (sk.shift() >= sdd.shift()) & (sk.shift() > 80), 'X22': (c_ < pc) & (vr >= 1.5),
        'X23': (c_ < o_) & (c_ < l_.shift(1)), 'X24': pdi < ndi,
    }
    b = lambda s: np.asarray(s.fillna(False) if s.dtype != bool else s, dtype=bool)
    return ({n: b(v) for n, v in P.items()}, {n: b(v) for n, v in F.items()}, {n: b(v) for n, v in X.items()},
            atr14.to_numpy(float))


def _pasaran(idx):
    """Rejim QQQ (tutup > SMA50 dan SMA10 > SMA20) dan SPY > SMA200, sebagai Series tarikh -> 0/1."""
    q = idx['QQQ'].close
    s = idx['SPY'].close
    on = ((q > q.rolling(50).mean()) & (q.rolling(10).mean() > q.rolling(20).mean())).astype(float)
    return on, (s > s.rolling(200).mean()).astype(float)


def bina(fr, idx, set_, layak_tambahan=None):
    """Bina panel bersambung untuk semua saham dalam `fr` (susunan ticker tersusun).
    set_: '431' atau 'kunci' (menentukan tempoh dan syarat layak). layak_tambahan: dict ticker -> ndarray bool
    (cth. topeng universe A02). Pulangkan dict tatasusunan numpy."""
    on, spy_atas = _pasaran(idx)
    tick = sorted(fr)
    px = pd.DataFrame({t: fr[t].close for t in tick})
    RS = (px / px.shift(126) - 1).rank(axis=1, pct=True) * 100
    bah = {k: [] for k in ('o', 'h', 'l', 'c', 'atr', 'tarikh', 'layak', 'tempoh', 'tid')}
    P = {n[:3]: [] for n in PENCETUS}
    F = {n[:3]: [] for n in PENAPIS}
    X = {n[:3]: [] for n in KELUAR}
    mula = [0]
    for ti, t in enumerate(tick):
        g = fr[t]
        T = len(g)
        rs = RS[t].reindex(g.index)
        p, f, x, atr = indikator(g, rs, on.reindex(g.index).ffill(), spy_atas.reindex(g.index).ffill())
        tarikh = (g.index.year * 10000 + g.index.month * 100 + g.index.day).to_numpy().astype(np.int32)
        ly = np.arange(T) >= 252
        if set_ in ('431', 'hadapan'):
            dv = (g.close * g.volume).rolling(20).mean().to_numpy(float)
            ly &= (g.close.to_numpy(float) >= 10) & (dv >= 1e6)
        if layak_tambahan is not None:
            ly &= layak_tambahan[t]
        tp = np.full(T, -1, np.int8)
        for k, (_, a, z) in enumerate(TEMPOH[set_]):
            tp[(tarikh >= a) & (tarikh <= z)] = k
        for nama, v in (('o', g.open), ('h', g.high), ('l', g.low), ('c', g.close)):
            bah[nama].append(v.to_numpy(float))
        bah['atr'].append(atr)
        bah['tarikh'].append(tarikh)
        bah['layak'].append(ly)
        bah['tempoh'].append(tp)
        bah['tid'].append(np.full(T, ti, np.int32))
        for d, s in ((P, p), (F, f), (X, x)):
            for n in d:
                d[n].append(s[n])
        mula.append(mula[-1] + T)
    out = {k: np.concatenate(v) for k, v in bah.items()}
    out['mula'] = np.asarray(mula, np.int64)
    out['ticker'] = np.asarray(tick)
    out['P'] = {n: np.concatenate(v) for n, v in P.items()}
    out['F'] = np.stack([np.concatenate(F[n[:3]]) for n in PENAPIS]).astype(np.uint8)
    out['X'] = np.stack([np.concatenate(X[n[:3]]) for n in KELUAR]).astype(np.uint8)
    return out


def mula_isyarat(sig, mula):
    """Pencetus = hari pertama isyarat (benar hari ini, palsu semalam), tidak merentas sempadan saham."""
    s = np.asarray(sig, bool)
    d = np.zeros_like(s)
    d[1:] = s[:-1]
    d[mula[:-1]] = False
    return s & ~d

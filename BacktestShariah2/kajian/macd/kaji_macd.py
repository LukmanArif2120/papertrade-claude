# Kajian MACD jadi positif + gabungan kaedah (25 Okt 2026; laporan kajian/KAJIAN_MACD.md).
# Soalan pengguna: adakah "MACD jadi positif" memberi kelebihan, boleh ia digabung dengan kaedah sedia ada, dan adakah
# kaedah gabungan baharu boleh memberi pulangan bulanan yang KONSISTEN (keutamaan pengguna 25 Okt 2026)?
# Dua set data:
#   D431  = data_mentah set 431 (2019-11 – 2026-10; kaedah direka atas data ini, bias kemandirian).
#   D2000 = AUTOTUNE 2000 saham AS paling cair setiap bulan (titik masa; tiada saham delist). Tempoh A 2010–2018 belum
#           pernah dilihat semasa kaedah direka (dipakai untuk memilih), tempoh B 2019 – Okt 2026 untuk pengesahan.
# Isyarat pada tutup hari d -> beli buka d+1. Kos 0.1% setiap belah. Portfolio 10 slot x 10% ekuiti, satu posisi setiap
# saham, slot diisi ikut RS tertinggi (rawak sebagai kawalan); logik portfolio sama dengan kajian/portfolio/kaji_portfolio.py.
# Guna (dari akar repo; perlu numba, pyarrow):
#   python3 BacktestShariah2/kajian/macd/kaji_macd.py sedia      -> matriks lebar + penunjuk (cache $KAJIAN_MACD)
#   python3 BacktestShariah2/kajian/macd/kaji_macd.py peristiwa  -> pulangan hadapan selepas isyarat (peristiwa.csv)
#   python3 BacktestShariah2/kajian/macd/kaji_macd.py sim        -> grid isyarat x penapis x keluar (grid.csv)
#   python3 BacktestShariah2/kajian/macd/kaji_macd.py penapis    -> MACD sebagai penapis 134 kaedah (penapis*.csv;
#                                                                   perlu dagangan KAJIAN_LORONG2/T daripada kaji_lorong2.py jana)
#   python3 BacktestShariah2/kajian/macd/kaji_macd.py calon      -> kaedah gabungan terpilih: semua tempoh, rawak, slot (calon.csv)
import argparse, glob, json, os, pickle, sys
import numpy as np, pandas as pd
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
OUT = os.environ.get('KAJIAN_MACD', '/tmp/kajian_macd')
L2DIR = os.environ.get('KAJIAN_LORONG2', '/tmp/kajian_lorong2')
COST = 0.001
BERMASALAH = {'ASST', 'FCEL', 'MTDR', 'OVV', 'PR', 'SM', 'VAL', 'XENE'}   # LAPORAN_UTAMA §10
TEMPOH = {'D2000_A': ('D2000', '2010-01-04', '2018-12-31'), 'D2000_B': ('D2000', '2019-01-02', '2026-10-16'),
          'D431': ('D431', '2019-11-01', '2026-10-02')}
ISYARAT = ['Z', 'H', 'Hn', 'Hp']          # Z = garisan MACD silang atas 0; H = histogram jadi +ve; Hn/Hp = H di bawah/atas 0
PENAPIS = ['F0', 'FT', 'FT2', 'FR', 'FRT']
KELUAR = {0: 'kaedah (MACD/histogram < 0)', 2: 'Chandelier tutup 4xATR14', 3: 'masa 21 hari'}


# ---------------------------------------------------------------- 1. data lebar + penunjuk
def _lebar(df, tick):
    """df panjang (ticker, date, open..volume) -> dict lajur -> DataFrame tarikh x ticker (float64)."""
    return {k: df.pivot(index='date', columns='ticker', values=k).reindex(columns=tick).astype('float64')
            for k in ('open', 'high', 'low', 'close', 'volume')}


def muat_d431():
    d = pd.concat([pd.read_csv(f'{AKAR}/data_mentah/dataset_{s}.csv') for s in ('S1', 'S2', 'S3', 'S4')])
    d['date'] = pd.to_datetime(d.date.astype(str)); d = d[~d.ticker.isin(BERMASALAH)]
    W = _lebar(d, sorted(d.ticker.unique()))
    ix = pd.read_csv(f'{AKAR}/data_mentah/index_benchmark.csv'); ix['date'] = pd.to_datetime(ix.date.astype(str))
    spy = ix[ix.ticker == 'SPY'].set_index('date').sort_index()
    rs = pd.read_csv(f'{BS2}/kajian/rs/rs_pasaran_431.csv.gz'); rs['date'] = pd.to_datetime(rs.date.astype(str))
    RS = rs.pivot(index='date', columns='ticker', values='rs_pasaran').reindex(index=W['close'].index,
                                                                                columns=W['close'].columns)
    U = W['close'].notna()
    return W, spy, RS, U


def skor_rs(C, layak):
    """RS rating seperti standard/kajian_rs.py: 0.4 x suku terakhir + 0.2 x tiga suku sebelumnya, persentil 1–99."""
    q = [C.shift(k) for k in (63, 126, 189, 252)]
    sk = 0.4 * (C / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1)
    sk = sk.replace([np.inf, -np.inf], np.nan).where(layak & q[3].notna())
    return (sk.rank(axis=1, pct=True) * 98 + 1).round()


def muat_d2000():
    sys.path.insert(0, AKAR)
    from AUTOTUNE.teras import data
    d = data.ambil()
    df = pd.concat([pd.read_parquet(p) for p in sorted(glob.glob(f'{d}/harga_*.parquet'))], ignore_index=True)
    univ = pd.read_parquet(f'{d}/universe.parquet')
    tick = sorted(set(df.ticker) & set(univ.ticker))
    W = _lebar(df[df.ticker.isin(tick)], tick)
    ix = pd.read_parquet(f'{d}/idx.parquet'); spy = ix[ix.ticker == 'SPY'].set_index('date').sort_index()
    dts = W['close'].index; ym = pd.Series(dts.year * 100 + dts.month, index=dts)
    univ['ym'] = univ.bulan.str[:4].astype(int) * 100 + univ.bulan.str[5:7].astype(int)
    M = pd.crosstab(univ.ym, univ.ticker).reindex(columns=tick, fill_value=0) > 0
    U = pd.DataFrame(M.reindex(ym.values, fill_value=False).to_numpy(), index=dts, columns=tick) & W['close'].notna()
    RS = skor_rs(W['close'], U)
    return W, spy, RS, U


def penunjuk(W):
    C, H, L = W['close'], W['high'], W['low']
    m = C.ewm(span=12, adjust=False).mean() - C.ewm(span=26, adjust=False).mean()
    hs = m - m.ewm(span=9, adjust=False).mean()
    pc = C.shift(1)
    tr = np.fmax(H - L, np.fmax((H - pc).abs(), (L - pc).abs()))
    bar = C.notna().cumsum()
    return dict(M=m.where(bar >= 60), Hs=hs.where(bar >= 60), S50=C.rolling(50).mean(), S200=C.rolling(200).mean(),
                ATR=tr.rolling(14).mean())


def cmd_sedia(a):
    os.makedirs(OUT, exist_ok=True)
    for nama, f in (('D431', muat_d431), ('D2000', muat_d2000)):
        W, spy, RS, U = f(); P = penunjuk(W)
        dts = W['close'].index
        A = {k: v.to_numpy(np.float32) for k, v in {**W, **P}.items()}
        A['RS'] = RS.to_numpy(np.float32); A['U'] = U.to_numpy(bool)
        A['spy_o'] = spy.open.reindex(dts).ffill().to_numpy(); A['spy_c'] = spy.close.reindex(dts).ffill().to_numpy()
        np.savez(f'{OUT}/{nama}.npz', dates=dts.values.astype('datetime64[D]'), tick=np.array(W['close'].columns), **A)
        print(nama, A['close'].shape, 'liputan RS %.1f%%' % (100 * np.isfinite(A['RS'][A['U']]).mean()), flush=True)


_CACHE = {}


def baca(nama):
    if nama not in _CACHE:
        z = np.load(f'{OUT}/{nama}.npz', allow_pickle=True); _CACHE[nama] = {k: z[k] for k in z.files}
        for k in ('open', 'high', 'low', 'close', 'ATR', 'M', 'Hs'): _CACHE[nama][k] = _CACHE[nama][k].astype(np.float64)
    return _CACHE[nama]


def topeng(A, isy, pen):
    """Isyarat (pada tutup) x penapis -> bool tarikh x ticker. Penapis dinilai pada tutup hari isyarat."""
    m, hs = A['M'], A['Hs']
    with np.errstate(invalid='ignore'):
        mp = np.vstack([np.full((1, m.shape[1]), np.nan, np.float32), m[:-1]])
        hp = np.vstack([np.full((1, hs.shape[1]), np.nan, np.float32), hs[:-1]])
        if isy == 'Z': s = (mp <= 0) & (m > 0)
        elif isy == 'SEMUA': s = np.isfinite(m)                 # kawalan: setiap hari penapis benar (tanpa masa MACD)
        else:
            s = (hp <= 0) & (hs > 0)
            if isy == 'Hn': s &= m < 0
            if isy == 'Hp': s &= m > 0
        c, s50, s200, rs = A['close'], A['S50'], A['S200'], A['RS']
        if pen in ('FT',): s &= c > s200
        if pen in ('FT2', 'FRT'): s &= (c > s50) & (s50 > s200)
        if pen in ('FR', 'FRT'): s &= rs >= 80
    return s & A['U']


# ---------------------------------------------------------------- 2. kajian peristiwa
def _nw_t(x, lag):
    """t Newey-West bagi purata siri x (pemerhatian bertindih)."""
    x = x[np.isfinite(x)]; n = len(x)
    if n < 20: return np.nan
    u = x - x.mean(); v = u @ u / n
    for j in range(1, lag + 1): v += 2 * (1 - j / (lag + 1)) * (u[j:] @ u[:-j]) / n
    return x.mean() / np.sqrt(v / n)


def cmd_peristiwa(a):
    rows = []
    for tp, (nama, d0, d1) in TEMPOH.items():
        A = baca(nama); dts = pd.DatetimeIndex(A['dates']); ok = (dts >= d0) & (dts <= d1)
        o, c = A['open'], A['close']
        o1 = np.vstack([o[1:], np.full((1, o.shape[1]), np.nan)])
        so1 = np.r_[A['spy_o'][1:], np.nan]
        for h in (5, 10, 21, 63):
            ch = np.vstack([c[h:], np.full((h, c.shape[1]), np.nan)])
            sch = np.r_[A['spy_c'][h:], np.full(h, np.nan)]
            with np.errstate(invalid='ignore', divide='ignore'):
                R = ch / o1 - 1; X = R - (sch / so1 - 1)[:, None]
            X[~ok] = np.nan
            for pen in PENAPIS:
                E = topeng(A, 'SEMUA', pen) & np.isfinite(X)
                xb = np.where(E, X, 0).sum(1) / np.maximum(E.sum(1), 1)
                for isy in ISYARAT:
                    S = topeng(A, isy, pen) & np.isfinite(X); n = S.sum(1); hd = n > 0
                    xs = np.where(S, X, 0).sum(1) / np.maximum(n, 1)
                    d_ = np.where(hd, xs - xb, np.nan)
                    rows.append(dict(tempoh=tp, h=h, isyarat=isy, penapis=pen, n=int(n.sum()), hari=int(hd.sum()),
                                     purata=np.nanmean(np.where(S, R, np.nan)) * 100,
                                     lebihan_spy=np.nanmean(np.where(hd, xs, np.nan)) * 100,
                                     t_spy=_nw_t(np.where(hd, xs, np.nan), h),
                                     atasi_spy=(X[S] > 0).mean() * 100,
                                     lebihan_penapis=np.nanmean(d_) * 100, t_penapis=_nw_t(d_, h)))
            print(tp, h, flush=True)
    R = pd.DataFrame(rows).round(3); R.to_csv(f'{HERE}/peristiwa.csv', index=False); print(R[R.h == 21].to_string())


# ---------------------------------------------------------------- 3. dagangan + portfolio
@njit(cache=True)
def keluar(o, h, l, c, atr, m, hs, e, jenis, nmaks):
    """Dagangan masuk buka e. jenis 0 = MACD < 0 pada tutup (isyarat Z) / histogram < 0 (isyarat H*) -> jual buka esok
    (jenis 0 guna m, jenis 1 guna hs); 2 = Chandelier tutup 4xATR14 paras hanya naik -> jual buka esok; 3 = 21 bar ->
    jual tutup. Pulang (indeks keluar, harga keluar). Bar tanpa data dilangkau; data tamat -> tutup terakhir."""
    n = len(c); hc = -1e18; lv = -1e18; last = -1; bil = 0
    for j in range(e, n):
        if not np.isfinite(c[j]): continue
        last = j; bil += 1
        s = False
        if jenis == 0: s = m[j] < 0
        elif jenis == 1: s = hs[j] < 0
        elif jenis == 2:
            hc = max(hc, c[j])
            if np.isfinite(atr[j]):
                lv = max(lv, hc - 4.0 * atr[j])
            s = c[j] < lv
        elif jenis == 3:
            if bil >= 21: return j, c[j]
        if nmaks > 0 and bil >= nmaks: return j, c[j]
        if s:
            for k in range(j + 1, n):
                if np.isfinite(o[k]): return k, o[k]
            return j, c[j]
    if last < 0: return e, o[e]
    return last, c[last]


@njit(cache=True)
def dagangan(O, Hh, Ll, C, ATR, M, HS, S, jenis, d0, d1, nmaks):
    """Semua isyarat S[d] (d0 <= d < d1) -> dagangan masuk buka d+1. Pulang tatasusunan (ent, ex, tk, buka, ret)."""
    nd, nt = S.shape; cap = 0
    for d in range(d0, min(d1, nd - 1)):
        for k in range(nt):
            if S[d, k] and np.isfinite(O[d + 1, k]): cap += 1
    E = np.empty(cap, np.int64); X = np.empty(cap, np.int64); T = np.empty(cap, np.int64)
    B = np.empty(cap); R = np.empty(cap); q = 0
    for k in range(nt):
        o = O[:, k]; h = Hh[:, k]; l = Ll[:, k]; c = C[:, k]; a = ATR[:, k]; m = M[:, k]; hs = HS[:, k]
        for d in range(d0, min(d1, nd - 1)):
            if not (S[d, k] and np.isfinite(o[d + 1])): continue
            e = d + 1; j, x = keluar(o, h, l, c, a, m, hs, e, jenis, nmaks)
            E[q] = e; X[q] = j; T[q] = k; B[q] = o[e]; R[q] = x / o[e] * (1 - 0.001) / (1 + 0.001) - 1; q += 1
    return E, X, T, B, R


@njit(cache=True)
def portfolio(ent, ex, ret, tk, buka, Cm, d0, d1, slots, w, ntk):
    """Ikut enjin.portfolio v1.2 / kaji_portfolio.portfolio: calon sudah disusun (ent, skor menurun). Keluar direalisasi
    dahulu; satu posisi setiap saham; saiz = min(tunai, ekuiti semalam x w)."""
    nd = d1 - d0; cv = np.empty(nd); cash = 1.0; eq = 1.0
    pq = np.full(slots, -1, np.int64); pa = np.zeros(slots); held = np.zeros(ntk, np.bool_)
    ambil = np.empty(len(ent), np.int64); na = 0; p = 0; nq = len(ent)
    while p < nq and ent[p] < d0: p += 1
    for d in range(d0, d1):
        for s in range(slots):
            q = pq[s]
            if q >= 0 and ex[q] <= d and ent[q] < d:
                cash += pa[s] * (1 + ret[q]); held[tk[q]] = False; pq[s] = -1
        while p < nq and ent[p] == d:
            q = p; p += 1
            if held[tk[q]]: continue
            s = -1
            for z in range(slots):
                if pq[z] < 0: s = z; break
            if s < 0: continue
            am = min(cash, eq * w)
            if am <= 1e-12: continue
            cash -= am; pq[s] = q; pa[s] = am; held[tk[q]] = True; ambil[na] = q; na += 1
        for s in range(slots):                       # v1.2: keluar pada hari masuk
            q = pq[s]
            if q >= 0 and ex[q] <= d and ent[q] == d:
                cash += pa[s] * (1 + ret[q]); held[tk[q]] = False; pq[s] = -1
        mv = 0.0
        for s in range(slots):
            q = pq[s]
            if q >= 0: mv += pa[s] * Cm[d, tk[q]] / buka[q]
        eq = cash + mv; cv[d - d0] = eq
    return cv, ambil[:na]


def ffill(C):
    df = pd.DataFrame(C); return df.ffill().to_numpy(np.float64)


def jana_dagangan(A, S, jenis, d0, d1, nmaks=0):
    return dagangan(A['open'], A['high'], A['low'], A['close'], A['ATR'], A['M'], A['Hs'], S, jenis, d0, d1, nmaks)


def susun(E, T, skor, benih=None):
    """Susun calon ikut hari masuk, skor menurun (RS), pemecah seri rawak tetap."""
    rng = np.random.default_rng(0 if benih is None else benih)
    sk = rng.random(len(E)) if benih is not None else np.nan_to_num(skor, nan=-1e9)
    return np.lexsort((rng.random(len(E)), -sk, E))


def metrik(cv, dts, ent, ex, ret, ambil, spy):
    s = pd.Series(cv, dts); y = (dts[-1] - dts[0]).days / 365.25
    mb = s.resample('ME').last(); rb = mb / mb.shift(1).fillna(1.0) - 1
    sb = pd.Series(spy, dts).resample('ME').last(); sbr = sb / sb.shift(1).fillna(spy[0]) - 1
    r = ret[ambil]; hari = (ex[ambil] - ent[ambil])
    return dict(cagr=((s.iloc[-1]) ** (1 / y) - 1) * 100, mdd=(s / s.cummax() - 1).min() * 100,
                bulan_purata=rb.mean() * 100, bulan_median=rb.median() * 100, bulan_sd=rb.std() * 100,
                bulan_untung=(rb > 0).mean() * 100, bulan_terburuk=rb.min() * 100, bulan_terbaik=rb.max() * 100,
                bulan_10=(rb >= 0.10).mean() * 100, bulan_atasi_spy=(rb > sbr).mean() * 100,
                sharpe_bulan=rb.mean() / rb.std() * np.sqrt(12) if rb.std() > 0 else np.nan,
                dagangan_setahun=len(r) / y, menang=(r > 0).mean() * 100 if len(r) else np.nan,
                purata_dagangan=r.mean() * 100 if len(r) else np.nan, hari_pegang=hari.mean() if len(r) else np.nan)


def rujukan(A, d0, d1):
    """SPY dan beli-pegang sama rata alam (universe) bagi tempoh sama."""
    dts = pd.DatetimeIndex(A['dates'][d0:d1]); out = {}
    c = A['close'][d0 - 1:d1].astype(np.float64); u = A['U'][d0:d1]
    with np.errstate(invalid='ignore', divide='ignore'):
        r = c[1:] / c[:-1] - 1
    r = np.where(u & np.isfinite(r), r, np.nan); ew = np.cumprod(1 + np.nan_to_num(np.nanmean(r, 1)))
    for k, v in (('SPY', A['spy_c'][d0:d1] / A['spy_c'][d0 - 1]), ('Sama rata alam', ew)):
        z = np.arange(1); out[k] = metrik(v, dts, z, z, np.zeros(1), z[:0], A['spy_c'][d0:d1])
    return out


def indeks(A, d0, d1):
    dts = pd.DatetimeIndex(A['dates']); return int(dts.searchsorted(pd.Timestamp(d0))), int(dts.searchsorted(pd.Timestamp(d1), 'right'))


def jalan(A, isy, pen, jenis, d0, d1, slots=10, w=0.10, benih=None, rejim=False, nmaks=0, skor='rs'):
    S = topeng(A, isy, pen)
    if rejim:                                     # beli baharu hanya bila SPY > SMA200
        sc = pd.Series(A['spy_c']); S = S & (sc > sc.rolling(200).mean()).to_numpy()[:, None]
    jn = (1 if isy != 'Z' else 0) if jenis == 0 else jenis
    E, X, T, B, R = jana_dagangan(A, S, jn, d0 - 1, d1 - 1, nmaks)
    sk = A['RS'][E - 1, T].astype(np.float64) if skor == 'rs' else -A['ATR'][E - 1, T] / A['close'][E - 1, T]
    o = susun(E, T, sk, benih)
    E, X, T, B, R = E[o], X[o], T[o], B[o], R[o]
    Cm = baca_cm(A)
    cv, ambil = portfolio(E, X, R, T, B, Cm, d0, d1, slots, w, A['close'].shape[1])
    dts = pd.DatetimeIndex(A['dates'][d0:d1])
    m = metrik(cv, dts, E, X, R, ambil, A['spy_c'][d0:d1])
    m.update(semua_n=len(R), semua_purata=R.mean() * 100 if len(R) else np.nan, semua_menang=(R > 0).mean() * 100 if len(R) else np.nan)
    return m, pd.Series(cv, dts)


def baca_cm(A):
    if '_Cm' not in A: A['_Cm'] = ffill(A['close'])
    return A['_Cm']


def cmd_sim(a):
    rows = []
    for tp, (nama, t0, t1) in TEMPOH.items():
        A = baca(nama); d0, d1 = indeks(A, t0, t1)
        for k, v in rujukan(A, d0, d1).items(): rows.append(dict(tempoh=tp, isyarat=k, penapis='', keluar='', **v))
        for pen in PENAPIS:
            for isy in ISYARAT + ['SEMUA']:
                for jenis in KELUAR:
                    if isy == 'SEMUA' and jenis == 0: continue
                    m, _ = jalan(A, isy, pen, jenis, d0, d1)
                    rows.append(dict(tempoh=tp, isyarat=isy, penapis=pen, keluar=KELUAR[jenis], **m))
                    print(tp, isy, pen, jenis, round(m['cagr'], 1), round(m['bulan_untung'], 1), flush=True)
        pd.DataFrame(rows).round(2).to_csv(f'{HERE}/grid.csv', index=False)


# ---------------------------------------------------------------- 4. MACD sebagai penapis 134 kaedah (D431)
def cmd_penapis(a):
    A = baca('D431'); dts = pd.DatetimeIndex(A['dates']); tick = list(A['tick']); tid = {t: i for i, t in enumerate(tick)}
    T = pd.concat([pickle.load(open(f, 'rb')) for f in sorted(glob.glob(f'{L2DIR}/T/*.pkl'))], ignore_index=True)
    T = T[(T.ent >= pd.Timestamp('2019-11-01')) & T.ticker.isin(tid)].reset_index(drop=True)
    k = T.ticker.map(tid).to_numpy(); s = dts.get_indexer(T.sig); e = dts.get_indexer(T.ent)
    T['macd_pos'] = A['M'][s, k] > 0; T['hist_pos'] = A['Hs'][s, k] > 0; T['rs'] = A['RS'][s, k]
    with np.errstate(invalid='ignore'):
        T['macd_naik'] = A['M'][s, k] > A['M'][s - 5, k]
    o, h, l, c, at = A['open'], A['high'], A['low'], A['close'], A['ATR']
    r2 = np.empty(len(T)); x2 = np.empty(len(T), np.int64)
    for q in range(len(T)):
        j, x = keluar(o[:, k[q]], h[:, k[q]], l[:, k[q]], c[:, k[q]], at[:, k[q]], at[:, k[q]], at[:, k[q]], e[q], 2, 0)
        x2[q] = j; r2[q] = x / o[e[q], k[q]] * (1 - COST) / (1 + COST) - 1
    T['ret2'] = r2; T['x2'] = x2; T['e'] = e; T['k'] = k
    T['x1'] = np.minimum(dts.searchsorted(T.ex), len(dts) - 1)
    # (a) peringkat dagangan: dalam setiap kaedah, banding subset MACD > 0 lawan <= 0
    rows = []
    for mid, G in T.groupby('mid'):
        for kol in ('macd_pos', 'hist_pos'):
            a1, a0 = G[G[kol]], G[~G[kol]]
            if len(a1) < 30 or len(a0) < 30: continue
            rows.append(dict(kaedah=mid, ciri=kol, n_ya=len(a1), n_tidak=len(a0),
                             L1_ya=a1.ret.mean() * 100, L1_tidak=a0.ret.mean() * 100,
                             L2_ya=a1.ret2.mean() * 100, L2_tidak=a0.ret2.mean() * 100))
    P = pd.DataFrame(rows).round(3); P.to_csv(f'{HERE}/penapis_kaedah.csv', index=False)
    # dagangan pada hari sama bergerak bersama pasaran: banding lebihan SPY ya lawan tidak dalam hari isyarat sama
    spy = pd.Series(A['spy_c'], dts); so = pd.Series(A['spy_o'], dts)
    for L, kr, ke in ((1, 'ret', 'ex'), (2, 'ret2', None)):
        exd = T.ex if ke else dts[np.minimum(T.x2, len(dts) - 1)]
        T[f'x{L}s'] = T[kr] - (spy.reindex(exd).to_numpy() / so.reindex(T.ent).to_numpy() - 1)
    rk = []
    for kol, G in P.groupby('ciri'):
        r = dict(ciri=kol, kaedah=len(G), L1_lebih_baik=int((G.L1_ya > G.L1_tidak).sum()),
                 L2_lebih_baik=int((G.L2_ya > G.L2_tidak).sum()), bahagian_ya=T[kol].mean() * 100)
        for L in (1, 2):
            g = T.groupby(['sig', kol])[f'x{L}s'].mean().unstack().dropna(); d = (g[True] - g[False]).to_numpy() * 100
            r.update({f'L{L}_beza_hari_sama': d.mean(), f'L{L}_t': _nw_t(d, 20), f'L{L}_hari': len(d)})
        rk.append(r); print(r)
    pd.DataFrame(rk).round(3).to_csv(f'{HERE}/penapis_ringkas.csv', index=False)
    # (b) portfolio RS_10 (kajian portfolio: semua isyarat, slot ikut RS) dengan / tanpa penapis MACD
    d0, d1 = indeks(A, '2020-11-02', '2026-10-02'); Cm = baca_cm(A); out = []
    for kol in (None, 'macd_pos', 'hist_pos', 'macd_naik'):
        G = T if kol is None else T[T[kol]]
        for L in (1, 2):
            X = (G.x1 if L == 1 else G.x2).to_numpy(np.int64); R = (G.ret if L == 1 else G.ret2).to_numpy(float)
            E = G.e.to_numpy(np.int64); K = G.k.to_numpy(np.int64); B = o[E, K]
            for nm, bn in [('RS', None)] + [('rawak', b) for b in range(1, 11)]:
                q = susun(E, K, G.rs.to_numpy(float), bn)
                cv, am = portfolio(E[q], X[q], R[q], K[q], B[q], Cm, d0, d1, 10, 0.10, len(tick))
                m = metrik(cv, dts[d0:d1], E[q], X[q], R[q], am, A['spy_c'][d0:d1])
                out.append(dict(penapis=kol or 'tiada', lorong=L, susun=nm, benih=bn, **m))
                print(kol, L, nm, bn, round(m['cagr'], 1), round(m['bulan_untung'], 1), flush=True)
    pd.DataFrame(out).round(2).to_csv(f'{HERE}/penapis_portfolio.csv', index=False)


# ---------------------------------------------------------------- 5. calon kaedah gabungan
def cmd_calon(a):
    G = pd.read_csv(f'{HERE}/grid.csv'); A_ = G[(G.tempoh == 'D2000_A') & (G.isyarat.isin(ISYARAT))]
    spy = G[(G.tempoh == 'D2000_A') & (G.isyarat == 'SPY')].cagr.iloc[0]
    # Peraturan pilih (ditetapkan sebelum melihat tempoh B / D431): Sharpe bulanan tertinggi dalam D2000 tempoh A,
    # dengan CAGR > SPY dan >= 20 dagangan setahun.
    ok = A_[(A_.cagr > spy) & (A_.dagangan_setahun >= 20)].sort_values('sharpe_bulan', ascending=False)
    pilih = ok.head(3)[['isyarat', 'penapis', 'keluar']].values.tolist()
    print('pilih', pilih)
    kj = {v: k for k, v in KELUAR.items()}; rows = []; kurva = {}
    for isy, pen, kel in pilih + [['SEMUA', pilih[0][1], KELUAR[2]]]:
        for tp, (nama, t0, t1) in TEMPOH.items():
            A = baca(nama); d0, d1 = indeks(A, t0, t1)
            ujian = [('asas 10 slot', {}), ('20 slot x 5%', dict(slots=20, w=0.05)), ('rejim SPY>SMA200', dict(rejim=True))]
            ujian += [(f'rawak {b}', dict(benih=b)) for b in range(1, 11)]
            for nm, kw in ujian:
                m, cv = jalan(A, isy, pen, kj[kel], d0, d1, **kw)
                rows.append(dict(isyarat=isy, penapis=pen, keluar=kel, tempoh=tp, ujian=nm, **m))
                if nm == 'asas 10 slot': kurva[f'{isy}|{pen}|{kel}|{tp}'] = cv
            print(isy, pen, kel, tp, flush=True)
    pd.DataFrame(rows).round(2).to_csv(f'{HERE}/calon.csv', index=False)
    pd.to_pickle(kurva, f'{OUT}/kurva.pkl')


# ---------------------------------------------------------------- 6. reka bentuk konsisten (keutamaan pengguna)
def cmd_konsisten(a):
    """Isyarat Z dan kawalan SEMUA x penapis x susunan (RS tertinggi / ATR% terendah) x slot (10/20) x rejim SPY.
    Peraturan pilih (ditetapkan sebelum melihat D2000_B / D431): Sharpe bulanan tertinggi dalam D2000_A dengan CAGR > SPY."""
    rows = []
    for tp, (nama, t0, t1) in TEMPOH.items():
        A = baca(nama); d0, d1 = indeks(A, t0, t1)
        for isy in ('Z', 'SEMUA'):
            for pen in ('F0', 'FT2', 'FR'):
                for skor in ('rs', 'atr_rendah'):
                    for slots, w in ((10, 0.10), (20, 0.05)):
                        for rejim in (False, True):
                            m, _ = jalan(A, isy, pen, 2, d0, d1, slots=slots, w=w, rejim=rejim, skor=skor)
                            rows.append(dict(tempoh=tp, isyarat=isy, penapis=pen, susunan=skor, slot=slots, rejim=rejim, **m))
                print(tp, isy, pen, flush=True)
        pd.DataFrame(rows).round(2).to_csv(f'{HERE}/konsisten.csv', index=False)
    K = pd.DataFrame(rows); kunci = ['isyarat', 'penapis', 'susunan', 'slot', 'rejim']
    spy = rujukan(baca('D2000'), *indeks(baca('D2000'), *TEMPOH['D2000_A'][1:]))['SPY']['cagr']
    a_ = K[(K.tempoh == 'D2000_A') & (K.cagr > spy)].sort_values('sharpe_bulan', ascending=False)
    pilih = a_.iloc[0][kunci].to_dict(); print('pilih', pilih)
    out = []
    for tp, (nama, t0, t1) in TEMPOH.items():
        A = baca(nama); d0, d1 = indeks(A, t0, t1)
        for b in range(1, 21):
            m, _ = jalan(A, pilih['isyarat'], pilih['penapis'], 2, d0, d1, slots=int(pilih['slot']), w=1 / pilih['slot'],
                         rejim=bool(pilih['rejim']), benih=b)
            out.append(dict(tempoh=tp, benih=b, **m))
    R = pd.DataFrame(out); R.round(2).to_csv(f'{HERE}/konsisten_rawak.csv', index=False)
    json.dump({k: (v.item() if hasattr(v, 'item') else v) for k, v in pilih.items()}, open(f'{HERE}/konsisten_pilih.json', 'w'))
    print(R.groupby('tempoh')[['cagr', 'mdd', 'sharpe_bulan', 'bulan_untung']].median())


if __name__ == '__main__':
    p = argparse.ArgumentParser(); s = p.add_subparsers(required=True)
    for n, f in (('sedia', cmd_sedia), ('peristiwa', cmd_peristiwa), ('sim', cmd_sim), ('penapis', cmd_penapis),
                 ('calon', cmd_calon), ('konsisten', cmd_konsisten)):
        s.add_parser(n).set_defaults(f=f)
    a = p.parse_args(); a.f(a)

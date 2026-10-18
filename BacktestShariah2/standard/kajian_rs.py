# Kajian RS rating (gaya IBD) lawan SELURUH pasaran AS, 2005–kini. Dijalankan oleh GitHub Actions
# `.github/workflows/kajian_rs.yml` (sesi Claude tidak boleh capai Yahoo). Tujuan: tentukan gred RS yang benar-benar
# mewakili pulangan masa depan sebelum `standard/gred.py` diubah (tugasan_v3.md §8).
#
# Guna:
#   python3 kajian_rs.py tarik --cache /tmp/rs.pkl            (yfinance: tv_us.csv + set 431 + SPY, sejak 2005)
#   python3 kajian_rs.py uji   --cache /tmp/rs.pkl --keluar BacktestShariah2/kajian/rs
#   python3 kajian_rs.py uji   --dataset data_mentah --keluar <folder>   (ujian setempat dengan data 431)
#
# Kaedah:
#   - RS = 40% pulangan 63 hari + 20% setiap satu tiga suku sebelumnya (anggaran umum formula IBD), dipangkat persentil
#     1–99 setiap hari berbanding semua saham AS dengan tutup >= USD5 dan >= 253 bar.
#   - Sampel dinilai setiap 5 hari dagangan; saham layak: tutup >= USD5, purata nilai dagangan 50 hari >= USD1 juta.
#   - Pulangan hadapan 5/21/63 hari; "lebihan" = pulangan saham tolak purata semua saham layak pada tarikh sama.
#   - Portfolio bulanan (tidak bertindih, 21 hari): sama berat setiap kumpulan RS, kos diabaikan.
#   - Pandangan pakar lain diuji: Novy-Marx 12-7, Frog-in-the-Pan (ID), Clenow (cerun x R²), RS / turun naik
#     (Barroso-Santa-Clara), MAX (Bali et al.), Mansfield & peringkat 2 (Weinstein), momentum mutlak (Antonacci), saiz.
#   - Tambahan: t Newey-West & CI95, tempoh 2005–2015/2016–2026, ketahanan (nilai >= USD10j, harga >= 15, tarikh
#     senarai), laluan O'Neil (+20% sebelum -8%), momentum residual (Blitz), RS meningkat & volum naik/turun (IBD),
#     RS industri (Moskowitz-Grinblatt), kos dagangan portfolio, kalibrasi skema gred lama lawan cadangan.
#   - Bias: yfinance tiada saham yang sudah delist (bias saham terselamat); senarai = pasaran AS kini (tv_us.csv).
import sys, os, glob, argparse, json, time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BS2)
MULA = '2005-01-01'
HARGA_MIN = 5.0
NILAI_MIN = 1e6
LANGKAH = 5
KOS = 0.002          # kos sehala (komisen + spread + gelinciran) bagi portfolio bulanan
UFUK = (5, 21, 63)
BIN_RS = [0, 39, 59, 69, 79, 89, 94, 99]
LABEL_RS = ['01-39', '40-59', '60-69', '70-79', '80-89', '90-94', '95-99']


# ---------- data ----------
def set_431():
    s = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'data_mentah', 'dataset_S*.csv'))):
        s |= set(pd.read_csv(f, usecols=['ticker']).ticker.dropna().astype(str))
    return s


def senarai():
    tv = pd.read_csv(os.path.join(BS2, 'data', 'skrin', 'tv_us.csv'), usecols=['ticker'])
    s = set(tv.ticker.dropna().astype(str)) | set_431()
    return sorted(t for t in s if t.replace('.', '').replace('-', '').isalnum())


def tarik(a):
    import yfinance as yf
    tk = senarai() + ['SPY']
    C, H, L, V, gagal = [], [], [], [], []
    for i in range(0, len(tk), 200):
        ks = [t.replace('.', '-') for t in tk[i:i + 200]]
        df = None
        for n in range(3):
            try:
                df = yf.download(ks, start=MULA, interval='1d', auto_adjust=False, actions=False,
                                 group_by='column', threads=True, progress=False)
                break
            except Exception as e:
                print(f'kumpulan {i}: cuba {n + 1} gagal ({e})', file=sys.stderr, flush=True)
                time.sleep(20 * (n + 1))
        if df is None or df.empty:
            gagal += ks; continue
        for nm, out in (('Close', C), ('High', H), ('Low', L), ('Volume', V)):
            x = df[nm].copy(); x.columns = [c.replace('-', '.') for c in x.columns]; out.append(x.astype('float32'))
        print(f'{i + len(ks)}/{len(tk)}', flush=True)
        time.sleep(2)
    c, h, l, v = (pd.concat(x, axis=1) for x in (C, H, L, V))
    for x in (c, h, l, v):
        x.index = pd.to_datetime(x.index).tz_localize(None)
    c = c.loc[:, c.notna().sum() > 0]
    pd.to_pickle({'c': c, 'h': h[c.columns], 'l': l[c.columns], 'v': v[c.columns], 'gagal': gagal}, a.cache)
    print(json.dumps({'saham': c.shape[1], 'bar': len(c), 'dari': str(c.index[0].date()), 'hingga': str(c.index[-1].date()),
                      'gagal': len(gagal)}))


def muat_dataset(folder):
    d = pd.concat([pd.read_csv(f, usecols=['ticker', 'date', 'close', 'high', 'low', 'volume'])
                   for f in sorted(glob.glob(os.path.join(folder, 'dataset_S*.csv')))]).drop_duplicates(['ticker', 'date'])
    ix = pd.read_csv(os.path.join(folder, 'index_benchmark.csv'), usecols=['ticker', 'date', 'close', 'high', 'low', 'volume'])
    d = pd.concat([d, ix[ix.ticker == 'SPY']])
    d['date'] = pd.to_datetime(d.date.astype(str))
    p = lambda k: d.pivot(index='date', columns='ticker', values=k).sort_index().astype('float32')
    return {'c': p('close'), 'h': p('high'), 'l': p('low'), 'v': p('volume'), 'gagal': []}


def bersih(c):
    """Buang lonjakan satu hari (data rosak): naik > 4x lalu jatuh < 0.3x keesokannya, atau sebaliknya."""
    r1, r2 = c / c.shift(), c.shift(-1) / c
    rosak = ((r1 > 4) & (r2 < 0.3)) | ((r1 < 0.25) & (r2 > 3.3))
    return c.mask(rosak)


# ---------- ciri ----------
def persentil(x, layak):
    x = x.where(layak)
    return (x.rank(axis=1, pct=True) * 98 + 1).round()


def ciri(D):
    c = bersih(D['c'].drop(columns='SPY', errors='ignore')).astype('float64')
    h = D['h'][c.columns].astype('float64').where(c.notna())
    v = D['v'][c.columns].astype('float64')
    spy = D['c']['SPY'].astype('float64').reindex(c.index).ffill()
    q = [c.shift(k) for k in (63, 126, 189, 252)]
    harga_ok = (c >= HARGA_MIN) & q[3].notna()
    sk = 0.4 * (c / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1)
    F = {
        'rs': persentil(sk.replace([np.inf, -np.inf], np.nan), harga_ok),
        'm12_1': persentil(c.shift(21) / q[3] - 1, harga_ok),
        'm6': persentil(c / q[1] - 1, harga_ok),
        'm3': persentil(c / q[0] - 1, harga_ok),
        'r1': persentil(c / c.shift(21) - 1, harga_ok),
        'jarak52': (c / h.rolling(252, min_periods=200).max() - 1) * 100,
    }
    rl = c.div(spy, axis=0)
    F['rsline_baru'] = (rl >= rl.rolling(252, min_periods=200).max() * 0.999).astype('float64').where(c.notna())
    F['atas200'] = (c > c.rolling(200).mean()).astype('float64').where(c.notna())
    # Pandangan pakar lain (lihat RINGKASAN §14–16)
    r = c.pct_change(fill_method=None)
    F['m12_7'] = persentil(q[1] / q[3] - 1, harga_ok)                      # Novy-Marx 2012
    F['m6_2'] = persentil(c.shift(21) / q[1] - 1, harga_ok)
    naik = (r > 0).astype('float64').where(r.notna()).rolling(231, min_periods=200).mean().shift(21)
    turun = (r < 0).astype('float64').where(r.notna()).rolling(231, min_periods=200).mean().shift(21)
    F['id_fip'] = np.sign(c.shift(21) / q[3] - 1) * (turun - naik)        # Da-Gurun-Warachka; negatif = berterusan
    y = np.log(c)
    T = pd.Series(np.arange(len(c), dtype='float64'), index=c.index)
    n = 90
    sy, st = y.rolling(n).sum(), T.rolling(n).sum()
    sty = y.mul(T, axis=0).rolling(n).sum()
    kov = (sty - sy.mul(st, axis=0) / n) / n
    vt = (n * n - 1) / 12.0
    vy = y.rolling(n).var(ddof=0)
    cerun = kov / vt
    F['clenow'] = persentil(((np.exp(cerun * 252) - 1) * (kov ** 2 / (vt * vy))).replace([np.inf, -np.inf], np.nan), harga_ok)
    sis = r.rolling(126, min_periods=100).std() * np.sqrt(252)
    F['rs_vol'] = persentil((sk / sis).replace([np.inf, -np.inf], np.nan), harga_ok)  # Barroso-Santa-Clara (peringkat saham)
    F['max21'] = persentil(r.rolling(21).max(), harga_ok)                 # Bali-Cakici-Whitelaw
    F['mansfield'] = (rl / rl.rolling(252, min_periods=200).mean() - 1) * 100   # Weinstein
    s150 = c.rolling(150).mean()
    F['peringkat2'] = ((c > s150) & (s150 > s150.shift(21))).astype('float64').where(c.notna())
    F['mutlak12'] = (c / q[3] - 1) * 100                                  # Antonacci (momentum mutlak)
    nilai = (c * v).rolling(50, min_periods=40).mean()
    F['nilai_pct'] = persentil(nilai, harga_ok)                           # proksi saiz/kecairan (Hong-Lim-Stein)
    F['nilai'] = nilai
    # Momentum residual (Blitz-Huij-Martens): pulangan 12-1 selepas buang beta x SPY, dibahagi turun naik residual
    m = spy.pct_change(fill_method=None)
    kov = r.mul(m, axis=0).rolling(252, min_periods=200).mean() - r.rolling(252, min_periods=200).mean().mul(
        m.rolling(252, min_periods=200).mean(), axis=0)
    beta = kov.div(m.rolling(252, min_periods=200).var(ddof=0), axis=0)
    e = r - beta.shift(1).mul(m, axis=0)
    F['res_mom'] = persentil((e.rolling(231, min_periods=200).sum() / e.rolling(231, min_periods=200).std()).shift(21), harga_ok)
    # IBD: RS meningkat; Accumulation/Distribution (proksi: volum hari naik / volum hari turun, 50 hari)
    F['rs_naik'] = F['rs'] - F['rs'].shift(21)
    vn = v.where(r > 0, 0).rolling(50, min_periods=40).sum()
    vtr = v.where(r < 0, 0).rolling(50, min_periods=40).sum()
    F['ud_vol'] = (vn / vtr.replace(0, np.nan)).where(c.notna())
    # Kumpulan industri (IBD Industry Group RS; Moskowitz-Grinblatt). Klasifikasi TradingView semasa (tv_us.csv).
    F['rs_industri'], F['rs_dalam_industri'] = industri(sk.where(harga_ok), c.columns)
    F = {k: x.astype('float32') for k, x in F.items()}
    layak = harga_ok & (nilai >= NILAI_MIN)
    hadapan = {k: c.shift(-k) / c - 1 for k in UFUK}
    rejim = pd.DataFrame({'spy_atas200': spy > spy.rolling(200).mean(), 'spy_12b_negatif': spy / spy.shift(252) < 1}, index=c.index)
    l = D['l'][c.columns].astype('float64').where(c.notna()) if 'l' in D else None
    return c, F, layak, hadapan, rejim, spy, h, l


def industri(sk, kolum):
    """(RS industri 1–99 setiap saham = pangkat median skor RS industrinya antara industri, RS dalam industri 1–99)."""
    f = os.path.join(BS2, 'data', 'skrin', 'tv_us.csv')
    kosong = pd.DataFrame(np.nan, index=sk.index, columns=kolum)
    if not os.path.exists(f):
        return kosong, kosong.copy()
    peta = pd.read_csv(f, usecols=['ticker', 'industry']).dropna().drop_duplicates('ticker').set_index('ticker').industry
    peta = peta[peta.index.isin(kolum)]
    kump = {i: list(g.index) for i, g in peta.groupby(peta) if len(g) >= 5}
    skor = pd.DataFrame({i: sk[t].median(axis=1).where(sk[t].notna().sum(axis=1) >= 5) for i, t in kump.items()})
    pi = (skor.rank(axis=1, pct=True) * 98 + 1).round()
    rind, rdal = kosong.copy(), kosong.copy()
    for i, t in kump.items():
        rind[t] = np.repeat(pi[i].values[:, None], len(t), axis=1)
        rdal[t] = (sk[t].rank(axis=1, pct=True) * 98 + 1).round().values
    return rind.where(sk.notna()), rdal.where(sk.notna())


def panjang(c, F, layak, hadapan, tarikh):
    """Jadual panjang (tarikh, ticker) bagi sampel tarikh."""
    m = layak.loc[tarikh].stack()
    m = m[m].index
    d = pd.DataFrame(index=m)
    for k, x in F.items():
        d[k] = x.loc[tarikh].stack().reindex(m).values
    for k, x in hadapan.items():
        f = x.loc[tarikh].stack().reindex(m)
        d[f'f{k}'] = f.values * 100
        d[f'x{k}'] = d[f'f{k}'] - d.groupby(level=0)[f'f{k}'].transform('mean')
    d.index.names = ['tarikh', 'ticker']
    return d.dropna(subset=['rs']).reset_index()


# ---------- ringkasan ----------
def statistik(x):
    q1, q99 = x.quantile([0.01, 0.99])
    t = x[(x >= q1) & (x <= q99)]
    return pd.Series({'n': len(x), 'purata': x.mean(), 'median': x.median(), 'purata_potong1': t.mean(),
                      'menang': (x > 0).mean() * 100, 'sisihan': x.std(), 'p5': x.quantile(0.05)})


def nw_t(z, lag):
    """Purata siri lebihan ikut tarikh: (t Newey-West, CI95 bawah, CI95 atas). Sampel bertindih -> lag = ufuk / langkah."""
    z = z[~np.isnan(z)]
    n = len(z)
    if n < 20:
        return (np.nan, np.nan, np.nan)
    u = z - z.mean()
    v = (u @ u) / n
    for j in range(1, min(lag, n - 1) + 1):
        v += 2 * (1 - j / (lag + 1)) * (u[j:] @ u[:-j]) / n
    se = np.sqrt(v / n)
    return (z.mean() / se if se > 0 else np.nan, z.mean() - 1.96 * se, z.mean() + 1.96 * se)


def ikut(d, kol, ufuk=UFUK):
    out = []
    for k in ufuk:
        s = d.dropna(subset=[f'f{k}', kol])
        if s.empty:
            continue
        a = s.groupby(kol, observed=True)[f'f{k}'].apply(statistik).unstack()
        b = s.groupby(kol, observed=True)[f'x{k}'].agg(lebihan_purata='mean', lebihan_median='median')
        # purata merentas tarikh dahulu (setiap tarikh sama berat)
        e = s.groupby([kol, 'tarikh'], observed=True)[f'x{k}'].mean().groupby(level=0, observed=True)
        b['lebihan_ikut_tarikh'] = e.mean(); b['tarikh_menang_pct'] = e.apply(lambda z: (z > 0).mean() * 100)
        b['atasi_pasaran_pct'] = s.groupby(kol, observed=True)[f'x{k}'].apply(lambda z: (z > 0).mean() * 100)
        nw = e.apply(lambda z: nw_t(z.values, int(np.ceil(k / LANGKAH))))
        b['t_nw'] = nw.map(lambda z: z[0]); b['ci95_bawah'] = nw.map(lambda z: z[1]); b['ci95_atas'] = nw.map(lambda z: z[2])
        out.append(a.join(b).assign(ufuk=k).reset_index().rename(columns={kol: 'kumpulan'}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=['kumpulan', 'ufuk'])


def portfolio(c, F, layak, kumpulan_fn, label):
    """Imbang semula setiap 21 hari dagangan; sama berat setiap kumpulan; pulangan 21 hari tidak bertindih."""
    tarikh = c.index[252::21]
    rek, ahli, pusing = [], {}, {}
    for i in range(len(tarikh) - 1):
        t0, t1 = tarikh[i], tarikh[i + 1]
        ok = layak.loc[t0]
        r = (c.loc[t1] / c.loc[t0] - 1)[ok].dropna().clip(-0.95, 5)
        if len(r) < 50:
            continue
        g = kumpulan_fn(t0).reindex(r.index)
        row = {'tarikh': t0, 'SEMUA': r.mean()}
        for k, x in r.groupby(g, observed=True):
            if len(x) >= 5:
                row[k] = x.mean()
                baru = set(x.index)
                if k in ahli:
                    pusing.setdefault(k, []).append(1 - len(baru & ahli[k]) / len(baru))
                ahli[k] = baru
        rek.append(row)
    p = pd.DataFrame(rek).set_index('tarikh')
    hasil = []
    for k in p.columns:
        s = p[k].dropna()
        if len(s) < 12:
            continue
        nilai = (1 + s).cumprod()
        thn = len(s) * 21 / 252
        hasil.append({'set': label, 'kumpulan': k, 'bulan': len(s), 'cagr': (nilai.iloc[-1] ** (1 / thn) - 1) * 100,
                      'turun_naik': s.std() * np.sqrt(12) * 100, 'sharpe': s.mean() / s.std() * np.sqrt(12),
                      'mdd': (nilai / nilai.cummax() - 1).min() * 100,
                      'lebihan_bulanan': (s - p['SEMUA'].reindex(s.index)).mean() * 100,
                      'bulan_atasi_semua': ((s - p['SEMUA'].reindex(s.index)) > 0).mean() * 100,
                      'pusing_ganti_pct': np.mean(pusing.get(k, [np.nan])) * 100})
        pg = np.nanmean(pusing.get(k, [np.nan])) if k != 'SEMUA' else 0.0
        bersih = s - 2 * KOS * (pg if not np.isnan(pg) else 0)
        nb = (1 + bersih).cumprod()
        hasil[-1]['cagr_selepas_kos'] = (nb.iloc[-1] ** (1 / thn) - 1) * 100
    return pd.DataFrame(hasil), p


def laluan(c, h, l, layak, tarikh, n=63, naik=0.20, turun=0.08):
    """Hasil laluan gaya O'Neil dalam n hari selepas tarikh: +20% dahulu atau -8% dahulu (hari sama = -8%), MAE, MFE."""
    C, H, Lw = c.values, h.values, l.values
    ix = {t: i for i, t in enumerate(c.index)}
    out = []
    for t in tarikh:
        i = ix[t]
        if i + n >= len(c):
            continue
        ok = layak.loc[t].values & ~np.isnan(C[i])
        j = np.where(ok)[0]
        c0 = C[i, j]
        hh, ll = H[i + 1:i + 1 + n, j], Lw[i + 1:i + 1 + n, j]
        ada = ~np.isnan(hh).all(axis=0)
        up, dn = hh >= c0 * (1 + naik), ll <= c0 * (1 - turun)
        fu = np.where(up.any(axis=0), up.argmax(axis=0), n + 1)
        fd = np.where(dn.any(axis=0), dn.argmax(axis=0), n + 1)
        with np.errstate(all='ignore'):
            mae = (np.nanmin(ll, axis=0) / c0 - 1) * 100
            mfe = (np.nanmax(hh, axis=0) / c0 - 1) * 100
        out.append(pd.DataFrame({'tarikh': t, 'ticker': c.columns[j], 'untung20_dulu': (fu < fd).astype(float),
                                 'kena8': (fd <= n).astype(float), 'kena8_dulu': (fd <= fu) & (fd <= n),
                                 'mae63': mae, 'mfe63': mfe})[ada])
    d = pd.concat(out, ignore_index=True)
    d['kena8_dulu'] = d.kena8_dulu.astype(float)
    return d


def ringkas_laluan(d, kol):
    g = d.groupby(kol, observed=True)
    return pd.DataFrame({'n': g.size(), 'untung20_dahulu_pct': g.untung20_dulu.mean() * 100,
                         'henti8_dahulu_pct': g.kena8_dulu.mean() * 100, 'pernah_turun8_pct': g.kena8.mean() * 100,
                         'mae_median': g.mae63.median(), 'mfe_median': g.mfe63.median(),
                         'nisbah_untung_henti': g.untung20_dulu.mean() / g.kena8_dulu.mean()}).reset_index().rename(columns={kol: 'kumpulan'})


def md(df, nombor=2):
    df = df.copy()
    for k in df.columns:
        if pd.api.types.is_float_dtype(df[k]):
            df[k] = df[k].round(nombor)
    kol = [str(k) for k in df.columns]
    baris = ['| ' + ' | '.join(kol) + ' |', '|' + '---|' * len(kol)]
    baris += ['| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |' for r in df.itertuples(index=False)]
    return '\n'.join(baris)


def bin_rs(x):
    return pd.cut(x, BIN_RS, labels=LABEL_RS)


BIN_HALUS = [0, 39, 59, 69, 74, 79, 84, 89, 92, 94, 97, 99]
LABEL_HALUS = ['01-39', '40-59', '60-69', '70-74', '75-79', '80-84', '85-89', '90-92', '93-94', '95-97', '98-99']


def bin_halus(x):
    return pd.cut(x, BIN_HALUS, labels=LABEL_HALUS)


def gred_cadangan(rs):
    return pd.cut(rs, [0, 69, 79, 89, 94, 99], labels=['D (<70)', 'C (70-79)', 'B (80-89)', 'A (90-94)', 'A! (95-99)'])


def gred_lama(rs):
    return pd.cut(rs, [0, 39, 59, 79, 89, 99], labels=['E (<40)', 'D (40-59)', 'C (60-79)', 'B (80-89)', 'A (90+)'])


def desil(x):
    return pd.cut(x, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99], labels=[f'D{i}' for i in range(1, 11)])


def uji(a):
    os.makedirs(a.keluar, exist_ok=True)
    D = pd.read_pickle(a.cache) if a.cache else muat_dataset(a.dataset)
    c, F, layak, hadapan, rejim, spy, h, l = ciri(D)
    s431 = set_431()
    tarikh = c.index[252:-max(UFUK)][::LANGKAH]
    d = panjang(c, F, layak, hadapan, tarikh)
    d['RS'] = bin_rs(d.rs)
    d['thn'] = d.tarikh.dt.year
    d['set'] = np.where(d.ticker.isin(s431), '431', 'lain')
    R = {}
    R['rs'] = ikut(d, 'RS')
    R['desil'] = pd.concat([ikut(d.assign(DS=desil(d[k])), 'DS', (21, 63)).assign(ciri=k)
                            for k in ('rs', 'm12_1', 'm6', 'm3', 'r1')], ignore_index=True)
    d['J52'] = pd.cut(d.jarak52, [-101, -40, -25, -15, -10, -5, -2, 0.01],
                      labels=['>40%', '25-40%', '15-25%', '10-15%', '5-10%', '2-5%', '<=2%'])
    R['jarak52'] = ikut(d, 'J52', (21, 63))
    R['rsline'] = ikut(d.assign(L=d.rsline_baru.map({1.0: 'baharu', 0.0: 'tidak'})), 'L', (21, 63))
    d['RSxJ'] = d.RS.astype(str) + ' | ' + np.where(d.jarak52 >= -15, 'dekat (<=15%)', 'jauh (>15%)')
    R['rs_x_jarak'] = ikut(d, 'RSxJ', (21, 63))
    tmp = (d.rs >= 70) & (d.jarak52 >= -25) & (d.atas200 == 1)
    R['templat'] = ikut(d.assign(T=np.where(tmp, 'lulus', 'gagal')), 'T', (21, 63))
    R['tahun'] = d.pivot_table(index='thn', columns='RS', values='x21', aggfunc='mean', observed=True).round(2).reset_index()
    R['tahun_median'] = d.pivot_table(index='thn', columns='RS', values='x21', aggfunc='median', observed=True).round(2).reset_index()
    rj = rejim.reindex(d.tarikh)
    d['rejim'] = np.where(rj.spy_atas200.values, 'SPY > SMA200', 'SPY < SMA200')
    d['panik'] = np.where(rj.spy_12b_negatif.values, 'SPY 12 bulan negatif', 'SPY 12 bulan positif')
    R['rejim'] = pd.concat([ikut(d[d.rejim == r], 'RS', (21,)).assign(rejim=r) for r in d.rejim.unique()]
                           + [ikut(d[d.panik == r], 'RS', (21,)).assign(rejim=r) for r in d.panik.unique()], ignore_index=True)
    R['set431'] = pd.concat([ikut(d[d.set == s], 'RS', (21, 63)).assign(set=s) for s in ('431', 'lain') if (d.set == s).any()], ignore_index=True)
    # kekekalan gred: RS 21 hari kemudian
    rs = F['rs']
    nanti = rs.shift(-21).loc[tarikh].stack()
    kini = rs.loc[tarikh].stack()
    j = pd.DataFrame({'kini': bin_rs(kini), 'nanti': bin_rs(nanti.reindex(kini.index))}).dropna()
    R['kekal21'] = (pd.crosstab(j.kini, j.nanti, normalize='index') * 100).round(1).reset_index()
    # RS lawan pasaran vs RS lawan 431 sahaja (bagi saham 431)
    k431 = [t for t in c.columns if t in s431]
    if k431 and len(k431) < c.shape[1]:
        c4 = c[k431]; q4 = [c4.shift(k) for k in (63, 126, 189, 252)]
        sk4 = 0.4 * (c4 / q4[0] - 1) + 0.2 * (q4[0] / q4[1] - 1) + 0.2 * (q4[1] / q4[2] - 1) + 0.2 * (q4[2] / q4[3] - 1)
        rs4 = persentil(sk4.replace([np.inf, -np.inf], np.nan), (c4 >= HARGA_MIN) & q4[3].notna())
        a4 = rs4.loc[tarikh].stack(); b4 = rs[k431].loc[tarikh].stack().reindex(a4.index)
        j4 = pd.DataFrame({'rs_431': bin_rs(a4), 'rs_pasaran': bin_rs(b4)}).dropna()
        R['banding_431'] = (pd.crosstab(j4.rs_431, j4.rs_pasaran, normalize='index') * 100).round(1).reset_index()
        out431 = rs[k431].loc['2019-01-01':].stack().dropna().astype('int8').rename('rs_pasaran').reset_index()
        out431.columns = ['date', 'ticker', 'rs_pasaran']
        out431['date'] = out431.date.dt.strftime('%Y%m%d')
        out431.to_csv(os.path.join(a.keluar, 'rs_pasaran_431.csv.gz'), index=False, compression='gzip')
    # portfolio bulanan
    P = []
    for lab, fn in [('RS', lambda t: bin_rs(F['rs'].loc[t])),
                    ('12-1', lambda t: bin_rs(F['m12_1'].loc[t])),
                    ('RS + dekat tinggi 52 minggu (<=15%)',
                     lambda t: bin_rs(F['rs'].loc[t]).astype(str).where(F['jarak52'].loc[t] >= -15, 'jauh'))]:
        P.append(portfolio(c, F, layak, fn, lab)[0])
    R['portfolio'] = pd.concat(P, ignore_index=True)
    # Ukuran kekuatan alternatif: desil dan portfolio 10% teratas
    alt = ['rs', 'm12_1', 'm12_7', 'm6_2', 'clenow', 'rs_vol']
    R['pakar_desil'] = pd.concat([ikut(d.assign(DS=desil(d[k])), 'DS', (21, 63)).assign(ciri=k) for k in alt],
                                 ignore_index=True)
    atas = lambda k: (lambda t: pd.Series(np.where(F[k].loc[t] >= 90, 'D10', np.where(F[k].loc[t].notna(), 'lain', None)),
                                          index=F[k].columns).dropna())
    R['pakar_portfolio'] = pd.concat([portfolio(c, F, layak, atas(k), k)[0] for k in alt], ignore_index=True)
    # Dalam RS >= 80: adakah syarat pakar memisahkan pemenang?
    k80 = d[d.rs >= 80].copy()
    ter = lambda x: pd.qcut(x.rank(method='first'), 3, labels=['rendah', 'tengah', 'tinggi'])
    syarat = {
        'id_fip (FIP; rendah = berterusan)': ter(k80.id_fip),
        'max21 (lonjakan sehari)': ter(k80.max21),
        'nilai dagangan (saiz)': ter(k80.nilai_pct),
        'jarak52': np.where(k80.jarak52 >= -15, 'dekat (<=15%)', 'jauh (>15%)'),
        'mansfield > 0': np.where(k80.mansfield > 0, 'ya', 'tidak'),
        'peringkat 2 Weinstein': np.where(k80.peringkat2 == 1, 'ya', 'tidak'),
        'r1 (pulangan 1 bulan)': ter(k80.r1),
    }
    R['dalam_rs80'] = pd.concat([ikut(k80.assign(S=v), 'S', (21, 63)).assign(syarat=s) for s, v in syarat.items()],
                                ignore_index=True)
    rj80 = rejim.reindex(k80.tarikh)
    k80['mutlak'] = np.where((k80.mutlak12 > 0) & rj80.spy_atas200.values, 'saham & SPY positif', 'tidak')
    R['dalam_rs80'] = pd.concat([R['dalam_rs80'], ikut(k80, 'mutlak', (21, 63)).assign(syarat='momentum mutlak (Antonacci)')],
                                ignore_index=True)
    # Syarat tambahan dalam RS >= 80 (IBD / Blitz / Moskowitz-Grinblatt)
    tambah = {
        'momentum residual (Blitz)': ter(k80.res_mom),
        'RS berubah 21 hari (IBD: RS meningkat)': pd.cut(k80.rs_naik, [-99, -5, 5, 99], labels=['turun >5', 'stabil', 'naik >5']),
        'volum naik/turun 50 hari (A/D)': ter(k80.ud_vol),
        'RS industri (kumpulan IBD)': pd.cut(k80.rs_industri, [0, 33, 66, 99], labels=['industri lemah', 'industri sederhana', 'industri kuat']),
        'RS dalam industri': pd.cut(k80.rs_dalam_industri, [0, 33, 66, 99], labels=['rendah', 'tengah', 'tinggi']),
    }
    R['dalam_rs80'] = pd.concat([R['dalam_rs80']] + [ikut(k80.assign(S=v), 'S', (21, 63)).assign(syarat=s)
                                                     for s, v in tambah.items() if pd.Series(v).notna().any()], ignore_index=True)
    R['pakar_desil'] = pd.concat([R['pakar_desil']] + [ikut(d.assign(DS=desil(d[k])), 'DS', (21, 63)).assign(ciri=k)
                                                       for k in ('res_mom', 'rs_industri') if d[k].notna().any()], ignore_index=True)
    # Sempadan halus, signifikan statistik, tempoh berasingan, ketahanan
    d['RSH'] = bin_halus(d.rs)
    R['rs_halus'] = ikut(d, 'RSH', (21, 63))
    d['tempoh'] = np.where(d.tarikh < '2016-01-01', '2005-2015', '2016-2026')
    R['tempoh'] = pd.concat([ikut(d[d.tempoh == t], 'RSH', (63,)).assign(tempoh=t) for t in ('2005-2015', '2016-2026')], ignore_index=True)
    awal = set(c.columns[c.iloc[:260].notna().any()])
    hrg = c.loc[tarikh].stack().rename('harga'); hrg.index.names = ['tarikh', 'ticker']
    d = d.merge(hrg.reset_index(), on=['tarikh', 'ticker'], how='left')
    uji_k = {'nilai >= USD10 juta': d.nilai >= 1e7, 'harga >= USD15': d.harga >= 15,
             'tersenarai sejak 2005': d.ticker.isin(awal), 'tersenarai selepas 2005': ~d.ticker.isin(awal)}
    R['ketahanan'] = pd.concat([ikut(d[m], 'RSH', (63,)).assign(subset=k) for k, m in uji_k.items() if m.any()], ignore_index=True)
    # Hasil laluan O'Neil (+20% sebelum -8% dalam 63 hari)
    if l is not None:
        L = laluan(c, h, l, layak, tarikh)
        d = d.merge(L, on=['tarikh', 'ticker'], how='left')
        dl = d.dropna(subset=['untung20_dulu'])
        R['laluan'] = ringkas_laluan(dl, 'RSH')
        R['laluan_rejim'] = pd.concat([ringkas_laluan(dl[dl.rejim == r], 'RSH').assign(rejim=r) for r in dl.rejim.unique()],
                                      ignore_index=True)
    # Kalibrasi skema gred: cadangan lawan gred.py sekarang
    rjd = rejim.reindex(d.tarikh)
    d['sah'] = np.where((d.mutlak12 > 0) & rjd.spy_atas200.values & (d.mansfield > 0), 'disahkan', 'tidak disahkan')
    d['GC'] = gred_cadangan(d.rs); d['GL'] = gred_lama(d.rs)
    d['GCS'] = d.GC.astype(str) + ' | ' + d.sah
    R['skema_lama'] = ikut(d, 'GL', (21, 63))
    R['skema_cadangan'] = ikut(d, 'GC', (21, 63))
    R['skema_cadangan_sah'] = ikut(d, 'GCS', (21, 63))
    R['skema_cadangan_rejim'] = pd.concat([ikut(d[d.rejim == r], 'GC', (63,)).assign(rejim=r) for r in d.rejim.unique()],
                                          ignore_index=True)
    R['skema_cadangan_tempoh'] = pd.concat([ikut(d[d.tempoh == t], 'GC', (63,)).assign(tempoh=t) for t in ('2005-2015', '2016-2026')],
                                           ignore_index=True)
    R['skema_cadangan_431'] = ikut(d[d.set == '431'], 'GC', (21, 63)) if (d.set == '431').any() else pd.DataFrame()
    if 'untung20_dulu' in d:
        dl = d.dropna(subset=['untung20_dulu'])
        R['skema_laluan'] = pd.concat([ringkas_laluan(dl, 'GC'), ringkas_laluan(dl, 'GCS')], ignore_index=True)
    R['skema_portfolio'] = portfolio(c, F, layak, lambda t: gred_cadangan(F['rs'].loc[t]), 'cadangan')[0]
    for k, x in R.items():
        x.to_csv(os.path.join(a.keluar, f'{k}.csv'), index=False, float_format='%.4g')
    meta = {'dijana': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'saham': int(c.shape[1]),
            'bar': int(len(c)), 'dari': str(c.index[0].date()), 'hingga': str(c.index[-1].date()),
            'sampel_tarikh': int(len(tarikh)), 'baris': int(len(d)), 'gagal_tarik': len(D.get('gagal', []))}
    json.dump(meta, open(os.path.join(a.keluar, 'meta.json'), 'w'), indent=1)
    ringkasan(a.keluar, R, meta)
    print(json.dumps(meta))


def ringkasan(keluar, R, meta):
    p = lambda df, k: df[df.ufuk == k].drop(columns='ufuk')
    lap = [f"# Kajian RS rating lawan seluruh pasaran AS\n",
           f"Dijana {meta['dijana']} oleh `standard/kajian_rs.py` (GitHub Actions `kajian_rs.yml`). Jangan ubah secara manual.\n",
           f"Data: {meta['saham']} saham, {meta['bar']} bar ({meta['dari']} hingga {meta['hingga']}); {meta['sampel_tarikh']} tarikh sampel "
           f"(setiap {LANGKAH} hari), {meta['baris']:,} pemerhatian. Saham layak: tutup >= USD{HARGA_MIN:g}, nilai dagangan 50 hari >= USD1 juta. "
           "Lebihan = pulangan tolak purata semua saham layak pada tarikh sama. Bias: saham yang sudah delist tiada.\n",
           "## 1. Gred RS: pulangan hadapan 21 hari (%)\n", md(p(R['rs'], 21)),
           "\n## 2. Gred RS: pulangan hadapan 63 hari (%)\n", md(p(R['rs'], 63)),
           "\n## 3. Portfolio bulanan sama berat (21 hari, tidak bertindih)\n", md(R['portfolio']),
           "\n## 4. Desil: lebihan ikut tarikh (%)\n",
           md(R['desil'].pivot_table(index=['ciri', 'ufuk'], columns='kumpulan', values='lebihan_ikut_tarikh', observed=True).reset_index()),
           "\n## 5. Lebihan purata 21 hari ikut tahun (%)\n", md(R['tahun']),
           "\n## 6. Rejim pasaran (21 hari)\n", md(R['rejim'][['rejim', 'kumpulan', 'n', 'purata', 'median', 'lebihan_ikut_tarikh', 'tarikh_menang_pct']]),
           "\n## 7. Jarak ke tinggi 52 minggu (21 hari)\n", md(p(R['jarak52'], 21)),
           "\n## 8. RS x jarak ke tinggi 52 minggu (63 hari)\n", md(p(R['rs_x_jarak'], 63)),
           "\n## 9. Templat Minervini (RS >= 70, <= 25% bawah tinggi 52 minggu, atas SMA200; 63 hari)\n", md(p(R['templat'], 63)),
           "\n## 10. RS line paras tertinggi 52 minggu (63 hari)\n", md(p(R['rsline'], 63)),
           "\n## 11. Set 431 (Shariah) lawan saham lain (21 hari)\n", md(p(R['set431'], 21)),
           "\n## 12. Kekekalan gred: % kekal/berpindah selepas 21 hari\n", md(R['kekal21'], 1)]
    if 'banding_431' in R:
        lap += ["\n## 13. RS lawan 431 sahaja (baris) berbanding RS lawan pasaran (lajur), % baris\n", md(R['banding_431'], 1)]
    lap += ["\n## 14. Ukuran kekuatan pakar: lebihan ikut tarikh mengikut desil (%)\n"
            "rs = IBD 40/20/20/20; m12_1 = akademik; m12_7 = Novy-Marx; m6_2 = momentum terkini; clenow = cerun regresi log 90 hari x R²; "
            "rs_vol = skor RS / turun naik 6 bulan (Barroso-Santa-Clara).\n",
            md(R['pakar_desil'].pivot_table(index=['ciri', 'ufuk'], columns='kumpulan', values='lebihan_ikut_tarikh', observed=True).reset_index()),
            "\n## 15. Portfolio bulanan 10% teratas setiap ukuran\n", md(R['pakar_portfolio']),
            "\n## 16. Dalam RS >= 80: syarat pakar tambahan (63 hari)\n",
            md(p(R['dalam_rs80'], 63)[['syarat', 'kumpulan', 'n', 'purata', 'median', 'menang', 'p5', 'lebihan_ikut_tarikh', 'tarikh_menang_pct', 't_nw']])]
    S = ['kumpulan', 'n', 'purata', 'median', 'menang', 'p5', 'lebihan_ikut_tarikh', 'ci95_bawah', 'ci95_atas', 't_nw',
         'tarikh_menang_pct', 'atasi_pasaran_pct']
    lap += ["\n## 17. Sempadan halus dengan signifikan statistik (63 hari)\n"
            "t_nw = statistik t Newey-West bagi purata lebihan ikut tarikh (|t| >= 2 kira-kira signifikan 95%); CI95 = selang keyakinan 95%; "
            "atasi_pasaran_pct = % pemerhatian dengan pulangan melebihi purata pasaran.\n", md(p(R['rs_halus'], 63).reindex(columns=S)),
            "\n## 18. Tempoh berasingan (63 hari)\n", md(R['tempoh'].reindex(columns=['tempoh'] + S)),
            "\n## 19. Ketahanan: subset (63 hari)\n", md(R['ketahanan'].reindex(columns=['subset'] + S))]
    if 'laluan' in R:
        lap += ["\n## 20. Hasil laluan gaya O'Neil dalam 63 hari (+20% dahulu lawan henti -8% dahulu)\n", md(R['laluan']),
                "\n## 21. Hasil laluan ikut rejim\n", md(R['laluan_rejim'])]
    lap += ["\n## 22. Kalibrasi skema gred: gred.py sekarang (63 hari)\n", md(p(R['skema_lama'], 63).reindex(columns=S)),
            "\n## 23. Kalibrasi skema gred cadangan (63 hari)\n", md(p(R['skema_cadangan'], 63).reindex(columns=S)),
            "\n## 24. Skema cadangan x pengesahan (saham 12 bulan > 0, SPY > SMA200, Mansfield > 0; 63 hari)\n",
            md(p(R['skema_cadangan_sah'], 63).reindex(columns=S)),
            "\n## 25. Skema cadangan ikut rejim dan tempoh (63 hari)\n",
            md(R['skema_cadangan_rejim'].reindex(columns=['rejim'] + S)), '', md(R['skema_cadangan_tempoh'].reindex(columns=['tempoh'] + S))]
    if len(R.get('skema_cadangan_431', [])):
        lap += ["\n## 26. Skema cadangan dalam set 431 (63 hari)\n", md(p(R['skema_cadangan_431'], 63).reindex(columns=S))]
    if 'skema_laluan' in R:
        lap += ["\n## 27. Skema cadangan: hasil laluan O'Neil\n", md(R['skema_laluan'])]
    lap += ["\n## 28. Skema cadangan: portfolio bulanan (kos 0.2% sehala)\n", md(R['skema_portfolio'])]
    open(os.path.join(keluar, 'RINGKASAN.md'), 'w', encoding='utf-8').write('\n'.join(lap) + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sp = ap.add_subparsers(dest='cmd', required=True)
    t = sp.add_parser('tarik'); t.add_argument('--cache', required=True)
    u = sp.add_parser('uji'); u.add_argument('--cache'); u.add_argument('--dataset'); u.add_argument('--keluar', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'tarik':
        tarik(a)
    else:
        if not a.cache and not a.dataset:
            raise SystemExit('perlu --cache atau --dataset')
        uji(a)


if __name__ == '__main__':
    main()

# Kajian gred industri lawan SELURUH pasaran AS, 2005–kini. Dijalankan oleh GitHub Actions
# `.github/workflows/kajian_industri.yml` (sesi Claude tidak boleh capai Yahoo). Tujuan: tentukan formula skor industri
# yang benar-benar menyusun pulangan masa depan A > B > C > D > E sebelum `standard/sektor_pasaran.py` diubah
# (tugasan_v3.md §8; kajian awal FMP 2016–2026 dan alam Shariah dalam binaan_v2_log_tambahan.md 18 Okt 2026).
#
# Guna:
#   python3 kajian_industri.py tarik --cache /tmp/ind.pkl          (yfinance: semua ticker peta_industri.csv + SPY, sejak 2005)
#   python3 kajian_industri.py uji   --cache /tmp/ind.pkl --keluar BacktestShariah2/kajian/industri
#   python3 kajian_industri.py uji   --dataset data_mentah --keluar <folder>   (ujian setempat dengan data 431)
#
# Kaedah:
#   - Industri = plate industri Moomoo (papertrade/peta_industri.csv), sama seperti gred masa sebenar.
#   - Saham layak: tutup >= USD5, purata nilai dagangan 50 hari >= USD1 juta (cerminan skrin Moomoo >= USD5).
#   - Industri dengan < MIN_SAHAM saham layak tidak diberi skor. Skor = pangkat persentil antara industri; gred ikut
#     kuintil (A = 20% teratas ... E = 20% terbawah).
#   - Wajaran nilai: purata nilai dagangan 20 hari (nilai pasaran sejarah tiada dalam yfinance).
#   - Sampel setiap 5 hari dagangan. Pulangan hadapan 10/21 hari: beli buka esok, jual tutup hari ke-h.
#     "Lebihan" = pulangan tolak purata semua saham layak pada tarikh sama. t-stat dilaras tindih (n x 5 / h).
#   - Bias: yfinance tiada saham yang sudah delist (bias saham terselamat); peta industri = klasifikasi kini.
import sys, os, glob, argparse, json, time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BS2)
MULA = '2005-01-01'
HARGA_MIN = 5.0
NILAI_MIN = 1e6
MIN_SAHAM = 3
LANGKAH = 5
UFUK = (10, 21)
GRED = list('ABCDE')
TEMPOH = [('2005-2012', '2005', '2012'), ('2013-2019', '2013', '2019'), ('2020-kini', '2020', '2030')]


# ---------- data ----------
def peta():
    p = pd.read_csv(os.path.join(BS2, 'papertrade', 'peta_industri.csv'))
    return p.dropna(subset=['ticker', 'industri']).drop_duplicates('ticker').set_index('ticker').industri


def set_431():
    s = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'data_mentah', 'dataset_S*.csv'))):
        s |= set(pd.read_csv(f, usecols=['ticker']).ticker.dropna().astype(str))
    return s


def tarik(a):
    import yfinance as yf
    tk = sorted(t for t in peta().index.astype(str) if t.replace('.', '').replace('-', '').isalnum()) + ['SPY']
    O, C, V, gagal = [], [], [], []
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
        for nm, out in (('Open', O), ('Close', C), ('Volume', V)):
            x = df[nm].copy(); x.columns = [c.replace('-', '.') for c in x.columns]; out.append(x.astype('float32'))
        print(f'{i + len(ks)}/{len(tk)}', flush=True)
        time.sleep(2)
    o, c, v = (pd.concat(x, axis=1) for x in (O, C, V))
    for x in (o, c, v):
        x.index = pd.to_datetime(x.index).tz_localize(None)
    c = c.loc[:, c.notna().sum() > 0]
    pd.to_pickle({'o': o[c.columns], 'c': c, 'v': v[c.columns], 'gagal': gagal}, a.cache)
    print(json.dumps({'saham': c.shape[1], 'bar': len(c), 'dari': str(c.index[0].date()), 'hingga': str(c.index[-1].date()),
                      'gagal': len(gagal)}))


def muat_dataset(folder):
    d = pd.concat([pd.read_csv(f, usecols=['ticker', 'date', 'open', 'close', 'volume'])
                   for f in sorted(glob.glob(os.path.join(folder, 'dataset_S*.csv')))]).drop_duplicates(['ticker', 'date'])
    d['date'] = pd.to_datetime(d.date.astype(str))
    p = lambda k: d.pivot(index='date', columns='ticker', values=k).sort_index().astype('float32')
    return {'o': p('open'), 'c': p('close'), 'v': p('volume'), 'gagal': []}


def bersih(c):
    """Buang lonjakan satu hari (data rosak): naik > 4x lalu jatuh < 0.3x keesokannya, atau sebaliknya."""
    r1, r2 = c / c.shift(), c.shift(-1) / c
    rosak = ((r1 > 4) & (r2 < 0.3)) | ((r1 < 0.25) & (r2 > 3.3))
    return c.mask(rosak)


# ---------- skor industri ----------
def purata_wajaran(x, w):
    m = x.notna() & w.notna() & (w > 0)
    return (x[m] * w[m]).sum() / w[m].sum() if m.any() else np.nan


def skor_industri(f):
    """f: DataFrame satu tarikh (indeks ticker) dengan ind, w, r1w, r1m, r3m, r6m, r12_1.
    Pulangkan DataFrame (indeks industri) skor 0–1 bagi setiap varian."""
    g = f.groupby('ind')
    n = g.size()
    ok = n[n >= MIN_SAHAM].index
    if len(ok) < 10:
        return None
    g = f[f.ind.isin(ok)].groupby('ind')
    med = g[['r1w', 'r1m', 'r3m', 'r6m']].median()
    br = g.r1m.apply(lambda x: (x > 0).mean())
    vw = lambda k: g.apply(lambda x: purata_wajaran(x[k], x.w))
    ew1m = g.r1m.mean()
    v1m, v3m, v6m, v12 = vw('r1m'), vw('r3m'), vw('r6m'), vw('r12_1')
    pk = lambda s: s.rank(pct=True)
    S = pd.DataFrame({
        'V0 semasa (1M.30 3M.25 1W.15 breadth.30, median)': 0.30 * pk(med.r1m) + 0.25 * pk(med.r3m) + 0.15 * pk(med.r1w) + 0.30 * pk(br),
        'K1 breadth 1M sahaja': pk(br),
        'K2 1W median sahaja': pk(med.r1w),
        'K3 1M median sahaja': pk(med.r1m),
        'K4 3M median sahaja': pk(med.r3m),
        'V1 1M wajaran nilai (Moskowitz-Grinblatt)': pk(v1m),
        'V1e 1M purata sama berat': pk(ew1m),
        'V4 3M wajaran nilai': pk(v3m),
        'V2 6M wajaran nilai (IBD/MSCI)': pk(v6m),
        'V3 12-1 bulan wajaran nilai': pk(v12),
        'V5 1M+6M wajaran nilai': 0.5 * pk(v1m) + 0.5 * pk(v6m),
    })
    S['n'] = n.loc[ok]
    return S


def kuintil(s):
    q = s.rank(pct=True)
    return pd.cut(q, [0, .2, .4, .6, .8, 1.0001], labels=['E', 'D', 'C', 'B', 'A'], include_lowest=True)


# ---------- jadual panjang ----------
def bina(D, s431):
    c = bersih(D['c'].drop(columns='SPY', errors='ignore')).astype('float64')
    o = D['o'][c.columns].astype('float64').where(c.notna())
    v = D['v'][c.columns].astype('float64')
    pi = peta()
    kol = [t for t in c.columns if t in pi.index]
    c, o, v = c[kol], o[kol], v[kol]
    ind = pi.reindex(kol)
    nilai50 = (c * v).rolling(50, min_periods=40).mean()
    w20 = (c * v).rolling(20, min_periods=15).mean()
    layak = (c >= HARGA_MIN) & (nilai50 >= NILAI_MIN) & c.shift(21).notna()
    R = {'r1w': c / c.shift(5) - 1, 'r1m': c / c.shift(21) - 1, 'r3m': c / c.shift(63) - 1,
         'r6m': c / c.shift(126) - 1, 'r12_1': c.shift(21) / c.shift(252) - 1}
    R = {k: x.astype('float32') for k, x in R.items()}   # jimat memori (~5,600 saham x 5,500 bar)
    H = {h: (c.shift(-h) / o.shift(-1) - 1).clip(-0.95, 5).astype('float32') for h in UFUK}
    # indeks industri harian (sama berat & wajaran nilai) untuk kegunaan setempat
    r = (c / c.shift() - 1).clip(-0.9, 3).where(layak.shift().fillna(False).astype(bool))
    w = w20.shift().where(r.notna())
    ew = r.T.groupby(ind).mean().T
    vwr = (r * w).T.groupby(ind).sum().T / w.T.groupby(ind).sum().T
    nn = r.notna().T.groupby(ind).sum().T
    harian = pd.concat({'ew': ew, 'vw': vwr, 'n': nn}, axis=1)
    tarikh = c.index[260:-max(UFUK) - 1][::LANGKAH]
    rows = []
    for t in tarikh:
        m = layak.loc[t]
        f = pd.DataFrame({k: x.loc[t] for k, x in R.items()})[m]
        f['ind'] = ind[m]; f['w'] = w20.loc[t][m]
        for h in UFUK:
            f[f'f{h}'] = H[h].loc[t][m] * 100
        f = f.dropna(subset=['ind', 'r1w', 'r1m', 'f10'])
        if len(f) < 50:
            continue
        S = skor_industri(f)
        if S is None:
            continue
        f = f[f.ind.isin(S.index)].copy()
        for h in UFUK:
            f[f'x{h}'] = f[f'f{h}'] - f[f'f{h}'].mean()
        for k in S.columns.drop('n'):
            f['G:' + k] = f.ind.map(kuintil(S[k].dropna())).astype(object)
        f['saiz'] = pd.qcut(f.w.rank(method='first'), 3, labels=['kecil', 'sederhana', 'besar']).astype(object)
        f['tarikh'] = t
        rows.append(f.reset_index(names='ticker'))
    d = pd.concat(rows, ignore_index=True)
    d['set'] = np.where(d.ticker.isin(s431), '431', 'lain')
    return d, harian, c


# ---------- ringkasan ----------
def nilai_varian(d, var, h, label):
    """Satu baris ringkasan: lebihan purata ikut tarikh setiap gred, A-E, t, tahun positif, monotonik, menang."""
    g = 'G:' + var
    s = d.dropna(subset=[g, f'x{h}'])
    if s.empty:
        return None
    M = s.groupby(['tarikh', g])[f'x{h}'].mean().unstack().reindex(columns=GRED)
    sp = (M.A - M.E).dropna()
    t = sp.mean() / sp.std() * np.sqrt(len(sp) * LANGKAH / h) if len(sp) > 2 else np.nan
    yr = M.groupby(M.index.year).mean()
    mm = M.mean()
    mono = pd.Series(mm.values).corr(pd.Series([5, 4, 3, 2, 1]), method='spearman')
    menang = s.groupby(g)[f'f{h}'].apply(lambda z: (z > 0).mean() * 100).reindex(GRED)
    med = s.groupby(g)[f'x{h}'].median().reindex(GRED)
    row = {'set': label, 'ufuk': h, 'varian': var}
    row.update({k: mm[k] for k in GRED})
    row.update({'A-E': sp.mean(), 't': t, 'tahun_positif_pct': ((yr.A - yr.E) > 0).mean() * 100, 'monotonik': mono,
                'menang_A': menang.A, 'menang_E': menang.E, 'median_A': med.A, 'median_E': med.E,
                'tarikh_A_atasi_E_pct': (sp > 0).mean() * 100, 'n': len(s)})
    for nm, a, b in TEMPOH:
        z = sp[a:b]
        row[f'A-E {nm}'] = z.mean() if len(z) else np.nan
    return row


def peringkat_industri(d, var, h):
    """Pulangan purata industri (sama berat ahli) mengikut gred: setiap industri sama berat pada setiap tarikh."""
    g = 'G:' + var
    s = d.dropna(subset=[g, f'x{h}'])
    i = s.groupby(['tarikh', 'ind']).agg(x=(f'x{h}', 'mean'), G=(g, 'first')).reset_index()
    i['ticker'] = i.ind
    i = i.rename(columns={'x': f'x{h}', 'G': g})
    i[f'f{h}'] = i[f'x{h}']
    return nilai_varian(i, var, h, 'industri (sama berat)')


def md(df, nombor=2):
    df = df.copy()
    for k in df.columns:
        if pd.api.types.is_float_dtype(df[k]):
            df[k] = df[k].round(nombor)
    kol = [str(k) for k in df.columns]
    baris = ['| ' + ' | '.join(kol) + ' |', '|' + '---|' * len(kol)]
    baris += ['| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |' for r in df.itertuples(index=False)]
    return '\n'.join(baris)


def uji(a):
    os.makedirs(a.keluar, exist_ok=True)
    D = pd.read_pickle(a.cache) if a.cache else muat_dataset(a.dataset)
    s431 = set_431()
    d, harian, c = bina(D, s431)
    var = [k[2:] for k in d.columns if k.startswith('G:')]
    out = []
    for h in UFUK:
        for v in var:
            out.append(peringkat_industri(d, v, h))
            out.append(nilai_varian(d, v, h, 'semua saham'))
            out.append(nilai_varian(d[d.set == '431'], v, h, 'saham 431 (Shariah)'))
            for z in ('kecil', 'sederhana', 'besar'):
                out.append(nilai_varian(d[d.saiz == z], v, h, f'saiz {z}'))
    R = pd.DataFrame([r for r in out if r])
    R.to_csv(os.path.join(a.keluar, 'varian.csv'), index=False, float_format='%.4g')
    # tahun bagi varian utama
    th = []
    for v in var:
        g = 'G:' + v
        M = d.dropna(subset=[g]).groupby(['tarikh', g]).x21.mean().unstack()
        y = M.groupby(M.index.year).mean()
        th.append(pd.DataFrame({'varian': v, 'tahun': y.index, 'A-E': (y.A - y.E).values}))
    T = pd.concat(th).pivot(index='tahun', columns='varian', values='A-E').reset_index()
    T.to_csv(os.path.join(a.keluar, 'tahun_A_E_21h.csv'), index=False, float_format='%.4g')
    h2 = harian.loc['2005-01-01':]
    h2.stack(level=1, future_stack=True).reset_index().rename(columns={'level_0': 'date', 'level_1': 'industri'}) \
        .dropna(subset=['ew']).assign(date=lambda x: x.date.dt.strftime('%Y%m%d')) \
        .to_csv(os.path.join(a.keluar, 'industri_harian.csv.gz'), index=False, float_format='%.6g', compression='gzip')
    meta = {'dijana': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'saham': int(c.shape[1]),
            'bar': int(len(c)), 'dari': str(c.index[0].date()), 'hingga': str(c.index[-1].date()),
            'sampel_tarikh': int(d.tarikh.nunique()), 'baris': int(len(d)),
            'industri_purata_sehari': round(float(d.groupby('tarikh').ind.nunique().mean()), 1),
            'gagal_tarik': len(D.get('gagal', []))}
    json.dump(meta, open(os.path.join(a.keluar, 'meta.json'), 'w'), indent=1)
    ringkasan(a.keluar, R, T, meta)
    print(json.dumps(meta))


def ringkasan(keluar, R, T, meta):
    kol = ['varian'] + GRED + ['A-E', 't', 'tahun_positif_pct', 'monotonik', 'menang_A', 'menang_E'] + [f'A-E {t[0]}' for t in TEMPOH]
    bah = lambda s, h: md(R[(R.set == s) & (R.ufuk == h)][kol])
    lap = ["# Kajian gred industri lawan seluruh pasaran AS\n",
           f"Dijana {meta['dijana']} oleh `standard/kajian_industri.py` (GitHub Actions `kajian_industri.yml`). Jangan ubah secara manual.\n",
           f"Data: {meta['saham']} saham, {meta['bar']} bar ({meta['dari']} hingga {meta['hingga']}); {meta['sampel_tarikh']} tarikh sampel "
           f"(setiap {LANGKAH} hari), {meta['baris']:,} pemerhatian, ~{meta['industri_purata_sehari']} industri sehari. Saham layak: tutup >= "
           f"USD{HARGA_MIN:g}, nilai dagangan 50 hari >= USD1 juta; industri >= {MIN_SAHAM} saham layak. Gred ikut kuintil skor industri. "
           "Lebihan (%) = pulangan (buka esok hingga tutup hari ke-h) tolak purata semua saham layak pada tarikh sama, dipuratakan ikut tarikh. "
           "t dilaras tindih. Bias: saham yang sudah delist tiada; industri = klasifikasi Moomoo kini.\n"]
    n = 1
    for s in ['industri (sama berat)', 'semua saham', 'saham 431 (Shariah)', 'saiz kecil', 'saiz sederhana', 'saiz besar']:
        for h in UFUK:
            lap += [f"## {n}. {s}: {h} hari\n", bah(s, h), '']
            n += 1
    lap += [f"## {n}. A-E 21 hari ikut tahun, semua saham (%)\n", md(T)]
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

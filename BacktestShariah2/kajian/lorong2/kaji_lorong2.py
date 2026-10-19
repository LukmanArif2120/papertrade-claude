# Kajian lorong 2 "pegang selagi naik" (19 Okt 2026; laporan kajian/KAJIAN_LORONG2.md).
# Calon peraturan keluar dinilai atas SEMUA dagangan enjin v1.2 134 kaedah (set 431, data_mentah 2019–2026).
# Logik henti sama seperti standard/keluar_lorong.py; isyarat peraturan pada tutup -> jual pada buka esok.
# Guna (dari akar repo; perlu numba):
#   python3 BacktestShariah2/kajian/lorong2/kaji_lorong2.py jana      -> dagangan setiap kaedah (OUT/T/<ID>.pkl), ~10 minit
#   python3 BacktestShariah2/kajian/lorong2/kaji_lorong2.py sim       -> keputusan setiap calon, dengan/tanpa henti kaedah
#   python3 BacktestShariah2/kajian/lorong2/kaji_lorong2.py ringkas   -> jadual laporan
import argparse, glob, importlib, os, pickle, sys, time
import numpy as np, pandas as pd
from numba import njit

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
KOD = os.path.join(AKAR, 'BacktestShariah2', 'kod'); DM = os.path.join(AKAR, 'data_mentah')
OUT = os.environ.get('KAJIAN_LORONG2', '/tmp/kajian_lorong2')
COST = 0.001
SEMI = {'NVDA', 'AMD', 'MU', 'LRCX', 'AMAT', 'AVGO', 'TSM', 'ASML', 'MRVL', 'SMCI', 'ARM', 'ADI', 'ON', 'QCOM', 'INTC', 'TER'}


def muat():
    fr = {}
    for s in ['S1', 'S2', 'S3', 'S4']:
        d = pd.read_csv(f'{DM}/dataset_{s}.csv'); d['date'] = pd.to_datetime(d.date.astype(str))
        for t, g in d.groupby('ticker'): fr[t] = g.sort_values('date').set_index('date').copy()
    ix = pd.read_csv(f'{DM}/index_benchmark.csv'); ix['date'] = pd.to_datetime(ix.date.astype(str))
    return fr, {t: g.sort_values('date').set_index('date').copy() for t, g in ix.groupby('ticker')}


# ---------------------------------------------------------------- 1. dagangan kaedah (lorong 1 = enjin v1.2)
FR = IDX = None


def _init():
    global FR, IDX
    sys.path.insert(0, KOD); os.chdir(KOD); FR, IDX = muat()


def _kerja(mid):
    f = f'{OUT}/T/{mid}.pkl'
    if os.path.exists(f): return mid, 'ada'
    from enjin import trades
    m = importlib.import_module(f'kaedah.{mid}')
    fr = {t: g[['open', 'high', 'low', 'close', 'volume', 'turnover']].copy() for t, g in FR.items()}
    m.sedia(fr, {k: v.copy() for k, v in IDX.items()})
    T = trades(fr, tmax=m.TMAX, warm=m.WARM)
    if len(T): T['stop'] = [float(fr[r.ticker].stop.loc[r.sig]) if 'stop' in fr[r.ticker] else np.nan for r in T.itertuples()]
    T['mid'] = mid
    pickle.dump(T, open(f, 'wb')); return mid, len(T)


def cmd_jana(a):
    from multiprocessing import Pool
    os.makedirs(f'{OUT}/T', exist_ok=True)
    mids = sorted(os.path.basename(p)[:-3] for p in glob.glob(f'{KOD}/kaedah/M*.py'))
    with Pool(a.proses, initializer=_init) as p:
        for r in p.imap_unordered(_kerja, mids): print(*r, flush=True)


# ---------------------------------------------------------------- 2. simulasi calon lorong 2
@njit(cache=True)
def sim(o, h, l, c, lvl, we, pwc, ks, sps, jenis, p1, p2):
    """jenis 0 = p1 tutup turun berturut; 1 = Chandelier tinggi (tinggi tertinggi − p1×lvl); 6 = Chandelier tutup (tutup
    tertinggi − p1×lvl); p2 = 1 -> paras hanya naik; 2 = trailing p1 dari tutup tertinggi; 3 = p1 tutup berturut < lvl;
    4 = p1 minggu tutup mingguan turun; 9 = henti sahaja. Pulang j keluar, harga, kod (0 henti kaedah, 1 peraturan, 2 terbuka)."""
    m = len(ks); n = len(c); J = np.empty(m, np.int64); X = np.empty(m); W = np.empty(m, np.int64)
    for q in range(m):
        k = ks[q]; sp = sps[q]; ada = np.isfinite(sp); cnt = 0; hh = -1e18; hc = -1e18; lv = -1e18; siap = False
        for j in range(k, n):
            if ada:
                if j > k and o[j] <= sp:
                    J[q] = j; X[q] = o[j]; W[q] = 0; siap = True; break
                if l[j] <= sp:
                    J[q] = j; X[q] = sp; W[q] = 0; siap = True; break
            hh = max(hh, h[j]); hc = max(hc, c[j]); s = False
            if jenis == 0:
                if j >= 1:
                    cnt = cnt + 1 if c[j] < c[j - 1] else 0
                s = cnt >= p1
            elif jenis == 1 or jenis == 6:
                v = (hh if jenis == 1 else hc) - p1 * lvl[j]
                if p2 == 1:
                    lv = max(lv, v); v = lv
                s = c[j] < v
            elif jenis == 2:
                s = c[j] < hc * (1.0 - p1)
            elif jenis == 3:
                cnt = cnt + 1 if c[j] < lvl[j] else 0
                s = cnt >= p1
            elif jenis == 4:
                if we[j]:
                    cnt = cnt + 1 if c[j] < pwc[j] else 0
                    s = cnt >= p1
            if s:
                if j + 1 < n:
                    J[q] = j + 1; X[q] = o[j + 1]; W[q] = 1
                else:
                    J[q] = n - 1; X[q] = c[n - 1]; W[q] = 2
                siap = True; break
        if not siap:
            J[q] = n - 1; X[q] = c[n - 1]; W[q] = 2
    return J, X, W


CALON = [('L2 lama: 2 tutup turun', 0, 2, 0, None), ('3 tutup turun', 0, 3, 0, None), ('4 tutup turun', 0, 4, 0, None)] + \
    [(f'Chandelier {m}xATR14', 1, m, 0, 'atr14') for m in (2, 2.5, 3, 3.5, 4, 5)] + \
    [(f'Chandelier tutup {m}xATR14', 6, m, 0, 'atr14') for m in (3, 3.5, 4, 4.5, 5)] + \
    [(f'Chandelier tutup {m}xATR14 paras naik', 6, m, 1, 'atr14') for m in (3, 3.5, 4, 4.5, 5)] + \
    [('Chandelier tutup 4xATR22 paras naik', 6, 4, 1, 'atr22')] + \
    [(f'Trailing {int(p * 100)}% dari puncak', 2, p, 0, None) for p in (0.08, 0.10, 0.15, 0.20, 0.25)] + \
    [('Tutup < MA20', 3, 1, 0, 'ma20'), ('2 tutup < MA20', 3, 2, 0, 'ma20'), ('Tutup < MA50', 3, 1, 0, 'ma50'),
     ('Tutup < rendah 20 hari', 3, 1, 0, 'lo20'), ('2 minggu tutup turun', 4, 2, 0, None), ('Henti sahaja', 9, 0, 0, None)]


def tatasusunan(g):
    o, h, l, c = [g[x].to_numpy(float) for x in ('open', 'high', 'low', 'close')]
    s = pd.Series(c); pc = np.r_[np.nan, c[:-1]]
    tr = pd.Series(np.fmax(h - l, np.fmax(np.abs(h - pc), np.abs(l - pc))))
    A = dict(atr14=tr.rolling(14).mean().to_numpy(), atr22=tr.rolling(22).mean().to_numpy(),
             ma20=s.rolling(20).mean().to_numpy(), ma50=s.rolling(50).mean().to_numpy(),
             lo20=pd.Series(l).rolling(20).min().shift(1).to_numpy())
    A = {k: np.nan_to_num(v, nan=np.inf if k.startswith('atr') else -np.inf) for k, v in A.items()}   # tiada data -> tiada isyarat
    iso = g.index.isocalendar(); wk = (iso.year * 100 + iso.week).to_numpy()
    we = np.r_[wk[1:] != wk[:-1], g.index[-1].weekday() == 4]
    pwc = np.full(len(c), -np.inf); last = -np.inf
    for j in np.flatnonzero(we): pwc[j] = last; last = c[j]
    return o, h, l, c, A, we, pwc


def cmd_sim(a):
    T = pd.concat([pickle.load(open(f, 'rb')) for f in sorted(glob.glob(f'{OUT}/T/*.pkl'))], ignore_index=True)
    T = T[T.ent >= pd.Timestamp('2019-11-01')].reset_index(drop=True)
    fr, idx = muat(); so, sc = idx['SPY'].open, idx['SPY'].close
    N, P = len(T), len(CALON); print('dagangan', N, 'kaedah', T.mid.nunique(), flush=True)
    out = {}
    for henti in (True, False):
        R = {k: np.zeros((P, N), t) for k, t in (('ret', np.float32), ('hari', np.int32), ('kod', np.int8), ('spy', np.float32))}
        for t, G in T.groupby('ticker'):
            o, h, l, c, A, we, pwc = tatasusunan(fr[t]); dts = fr[t].index
            ks = dts.get_indexer(G.ent).astype(np.int64); ix = G.index.to_numpy(); e = o[ks]
            sps = G.stop.to_numpy(float) if henti else np.full(len(ks), np.nan)
            s0 = so.reindex(dts[ks]).to_numpy()
            if henti: T.loc[ix, 'mx120'] = [c[k:k + 120].max() / o[k] - 1 for k in ks]
            for r, (_, jn, p1, p2, lv) in enumerate(CALON):
                J, X, W = sim(o, h, l, c, A[lv] if lv else c, we, pwc, ks, sps, jn, float(p1), int(p2))
                R['ret'][r, ix] = X / e * (1 - COST) / (1 + COST) - 1; R['hari'][r, ix] = J - ks + 1; R['kod'][r, ix] = W
                R['spy'][r, ix] = sc.reindex(dts[J]).to_numpy() / s0 - 1
        out[henti] = R
    T.drop(columns=['mfe'], errors='ignore').to_pickle(f'{OUT}/T_semua.pkl'); pickle.dump(out, open(f'{OUT}/sim.pkl', 'wb'))


# ---------------------------------------------------------------- 3. ringkasan
def cmd_ringkas(a):
    T = pd.read_pickle(f'{OUT}/T_semua.pkl'); out = pickle.load(open(f'{OUT}/sim.pkl', 'rb'))
    jen = pd.read_csv(f'{KOD}/jenis_kaedah.csv').set_index('kaedah').jenis
    mids = T.mid.to_numpy(); yr = T.ent.dt.year.to_numpy(); pan = (T.mid.map(jen) == 'pantulan').to_numpy()
    besar = (T.mx120 >= 0.30).to_numpy()
    semi = (T.ticker.isin(SEMI) & (T.ent >= '2026-03-25') & (T.ent <= '2026-05-15')).to_numpy()
    l1 = pd.Series(T.ret.to_numpy(float)).groupby(mids).mean()
    pd.set_option('display.width', 250)
    for henti, R in out.items():
        rows = []
        for r, (lab, *_) in enumerate(CALON):
            x = R['ret'][r].astype(float); d = R['hari'][r].astype(float); ex = x - R['spy'][r].astype(float)
            row = dict(peraturan=lab, purata=x.mean() * 100, median=np.median(x) * 100, p5=np.percentile(x, 5) * 100, hari=d.mean(),
                       sebulan=x.mean() / d.mean() * 21 * 100, lebih_spy_sebulan=np.nanmean(ex) / d.mean() * 21 * 100,
                       besar=x[besar].mean() * 100, semikon26=x[semi].mean() * 100, momentum=np.nanmean(ex[~pan]) * 100,
                       pantulan=np.nanmean(ex[pan]) * 100, lawan_lorong1=(pd.Series(x).groupby(mids).mean() > l1).mean() * 100,
                       henti_kaedah=(R['kod'][r] == 0).mean() * 100)
            row.update({str(y): np.nanmean(ex[yr == y]) * 100 for y in range(2020, 2027)})
            rows.append(row)
        print(f"\n== {'DENGAN' if henti else 'TANPA'} henti kaedah ({len(T)} dagangan, {T.mid.nunique()} kaedah)")
        print(pd.DataFrame(rows).set_index('peraturan').round(1).to_string())
    x = T.ret.to_numpy(float)
    print(f'\nLorong 1 (kaedah): purata {x.mean() * 100:.1f}%, hari {T.days.mean():.1f}, trend besar {x[besar].mean() * 100:.1f}%, '
          f'semikon26 {x[semi].mean() * 100:.1f}%')
    R = out[False]; r = [c[0] for c in CALON].index('Chandelier tutup 4xATR14 paras naik'); d = R['hari'][r]
    print('Pegangan (hari dagangan) dipilih: semua p25/50/75', np.percentile(d, [25, 50, 75]), '| trend besar', np.percentile(d[besar], [25, 50, 75]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); s = ap.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('jana'); x.add_argument('--proses', type=int, default=4); x.set_defaults(f=cmd_jana)
    s.add_parser('sim').set_defaults(f=cmd_sim); s.add_parser('ringkas').set_defaults(f=cmd_ringkas)
    a = ap.parse_args(); a.f(a)

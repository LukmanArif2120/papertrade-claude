"""Jarak ke tinggi 52 minggu — pradaftar `REVERSE/SPEC_52W.md`.

8 band x 5 keluar x 2 tingkap, plus ujian URUTAN (desil keratan rentas + IC harian).
Takrif `tinggi_52w` sama baris dengan `step18_nxx.py:61`; pariti disemak sebelum apa-apa
nombor dilaporkan (spec §3, §11).

Guna: python3 REVERSE/step40_52w.py [--laporan-sahaja]
Output: REVERSE/JARAK_52W.md, REVERSE/jarak_52w.csv, REVERSE/jarak_52w_desil.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import kos as K  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = KELUAR / '.cache'
HARGA = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
PANEL = CACHE / 'panel_52w.parquet'

TH0, TH1 = 2012, 2025
LATIH, TAHAN = (2012, 2019), (2020, 2025)
ATR_N, TMAX = 14, 126
CAIR = 100_000.0
MIN_N = 200
MIN_HARI = 20
M_PRADAFTAR = 40          # spec §7 gate2: 8 band x 5 keluar
UFUK = (21, 63, 126)
XK = ['H21', 'H63', 'H126', 'X13', 'X15']

# spec §4 — dikunci
BAND = [('B0', 0.0, np.inf), ('B1', -2.0, 0.0), ('B2', -5.0, -2.0), ('B3', -10.0, -5.0),
        ('B4', -15.0, -10.0), ('B5', -25.0, -15.0), ('B6', -40.0, -25.0),
        ('B7', -np.inf, -40.0)]
NAMA_BAND = {'B0': 'di atas tinggi 52w', 'B1': '-2% .. 0%', 'B2': '-5% .. -2%',
             'B3': '-10% .. -5%', 'B4': '-15% .. -10%', 'B5': '-25% .. -15%',
             'B6': '-40% .. -25%', 'B7': 'bawah -40%'}


def _wilder(x, n):
    return pd.Series(x).ewm(alpha=1 / n, adjust=False, min_periods=n).mean().to_numpy()


def siri_ticker(g):
    """Satu ticker -> DataFrame per bar: j52, j52c, nilai20, 5 pulangan keluar."""
    o = g.open.to_numpy('float64')
    h = g.high.to_numpy('float64')
    lo = g.low.to_numpy('float64')
    c = g.close.to_numpy('float64')
    v = g.volume.to_numpy('float64')
    m = len(c)
    cs, vs, hs = pd.Series(c), pd.Series(v), pd.Series(h)
    pc = cs.shift(1)
    tr = np.maximum(h - lo, np.maximum((h - pc).abs(), (lo - pc).abs()))
    atr = _wilder(tr, ATR_N)
    dl = cs.diff()
    up = _wilder(dl.clip(lower=0).to_numpy(), ATR_N)
    dn = _wilder((-dl.clip(upper=0)).to_numpy(), ATR_N)
    rsi = 100 - 100 / (1 + up / (dn + 1e-12))
    nilai20 = (cs * vs).rolling(20, min_periods=10).median().to_numpy()

    # spec §3 — SAMA baris seperti step18_nxx.py:61 dan ind.py (varian tutup)
    t52 = hs.rolling(252, min_periods=200).max().shift(1).to_numpy()
    t52c = cs.rolling(252, min_periods=252).max().to_numpy()
    with np.errstate(invalid='ignore', divide='ignore'):
        j52 = (c / np.where(t52 > 0, t52, np.nan) - 1.0) * 100.0
        j52c = (c / np.where(t52c > 0, t52c, np.nan) - 1.0) * 100.0

    idx = np.arange(m)
    masuk = np.concatenate([o[1:], [np.nan]])          # beli buka esok (C01)
    ks = K.KOMISEN + np.array([K.slippage(x) for x in nilai20])
    d = {'j52': j52, 'j52c': j52c, 'nilai20': nilai20}

    def pulangan(px):
        with np.errstate(invalid='ignore', divide='ignore'):
            return (px * (1 - ks)) / (masuk * (1 + ks)) - 1.0

    # --- keluar ufuk tulen: pegang N sesi, jual buka ---
    for N in UFUK:
        kk = idx + 1 + N
        sah = kk < m
        px = np.where(sah, o[np.minimum(kk, m - 1)], np.nan)
        d[f'pul_H{N}'] = pulangan(px)

    # --- X13: rsi14 > 70 -> jual buka esok; TMAX 126; tiada henti ---
    # --- X15: Chandelier tutup 4xATR14 -> jual buka esok; TMAX 126 ---
    bar13, px13 = np.full(m, -1), np.full(m, np.nan)
    bar15, px15 = np.full(m, -1), np.full(m, np.nan)
    puncak = np.full(m, -np.inf)
    for j in range(1, TMAX + 1):
        s = np.minimum(idx + j, m - 1)                 # bar isyarat (hari pegang ke-j)
        e = np.minimum(s + 1, m - 1)                   # jual buka esok
        sah = (idx + j + 1) < m
        oe = np.where(sah, o[e], np.nan)
        cj = np.where(sah, c[s], np.nan)
        aj = np.where(sah, atr[s], np.nan)
        rj = np.where(sah, rsi[s], np.nan)
        kena = sah & (bar13 < 0) & np.isfinite(rj) & (rj > 70.0)
        bar13[kena], px13[kena] = e[kena], oe[kena]
        puncak = np.where(sah & np.isfinite(cj), np.maximum(puncak, cj), puncak)
        kena = (sah & (bar15 < 0) & np.isfinite(cj) & np.isfinite(aj)
                & (cj < puncak - 4.0 * aj))
        bar15[kena], px15[kena] = e[kena], oe[kena]
    ek = idx + 1 + TMAX
    sah_ek = ek < m
    for bb, pp in ((bar13, px13), (bar15, px15)):
        belum = bb < 0
        amb = belum & sah_ek
        pp[amb] = o[np.minimum(ek, m - 1)][amb]
        pp[belum & ~sah_ek] = np.nan
    d['pul_X13'] = pulangan(px13)
    d['pul_X15'] = pulangan(px15)

    out = pd.DataFrame(d)
    out.insert(0, 'date', g.date.to_numpy())
    out.insert(0, 'ticker', g.ticker.iloc[0])
    return out


def pariti():
    """Spec §3: tinggi_52w mesti identik dengan step18, j52c dengan ind.kira. Ralat -> batal."""
    import importlib
    s18 = importlib.import_module('REVERSE.step18_nxx')
    from REVERSE.teras import ind as I
    df = pd.read_parquet(HARGA / 'harga_2015.parquet',
                         columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
    bhg = [pd.read_parquet(HARGA / f'harga_{y}.parquet',
                           columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
           for y in (2012, 2013, 2014, 2016)]
    df = pd.concat([df] + bhg, ignore_index=True).sort_values(['ticker', 'date'])
    tick = sorted(df.ticker.unique())[:40]
    df = df[df.ticker.isin(tick)]
    n = 0
    for tk, g in df.groupby('ticker', sort=True):
        g = g.reset_index(drop=True)
        gi = g.set_index('date')
        a = s18.tambahan(gi)['tinggi_52w'].to_numpy()
        b = (gi['high'].rolling(252, min_periods=200).max().shift(1)).to_numpy()
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() and not np.array_equal(a[ok], b[ok]):
            raise SystemExit(f'PARITI GAGAL tinggi_52w pada {tk}')
        ind = I.kira(gi)
        jc = ind['j_52w_tinggi'].to_numpy()
        mine = ((gi['close'] / gi['close'].rolling(252, min_periods=252).max() - 1.0)
                * 100.0).to_numpy()
        ok = np.isfinite(jc) & np.isfinite(mine)
        if ok.sum() and not np.allclose(jc[ok], mine[ok], rtol=0, atol=1e-9):
            raise SystemExit(f'PARITI GAGAL j52c pada {tk}')
        n += 1
    print(f'  pariti LULUS pada {n} ticker (tinggi_52w vs step18, j52c vs ind.kira)', flush=True)


def bina():
    if PANEL.exists():
        return pd.read_parquet(PANEL)
    t0 = time.time()
    CACHE.mkdir(parents=True, exist_ok=True)
    bhgn = CACHE / 'panel_52w_parts'
    bhgn.mkdir(parents=True, exist_ok=True)
    for old in bhgn.glob('*.parquet'):
        old.unlink()
    bhg = []
    for y in range(TH0 - 3, TH1 + 1):
        p = HARGA / f'harga_{y}.parquet'
        if p.exists():
            bhg.append(pd.read_parquet(p, columns=['ticker', 'date', 'open', 'high', 'low',
                                                   'close', 'volume']))
    df = pd.concat(bhg, ignore_index=True)
    df = df[df.date <= pd.Timestamp(f'{TH1}-12-31')].sort_values(['ticker', 'date'])
    print(f'  [{time.time()-t0:.0f}s] bar mentah {len(df):,} | ticker {df.ticker.nunique():,}',
          flush=True)
    buf, j, n, jum = [], 0, 0, 0

    def _tulis(buf, j):
        R = pd.concat(buf, ignore_index=True)
        for c in R.columns:
            if R[c].dtype == 'float64':
                R[c] = R[c].astype('float32')
        R.to_parquet(bhgn / f'p{j:03d}.parquet', index=False)
        return len(R)

    for tk, g in df.groupby('ticker', sort=False):
        if len(g) < 320:
            continue
        buf.append(siri_ticker(g.reset_index(drop=True)))
        n += 1
        if len(buf) >= 400:
            jum += _tulis(buf, j)
            buf, j = [], j + 1
            print(f'    [{time.time()-t0:.0f}s] {n} ticker | {jum:,} bar', flush=True)
    if buf:
        jum += _tulis(buf, j)
    del df
    R = pd.read_parquet(bhgn)
    R.to_parquet(PANEL, index=False)
    for old in bhgn.glob('*.parquet'):
        old.unlink()
    bhgn.rmdir()
    print(f'  [{time.time()-t0:.0f}s] panel {len(R):,} bar x {R.shape[1]} lajur', flush=True)
    return R


def metrik(pul):
    pul = pul[np.isfinite(pul)]
    if pul.size == 0:
        return dict(n=0, menang=np.nan, untung=np.nan, rugi=np.nan, jangkaan=np.nan,
                    tanpa5=np.nan)
    w = pul > 0
    u = np.sort(pul)[::-1]
    return dict(n=int(pul.size), menang=float(w.mean() * 100),
                untung=float(pul[w].mean() * 100) if w.any() else 0.0,
                rugi=float(pul[~w].mean() * 100) if (~w).any() else 0.0,
                jangkaan=float(pul.mean() * 100),
                tanpa5=float(u[int(np.ceil(0.05 * u.size)):].mean() * 100) if u.size > 20
                else np.nan)


def t_beza_hari(pul, hari, dalam):
    """t satu hujung bagi (band - asas), SE berkelompok ikut hari beli.

    Setiap hari: min band hari itu - min SEMUA bar cair hari itu. t atas siri harian.
    """
    from scipy import stats as sps
    ok = np.isfinite(pul)
    pul, hari, dalam = pul[ok], hari[ok], dalam[ok]
    o = np.argsort(hari, kind='stable')
    pul, hari, dalam = pul[o], hari[o], dalam[o]
    sem = np.flatnonzero(np.concatenate([[True], hari[1:] != hari[:-1], [True]]))
    lo, hi = sem[:-1], sem[1:]
    n_all = hi - lo
    s_all = np.add.reduceat(pul, lo)
    n_bd = np.add.reduceat(dalam.astype('float64'), lo)
    s_bd = np.add.reduceat(np.where(dalam, pul, 0.0), lo)
    ada = n_bd > 0
    if ada.sum() < MIN_HARI:
        return np.nan, np.nan, int(ada.sum())
    diff = s_bd[ada] / n_bd[ada] - s_all[ada] / n_all[ada]
    k = diff.size
    se = diff.std(ddof=1) / np.sqrt(k)
    if not np.isfinite(se) or se <= 0:
        return np.nan, np.nan, k
    t = float(diff.mean() / se)
    return t, float(sps.t.sf(t, df=k - 1)), k


def bh_m(p, m, q=0.05):
    p = np.asarray(p, dtype='float64')
    lulus = np.zeros(p.size, dtype=bool)
    idx = np.flatnonzero(np.isfinite(p))
    if idx.size == 0:
        return lulus, np.nan
    srt = idx[np.argsort(p[idx])]
    amb = np.nan
    for i in range(srt.size - 1, -1, -1):
        if p[srt[i]] <= q * (i + 1) / m:
            amb = p[srt[i]]
            lulus[srt[:i + 1]] = True
            break
    return lulus, amb


def t_nw(x, lag):
    """t Newey-West bagi min siri (pulangan hadapan bertindih -> autokorelasi)."""
    x = np.asarray(x, dtype='float64')
    x = x[np.isfinite(x)]
    n = x.size
    if n < 30:
        return np.nan, 0
    e = x - x.mean()
    g0 = float(e @ e) / n
    s = g0
    for L in range(1, min(lag, n - 1) + 1):
        gl = float(e[L:] @ e[:-L]) / n
        s += 2.0 * (1.0 - L / (lag + 1.0)) * gl
    if s <= 0:
        return np.nan, n
    return float(x.mean() / np.sqrt(s / n)), n


def jalan(P):
    th = P.date.dt.year.to_numpy()
    cair = P.nilai20.to_numpy() >= CAIR
    hari = P.date.values.astype('datetime64[D]').astype('int64')
    j52 = P.j52.to_numpy('float64')
    j52c = P.j52c.to_numpy('float64')
    W = {'latih': (th >= LATIH[0]) & (th <= LATIH[1]) & cair & np.isfinite(j52),
         'tahan': (th >= TAHAN[0]) & (th <= TAHAN[1]) & cair & np.isfinite(j52)}
    baris = []
    for nama_w, wm in W.items():
        for kod in XK:
            pul = P[f'pul_{kod}'].to_numpy('float64')
            pw, hw, jw, jcw = pul[wm], hari[wm], j52[wm], j52c[wm]
            asas = metrik(pw)
            baris.append(dict(tingkap=nama_w, keluar=kod, band='ASAS', lo=np.nan, hi=np.nan,
                              varian='j52', **asas, lift=0.0, lift_tanpa5=0.0,
                              t=np.nan, p=np.nan, hari=np.nan))
            for varian, nilai in (('j52', jw), ('j52c', jcw)):
                for kodb, b0, b1 in BAND:
                    dalam = np.isfinite(nilai) & (nilai >= b0) & (nilai < b1)
                    mb = metrik(pw[dalam])
                    t, p, k = t_beza_hari(pw, hw, dalam)
                    baris.append(dict(tingkap=nama_w, keluar=kod, band=kodb, lo=b0, hi=b1,
                                      varian=varian, **mb,
                                      lift=mb['jangkaan'] - asas['jangkaan'],
                                      lift_tanpa5=mb['tanpa5'] - asas['tanpa5'],
                                      t=t, p=p, hari=k))
    R = pd.DataFrame(baris)
    # gate (spec §7) — hanya varian utama j52
    R['gate0'] = False
    R['gate1'] = False
    R['gate2'] = False
    R['gate3'] = False
    u = R[(R.varian == 'j52') & (R.band != 'ASAS')]
    for kod in XK:
        for kodb, _, _ in BAND:
            s = u[(u.keluar == kod) & (u.band == kodb)]
            if len(s) != 2:
                continue
            la = s[s.tingkap == 'latih'].iloc[0]
            ta = s[s.tingkap == 'tahan'].iloc[0]
            g0 = (la.n >= MIN_N) and (ta.n >= MIN_N)
            g1 = g0 and (la.lift > 0) and (ta.lift > 0)
            g3 = (ta.jangkaan > 0) and (ta.lift_tanpa5 > 0)
            for i in s.index:
                R.loc[i, 'gate0'] = bool(g0)
                R.loc[i, 'gate1'] = bool(g1)
                R.loc[i, 'gate3'] = bool(g3)
    mt = (R.varian == 'j52') & (R.band != 'ASAS') & (R.tingkap == 'tahan')
    lulus, amb = bh_m(R.loc[mt, 'p'].to_numpy(), M_PRADAFTAR)
    R.loc[mt, 'gate2'] = lulus
    for i in R.index[mt]:
        par = R[(R.varian == 'j52') & (R.band == R.at[i, 'band'])
                & (R.keluar == R.at[i, 'keluar']) & (R.tingkap == 'latih')]
        if len(par):
            R.loc[par.index[0], 'gate2'] = R.at[i, 'gate2']
    return R, amb


def urutan(P):
    """Spec §7 gate4: desil keratan rentas + IC harian (Spearman) dengan t Newey-West."""
    th = P.date.dt.year.to_numpy()
    cair = P.nilai20.to_numpy() >= CAIR
    out_d, out_ic = [], []
    for nama_w, (y0, y1) in (('latih', LATIH), ('tahan', TAHAN)):
        wm = (th >= y0) & (th <= y1) & cair & np.isfinite(P.j52.to_numpy())
        Q = P.loc[wm, ['date', 'j52'] + [f'pul_H{n}' for n in UFUK]]
        for N in UFUK:
            kol = f'pul_H{N}'
            S = Q[['date', 'j52', kol]].dropna()
            g = S.groupby('date', sort=True)
            n_hari = g.size()
            sah = n_hari[n_hari >= 20].index
            S = S[S.date.isin(sah)]
            g = S.groupby('date', sort=False)
            pr_j = g.j52.rank(pct=True)
            pr_r = g[kol].rank(pct=True)
            S = S.assign(rj=pr_j.to_numpy(), rr=pr_r.to_numpy())
            # IC harian = Spearman = korelasi Pearson atas pangkat (agregat, bukan apply)
            A = pd.DataFrame({'date': S.date.to_numpy(), 'x': S.rj.to_numpy(),
                              'y': S.rr.to_numpy()})
            A['xy'] = A.x * A.y
            A['xx'] = A.x * A.x
            A['yy'] = A.y * A.y
            gg = A.groupby('date', sort=True)
            nn_h = gg.size().to_numpy('float64')
            sx = gg.x.sum().to_numpy('float64')
            sy = gg.y.sum().to_numpy('float64')
            sxy = gg.xy.sum().to_numpy('float64')
            sxx = gg.xx.sum().to_numpy('float64')
            syy = gg.yy.sum().to_numpy('float64')
            mx, my = sx / nn_h, sy / nn_h
            cov = sxy / nn_h - mx * my
            vx = np.maximum(sxx / nn_h - mx * mx, 0.0)
            vy = np.maximum(syy / nn_h - my * my, 0.0)
            with np.errstate(invalid='ignore', divide='ignore'):
                ic = pd.Series(cov / np.sqrt(vx * vy), index=gg.size().index)
            t, nn = t_nw(ic.to_numpy(), lag=N)
            out_ic.append(dict(tingkap=nama_w, ufuk=N, ic_min=float(np.nanmean(ic)),
                               ic_median=float(np.nanmedian(ic)), t_nw=t, hari=nn,
                               positif=float(np.nanmean(ic.to_numpy() > 0) * 100)))
            des = np.minimum((S.rj.to_numpy() * 10).astype(int), 9) + 1
            S = S.assign(desil=des)
            dd = S.groupby('desil')[kol].agg(['mean', 'median', 'size'])
            for k, r in dd.iterrows():
                out_d.append(dict(tingkap=nama_w, ufuk=N, desil=int(k),
                                  jangkaan=float(r['mean'] * 100),
                                  median=float(r['median'] * 100), n=int(r['size']),
                                  j52_min=float(S.loc[S.desil == k, 'j52'].min()),
                                  j52_maks=float(S.loc[S.desil == k, 'j52'].max()),
                                  j52_median=float(S.loc[S.desil == k, 'j52'].median())))
    return pd.DataFrame(out_d), pd.DataFrame(out_ic)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f_r = KELUAR / 'jarak_52w.csv'
    f_d = KELUAR / 'jarak_52w_desil.csv'
    f_i = KELUAR / 'jarak_52w_ic.csv'
    if a.laporan_sahaja and f_r.exists():
        R, D, I2 = pd.read_csv(f_r), pd.read_csv(f_d), pd.read_csv(f_i)
        amb = np.nan
    else:
        print('[1/4] pariti', flush=True)
        pariti()
        print('[2/4] panel', flush=True)
        P = bina()
        P['date'] = pd.to_datetime(P['date'])
        print('[3/4] band', flush=True)
        R, amb = jalan(P)
        R.to_csv(f_r, index=False)
        print('[4/4] urutan', flush=True)
        D, I2 = urutan(P)
        D.to_csv(f_d, index=False)
        I2.to_csv(f_i, index=False)
    laporan(R, D, I2, amb)
    print('siap: REVERSE/JARAK_52W.md')


def _b(x, n=3):
    return '—' if not np.isfinite(x) else f'{x:+.{n}f}'


def laporan(R, D, I2, amb):
    L = ['# Jarak ke tinggi 52 minggu — keputusan', '',
         f'Pradaftar `REVERSE/SPEC_52W.md`. Dijalankan {pd.Timestamp.today():%Y-%m-%d}.',
         'Alam A02 2012–2025, bar cair (median nilai 20 hari ≥ USD100k), masuk buka esok,',
         'kos penuh dua sisi, `stop = NaN` pada kesemua keluar.', '']
    asas = {(r.tingkap, r.keluar): r for r in
            R[(R.band == 'ASAS')].itertuples()}
    L += ['## 1. Asas (semua bar cair, tiada penapis)', '',
          '| Keluar | Tingkap | n | Menang | Jangkaan | `tanpa5` |', '|---|---|---|---|---|---|']
    for kod in XK:
        for w in ('latih', 'tahan'):
            r = asas.get((w, kod))
            if r is None:
                continue
            L.append(f'| `{kod}` | {w} | {r.n:,} | {r.menang:.1f}% | {_b(r.jangkaan)}% | '
                     f'{_b(r.tanpa5)}% |')
    L.append('')
    U = R[(R.varian == 'j52') & (R.band != 'ASAS')]
    for kod in XK:
        L += [f'## 2.{XK.index(kod)+1} Band × `{kod}`', '',
              '| Band | n latih | n tahan | Jangkaan latih | Jangkaan tahan | Lift latih | '
              'Lift tahan | Menang tahan | `tanpa5` tahan | Lift `tanpa5` | p (tahan) | Gate |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|']
        for kodb, _, _ in BAND:
            la = U[(U.keluar == kod) & (U.band == kodb) & (U.tingkap == 'latih')]
            ta = U[(U.keluar == kod) & (U.band == kodb) & (U.tingkap == 'tahan')]
            if not len(la) or not len(ta):
                continue
            la, ta = la.iloc[0], ta.iloc[0]
            g = []
            for nm in ('gate0', 'gate1', 'gate2', 'gate3'):
                g.append(nm[-1] if bool(ta[nm]) else '')
            gs = ''.join(g) or '—'
            L.append(f'| `{kodb}` {NAMA_BAND[kodb]} | {la.n:,} | {ta.n:,} | '
                     f'{_b(la.jangkaan)}% | {_b(ta.jangkaan)}% | {_b(la.lift)} | '
                     f'{_b(ta.lift)} | {ta.menang:.1f}% | {_b(ta.tanpa5)}% | '
                     f'{_b(ta.lift_tanpa5)} | '
                     f'{"—" if not np.isfinite(ta.p) else f"{ta.p:.2g}"} | {gs} |')
        L.append('')
    L += ['### Kiraan gate (varian `j52`, 40 sel)', '',
          '| Gate | Lulus |', '|---|---|']
    T = U[U.tingkap == 'tahan']
    for nm, ket in (('gate0', 'n ≥ 200 dua tingkap'), ('gate1', 'lift > 0 DUA tingkap'),
                    ('gate2', f'BH-FDR m={M_PRADAFTAR}'),
                    ('gate3', 'jangkaan > 0 DAN lift tanpa5 > 0')):
        L.append(f'| `{nm}` ({ket}) | **{int(T[nm].sum())}/40** |')
    semua = T[T.gate0 & T.gate1 & T.gate2 & T.gate3]
    L += ['', f'Lulus **kesemua** gate0–gate3: **{len(semua)}/40**'
          + ('' if len(semua) == 0 else ' — ' + ', '.join(
              f'`{r.band}×{r.keluar}`' for r in semua.itertuples())) + '.',
          f'Ambang BH: {"—" if not np.isfinite(amb) else f"{amb:.2g}"}.', '']
    # varian j52c
    L += ['## 3. Kekukuhan konvensyen: `j52c` (tinggi 252 sesi atas TUTUP, termasuk hari ini)', '',
          '| Band | Jangkaan tahan `j52` | Jangkaan tahan `j52c` | Lift `j52` | Lift `j52c` |',
          '|---|---|---|---|---|']
    for kodb, _, _ in BAND:
        a = R[(R.varian == 'j52') & (R.band == kodb) & (R.keluar == 'H126')
              & (R.tingkap == 'tahan')]
        b = R[(R.varian == 'j52c') & (R.band == kodb) & (R.keluar == 'H126')
              & (R.tingkap == 'tahan')]
        if not len(a) or not len(b):
            continue
        a, b = a.iloc[0], b.iloc[0]
        L.append(f'| `{kodb}` {NAMA_BAND[kodb]} | {_b(a.jangkaan)}% | {_b(b.jangkaan)}% | '
                 f'{_b(a.lift)} | {_b(b.lift)} |')
    L += ['', '(`H126`; `j52c` ≤ 0 secara binaan jadi band `B0` kosong/kecil.)', '']
    # urutan
    L += ['## 4. Urutan (paksi U) — desil keratan rentas', '']
    for N in UFUK:
        L += [f'### Ufuk {N} sesi', '',
              '| Desil | `j52` median | n latih | Jangkaan latih | n tahan | Jangkaan tahan |',
              '|---|---|---|---|---|---|']
        for k in range(1, 11):
            la = D[(D.tingkap == 'latih') & (D.ufuk == N) & (D.desil == k)]
            ta = D[(D.tingkap == 'tahan') & (D.ufuk == N) & (D.desil == k)]
            if not len(la) or not len(ta):
                continue
            la, ta = la.iloc[0], ta.iloc[0]
            L.append(f'| D{k} | {ta.j52_median:+.1f}% | {la.n:,} | {_b(la.jangkaan)}% | '
                     f'{ta.n:,} | {_b(ta.jangkaan)}% |')
        L.append('')
    from scipy.stats import spearmanr
    L += ['### IC harian (Spearman `j52` lawan pulangan hadapan), t Newey-West', '',
          '| Tingkap | Ufuk | IC min | IC median | % hari positif | t (NW) | Hari | '
          'Monoton desil (rho) |', '|---|---|---|---|---|---|---|---|']
    for w in ('latih', 'tahan'):
        for N in UFUK:
            r = I2[(I2.tingkap == w) & (I2.ufuk == N)]
            d = D[(D.tingkap == w) & (D.ufuk == N)].sort_values('desil')
            rho = (spearmanr(d.desil.to_numpy(), d.jangkaan.to_numpy()).statistic
                   if len(d) >= 3 else np.nan)
            if not len(r):
                continue
            r = r.iloc[0]
            L.append(f'| {w} | {N} | {r.ic_min:+.4f} | {r.ic_median:+.4f} | '
                     f'{r.positif:.1f}% | {_b(r.t_nw, 2)} | {int(r.hari):,} | {_b(rho, 2)} |')
    L.append('')
    (KELUAR / 'JARAK_52W.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()

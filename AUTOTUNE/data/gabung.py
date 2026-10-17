"""Gabung shard, QC, universe bulanan titik-masa, kumpulan A/B (SPEC §1).
Cth: gabung.py --masuk DIR_SHARD --keluar DIR_KELUAR  (tulis juga AUTOTUNE/data/manifest.json + QC.md)"""
import argparse
import datetime as dt
import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LAJUR = ['open', 'high', 'low', 'close', 'volume']
HARGA4 = ['open', 'high', 'low', 'close']
N_UNIVERSE = 2000
HARGA_MIN = 10.0
DV_MIN = 1e6
BAR_MIN = 200
TETINGKAP = 60
BAR60_MIN = 50          # sekurang-kurangnya 50 daripada 60 bar sah untuk median (toleransi bar hilang)
LOMPAT = 0.5
HARI_LOMPAT_MAX = 5
BENCH = ('SPY', 'QQQ')


def kumpulan(ticker):
    """A jika int(md5(ticker).hexdigest(), 16) % 2 == 0, selain itu B (SPEC §1)."""
    return 'A' if int(hashlib.md5(ticker.encode()).hexdigest(), 16) % 2 == 0 else 'B'


def bersih(df):
    """Buang bar harga <= 0 / NaN / high < low. Pulangkan (df_bersih, bilangan_dibuang). Volume NaN/neg -> 0."""
    p = df[HARGA4]
    ok = p.notna().all(axis=1) & (p > 0).all(axis=1) & (df['high'] >= df['low'])
    out = df[ok].copy()
    out['volume'] = out['volume'].fillna(0).clip(lower=0)
    return out, int((~ok).sum())


def bilangan_lompat(df, ambang=LOMPAT):
    """Bilangan hari |pulangan harian close| > ambang bagi setiap ticker (df telah disusun ticker,date)."""
    c = df['close'].to_numpy(dtype='float64')
    t = df['ticker'].to_numpy()
    r = np.full(len(df), np.nan)
    if len(df) > 1:
        sama = t[1:] == t[:-1]
        r[1:][sama] = c[1:][sama] / c[:-1][sama] - 1
    lompat = pd.Series(np.abs(r) > ambang, index=df.index)
    return lompat.groupby(df['ticker'].to_numpy()).sum().astype(int)


def bina_universe(close, vol, kal, dikecualikan=()):
    """Universe bulanan titik-masa. close/vol: DataFrame lebar (tarikh x ticker, float), kal: DatetimeIndex.
    Pada hari dagangan terakhir bulan m: close > 10, median(close*volume, 60 hari) >= 1e6, >= 200 bar;
    2000 teratas ikut median; berkuat kuasa bulan m+1. Pulangkan DataFrame bulan,ticker,kedudukan,kumpulan."""
    close = close.reindex(kal)
    vol = vol.reindex(kal)
    tick = [t for t in close.columns if t not in set(dikecualikan) and t not in BENCH]
    C = close[tick].to_numpy(dtype='float32')
    dv = C * vol[tick].to_numpy(dtype='float32')
    bar = np.cumsum(~np.isnan(C), axis=0)
    per = kal.to_period('M')
    akhir = np.flatnonzero(np.append(per[1:] != per[:-1], True))
    tick_a = np.array(tick, dtype=object)
    baris = []
    for p in akhir:
        win = dv[max(0, p - TETINGKAP + 1):p + 1]
        sah = (~np.isnan(win)).sum(axis=0)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            med = np.nanmedian(win, axis=0)
        ok = (C[p] > HARGA_MIN) & (med >= DV_MIN) & (bar[p] >= BAR_MIN) & (sah >= BAR60_MIN)
        idx = np.flatnonzero(ok)
        if len(idx) == 0:
            continue
        susun = idx[np.argsort(-med[idx], kind='stable')][:N_UNIVERSE]
        bulan = str(per[p] + 1)
        for k, j in enumerate(susun, 1):
            baris.append((bulan, tick_a[j], k))
    u = pd.DataFrame(baris, columns=['bulan', 'ticker', 'kedudukan'])
    u['kumpulan'] = u['ticker'].map(kumpulan)
    u['kedudukan'] = u['kedudukan'].astype('int16')
    return u


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def baca_shard(masuk):
    fail = sorted(Path(masuk).rglob('shard_*.parquet'))
    if not fail:
        raise SystemExit('tiada shard_*.parquet')
    df = pd.concat([pd.read_parquet(f) for f in fail], ignore_index=True)
    stat = []
    for f in sorted(Path(masuk).rglob('shard_*.json')):
        stat.append(json.loads(f.read_text()))
    return df, stat


def proses(masuk, keluar, calon_fail=None, tarikan=None, repo_dir=HERE):
    keluar = Path(keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    df, stat = baca_shard(masuk)
    df['date'] = pd.to_datetime(df['date']).astype('datetime64[ns]')
    df = df.drop_duplicates(['ticker', 'date'], keep='last').sort_values(['ticker', 'date']).reset_index(drop=True)
    n_dimuat = df.ticker.nunique()
    df, n_buang = bersih(df)
    df = df.reset_index(drop=True)

    idx_df = df[df.ticker.isin(BENCH)]
    if set(idx_df.ticker.unique()) != set(BENCH):
        raise SystemExit('SPY/QQQ tiada dalam data')
    sah = df[~df.ticker.isin(BENCH)].reset_index(drop=True)

    lompat = bilangan_lompat(sah)
    bendera = lompat[lompat > HARI_LOMPAT_MAX].index.tolist()
    kal = pd.DatetimeIndex(sorted(idx_df[idx_df.ticker == 'SPY'].date.unique()))
    close = sah.pivot(index='date', columns='ticker', values='close')
    vol = sah.pivot(index='date', columns='ticker', values='volume')
    univ = bina_universe(close, vol, kal, dikecualikan=bendera)
    del close, vol

    ada = set(univ.ticker.unique())
    qc = sah.groupby('ticker').agg(bar=('date', 'size'), pertama=('date', 'min'), terakhir=('date', 'max'))
    qc['lompat50'] = lompat.reindex(qc.index).fillna(0).astype(int)
    qc['bendera'] = qc.index.isin(bendera)
    qc['dalam_universe'] = qc.index.isin(ada)
    qc['kumpulan'] = [kumpulan(t) for t in qc.index]
    qc = qc.reset_index()
    qc['pertama'] = qc.pertama.dt.strftime('%Y-%m-%d')
    qc['terakhir'] = qc.terakhir.dt.strftime('%Y-%m-%d')
    qc.to_csv(keluar / 'qc.csv', index=False)

    simpan = pd.concat([sah[sah.ticker.isin(ada)], idx_df], ignore_index=True)
    simpan = simpan.sort_values(['ticker', 'date']).reset_index(drop=True)
    for c in HARGA4:
        simpan[c] = simpan[c].astype('float32')
    simpan['volume'] = simpan['volume'].astype('float64')
    idx_out = simpan[simpan.ticker.isin(BENCH)]
    idx_out.to_parquet(keluar / 'idx.parquet', index=False, compression='zstd')
    ekuiti = simpan[~simpan.ticker.isin(BENCH)]
    for y, g in ekuiti.groupby(ekuiti.date.dt.year):
        g.to_parquet(keluar / f'harga_{y}.parquet', index=False, compression='zstd')
    univ.to_parquet(keluar / 'universe.parquet', index=False, compression='zstd')

    fail = sorted(p for p in keluar.iterdir() if p.suffix in ('.parquet', '.csv'))
    manifest = {
        'tag': 'autotune-data',
        'tarikan': tarikan or dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
        'n_ticker': int(ekuiti.ticker.nunique()),
        'tarikh_mula': str(simpan.date.min().date()),
        'tarikh_akhir': str(simpan.date.max().date()),
        'fail': [{'nama': p.name, 'bait': p.stat().st_size, 'sha256': sha256(p)} for p in fail],
    }
    (keluar / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    Path(repo_dir, 'manifest.json').write_text(json.dumps(manifest, indent=1))

    n_calon = len(Path(calon_fail).read_text().split()) if calon_fail and Path(calon_fail).exists() else None
    tulis_qc(Path(repo_dir) / 'QC.md', manifest, univ, qc, n_calon, n_dimuat, n_buang, stat, bendera)
    return manifest, univ, qc


def tulis_qc(laluan, manifest, univ, qc, n_calon, n_dimuat, n_buang, stat, bendera):
    gagal = sum(s['gagal'] for s in stat) if stat else None
    u = univ.groupby('bulan').size().rename('n').reset_index()
    u['tahun'] = u.bulan.str[:4]
    ring = u.groupby('tahun').n.agg(['min', 'median', 'max'])
    ab = univ.groupby('bulan').kumpulan.value_counts().unstack(fill_value=0).mean().round(0)
    jumlah_mb = sum(f['bait'] for f in manifest['fail']) / 1e6
    L = ['# QC data AUTOTUNE', '',
         f"- Tarikan: {manifest['tarikan']}; julat bar {manifest['tarikh_mula']} hingga {manifest['tarikh_akhir']}",
         f'- Calon: {n_calon}; dimuat turun (ada data, termasuk SPY/QQQ): {n_dimuat}; gagal: {gagal}',
         f'- Bar dibuang (harga <=0/NaN/high<low): {n_buang}',
         f'- Ticker ditanda (>{HARI_LOMPAT_MAX} hari |pulangan|>50%, dikeluarkan): {len(bendera)}'
         + (f" (cth {', '.join(bendera[:8])})" if bendera else ''),
         f"- Ticker pernah dalam universe (disimpan dalam harga_*.parquet): {manifest['n_ticker']}",
         f"- Ticker unik dalam universe: {univ.ticker.nunique()}; baris universe: {len(univ)}",
         f"- Kumpulan (ticker pernah dalam universe): A={int((qc[qc.dalam_universe].kumpulan == 'A').sum())}, "
         f"B={int((qc[qc.dalam_universe].kumpulan == 'B').sum())}; purata sebulan A={int(ab.get('A', 0))}, B={int(ab.get('B', 0))}",
         f'- Saiz aset Release: {jumlah_mb:.0f} MB', '',
         f'Saiz universe sebulan mengikut tahun berkuat kuasa (min / median / maks):', '',
         '| Tahun | min | median | maks |', '|---|---|---|---|']
    for y, r in ring.iterrows():
        L.append(f"| {y} | {int(r['min'])} | {int(r['median'])} | {int(r['max'])} |")
    L += ['', 'Nota: median nilai dagangan 60 hari memerlukan >= 50 bar sah; ticker ditanda dan ticker yang tidak pernah '
          'layak dibuang daripada harga_*.parquet (senarai penuh dalam qc.csv). Tiada saham delist (bias survivorship).']
    Path(laluan).write_text('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--masuk', required=True)
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--calon', default=str(HERE / 'calon.txt'))
    a = ap.parse_args()
    m, u, qc = proses(a.masuk, a.keluar, a.calon)
    print(f"ticker={m['n_ticker']} universe_baris={len(u)} bulan={u.bulan.nunique()} "
          f"bendera={int(qc.bendera.sum())} fail={len(m['fail'])} "
          f"MB={sum(f['bait'] for f in m['fail']) / 1e6:.0f}")


if __name__ == '__main__':
    main()

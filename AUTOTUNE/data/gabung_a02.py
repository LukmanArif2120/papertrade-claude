"""Gabung shard A02: QC peringkat bar, universe bulanan titik-masa berasaskan harga tidak dilaras, kumpulan A/B (SPEC_A02 §1).
A01 (gabung.py) tidak diubah. Cth: gabung_a02.py --masuk DIR_SHARD --keluar DIR_KELUAR
(tulis juga AUTOTUNE/data/manifest_a02.json + QC_A02.md)."""
import argparse
import datetime as dt
import importlib.util
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def _muat_a01():
    sp = importlib.util.spec_from_file_location('at_gabung_a01', HERE / 'gabung.py')
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A01 = _muat_a01()
HARGA4 = A01.HARGA4
BENCH = A01.BENCH
N_UNIVERSE, HARGA_MIN, DV_MIN, BAR_MIN = A01.N_UNIVERSE, A01.HARGA_MIN, A01.DV_MIN, A01.BAR_MIN
TETINGKAP, BAR60_MIN = A01.TETINGKAP, A01.BAR60_MIN
LONJAKAN = 0.40
TAG = 'autotune-data-a02'
SEMAK = {'NVDA': 'NVDA', 'AAPL': 'AAPL', 'TSLA': 'TSLA', 'AVGO': 'AVGO', 'NFLX': 'NFLX', 'ANET': 'ANET',
         'SMCI': 'SMCI', 'CMG': 'CMG'}
SEMAK_BULAN = ('2013-06', '2016-06', '2019-06')
kumpulan = A01.kumpulan


def qc_bar(df, ambang=LONJAKAN):
    """QC peringkat bar (df: ticker,date,open..volume,... tersusun ticker,date).
    Buang bar t jika (a) harga <=0/NaN atau high<low; (b) |r_t|>ambang dan r_{t+1} berbalik arah dengan |r_{t+1}|>ambang
    (r = pulangan close tertib; hanya bar t dibuang). Pulangkan (df_bersih, DataFrame bar dibuang: ticker,date,sebab,close,r_t,r_t1).
    Volume NaN/negatif -> 0."""
    p = df[HARGA4]
    tak_sah = ~(p.notna().all(axis=1) & (p > 0).all(axis=1))
    hl = ~tak_sah & (df['high'] < df['low'])
    ok = ~(tak_sah | hl)
    dibuang = [df.loc[tak_sah, ['ticker', 'date', 'close']].assign(sebab='harga_tidak_sah', r_t=np.nan, r_t1=np.nan),
               df.loc[hl, ['ticker', 'date', 'close']].assign(sebab='high<low', r_t=np.nan, r_t1=np.nan)]
    d = df[ok].reset_index(drop=True)
    c = d['close'].to_numpy(dtype='float64')
    t = d['ticker'].to_numpy()
    n = len(d)
    r = np.full(n, np.nan)
    r1 = np.full(n, np.nan)
    if n > 1:
        sama = t[1:] == t[:-1]
        rr = np.where(sama, c[1:] / c[:-1] - 1, np.nan)
        r[1:] = rr          # r[i] = pulangan bar i berbanding bar i-1
        r1[:-1] = rr        # r1[i] = pulangan bar i+1 berbanding bar i
    with np.errstate(invalid='ignore'):
        lonjak = (np.abs(r) > ambang) & (np.abs(r1) > ambang) & (np.sign(r) != np.sign(r1))
    dibuang.append(d.loc[lonjak, ['ticker', 'date', 'close']].assign(sebab='lonjakan', r_t=r[lonjak], r_t1=r1[lonjak]))
    d = d[~lonjak].copy()
    d['volume'] = d['volume'].fillna(0).clip(lower=0)
    db = pd.concat(dibuang, ignore_index=True)
    db['date'] = pd.to_datetime(db['date']).dt.strftime('%Y-%m-%d')
    return d.reset_index(drop=True), db[['ticker', 'date', 'sebab', 'close', 'r_t', 'r_t1']]


def bina_universe(close, vol, fak, kal, dikecualikan=()):
    """Universe bulanan titik-masa A02. close/vol/fak: DataFrame lebar (tarikh x ticker); close dilaras (auto_adjust),
    fak = faktor_split. Pada hari dagangan terakhir bulan m: tutup_mentah = close*fak > 10; median 60 hari
    (tutup_mentah * volum_mentah = close*volume, volum_mentah = volume/fak) >= 1e6; >= 200 bar (>=50 sah dalam 60 hari);
    2000 teratas; berkuat kuasa bulan m+1. Pulangkan DataFrame bulan,ticker,kedudukan,kumpulan."""
    close = close.reindex(kal)
    vol = vol.reindex(kal)
    tick = [t for t in close.columns if t not in set(dikecualikan) and t not in BENCH]
    fak = fak.reindex(index=kal, columns=tick)
    C = close[tick].to_numpy(dtype='float64')
    F = fak.to_numpy(dtype='float64')
    V = vol[tick].to_numpy(dtype='float64')
    mentah = C * F                      # tutup_mentah
    dv = mentah * (V / F)               # tutup_mentah * volum_mentah
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
        with np.errstate(invalid='ignore'):
            ok = (mentah[p] > HARGA_MIN) & (med >= DV_MIN) & (bar[p] >= BAR_MIN) & (sah >= BAR60_MIN)
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


def proses(masuk, keluar, calon_fail=None, tarikan=None, repo_dir=HERE):
    keluar = Path(keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    df, stat = A01.baca_shard(masuk)
    if 'faktor_split' not in df.columns:
        raise SystemExit('shard tiada lajur faktor_split (guna muat_turun_a02.py)')
    df['date'] = pd.to_datetime(df['date']).astype('datetime64[ns]')
    df = df.drop_duplicates(['ticker', 'date'], keep='last').sort_values(['ticker', 'date']).reset_index(drop=True)
    n_dimuat = df.ticker.nunique()
    n_split_tick = int(df.groupby('ticker').faktor_split.agg(lambda s: (s != 1.0).any()).sum())
    df, qc = qc_bar(df)

    idx_df = df[df.ticker.isin(BENCH)]
    if set(idx_df.ticker.unique()) != set(BENCH):
        raise SystemExit('SPY/QQQ tiada dalam data')
    sah = df[~df.ticker.isin(BENCH)].reset_index(drop=True)
    kal = pd.DatetimeIndex(sorted(idx_df[idx_df.ticker == 'SPY'].date.unique()))
    close = sah.pivot(index='date', columns='ticker', values='close')
    vol = sah.pivot(index='date', columns='ticker', values='volume')
    fak = sah.pivot(index='date', columns='ticker', values='faktor_split')
    univ = bina_universe(close, vol, fak, kal)
    del close, vol, fak

    ada = set(univ.ticker.unique())
    qc.to_csv(keluar / 'qc.csv', index=False)

    simpan = pd.concat([sah[sah.ticker.isin(ada)], idx_df], ignore_index=True)
    simpan = simpan.sort_values(['ticker', 'date']).reset_index(drop=True)
    for c in HARGA4 + ['faktor_split']:
        simpan[c] = simpan[c].astype('float32')
    simpan['volume'] = simpan['volume'].astype('float64')
    simpan[simpan.ticker.isin(BENCH)].to_parquet(keluar / 'idx.parquet', index=False, compression='zstd')
    ekuiti = simpan[~simpan.ticker.isin(BENCH)]
    for y, g in ekuiti.groupby(ekuiti.date.dt.year):
        g.to_parquet(keluar / f'harga_{y}.parquet', index=False, compression='zstd')
    univ.to_parquet(keluar / 'universe.parquet', index=False, compression='zstd')

    fail = sorted(p for p in keluar.iterdir() if p.suffix in ('.parquet', '.csv'))
    manifest = {
        'tag': TAG,
        'tarikan': tarikan or dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
        'n_ticker': int(ekuiti.ticker.nunique()),
        'tarikh_mula': str(simpan.date.min().date()),
        'tarikh_akhir': str(simpan.date.max().date()),
        'fail': [{'nama': p.name, 'bait': p.stat().st_size, 'sha256': A01.sha256(p)} for p in fail],
    }
    (keluar / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    Path(repo_dir, 'manifest_a02.json').write_text(json.dumps(manifest, indent=1))

    n_calon = len(Path(calon_fail).read_text().split()) if calon_fail and Path(calon_fail).exists() else None
    tulis_qc(Path(repo_dir) / 'QC_A02.md', manifest, univ, qc, n_calon, n_dimuat, n_split_tick, stat)
    return manifest, univ, qc


def semak_keahlian(univ, tickers=tuple(SEMAK), bulan=SEMAK_BULAN):
    """{ticker: {bulan: kedudukan atau None}}."""
    out = {}
    for t in tickers:
        out[t] = {}
        for b in bulan:
            r = univ[(univ.bulan == b) & (univ.ticker == t)]
            out[t][b] = int(r.kedudukan.iloc[0]) if len(r) else None
    return out


def tulis_qc(laluan, manifest, univ, qc, n_calon, n_dimuat, n_split_tick, stat):
    gagal = sum(s['gagal'] for s in stat) if stat else None
    u = univ.groupby('bulan').size().rename('n').reset_index()
    u['tahun'] = u.bulan.str[:4]
    ring = u.groupby('tahun').n.agg(['min', 'median', 'max'])
    ab = univ.groupby('bulan').kumpulan.value_counts().unstack(fill_value=0).mean().round(0)
    jumlah_mb = sum(f['bait'] for f in manifest['fail']) / 1e6
    kira = qc.sebab.value_counts().to_dict()
    kum = {k: int(univ.drop_duplicates('ticker').kumpulan.eq(k).sum()) for k in 'AB'}
    L = ['# QC data AUTOTUNE A02', '',
         f"- Tarikan: {manifest['tarikan']}; julat bar {manifest['tarikh_mula']} hingga {manifest['tarikh_akhir']}",
         f'- Calon: {n_calon}; dimuat turun (ada data, termasuk SPY/QQQ): {n_dimuat}; gagal: {gagal}',
         f'- Ticker dengan sekurang-kurangnya satu split: {n_split_tick} (lajur faktor_split; harga kekal auto_adjust)',
         f"- Bar dibuang: {len(qc)} (harga tidak sah {kira.get('harga_tidak_sah', 0)}, high<low {kira.get('high<low', 0)}, "
         f"lonjakan >{int(LONJAKAN * 100)}% yang berbalik {kira.get('lonjakan', 0)}); senarai penuh dalam qc.csv",
         '- Tiada ticker dibuang kerana kemeruapan',
         f"- Ticker pernah dalam universe (disimpan dalam harga_*.parquet): {manifest['n_ticker']}",
         f"- Baris universe: {len(univ)}; kumpulan (ticker pernah dalam universe): A={kum['A']}, B={kum['B']}; "
         f"purata sebulan A={int(ab.get('A', 0))}, B={int(ab.get('B', 0))}",
         f'- Saiz aset Release: {jumlah_mb:.0f} MB', '',
         'Saiz universe sebulan mengikut tahun berkuat kuasa (min / median / maks):', '',
         '| Tahun | min | median | maks |', '|---|---|---|---|']
    for y, r in ring.iterrows():
        L.append(f"| {y} | {int(r['min'])} | {int(r['median'])} | {int(r['max'])} |")
    sk = semak_keahlian(univ)
    L += ['', 'Semakan keahlian universe (kedudukan ikut median nilai dagangan; "-" = tiada):', '',
          '| Ticker | ' + ' | '.join(SEMAK_BULAN) + ' |', '|---|' + '---|' * len(SEMAK_BULAN)]
    for t, d in sk.items():
        L.append(f'| {t} | ' + ' | '.join(str(d[b]) if d[b] is not None else '-' for b in SEMAK_BULAN) + ' |')
    L += ['', 'Nota: harga universe = close dilaras x faktor_split (tidak dilaras split, tetapi masih dilaras dividen); '
          'median 60 hari memerlukan >= 50 bar sah. Tiada saham delist (bias survivorship; had atas).']
    Path(laluan).write_text('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--masuk', required=True)
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--calon', default=str(HERE / 'calon.txt'))
    a = ap.parse_args()
    m, u, qc = proses(a.masuk, a.keluar, a.calon)
    print(f"ticker={m['n_ticker']} universe_baris={len(u)} bulan={u.bulan.nunique()} bar_dibuang={len(qc)} "
          f"fail={len(m['fail'])} MB={sum(f['bait'] for f in m['fail']) / 1e6:.0f}")


if __name__ == '__main__':
    main()

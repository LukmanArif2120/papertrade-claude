"""Lapisan data REVERSE: harga A02, universe titik-masa, sektor/industri, indeks sektor.

Harga: Release `autotune-data-a02` melalui AUTOTUNE/teras/data.py `ambil()` (tiada pemuat baharu).
Sektor/industri: BacktestShariah2/papertrade/peta_industri.csv (industri Moomoo -> 11 sektor
Morningstar, sektor_pasaran.SEKTOR_INDUSTRI); sandaran BacktestShariah2/data/skrin/tv_us.csv.
Kaveat: peta sektor ini bukan titik-masa (petikan 2026); sektor syarikat jarang berubah.
"""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
sys.path.insert(0, str(AKAR / 'BacktestShariah2' / 'standard'))
from AUTOTUNE.teras.data import ambil  # noqa: E402

TAG = 'autotune-data-a02'
CACHE = AKAR / 'REVERSE' / '.cache'
LAJUR = ['open', 'high', 'low', 'close', 'volume']


def _peta_sektor():
    """DataFrame indeks ticker, lajur industri + sektor."""
    from sektor_pasaran import SEKTOR_INDUSTRI
    p = pd.read_csv(AKAR / 'BacktestShariah2' / 'papertrade' / 'peta_industri.csv')
    p = p[['ticker', 'industri']].dropna().drop_duplicates('ticker')
    p['sektor'] = p['industri'].map(SEKTOR_INDUSTRI)
    # Sandaran tv_us: HANYA industri dipakai, dipeta semula ke 11 sektor Morningstar supaya
    # taksonomi kekal satu (taksonomi sektor TradingView TIDAK dicampur).
    tv = pd.read_csv(AKAR / 'BacktestShariah2' / 'data' / 'skrin' / 'tv_us.csv',
                     usecols=['ticker', 'industry']).dropna(subset=['ticker'])
    tv = tv.drop_duplicates('ticker').rename(columns={'industry': 'industri'})
    tv['sektor'] = tv['industri'].map(SEKTOR_INDUSTRI)
    tv['sumber'] = 'tv_us'
    p['sumber'] = 'peta_industri'
    gab = pd.concat([p, tv[~tv.ticker.isin(set(p.ticker))]], ignore_index=True)
    gab = gab.set_index('ticker')
    gab['sektor'] = gab['sektor'].fillna('Lain-lain')
    gab['industri'] = gab['industri'].fillna('Lain-lain')
    return gab


def peta_sektor(tickers):
    """Peta sektor/industri bagi senarai ticker; kelas saham (BRK-B) jatuh balik ke ticker asas."""
    gab = _peta_sektor()
    rows = []
    for t in tickers:
        if t in gab.index:
            r = gab.loc[t]
            rows.append((t, r['industri'], r['sektor'], r['sumber']))
            continue
        asas = t.split('-')[0]
        if asas in gab.index:
            r = gab.loc[asas]
            rows.append((t, r['industri'], r['sektor'], 'kelas_asas'))
        else:
            rows.append((t, 'Lain-lain', 'Lain-lain', 'tiada'))
    return pd.DataFrame(rows, columns=['ticker', 'industri', 'sektor', 'sumber_sektor']).set_index('ticker')


def tickers_tahun(tahun, univ=None, kumpulan='AB'):
    """Ticker yang ada dalam universe sekurang-kurangnya satu bulan dalam `tahun`."""
    univ = universe() if univ is None else univ
    m = (univ['bulan'].str[:4] == str(tahun)) & univ['kumpulan'].isin(list(kumpulan))
    return sorted(univ.loc[m, 'ticker'].unique())


_UNIV = {}


def universe():
    if 'u' not in _UNIV:
        _UNIV['u'] = pd.read_parquet(ambil(tag=TAG) / 'universe.parquet')
    return _UNIV['u']


def topeng_bulan(univ):
    """Set (ticker, YYYYMM) keahlian universe — untuk tapis peristiwa/run ikut bulan."""
    bi = (univ['bulan'].str[:4] + univ['bulan'].str[5:7]).astype(int)
    return set(zip(univ['ticker'].to_numpy(), bi.to_numpy()))


def muat_harga(tickers, mula, akhir):
    """{ticker: DataFrame OHLCV float64 indeks tarikh} bagi [mula, akhir]."""
    d = ambil(tag=TAG)
    mula, akhir = pd.Timestamp(mula), pd.Timestamp(akhir)
    tick = list(tickers)
    bahagian = []
    for y in range(mula.year, akhir.year + 1):
        p = d / f'harga_{y}.parquet'
        if p.exists():
            bahagian.append(pd.read_parquet(p, filters=[('ticker', 'in', tick)]))
    fr = {}
    if bahagian:
        df = pd.concat(bahagian, ignore_index=True)
        df = df[(df['date'] >= mula) & (df['date'] <= akhir)]
        for t, g in df.groupby('ticker', sort=True):
            fr[t] = g.sort_values('date').set_index('date')[LAJUR].astype('float64')
    return fr


def muat_indeks(mula, akhir):
    """{'SPY': Series tutup, 'QQQ': Series tutup} dan DataFrame OHLCV penuh."""
    d = ambil(tag=TAG)
    ix = pd.read_parquet(d / 'idx.parquet')
    ix = ix[(ix['date'] >= pd.Timestamp(mula)) & (ix['date'] <= pd.Timestamp(akhir))]
    out = {}
    for t, g in ix.groupby('ticker'):
        out[t] = g.sort_values('date').set_index('date')[LAJUR].astype('float64')
    return out


def indeks_sektor(fr, peta, univ, kalendar):
    """Indeks sektor berpemberat sama (pindaan SPEC 27 Okt 2026: ganti ETF SPDR).

    Setiap hari: pulangan sektor = MEDIAN pulangan harian ahli universe (titik masa) dalam sektor itu;
    indeks = hasil darab kumulatif (1 + median). Pulangan dikira daripada tutup A02.
    Pulangan ahli hanya dikira pada hari yang bulannya ahli itu ada dalam universe.
    """
    ahli = topeng_bulan(univ)
    kal = pd.DatetimeIndex(kalendar)
    ym = kal.year * 100 + kal.month
    sekt = sorted(set(peta['sektor']))
    pul = {s: [] for s in sekt}
    for t, g in fr.items():
        if t not in peta.index:
            continue
        s = peta.loc[t, 'sektor']
        r = g['close'].pct_change().reindex(kal)
        sah = np.array([(t, int(x)) in ahli for x in ym])
        pul[s].append(r.where(sah))
    out = {}
    for s, lst in pul.items():
        if not lst:
            continue
        m = pd.concat(lst, axis=1).median(axis=1, skipna=True).fillna(0.0)
        out[s] = (1.0 + m).cumprod()
    return pd.DataFrame(out, index=kal)


def ambil_data():
    """Pastikan aset Release A02 ada; pulangkan Path cache."""
    return ambil(tag=TAG)

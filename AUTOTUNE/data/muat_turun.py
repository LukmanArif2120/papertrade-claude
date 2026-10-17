"""Muat turun satu shard harga yfinance (SPEC §1).
Cth: muat_turun.py --shard 0 --shards 10 --mula 2009-01-01 --keluar DIR"""
import argparse
import datetime as dt
import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd

LAJUR = ['open', 'high', 'low', 'close', 'volume']
PETA = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}


def _satu(d, t):
    """Satu DataFrame yfinance (lajur Open..Volume) -> bentuk standard; None jika kosong."""
    if d is None or len(d) == 0:
        return None
    d = d.rename(columns=PETA)
    if not set(LAJUR) <= set(d.columns):
        return None
    d = d[LAJUR].dropna(how='all', subset=['open', 'high', 'low', 'close'])
    if d.empty:
        return None
    idx = pd.DatetimeIndex(d.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    d = d.copy()
    d.index = idx.normalize()
    d.index.name = 'date'
    d = d[~d.index.duplicated(keep='last')].reset_index()
    d.insert(0, 'ticker', t)
    return d


def urai(df, kelompok):
    """Keluaran yf.download (group_by='ticker') -> {ticker: DataFrame standard}."""
    out = {}
    if df is None or len(df) == 0:
        return out
    if isinstance(df.columns, pd.MultiIndex):
        for t in pd.unique(df.columns.get_level_values(0)):
            if t in kelompok:
                r = _satu(df[t], t)
                if r is not None:
                    out[t] = r
    elif len(kelompok) == 1:
        r = _satu(df, kelompok[0])
        if r is not None:
            out[kelompok[0]] = r
    return out


def tarik_kelompok(yf, kelompok, mula):
    try:
        df = yf.download(kelompok, start=mula, auto_adjust=True, group_by='ticker', threads=True,
                         progress=False)
    except Exception as e:  # rangkaian / had kadar
        print(f'  ralat kelompok: {type(e).__name__}: {str(e)[:100]}', flush=True)
        return {}
    return urai(df, kelompok)


def tarik_satu(yf, t, mula):
    try:
        d = yf.Ticker(t).history(start=mula, auto_adjust=True)
    except Exception:
        return None
    return _satu(d, t)


def potong_hari_ini(d):
    """Buang bar bertarikh hari ini jika pasaran AS mungkin belum tutup (sebelum 22:00 UTC)."""
    n = dt.datetime.now(dt.timezone.utc)
    if n.hour < 22:
        d = d[d['date'] < pd.Timestamp(n.date())]
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, required=True)
    ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--mula', default='2009-01-01')
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--calon', default=str(Path(__file__).parent / 'calon.txt'))
    ap.add_argument('--lote', type=int, default=50)
    ap.add_argument('--jeda', type=float, default=2.0)
    ap.add_argument('--cuba', type=int, default=3)
    a = ap.parse_args()
    import yfinance as yf
    logging.getLogger('yfinance').setLevel(logging.CRITICAL)

    calon = [t for t in Path(a.calon).read_text().split() if t]
    senarai = calon[a.shard::a.shards]
    if a.shard == 0:
        senarai = senarai + [t for t in ('SPY', 'QQQ') if t not in senarai]
    print(f'shard {a.shard}/{a.shards}: {len(senarai)} ticker, mula={a.mula}', flush=True)

    hasil = {}
    for i in range(0, len(senarai), a.lote):
        k = senarai[i:i + a.lote]
        r = tarik_kelompok(yf, k, a.mula)
        if len(r) < 0.1 * len(k):  # kemungkinan had kadar: tunggu, cuba kelompok sekali lagi
            time.sleep(30)
            r2 = tarik_kelompok(yf, k, a.mula)
            if len(r2) > len(r):
                r = r2
        hasil.update(r)
        if (i // a.lote) % 10 == 0:
            print(f'  {min(i + a.lote, len(senarai))}/{len(senarai)} dapat={len(hasil)}', flush=True)
        time.sleep(a.jeda)

    gagal = [t for t in senarai if t not in hasil]
    n_kelompok_gagal = len(gagal)
    for pusingan in range(a.cuba):
        if not gagal:
            break
        print(f'  cuba semula {pusingan + 1}: {len(gagal)} ticker', flush=True)
        time.sleep(5 * (pusingan + 1))
        baki = []
        for t in gagal:
            d = tarik_satu(yf, t, a.mula)
            if d is None:
                baki.append(t)
            else:
                hasil[t] = d
            time.sleep(0.3)
        gagal = baki

    keluar = Path(a.keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    n_bar = 0
    if hasil:
        df = pd.concat(hasil.values(), ignore_index=True)
        df['date'] = pd.to_datetime(df['date']).astype('datetime64[ns]')
        df = potong_hari_ini(df)
        for c in ('open', 'high', 'low', 'close'):
            df[c] = df[c].astype('float32')
        df['volume'] = df['volume'].astype('float64')
        df.to_parquet(keluar / f'shard_{a.shard}.parquet', index=False, compression='zstd')
        n_bar = len(df)
    stat = {'shard': a.shard, 'diminta': len(senarai), 'dapat': len(hasil), 'gagal': len(gagal),
            'gagal_selepas_kelompok': n_kelompok_gagal, 'bar': n_bar, 'gagal_senarai': gagal}
    (keluar / f'shard_{a.shard}.json').write_text(json.dumps(stat))
    print(f'siap: diminta={len(senarai)} dapat={len(hasil)} gagal={len(gagal)} bar={n_bar}', flush=True)
    if len(hasil) < 0.5 * len(senarai):
        sys.exit('kadar kejayaan < 50%: kemungkinan had kadar Yahoo')


if __name__ == '__main__':
    main()

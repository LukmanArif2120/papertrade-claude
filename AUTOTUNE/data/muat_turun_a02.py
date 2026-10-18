"""Muat turun satu shard harga yfinance untuk A02 (SPEC_A02 §1): harga auto_adjust=True (seperti A01) DITAMBAH
peristiwa split -> lajur `faktor_split(t)` = hasil darab nisbah split yang bertarikh SELEPAS t (1.0 jika tiada).
tutup_mentah = close * faktor_split. A01 (muat_turun.py) tidak diubah.
Cth: muat_turun_a02.py --shard 0 --shards 10 --mula 2009-01-01 --keluar DIR"""
import argparse
import importlib.util
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent


def _muat_a01():
    sp = importlib.util.spec_from_file_location('at_muat_turun_a01', _HERE / 'muat_turun.py')
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A01 = _muat_a01()
LAJUR = A01.LAJUR


def faktor_split(tarikh, splits):
    """tarikh: DatetimeIndex bar; splits: Series (indeks tarikh efektif split -> nisbah, cth 4.0 bagi 4:1, 0.1 bagi 1:10).
    Pulangkan ndarray float64: hasil darab nisbah split dengan tarikh split STRICTLY selepas setiap tarikh bar."""
    tarikh = pd.DatetimeIndex(tarikh)
    if splits is None or len(splits) == 0:
        return np.ones(len(tarikh))
    s = splits.sort_index()
    sd = pd.DatetimeIndex(s.index).values
    r = s.to_numpy(dtype='float64')
    # akhiran[k] = hasil darab r[k:], akhiran[n] = 1
    akhiran = np.append(np.cumprod(r[::-1])[::-1], 1.0)
    k = np.searchsorted(sd, tarikh.values, side='right')  # bilangan split dengan tarikh <= tarikh bar
    return akhiran[k]


def _splits(d):
    """Series nisbah split (indeks tarikh tz-naif ternormal) daripada lajur 'Stock Splits'; kosong jika tiada."""
    if d is None or 'Stock Splits' not in d.columns:
        return pd.Series(dtype='float64')
    s = pd.to_numeric(d['Stock Splits'], errors='coerce').dropna()
    s = s[(s > 0) & (s != 1.0)]
    if s.empty:
        return pd.Series(dtype='float64')
    idx = pd.DatetimeIndex(s.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    s = pd.Series(s.to_numpy(dtype='float64'), index=idx.normalize())
    return s.groupby(level=0).prod()


def _satu(d, t):
    """DataFrame yfinance (OHLCV + 'Stock Splits') -> bentuk standard + faktor_split; None jika kosong."""
    r = A01._satu(d, t)
    if r is None:
        return None
    r['faktor_split'] = faktor_split(pd.DatetimeIndex(r['date']), _splits(d)).astype('float32')
    return r


def urai(df, kelompok):
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
        df = yf.download(kelompok, start=mula, auto_adjust=True, actions=True, group_by='ticker', threads=True,
                         progress=False)
    except Exception as e:
        print(f'  ralat kelompok: {type(e).__name__}: {str(e)[:100]}', flush=True)
        return {}
    return urai(df, kelompok)


def tarik_satu(yf, t, mula):
    try:
        d = yf.Ticker(t).history(start=mula, auto_adjust=True, actions=True)
    except Exception:
        return None
    return _satu(d, t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, required=True)
    ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--mula', default='2009-01-01')
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--calon', default=str(_HERE / 'calon.txt'))
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
    print(f'shard {a.shard}/{a.shards}: {len(senarai)} ticker, mula={a.mula} (A02: actions=True)', flush=True)

    hasil = {}
    for i in range(0, len(senarai), a.lote):
        k = senarai[i:i + a.lote]
        r = tarik_kelompok(yf, k, a.mula)
        if len(r) < 0.1 * len(k):
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
    n_split = None
    if hasil:
        df = pd.concat(hasil.values(), ignore_index=True)
        df['date'] = pd.to_datetime(df['date']).astype('datetime64[ns]')
        df = A01.potong_hari_ini(df)
        for c in ('open', 'high', 'low', 'close'):
            df[c] = df[c].astype('float32')
        df['volume'] = df['volume'].astype('float64')
        df['faktor_split'] = df['faktor_split'].astype('float32')
        df.to_parquet(keluar / f'shard_{a.shard}.parquet', index=False, compression='zstd')
        n_bar = len(df)
        g = df.groupby('ticker').faktor_split
        n_split = int(((g.min() != 1.0) | (g.max() != 1.0)).sum())
    stat = {'shard': a.shard, 'diminta': len(senarai), 'dapat': len(hasil), 'gagal': len(gagal),
            'gagal_selepas_kelompok': n_kelompok_gagal, 'bar': n_bar, 'ticker_ada_split': n_split,
            'gagal_senarai': gagal}
    (keluar / f'shard_{a.shard}.json').write_text(json.dumps(stat))
    print(f'siap: diminta={len(senarai)} dapat={len(hasil)} gagal={len(gagal)} bar={n_bar} ada_split={n_split}',
          flush=True)
    if len(hasil) < 0.5 * len(senarai):
        sys.exit('kadar kejayaan < 50%: kemungkinan had kadar Yahoo')


if __name__ == '__main__':
    main()

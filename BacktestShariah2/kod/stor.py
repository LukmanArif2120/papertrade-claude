"""Stor harga harian untuk scan Papertrade.
Fail: harga_A.csv (saham set 431), harga_B.csv (saham lain), harga_idx.csv (SPY, QQQ).
Lajur: ticker,date(YYYYMMDD),open,high,low,close,volume
"""
import pandas as pd, numpy as np, json, os, glob

SIMPAN_BAR = 520
LAJ = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']


def baca_kline(path):
    d = json.load(open(path))
    if isinstance(d, list):
        d = json.loads(d[0]['text'])
    kl = d['data']['kline_list']
    return pd.DataFrame([(b['date'], b['open'], b['high'], b['low'], b['close'], b['volume']) for b in kl],
                        columns=['date', 'open', 'high', 'low', 'close', 'volume'])


def muat(folder):
    out = {}
    for nm in ['harga_A.csv', 'harga_B.csv', 'harga_idx.csv']:
        p = os.path.join(folder, nm)
        if os.path.exists(p):
            out[nm] = pd.read_csv(p)
    return out


def simpan(folder, frames):
    for nm, d in frames.items():
        d = d.sort_values(['ticker', 'date']).drop_duplicates(['ticker', 'date'], keep='last')
        d = d.groupby('ticker', group_keys=False).tail(SIMPAN_BAR)
        d[LAJ].to_csv(os.path.join(folder, nm), index=False, float_format='%.6g')


def gabung_kline(d, ticker, kl):
    """Gabung bar kline (DataFrame) ke stor d untuk satu ticker, dengan penyelarasan jika harga lama berbeza (split/dividen)."""
    lama = d[d.ticker == ticker]
    kl = kl.copy(); kl['ticker'] = ticker
    if len(lama):
        sama = lama.merge(kl, on='date', suffixes=('_l', '_k'))
        if len(sama):
            r = (sama.close_k / sama.close_l).median()
            if abs(r - 1) > 0.003:  # harga lama perlu dilaras
                lama = lama.copy()
                for c in ['open', 'high', 'low', 'close']:
                    lama[c] = lama[c] * r
                lama['volume'] = (lama['volume'] / r).round()
        lama = lama[~lama.date.isin(kl.date)]
    baru = pd.concat([d[d.ticker != ticker], lama, kl[LAJ]], ignore_index=True)
    return baru


def frames_dict(frames):
    """-> fr (dict ticker->DataFrame berindeks tarikh), idx (SPY/QQQ)"""
    fr = {}
    for nm in ['harga_A.csv', 'harga_B.csv']:
        if nm not in frames: continue
        for t, g in frames[nm].groupby('ticker'):
            g = g.sort_values('date').copy(); g.index = pd.to_datetime(g.date.astype(str)); g.index.name = 'date'
            fr[t] = g[['open', 'high', 'low', 'close', 'volume']].astype(float)
    idx = {}
    if 'harga_idx.csv' in frames:
        for t, g in frames['harga_idx.csv'].groupby('ticker'):
            g = g.sort_values('date').copy(); g.index = pd.to_datetime(g.date.astype(str)); g.index.name = 'date'
            idx[t] = g[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return fr, idx

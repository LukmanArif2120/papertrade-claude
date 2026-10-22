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


TOL_LARAS = 0.003       # beza median tutup bertindih minimum sebelum sejarah lama dilaras
SERAK_MAKS = 0.002      # pelarasan sah (pecahan/faktor vendor) = nisbah SERAGAM merentas semua bar bertindih
NISBAH_PECAHAN = (1.25, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 25, 30, 50, 100)
LOG_LARAS = []          # rekod keputusan laras larian ini (pemanggil menulis ke log_laras.csv)


def nisbah_laras(lama, baru):
    """Keputusan bagi sejarah lama apabila bar bertindih (tarikh sama) berbeza (22 Okt 2026; laporan kajian
    'Pengesanan data tercemar yang tinggal'). Pulang (r, keputusan, n, serak):
      'sama'    |median r - 1| <= 0.3%: tiada laras (bar baharu menggantikan bar bertindih sahaja)
      'laras'   nisbah seragam (serak <= 0.2%) dan >= 3 bar bertindih atau r = nisbah pecahan lazim: darab sejarah lama r
      'anomali' selainnya (sebahagian bar sahaja berubah, ralat vendor, 1–2 bar bukan nisbah pecahan): sejarah lama TIDAK
                diubah. Dahulu median sahaja menentukan dan seluruh sejarah boleh dilaras oleh satu bar salah."""
    sama = lama.merge(baru, on='date', suffixes=('_l', '_k'))
    if not len(sama):
        return 1.0, 'tiada', 0, 0.0
    rr = (sama.close_k / sama.close_l).astype(float)
    r, n = float(rr.median()), int(len(rr))
    serak = float(rr.max() / rr.min() - 1) if rr.min() > 0 else float('inf')
    if abs(r - 1) <= TOL_LARAS:
        return r, 'sama', n, serak
    pecahan = any(abs(r * k - 1) < 0.01 or abs(r / k - 1) < 0.01 for k in NISBAH_PECAHAN)
    if serak <= SERAK_MAKS and (n >= 3 or pecahan):
        return r, 'laras', n, serak
    return r, 'anomali', n, serak


def gabung_kline(d, ticker, kl, sumber='kline'):
    """Gabung bar kline (DataFrame) ke stor d untuk satu ticker. Sejarah lama dilaras hanya jika nisbah bertindih seragam
    (nisbah_laras); keputusan selain 'sama'/'tiada' direkod dalam LOG_LARAS."""
    lama = d[d.ticker == ticker]
    kl = kl.copy(); kl['ticker'] = ticker
    if len(lama):
        r, kep, n, serak = nisbah_laras(lama, kl)
        if kep == 'laras':
            lama = lama.copy()
            for c in ['open', 'high', 'low', 'close']:
                lama[c] = lama[c] * r
            lama['volume'] = (lama['volume'] / r).round()
        if kep in ('laras', 'anomali'):
            LOG_LARAS.append(dict(ticker=ticker, nisbah=round(r, 6), bar=n, serak=round(serak, 6), keputusan=kep, sumber=sumber))
        lama = lama[~lama.date.isin(kl.date)]
    baru = pd.concat([d[d.ticker != ticker], lama, kl[LAJ]], ignore_index=True)
    return baru


def tulis_log_laras(folder, rekod, masa=None):
    """Tambah rekod laras/anomali ke <folder>/log_laras.csv (tambah sahaja)."""
    if not rekod:
        return 0
    p = os.path.join(folder, 'log_laras.csv')
    x = pd.DataFrame(rekod).assign(masa=masa or pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'))
    x = x[['masa', 'ticker', 'nisbah', 'bar', 'serak', 'keputusan', 'sumber']]
    x.to_csv(p, mode='a', header=not os.path.exists(p), index=False)
    return len(x)


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

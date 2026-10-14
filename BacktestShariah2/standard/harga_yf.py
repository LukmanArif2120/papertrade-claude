"""Harga harian percuma (yfinance) untuk stor harga papertrade.

Dijalankan oleh GitHub Actions (`.github/workflows/harga_harian.yml`) selepas pasaran AS tutup;
sesi Claude tidak boleh capai Yahoo (polisi rangkaian), jadi tugasan Claude hanya membaca fail di repo.

Subarahan:
  python3 harga_yf.py terkini  [--hari 10]        -> data/harga/terkini.csv (10 sesi terakhir, semua universe)
  python3 harga_yf.py sejarah  [--maks 300]       -> data/harga/sejarah.csv (520 bar; ticker dalam perlu_sejarah.txt)
  python3 harga_yf.py gabung   --stor DIR [--fail F ...]   gabung ke stor harga_A/B/idx.csv (format kod/stor.py);
                                                         lalai terkini.csv; sejarah.csv hanya jika diberi dengan --fail
  python3 harga_yf.py semak    --kline TICKER=fail.json ... banding dengan kline Moomoo; keluar 1 jika beza > 0.5%

Universe = set 431 (data_mentah/dataset_S*.csv) + semua saham dalam papertrade/*.csv + data/harga/univ.txt
(senarai skrin Shariah Moomoo, ditulis oleh imbasan 8:02 malam) + SPY, QQQ.
Harga: OHLC mentah (auto_adjust=False; split dilaras oleh Yahoo, dividen tidak). Sumber tidak rasmi —
Moomoo menang jika berbeza.
"""
import sys, os, json, glob, argparse, time
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
ROOT = os.path.dirname(BS2)
HARGA = os.path.join(BS2, 'data', 'harga')
sys.path.insert(0, os.path.join(BS2, 'kod'))
from stor import LAJ, SIMPAN_BAR, baca_kline  # noqa: E402

IDX = ['SPY', 'QQQ']
TOLERANSI = 0.005


def ke_yahoo(t):
    return t.replace('.', '-')


def dari_yahoo(t):
    return t.replace('-', '.')


def set_431():
    s = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'data_mentah', 'dataset_S*.csv'))):
        s |= set(pd.read_csv(f, usecols=['ticker']).ticker.dropna().astype(str))
    return s


def universe():
    s = set_431()
    for f in glob.glob(os.path.join(BS2, 'papertrade', '*.csv')):
        d = pd.read_csv(f, nrows=0)
        kol = next((c for c in d.columns if c.lower() in ('saham', 'ticker')), None)
        if kol and not f.endswith(('peta_industri.csv', 'sektor_pasaran.csv', 'sektor.csv')):
            s |= set(pd.read_csv(f, usecols=[kol])[kol].dropna().astype(str).str.strip())
    u = os.path.join(HARGA, 'univ.txt')
    if os.path.exists(u):
        s |= {x.strip() for x in open(u) if x.strip()}
    s = {t.replace('US.', '') for t in s if t and t.replace('.', '').replace('-', '').isalnum()}
    return sorted(s - set(IDX)), IDX


def panjang(df):
    """DataFrame yf.download (lajur MultiIndex (medan, ticker)) -> format panjang LAJ."""
    if df is None or df.empty:
        return pd.DataFrame(columns=LAJ)
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError('jangka lajur MultiIndex (group_by=column)')
    d = df.stack(level=1, future_stack=True).reset_index()
    d.columns = [str(c).lower() for c in d.columns]
    d = d.rename(columns={'level_1': 'ticker', 'date': 'date'})
    d['ticker'] = d['ticker'].map(dari_yahoo)
    d['date'] = pd.to_datetime(d['date']).dt.strftime('%Y%m%d').astype(int)
    return bersih(d[LAJ])


def bersih(d):
    d = d.dropna(subset=['open', 'high', 'low', 'close']).copy()
    h = d[['open', 'high', 'low', 'close']]
    ok = (h > 0).all(axis=1)
    # high/low mesti meliputi open/close (toleransi bundar)
    ok &= d.high >= h[['open', 'close', 'low']].max(axis=1) * (1 - 1e-4)
    ok &= d.low <= h[['open', 'close', 'high']].min(axis=1) * (1 + 1e-4)
    d = d[ok]
    d['volume'] = d['volume'].fillna(0).clip(lower=0).round().astype('int64')
    return d.sort_values(['ticker', 'date']).reset_index(drop=True)


def muat_turun(tickers, period, kumpulan=200, cuba=3):
    import yfinance as yf
    out, gagal = [], []
    for i in range(0, len(tickers), kumpulan):
        ks = [ke_yahoo(t) for t in tickers[i:i + kumpulan]]
        for n in range(cuba):
            try:
                df = yf.download(ks, period=period, interval='1d', auto_adjust=False, actions=False,
                                 group_by='column', threads=True, progress=False)
                d = panjang(df)
                break
            except Exception as e:  # had kadar / rangkaian
                if n == cuba - 1:
                    print(f'kumpulan {i}: gagal ({e})', file=sys.stderr); d = pd.DataFrame(columns=LAJ)
                time.sleep(20 * (n + 1))
        out.append(d)
        gagal += [dari_yahoo(k) for k in ks if dari_yahoo(k) not in set(d.ticker)]
        time.sleep(2)
    return (pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=LAJ)), gagal


def sesi_terakhir():
    import exchange_calendars as xc
    c = xc.get_calendar('XNYS')
    now = pd.Timestamp.now(tz='America/New_York')
    d = now.normalize().tz_localize(None)
    if c.is_session(d) and now.hour * 60 + now.minute >= 16 * 60 + 15:
        return int(d.strftime('%Y%m%d'))
    return int(c.date_to_session(d, direction='previous').strftime('%Y%m%d')) if not c.is_session(d) \
        else int(c.previous_session(d).strftime('%Y%m%d'))


def tulis_status(nama, **kv):
    p = os.path.join(HARGA, 'status.json')
    st = json.load(open(p)) if os.path.exists(p) else {}
    st[nama] = dict(dijana=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'), **kv)
    json.dump(st, open(p, 'w'), ensure_ascii=False, indent=1)


def cmd_terkini(a):
    os.makedirs(HARGA, exist_ok=True)
    saham, idx = universe()
    sesi = sesi_terakhir()
    d, gagal = muat_turun(saham + idx, period='1mo')
    d = d[d.date <= sesi].groupby('ticker', group_keys=False).tail(a.hari)
    akhir = d.groupby('ticker').date.max()
    lewat = sorted(akhir[akhir < sesi].index)
    if d.ticker.nunique() < 0.5 * (len(saham) + len(idx)):
        print(f'GAGAL: hanya {d.ticker.nunique()} ticker; fail lama dikekalkan', file=sys.stderr); sys.exit(1)
    d.to_csv(os.path.join(HARGA, 'terkini.csv'), index=False, float_format='%.6g')
    tulis_status('terkini', sesi=sesi, bil_ticker=int(d.ticker.nunique()), bil_universe=len(saham) + len(idx),
                 tiada_data=gagal, tiada_bar_sesi=lewat[:200], bil_tiada_bar_sesi=len(lewat))
    print(json.dumps(dict(sesi=sesi, ticker=int(d.ticker.nunique()), gagal=len(gagal), lewat=len(lewat))))


def cmd_sejarah(a):
    p = os.path.join(HARGA, 'perlu_sejarah.txt')
    t = sorted({x.strip().replace('US.', '') for x in open(p) if x.strip()})[:a.maks] if os.path.exists(p) else []
    if not t:
        print('tiada ticker dalam perlu_sejarah.txt'); return
    d, gagal = muat_turun(t, period='3y')
    d = d.groupby('ticker', group_keys=False).tail(SIMPAN_BAR)
    d.to_csv(os.path.join(HARGA, 'sejarah.csv'), index=False, float_format='%.6g')
    tulis_status('sejarah', bil_ticker=int(d.ticker.nunique()), diminta=t, tiada_data=gagal)
    os.remove(p)  # permintaan selesai; sejarah.csv kekal sehingga permintaan seterusnya
    print(json.dumps(dict(ticker=int(d.ticker.nunique()), gagal=gagal)))


def gabung_satu(lama, kl):
    """Logik sama dengan kod/stor.py gabung_kline (laras nisbah jika harga lama berbeza > 0.3%)."""
    if len(lama):
        sama = lama.merge(kl, on='date', suffixes=('_l', '_k'))
        if len(sama):
            r = (sama.close_k / sama.close_l).median()
            if abs(r - 1) > 0.003:
                lama = lama.copy()
                for c in ['open', 'high', 'low', 'close']:
                    lama[c] = lama[c] * r
                lama['volume'] = (lama['volume'] / r).round()
        lama = lama[~lama.date.isin(kl.date)]
    return pd.concat([lama, kl[LAJ]], ignore_index=True)


def gabung(stor, baru):
    """stor: dict nama->DataFrame (harga_A/B/idx). baru: DataFrame LAJ. Pulang (stor, nota)."""
    A = set(stor.get('harga_A.csv', pd.DataFrame(columns=LAJ)).ticker)
    nota = {}
    for nm in ['harga_A.csv', 'harga_B.csv', 'harga_idx.csv']:
        d = stor.get(nm, pd.DataFrame(columns=LAJ))
        if nm == 'harga_idx.csv':
            pilih = baru[baru.ticker.isin(IDX)]
        elif nm == 'harga_A.csv':
            pilih = baru[baru.ticker.isin(A)]
        else:
            pilih = baru[~baru.ticker.isin(A | set(IDX))]
        if pilih.empty:
            stor[nm] = d; continue
        kump = dict(tuple(d.groupby('ticker'))) if len(d) else {}
        hasil = [g for t, g in kump.items() if t not in set(pilih.ticker)]
        for t, kl in pilih.groupby('ticker'):
            hasil.append(gabung_satu(kump.get(t, pd.DataFrame(columns=LAJ)), kl))
        x = pd.concat(hasil, ignore_index=True).sort_values(['ticker', 'date'])
        stor[nm] = x.drop_duplicates(['ticker', 'date'], keep='last').groupby('ticker', group_keys=False).tail(SIMPAN_BAR)
        nota[nm] = dict(ticker_dikemaskini=int(pilih.ticker.nunique()), bar_terakhir=int(stor[nm].date.max()))
    return stor, nota


def cmd_gabung(a):
    fail = a.fail or [os.path.join(HARGA, 'terkini.csv')]
    baru = pd.concat([pd.read_csv(f) for f in fail if os.path.exists(f)], ignore_index=True)
    stor = {nm: pd.read_csv(os.path.join(a.stor, nm)) for nm in ['harga_A.csv', 'harga_B.csv', 'harga_idx.csv']
            if os.path.exists(os.path.join(a.stor, nm))}
    stor, nota = gabung(stor, baru)
    for nm, d in stor.items():
        d[LAJ].to_csv(os.path.join(a.stor, nm), index=False, float_format='%.6g')
    print(json.dumps(nota, indent=1))


def banding(yf_d, mm_d):
    """Pulang DataFrame beza relatif (open/high/low/close) bagi tarikh yang sama."""
    m = yf_d.merge(mm_d, on='date', suffixes=('_yf', '_mm'))
    for c in ['open', 'high', 'low', 'close']:
        m[c] = (m[c + '_yf'] / m[c + '_mm'] - 1).abs()
    return m[['date', 'open', 'high', 'low', 'close']]


def cmd_semak(a):
    d = pd.concat([pd.read_csv(os.path.join(HARGA, f)) for f in ('terkini.csv',) if os.path.exists(os.path.join(HARGA, f))])
    buruk = []
    for spec in a.kline:
        t, path = spec.split('=', 1)
        mm = baca_kline(path); mm['date'] = pd.to_datetime(mm['date']).dt.strftime('%Y%m%d').astype(int)
        b = banding(d[d.ticker == t], mm)
        mx = float(b[['open', 'high', 'low', 'close']].max().max()) if len(b) else None
        print(f'{t}: {len(b)} tarikh sama, beza maks {mx:.4%}' if mx is not None else f'{t}: tiada tarikh sama')
        if mx is None or mx > TOLERANSI:
            buruk.append(t)
    if buruk:
        print('BERBEZA (guna Moomoo):', ' '.join(buruk)); sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('terkini'); x.add_argument('--hari', type=int, default=10); x.set_defaults(f=cmd_terkini)
    x = s.add_parser('sejarah'); x.add_argument('--maks', type=int, default=300); x.set_defaults(f=cmd_sejarah)
    x = s.add_parser('gabung'); x.add_argument('--stor', required=True); x.add_argument('--fail', nargs='*'); x.set_defaults(f=cmd_gabung)
    x = s.add_parser('semak'); x.add_argument('--kline', nargs='+', required=True); x.set_defaults(f=cmd_semak)
    a = p.parse_args(); a.f(a)


if __name__ == '__main__':
    main()

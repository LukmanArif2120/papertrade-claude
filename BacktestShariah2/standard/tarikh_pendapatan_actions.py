# Bina BacktestShariah2/data/pemangkin/tarikh_pendapatan.csv (M164) — dijalankan dalam GitHub Actions
# (sesi Claude tidak boleh capai Nasdaq/Yahoo). Sumber 1: kalendar earnings Nasdaq ikut tarikh (setiap hari bekerja
# dari --dari hingga --hingga). Sumber 2: yfinance get_earnings_dates (limit 40) setiap saham. Hanya 431 saham
# data_mentah. Lajur: ticker, d0, masa, sumber (nasdaq | yahoo | kedua), beza_hari (yahoo - nasdaq, jika kedua-duanya).
# Guna: python3 tarikh_pendapatan_actions.py --dari 2018-10-01 --hingga 2026-10-16 --keluar <csv>
import argparse, csv, glob, os, sys, time
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pemangkin_actions import UA, NASDAQ

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def saham431():
    s = set()
    for f in sorted(glob.glob(os.path.join(AKAR, 'data_mentah', 'dataset_S*.csv'))):
        with open(f) as h:
            for r in csv.DictReader(h): s.add(r['ticker'])
    return s


def nasdaq(dari, hingga, simpan, rehat=0.4):
    import requests
    h = {'user-agent': UA, 'accept': 'application/json, text/plain, */*', 'origin': 'https://www.nasdaq.com',
         'referer': 'https://www.nasdaq.com/'}
    sesi, out, ralat, d = requests.Session(), {}, [], dari
    while d <= hingga:
        if d.weekday() < 5:
            for cuba in range(3):
                try:
                    r = sesi.get(NASDAQ, params={'date': d.isoformat()}, headers=h, timeout=20); r.raise_for_status()
                    for x in ((r.json().get('data') or {}).get('rows') or []):
                        t = str(x.get('symbol') or '').strip().upper()
                        if t in simpan: out[(t, d.isoformat())] = x.get('time') or ''
                    break
                except Exception as x:
                    if cuba == 2: ralat.append(f'{d}: {type(x).__name__}')
                    else: time.sleep(5)
            time.sleep(rehat)
        d += timedelta(days=1)
    return out, ralat


def yahoo(tickers, rehat=0.3):
    import yfinance as yf
    out, ralat = {}, []
    for t in sorted(tickers):
        try:
            e = yf.Ticker(t).get_earnings_dates(limit=40)
            if e is not None:
                for ts in e.index:
                    out[(t, ts.tz_convert('America/New_York').date().isoformat())] = ts.tz_convert('America/New_York').strftime('%H:%M')
        except Exception as x:
            ralat.append(f'{t}: {type(x).__name__}')
        time.sleep(rehat)
    return out, ralat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dari', default='2018-10-01'); ap.add_argument('--hingga', default=date.today().isoformat())
    ap.add_argument('--keluar', required=True); ap.add_argument('--tanpa_yahoo', action='store_true')
    a = ap.parse_args()
    S = saham431(); print('saham', len(S))
    N, rn = nasdaq(date.fromisoformat(a.dari), date.fromisoformat(a.hingga), S); print('nasdaq', len(N), 'hari ralat', len(rn))
    Y, ry = ({}, []) if a.tanpa_yahoo else yahoo(S); print('yahoo', len(Y), 'saham ralat', len(ry))
    Y = {k: v for k, v in Y.items() if a.dari <= k[1] <= a.hingga}
    # padankan Yahoo ke Nasdaq dalam +-3 hari kalendar
    nk = {}
    for (t, d) in N: nk.setdefault(t, []).append(d)
    baris, guna_y = [], set()
    for (t, d), m in sorted(N.items()):
        cocok = [(abs((date.fromisoformat(y) - date.fromisoformat(d)).days), y) for (tt, y) in Y if tt == t
                 and abs((date.fromisoformat(y) - date.fromisoformat(d)).days) <= 3] if Y else []
        if cocok:
            _, y = min(cocok); guna_y.add((t, y))
            baris.append([t, d, m, 'kedua', (date.fromisoformat(y) - date.fromisoformat(d)).days])
        else:
            baris.append([t, d, m, 'nasdaq', ''])
    for (t, y), m in sorted(Y.items()):
        if (t, y) not in guna_y: baris.append([t, y, m, 'yahoo', ''])
    baris.sort()
    os.makedirs(os.path.dirname(a.keluar), exist_ok=True)
    with open(a.keluar, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['ticker', 'd0', 'masa', 'sumber', 'beza_hari']); w.writerows(baris)
    with open(a.keluar.replace('.csv', '_status.txt'), 'w') as f:
        f.write(f'dari {a.dari} hingga {a.hingga}; saham {len(S)}; nasdaq {len(N)} (hari ralat {len(rn)}); yahoo {len(Y)} '
                f'(saham ralat {len(ry)}); baris {len(baris)}\n' + '\n'.join(rn[:50] + ry[:50]) + '\n')
    print('baris', len(baris))


if __name__ == '__main__':
    main()

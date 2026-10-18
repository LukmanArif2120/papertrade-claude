# Bina data sejarah untuk kajian gred pemangkin — dijalankan dalam GitHub Actions (sesi Claude tidak boleh capai
# Yahoo/SEC). Sekali jalan, manual (.github/workflows/kajian_pemangkin.yml). Tiada kesan pada rutin harian.
# Alam saham: data_mentah/dataset_S1–S4 (431) + stor harga dashboard (data/harga/stor/harga_A/B.csv).
# Output dalam BacktestShariah2/data/pemangkin/sejarah/:
#   analisis.csv.gz    : ticker, tarikh (New York), firma, dari, ke, tindakan, tindakan_sasaran, sasaran, sasaran_lalu
#                        (yfinance upgrades_downgrades, semua sejarah)
#   eps.csv            : ticker, tarikh (New York), masa, eps_anggaran, eps_sebenar, kejutan_pct (yfinance, 40 suku)
#   harga.csv.gz       : ticker, date, open, close, volume (yfinance, dilaras pecahan/dividen, sejak --dari; + SPY, QQQ)
#   orang_dalam.csv.gz : ticker, tarikh_fail, tarikh_dagang, pemilik_cik, pemilik, hubungan, jawatan, kod (P/S),
#                        saham, harga, rancangan_10b5 (set data pukal SEC Form 3/4/5, sejak --dari)
#   status_<bahagian>.txt : liputan dan ralat setiap larian
# Guna: python3 sejarah_pemangkin_actions.py --bahagian analisis,eps,harga,sec --dari 2012-01-01
import argparse, csv, glob, io, os, sys, time, zipfile
from datetime import date

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
KELUAR = os.path.join(BS2, 'data', 'pemangkin', 'sejarah')
INDEKS = ['SPY', 'QQQ']  # penanda aras (harga sahaja)
SEC_URL = 'https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{t}q{q}_form345.zip'
SEC_UA = 'papertrade-claude kajian-pemangkin 41898282+github-actions[bot]@users.noreply.github.com'


def alam_saham():
    s = set()
    for f in sorted(glob.glob(os.path.join(AKAR, 'data_mentah', 'dataset_S*.csv'))) + \
            sorted(glob.glob(os.path.join(BS2, 'data', 'harga', 'stor', 'harga_[AB].csv'))):
        with open(f, newline='') as h:
            for r in csv.DictReader(h):
                if r.get('ticker'):
                    s.add(r['ticker'].strip().upper())
    return sorted(s)


def yf_simbol(t):
    return t.replace('.', '-')


def _num(x, dp=4):
    try:
        v = float(x)
        return '' if v != v else round(v, dp)
    except (TypeError, ValueError):
        return ''


def tarikh_ny(idx):
    import pandas as pd
    ts = pd.Timestamp(idx)
    return (ts.tz_localize('UTC') if ts.tzinfo is None else ts).tz_convert('America/New_York')


def baris_analisis(t, df):
    """yfinance upgrades_downgrades -> baris CSV (semua sejarah)."""
    out = []
    if df is None or getattr(df, 'empty', True):
        return out
    for idx, r in df.iterrows():
        try:
            d = tarikh_ny(idx).date().isoformat()
        except (ValueError, TypeError):
            continue
        out.append([t, d, str(r.get('Firm') or ''), str(r.get('FromGrade') or ''), str(r.get('ToGrade') or ''),
                    str(r.get('Action') or '').lower(), str(r.get('priceTargetAction') or ''),
                    _num(r.get('currentPriceTarget'), 2), _num(r.get('priorPriceTarget'), 2)])
    return out


def baris_eps(t, df):
    """yfinance get_earnings_dates -> baris CSV (tarikh New York, masa HH:MM)."""
    out = []
    if df is None or getattr(df, 'empty', True):
        return out
    for idx, r in df.iterrows():
        try:
            ts = tarikh_ny(idx)
        except (ValueError, TypeError):
            continue
        out.append([t, ts.date().isoformat(), ts.strftime('%H:%M'), _num(r.get('EPS Estimate')),
                    _num(r.get('Reported EPS')), _num(r.get('Surprise(%)'), 2)])
    return out


def tarik_yahoo(S, bahagian, rehat=0.3):
    import yfinance as yf
    A, E, ralat = [], [], []
    for n, t in enumerate(S):
        tk = yf.Ticker(yf_simbol(t))
        for nama, fn in [('analisis', lambda: A.extend(baris_analisis(t, tk.upgrades_downgrades))),
                         ('eps', lambda: E.extend(baris_eps(t, tk.get_earnings_dates(limit=40))))]:
            if nama not in bahagian:
                continue
            for cuba in range(3):
                try:
                    fn(); break
                except Exception as x:
                    if cuba == 2:
                        ralat.append(f'{t} {nama}: {type(x).__name__}')
                    time.sleep(2 * (cuba + 1))
            time.sleep(rehat)
        if n % 100 == 0:
            print(n, t, 'analisis', len(A), 'eps', len(E), 'ralat', len(ralat), flush=True)
    return A, E, ralat


def tarik_harga(S, dari, kumpulan=50):
    import pandas as pd, yfinance as yf
    fr, ralat = [], []
    for i in range(0, len(S), kumpulan):
        sub = S[i:i + kumpulan]
        peta = {yf_simbol(t): t for t in sub}
        try:
            d = yf.download(list(peta), start=dari, auto_adjust=True, group_by='ticker', threads=True, progress=False)
        except Exception as x:
            ralat.append(f'harga {sub[0]}..: {type(x).__name__}'); continue
        for s, t in peta.items():
            try:
                x = d[s][['Open', 'Close', 'Volume']].dropna(subset=['Close'])
            except KeyError:
                ralat.append(f'harga {t}: tiada'); continue
            if x.empty:
                ralat.append(f'harga {t}: kosong'); continue
            x = x.reset_index().rename(columns={'Date': 'date', 'Open': 'open', 'Close': 'close', 'Volume': 'volume'})
            x['date'] = pd.to_datetime(x['date']).dt.strftime('%Y%m%d')
            x.insert(0, 'ticker', t)
            fr.append(x.round({'open': 4, 'close': 4}))
        print('harga', i + len(sub), flush=True)
        time.sleep(1)
    return (pd.concat(fr) if fr else pd.DataFrame(columns=['ticker', 'date', 'open', 'close', 'volume'])), ralat


def _tsv(z, nama, lajur):
    import pandas as pd
    f = next((n for n in z.namelist() if n.upper().endswith(nama)), None)
    if f is None:
        return pd.DataFrame(columns=lajur)
    d = pd.read_csv(io.BytesIO(z.read(f)), sep='\t', dtype=str, quoting=3, on_bad_lines='skip', encoding_errors='replace')
    for c in lajur:
        if c not in d.columns:
            d[c] = ''
    return d[lajur]


def _tarikh_sec(s):
    import pandas as pd
    d = pd.to_datetime(s, format='%d-%b-%Y', errors='coerce')
    d = d.fillna(pd.to_datetime(s, format='mixed', errors='coerce'))
    return d.dt.strftime('%Y-%m-%d')


def baca_sec(data, S):
    """Satu zip set data SEC Form 3/4/5 (bytes) -> DataFrame dagangan pasaran terbuka (kod P/S) bagi ticker S."""
    import pandas as pd
    z = zipfile.ZipFile(io.BytesIO(data))
    sub = _tsv(z, 'SUBMISSION.TSV', ['ACCESSION_NUMBER', 'FILING_DATE', 'DOCUMENT_TYPE', 'ISSUERTRADINGSYMBOL', 'AFF10B5ONE'])
    sub['ticker'] = sub['ISSUERTRADINGSYMBOL'].fillna('').str.strip().str.upper()
    sub = sub[sub['ticker'].isin(set(S)) & sub['DOCUMENT_TYPE'].fillna('').str.startswith('4')]
    tr = _tsv(z, 'NONDERIV_TRANS.TSV', ['ACCESSION_NUMBER', 'TRANS_DATE', 'TRANS_CODE', 'TRANS_SHARES',
                                         'TRANS_PRICEPERSHARE', 'TRANS_ACQUIRED_DISP_CD'])
    tr = tr[tr['TRANS_CODE'].isin(['P', 'S']) & tr['ACCESSION_NUMBER'].isin(set(sub['ACCESSION_NUMBER']))]
    ow = _tsv(z, 'REPORTINGOWNER.TSV', ['ACCESSION_NUMBER', 'RPTOWNERCIK', 'RPTOWNERNAME', 'RPTOWNER_RELATIONSHIP',
                                        'RPTOWNER_TITLE'])
    ow = ow[ow['ACCESSION_NUMBER'].isin(set(tr['ACCESSION_NUMBER']))].drop_duplicates('ACCESSION_NUMBER')
    d = tr.merge(sub, on='ACCESSION_NUMBER').merge(ow, on='ACCESSION_NUMBER', how='left')
    if d.empty:
        return pd.DataFrame()
    d['saham'] = pd.to_numeric(d['TRANS_SHARES'], errors='coerce')
    d['harga'] = pd.to_numeric(d['TRANS_PRICEPERSHARE'], errors='coerce')
    d['nilai'] = d['saham'] * d['harga']
    # satu baris setiap (pengisytiharan, kod, tarikh dagang): jumlah saham, harga purata berwajaran
    g = d.groupby(['ACCESSION_NUMBER', 'TRANS_CODE', 'TRANS_DATE'], as_index=False).agg(
        ticker=('ticker', 'first'), tarikh_fail=('FILING_DATE', 'first'), pemilik_cik=('RPTOWNERCIK', 'first'),
        pemilik=('RPTOWNERNAME', 'first'), hubungan=('RPTOWNER_RELATIONSHIP', 'first'), jawatan=('RPTOWNER_TITLE', 'first'),
        rancangan_10b5=('AFF10B5ONE', 'first'), saham=('saham', 'sum'), nilai=('nilai', 'sum'))
    g['harga'] = (g['nilai'] / g['saham']).round(4)
    g['tarikh_fail'] = _tarikh_sec(g['tarikh_fail']); g['tarikh_dagang'] = _tarikh_sec(g['TRANS_DATE'])
    g = g.rename(columns={'TRANS_CODE': 'kod'})
    return g[['ticker', 'tarikh_fail', 'tarikh_dagang', 'pemilik_cik', 'pemilik', 'hubungan', 'jawatan', 'kod',
              'saham', 'harga', 'rancangan_10b5']]


def tarik_sec(S, dari):
    import pandas as pd, requests
    fr, ralat, kini = [], [], date.today()
    for t in range(dari.year, kini.year + 1):
        for q in range(1, 5):
            if (t, q) < (dari.year, (dari.month - 1) // 3 + 1) or (t, q) > (kini.year, (kini.month - 1) // 3 + 1):
                continue
            url = SEC_URL.format(t=t, q=q)
            for cuba in range(3):
                try:
                    r = requests.get(url, headers={'User-Agent': SEC_UA, 'Accept-Encoding': 'gzip, deflate'}, timeout=180)
                    if r.status_code == 404:
                        ralat.append(f'sec {t}q{q}: 404'); break
                    r.raise_for_status()
                    x = baca_sec(r.content, S)
                    fr.append(x); print('sec', t, q, len(x), flush=True); break
                except Exception as e:
                    if cuba == 2:
                        ralat.append(f'sec {t}q{q}: {type(e).__name__}')
                    time.sleep(5 * (cuba + 1))
            time.sleep(1)
    fr = [x for x in fr if not x.empty]
    d = pd.concat(fr).drop_duplicates() if fr else pd.DataFrame()
    return d, ralat


def tulis_csv(nama, kepala, baris):
    with open(os.path.join(KELUAR, nama), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(kepala); w.writerows(sorted(baris, key=lambda r: (r[0], r[1])))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--bahagian', default='analisis,eps,harga,sec')
    ap.add_argument('--dari', default='2012-01-01')
    ap.add_argument('--had', type=int, default=0, help='hadkan bilangan saham (ujian)')
    a = ap.parse_args(argv)
    bahagian = set(a.bahagian.split(','))
    S = alam_saham()
    if a.had:
        S = S[:a.had]
    os.makedirs(KELUAR, exist_ok=True)
    status = [f'dijana {date.today().isoformat()}; dari {a.dari}; saham {len(S)}; bahagian {",".join(sorted(bahagian))}']
    if bahagian & {'analisis', 'eps'}:
        A, E, r = tarik_yahoo(S, bahagian)
        import pandas as pd
        if 'analisis' in bahagian:
            pd.DataFrame(sorted(A, key=lambda x: (x[0], x[1])), columns=['ticker', 'tarikh', 'firma', 'dari', 'ke', 'tindakan',
                         'tindakan_sasaran', 'sasaran', 'sasaran_lalu']).to_csv(os.path.join(KELUAR, 'analisis.csv.gz'), index=False)
            status.append(f'analisis {len(A)} baris; {len({x[0] for x in A})} saham')
        if 'eps' in bahagian:
            tulis_csv('eps.csv', ['ticker', 'tarikh', 'masa', 'eps_anggaran', 'eps_sebenar', 'kejutan_pct'], E)
            status.append(f'eps {len(E)} baris; {len({x[0] for x in E})} saham')
        status.append(f'ralat yahoo {len(r)}'); status += r[:100]
    if 'harga' in bahagian:
        H, r = tarik_harga(S + [t for t in INDEKS if t not in S], a.dari)
        H.to_csv(os.path.join(KELUAR, 'harga.csv.gz'), index=False)
        status.append(f'harga {len(H)} baris; {H["ticker"].nunique() if len(H) else 0} saham; ralat {len(r)}'); status += r[:100]
    if 'sec' in bahagian:
        D, r = tarik_sec(S, date.fromisoformat(a.dari))
        if len(D):
            D.sort_values(['ticker', 'tarikh_dagang']).to_csv(os.path.join(KELUAR, 'orang_dalam.csv.gz'), index=False)
        status.append(f'orang_dalam {len(D)} baris; {D["ticker"].nunique() if len(D) else 0} saham; ralat {len(r)}'); status += r[:100]
    with open(os.path.join(KELUAR, f'status_{"_".join(sorted(bahagian))}.txt'), 'w') as f:
        f.write('\n'.join(status) + '\n')
    print('\n'.join(status[:12]))


if __name__ == '__main__':
    sys.exit(main())

# pemangkin_actions.py — kumpul data pemangkin percuma di GitHub Actions (.github/workflows/pemangkin.yml),
# supaya imbasan malam tidak perlu ~3 panggilan Moomoo bagi setiap saham watchlist (gred P Peringkat 3).
# Sesi Claude tidak boleh capai Yahoo/Nasdaq; runner GitHub boleh. Hasil (folder --keluar):
#   yahoo.json           : {dijana, tarikh (MYT), liputan, saham: {T: {diambil (saat UTC), berita, analisis, orang_dalam, ralat?}}}
#                          berita [{tajuk, masa (saat UTC), url}] (RSS Yahoo, ≤ 11 hari, ditapis gred.relevan), analisis [{tarikh,
#                          firma, dari, ke, tindakan, sasaran, sasaran_lalu}] (≤ 11 hari), orang_dalam [{tarikh, nama,
#                          teks, saham}] (belian, ≤ 31 hari)
#   earnings_nasdaq.json : {dijana, tarikh, dari, hingga, hari_ralat, saham: {T: {lalu, lalu_masa, seterusnya, seterusnya_masa}}}
#   status.json          : ringkasan dan ralat
# Cache: ticker yang sudah dikumpul tanpa ralat pada tarikh MYT sama dan <= 2 jam lalu tidak dikumpul semula (setiap
# push watchlist / senarai_beli mencetus workflow; hanya ticker baharu, gagal atau lama). Kalendar Nasdaq sekali sehari.
# gred.py hanya memakai entri yang diambil selepas 6:00 petang MYT pada tarikh imbasan.
# Format ini dibaca oleh `gred.py kumpul --yahoo … --nasdaq …` dan `gred.py tambah --nasdaq …`.
# Sumber tidak rasmi (Yahoo melalui yfinance, API kalendar Nasdaq): maklumat gred sahaja, bukan isyarat beli.
import argparse, csv, json, os, re, sys, time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/126.0.0.0 Safari/537.36')
NASDAQ = 'https://api.nasdaq.com/api/calendar/earnings'


def hari_ini_myt():
    return (datetime.now(timezone.utc) + timedelta(hours=8)).date()


def baca_ticker(csvs):
    """Ticker unik dan nama syarikat mengikut susunan fail (fail pertama = keutamaan masa)."""
    out = {}
    for f in csvs:
        if not os.path.exists(f):
            continue
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            t = (r.get('saham') or r.get('Saham') or '').strip().upper()
            if t and t not in out:
                out[t] = (r.get('nama') or r.get('Nama') or '').strip()
    return out


def baca_json(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _masa(x):
    """pubDate ISO / epoch -> saat UTC (int) atau None."""
    if x in (None, ''):
        return None
    if isinstance(x, (int, float)):
        return int(x / 1000 if x > 1e11 else x)
    try:
        return int(datetime.fromisoformat(str(x).replace('Z', '+00:00')).timestamp())
    except ValueError:
        return None


def berita_yf(items, sejak, ticker='', nama=''):
    """yfinance Ticker.news (format baharu {'content': {...}} atau lama) -> berita relevan (gred.relevan) <= 10."""
    from gred import relevan
    out = []
    for it in items or []:
        c = it.get('content') if isinstance(it.get('content'), dict) else it
        tajuk = c.get('title')
        masa = _masa(c.get('pubDate') or c.get('displayTime') or c.get('providerPublishTime'))
        url = ((c.get('canonicalUrl') or {}).get('url') or (c.get('clickThroughUrl') or {}).get('url')
               or c.get('link') or '')
        if tajuk and masa and masa >= sejak and relevan(tajuk, ticker, nama):
            out.append({'tajuk': str(tajuk)[:200], 'masa': masa, 'url': url})
    return out[:10]


def _num(x):
    try:
        v = float(x)
        return None if v != v or v <= 0 else round(v, 2)
    except (TypeError, ValueError):
        return None


def analisis_yf(df, sejak_tarikh):
    """yfinance upgrades_downgrades (indeks GradeDate = cap masa UTC) -> tindakan dengan tarikh New York."""
    import pandas as pd
    out = []
    if df is None or getattr(df, 'empty', True):
        return out
    for idx, r in df.iterrows():
        try:
            ts = pd.Timestamp(idx)
            t = (ts.tz_localize('UTC') if ts.tzinfo is None else ts).tz_convert('America/New_York').date()
        except (ValueError, TypeError):
            continue
        if t < sejak_tarikh:
            continue
        out.append({'tarikh': t.isoformat(), 'firma': str(r.get('Firm') or ''), 'dari': str(r.get('FromGrade') or ''),
                    'ke': str(r.get('ToGrade') or ''), 'tindakan': str(r.get('Action') or '').lower(),
                    'sasaran': _num(r.get('currentPriceTarget')), 'sasaran_lalu': _num(r.get('priorPriceTarget'))})
    return out[:20]


def orang_dalam_yf(df, sejak_tarikh):
    out = []
    if df is None or getattr(df, 'empty', True):
        return out
    for _, r in df.iterrows():
        teks = str(r.get('Text') or '')
        if not re.match(r'\s*purchase', teks, re.I):
            continue
        try:
            t = datetime.fromisoformat(str(r.get('Start Date'))[:10]).date()
        except ValueError:
            continue
        if t < sejak_tarikh:
            continue
        try:
            saham = int(float(r.get('Shares') or 0))
        except (TypeError, ValueError):
            saham = 0
        out.append({'tarikh': t.isoformat(), 'nama': str(r.get('Insider') or ''), 'teks': teks[:120], 'saham': saham})
    return out[:20]


def tiada_data(x):
    """Ralat yfinance yang bermaksud 'tiada data' (saham tanpa liputan analisis / modul tiada / 404 Yahoo bagi
    saham kelas atau senaraian baharu), bukan kegagalan."""
    return isinstance(x, (KeyError, IndexError)) or (
        type(x).__name__ == 'YFDataException' and 'history found' in str(x)) or 'HTTP Error 404' in str(x)


RSS_YAHOO = 'https://feeds.finance.yahoo.com/rss/2.0/headline'
BERITA_NASDAQ = 'https://api.nasdaq.com/api/news/topic/articlebysymbol'
RSS_GOOGLE = 'https://news.google.com/rss/search'


def _rss(url, params):
    """RSS -> [{title, pubDate (saat UTC), link}] (format lama yfinance; dibaca terus oleh berita_yf)."""
    import requests, xml.etree.ElementTree as ET
    from email.utils import parsedate_to_datetime
    r = requests.get(url, params=params, headers={'user-agent': UA}, timeout=20)
    r.raise_for_status()
    out = []
    for it in ET.fromstring(r.content).iter('item'):
        try:
            masa = int(parsedate_to_datetime(it.findtext('pubDate')).timestamp())
        except (TypeError, ValueError):
            continue
        out.append({'title': (it.findtext('title') or '').strip(), 'pubDate': masa, 'link': (it.findtext('link') or '').strip()})
    return out


def rss_yahoo(ticker):
    return _rss(RSS_YAHOO, {'s': ticker, 'region': 'US', 'lang': 'en-US'})


def rss_google(ticker, nama=''):
    q = (f'"{nama}" OR ' if nama else '') + f'{ticker} stock when:11d'
    return _rss(RSS_GOOGLE, {'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})


def berita_nasdaq(ticker):
    import requests
    h = {'user-agent': UA, 'accept': 'application/json, text/plain, */*', 'origin': 'https://www.nasdaq.com',
         'referer': 'https://www.nasdaq.com/'}
    r = requests.get(BERITA_NASDAQ, params={'q': f'{ticker}|stocks', 'offset': 0, 'limit': 10, 'fallback': 'false'},
                     headers=h, timeout=20)
    r.raise_for_status()
    out = []
    for x in ((r.json().get('data') or {}).get('rows') or []):
        try:
            masa = int(datetime.strptime(str(x.get('created')), '%b %d, %Y').replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            continue
        u = str(x.get('url') or '')
        out.append({'title': x.get('title') or '', 'pubDate': masa, 'link': u if u.startswith('http') else 'https://www.nasdaq.com' + u})
    return out


def diagnostik(pasangan):
    """Bandingkan sumber berita percuma bagi 'TICKER:Nama_Syarikat' (_ = ruang); cetak ke log Actions sahaja."""
    import yfinance as yf
    try:
        yf.config.debug.hide_exceptions = False
    except AttributeError:
        pass
    print('yfinance', getattr(yf, '__version__', '?'))
    sejak = int((datetime.now(timezone.utc) - timedelta(days=11)).timestamp())
    for p in pasangan:
        t, _, nm = p.partition(':')
        nm = nm.replace('_', ' ')
        for sumber, fn in (('yfinance', lambda: yf.Ticker(t).get_news(count=10)), ('rss_yahoo', lambda: rss_yahoo(t)),
                           ('nasdaq', lambda: berita_nasdaq(t)), ('rss_google', lambda: rss_google(t, nm))):
            try:
                n = fn()
                rel = berita_yf(n, sejak, t, nm)
                print(f'{t} {sumber}: {len(n)} item; relevan <= 11 hari: {len(rel)}')
                for x in rel[:2]:
                    print('    ', datetime.fromtimestamp(x['masa'], timezone.utc).strftime('%Y-%m-%d %H:%M'), '|', x['tajuk'][:90], '|', x['url'][:80])
            except Exception as x:
                print(f'{t} {sumber}: RALAT {type(x).__name__}: {str(x)[:200]}')


def tarik_yahoo(nama, hari_ini, had_saat=1500, rehat=0.35):
    """nama: {ticker: nama syarikat} mengikut keutamaan. Berhenti selepas had_saat (baki dikumpul larian berikutnya)."""
    import yfinance as yf
    try:
        yf.config.debug.hide_exceptions = False   # ralat HTTP/429 mesti kelihatan, bukan DataFrame kosong senyap
    except AttributeError:
        pass
    sejak_berita = int((datetime.now(timezone.utc) - timedelta(days=11)).timestamp())
    s10, s30 = hari_ini - timedelta(days=11), hari_ini - timedelta(days=31)
    mula, out = time.time(), {}
    for t, nm in nama.items():
        if time.time() - mula > had_saat:
            break
        e, ralat, tk = {}, [], yf.Ticker(t.replace('.', '-'))
        # berita: RSS Yahoo (yfinance get_news memulangkan 0 item dari runner GitHub, diagnostik 16 Okt 2026)
        for medan, fn in (('berita', lambda: berita_yf(rss_yahoo(t.replace('.', '-')), sejak_berita, t, nm)),
                          ('analisis', lambda: analisis_yf(tk.upgrades_downgrades, s10)),
                          ('orang_dalam', lambda: orang_dalam_yf(tk.insider_transactions, s30))):
            for cuba in range(2):
                try:
                    e[medan] = fn()
                    break
                except Exception as x:
                    if tiada_data(x):
                        e[medan] = []
                        break
                    if cuba:   # 429 / rangkaian / format berubah: cuba sekali lagi, kemudian rekod ralat
                        ralat.append(f'{medan}: {type(x).__name__}: {str(x)[:80]}')
                        e[medan] = []
                    else:
                        time.sleep(20 if 'Rate' in type(x).__name__ else 5)
            time.sleep(rehat)
        e['diambil'] = int(time.time())
        if ralat:
            e['ralat'] = ralat
        out[t] = e
    return out


def tarik_nasdaq(hari_ini, simpan=None, ke_belakang=95, ke_hadapan=35, rehat=0.5):
    """Kalendar earnings Nasdaq setiap hari bekerja dalam tetingkap -> {T: {lalu, lalu_masa, seterusnya,
    seterusnya_masa}}; lalu = tarikh terkini <= hari_ini, seterusnya = terawal > hari_ini. simpan: set ticker
    (universe + calon) untuk mengecilkan fail; None = semua."""
    import requests
    h = {'user-agent': UA, 'accept': 'application/json, text/plain, */*', 'origin': 'https://www.nasdaq.com',
         'referer': 'https://www.nasdaq.com/'}
    sesi, saham, ralat = requests.Session(), {}, []
    d = hari_ini - timedelta(days=ke_belakang)
    while d <= hari_ini + timedelta(days=ke_hadapan):
        if d.weekday() < 5:
            for cuba in range(2):
                try:
                    r = sesi.get(NASDAQ, params={'date': d.isoformat()}, headers=h, timeout=20)
                    r.raise_for_status()
                    for x in ((r.json().get('data') or {}).get('rows') or []):
                        t = str(x.get('symbol') or '').strip().upper()
                        if not t or (simpan is not None and t not in simpan):
                            continue
                        e = saham.setdefault(t, {})
                        if d <= hari_ini:
                            if not e.get('lalu') or d.isoformat() > e['lalu']:
                                e['lalu'], e['lalu_masa'] = d.isoformat(), x.get('time') or ''
                        elif not e.get('seterusnya') or d.isoformat() < e['seterusnya']:
                            e['seterusnya'], e['seterusnya_masa'] = d.isoformat(), x.get('time') or ''
                    break
                except Exception as x:
                    if cuba:
                        ralat.append(f'{d}: {type(x).__name__}: {str(x)[:80]}')
                    else:
                        time.sleep(3)
            time.sleep(rehat)
        d += timedelta(days=1)
    return {'dari': (hari_ini - timedelta(days=ke_belakang)).isoformat(),
            'hingga': (hari_ini + timedelta(days=ke_hadapan)).isoformat(), 'hari_ralat': len(ralat),
            'ralat': ralat[:20], 'saham': dict(sorted(saham.items()))}


def tulis(p, d, **kw):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, **(kw or {'separators': (',', ':')}))


def main(argv=None, tarik_y=None, tarik_n=None, hari_ini=None):
    ap = argparse.ArgumentParser(description='Data pemangkin percuma (Yahoo + Nasdaq) untuk gred P')
    ap.add_argument('--csv', nargs='+', required=True, help='senarai_beli.csv watchlist.csv (susunan = keutamaan)')
    ap.add_argument('--univ', help='data/harga/univ.txt: ticker universe untuk kalendar Nasdaq (selain calon)')
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--paksa', action='store_true', help='kumpul semula semua walaupun sudah dikumpul hari ini')
    ap.add_argument('--had-saat', type=int, default=1500)
    ap.add_argument('--segar-jam', type=float, default=2.0, help='entri hari ini yang lebih muda daripada ini dipakai semula')
    ap.add_argument('--diagnostik', nargs='*', help='TICKER:Nama … : cetak data mentah Yahoo sahaja (tiada fail ditulis)')
    a = ap.parse_args(argv)
    if a.diagnostik:
        diagnostik(a.diagnostik)
        return 0
    tarik_y, tarik_n = tarik_y or tarik_yahoo, tarik_n or tarik_nasdaq
    os.makedirs(a.keluar, exist_ok=True)
    hari_ini = hari_ini or hari_ini_myt()
    hi = hari_ini.isoformat()
    nama = baca_ticker(a.csv)
    p_yh, p_nas, p_st = (os.path.join(a.keluar, f) for f in ('yahoo.json', 'earnings_nasdaq.json', 'status.json'))
    lama_yh, lama_nas = baca_json(p_yh), baca_json(p_nas)
    kini = time.time()
    sedia = {} if a.paksa or lama_yh.get('tarikh') != hi else \
        {t: e for t, e in (lama_yh.get('saham') or {}).items()
         if t in nama and not e.get('ralat') and kini - (e.get('diambil') or 0) <= a.segar_jam * 3600}
    perlu = {t: n for t, n in nama.items() if t not in sedia}
    nas_segar = not a.paksa and lama_nas.get('tarikh') == hi and lama_nas.get('hari_ralat') == 0
    if not perlu and nas_segar:
        print(f'{len(nama)} ticker sudah dikumpul hari ini ({hi}); tiada kerja')
        return 0
    dijana = lambda: datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    if nas_segar:
        nas = lama_nas
    else:
        simpan = set(nama)
        if a.univ and os.path.exists(a.univ):
            simpan |= {x.strip().upper() for x in open(a.univ, encoding='utf-8') if x.strip()}
        nas = dict(dijana=dijana(), tarikh=hi, **tarik_n(hari_ini, simpan))
        tulis(p_nas, nas)
    baru = tarik_y(perlu, hari_ini, had_saat=a.had_saat) if perlu else {}
    saham = {t: sedia.get(t) or baru[t] for t in nama if t in sedia or t in baru}
    ok = sum(1 for e in saham.values() if not e.get('ralat'))
    tulis(p_yh, {'dijana': dijana(), 'tarikh': hi, 'liputan': f'{ok}/{len(nama)}', 'saham': saham})
    status = {'dijana': dijana(), 'tarikh': hi, 'lengkap': ok == len(nama), 'ticker': len(nama),
              'yahoo_dikumpul': ok, 'yahoo_baru': len(baru), 'yahoo_ralat': len(saham) - ok,
              'yahoo_belum': len(nama) - len(saham),
              'yahoo_berita': sum(1 for e in saham.values() if e.get('berita')),
              'yahoo_analisis': sum(1 for e in saham.values() if e.get('analisis')),
              'yahoo_orang_dalam': sum(1 for e in saham.values() if e.get('orang_dalam')),
              'nasdaq_tarikh': nas.get('tarikh'), 'nasdaq_saham': len(nas.get('saham') or {}),
              'nasdaq_hari_ralat': nas.get('hari_ralat'),
              'contoh_ralat': [x for e in saham.values() for x in e.get('ralat', [])][:5] + (nas.get('ralat') or [])[:3]}
    tulis(p_st, status, indent=1)
    print(json.dumps(status, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())

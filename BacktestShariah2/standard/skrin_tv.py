# skrin_tv.py — saringan malam seluruh pasaran saham AS daripada TradingView (percuma, data lewat 15 minit) dan
# pegangan ETF Shariah (SP Funds). Dijalankan oleh GitHub Actions (.github/workflows/skrin_tv.yml) kerana sesi
# Claude tidak boleh capai scanner.tradingview.com. Tugasan Claude hanya membaca fail hasil.
# Hasil (folder --keluar):
#   tv_us.csv        : satu baris setiap saham AS (NASDAQ/NYSE/AMEX, harga >= --harga_min), medan dalam MEDAN
#   etf_shariah.csv  : ticker,etf (pegangan SPUS/SPTE; ada dalam senarai = pengesahan positif sahaja)
#   status.json      : masa jana, bilangan baris, medan yang tiada data, taburan is_shariah_compliant, status ETF
# Sumber tidak rasmi: endpoint scanner TradingView tidak didokumenkan dan kaedah Shariahnya tidak didedahkan.
# Gunakan sebagai semakan silang sahaja; screener Shariah Moomoo kekal sumber utama (tugasan_v3 §3).
import argparse, csv, io, json, os, sys, time
from datetime import datetime, timezone

import requests

URL = 'https://scanner.tradingview.com/america/scan'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/126.0.0.0 Safari/537.36')
HEADERS = {'user-agent': UA, 'origin': 'https://www.tradingview.com', 'referer': 'https://www.tradingview.com/',
           'accept': 'application/json', 'content-type': 'application/json'}
MEDAN = ['name', 'description', 'exchange', 'close', 'volume', 'market_cap_basic', 'sector', 'industry',
         'is_shariah_compliant', 'price_52_week_high', 'price_52_week_low', 'Perf.W', 'Perf.1M', 'Perf.3M',
         'Perf.6M', 'Perf.Y', 'relative_volume_10d_calc', 'average_volume_30d_calc', 'SMA50', 'SMA200', 'RSI',
         'earnings_release_next_date', 'earnings_release_date']
ETF = {'SPUS': 'https://www.sp-funds.com/wp-content/uploads/data/TidalFG_Holdings_SPUS.csv',
       'SPTE': 'https://www.sp-funds.com/wp-content/uploads/data/TidalFG_Holdings_SPTE.csv'}


def pertanyaan(offset, saiz, harga_min):
    return {
        'markets': ['america'], 'symbols': {}, 'options': {'lang': 'en'}, 'columns': MEDAN,
        'filter': [{'left': 'type', 'operation': 'equal', 'right': 'stock'},
                   {'left': 'exchange', 'operation': 'in_range', 'right': ['NASDAQ', 'NYSE', 'AMEX']},
                   {'left': 'close', 'operation': 'egreater', 'right': harga_min}],
        'sort': {'sortBy': 'market_cap_basic', 'sortOrder': 'desc'},
        'range': [offset, offset + saiz], 'ignore_unknown_fields': True,
    }


def tarik_tv(harga_min=5.0, saiz=2000, rehat=2.0, sesi=None):
    sesi = sesi or requests.Session()
    baris, jumlah, offset = [], None, 0
    while jumlah is None or offset < jumlah:
        for cuba in range(3):
            r = sesi.post(URL, json=pertanyaan(offset, saiz, harga_min), headers=HEADERS, timeout=30)
            if r.ok:
                break
            time.sleep(10 * (cuba + 1))
        r.raise_for_status()
        j = r.json()
        jumlah = int(j.get('totalCount') or 0)
        data = j.get('data') or []
        if not data:
            break
        for x in data:
            sym = x.get('s', '')
            d = dict(zip(MEDAN, x.get('d') or []))
            d['ticker'] = sym.split(':', 1)[-1]
            d['tv_simbol'] = sym
            baris.append(d)
        offset += saiz
        time.sleep(rehat)
    return baris, jumlah


def tarik_etf(nama, url, sesi=None):
    sesi = sesi or requests.Session()
    r = sesi.get(url, headers={'user-agent': UA, 'accept': 'text/csv,*/*'}, timeout=30)
    r.raise_for_status()
    teks = r.content.decode('utf-8-sig', errors='replace')
    if teks.lstrip().startswith('<'):
        raise ValueError('bukan CSV (halaman HTML/sekatan)')
    rows = list(csv.DictReader(io.StringIO(teks)))
    kunci = next((k for k in (rows[0].keys() if rows else []) if k and k.strip().lower() in ('stockticker', 'ticker')), None)
    if not kunci:
        raise ValueError('lajur ticker tiada')
    return sorted({(r.get(kunci) or '').strip().upper() for r in rows if (r.get(kunci) or '').strip()})


def ringkas(baris):
    tiada = [m for m in MEDAN if all(b.get(m) is None for b in baris)] if baris else list(MEDAN)
    sh = {'benar': 0, 'salah': 0, 'tiada': 0}
    for b in baris:
        v = b.get('is_shariah_compliant')
        sh['benar' if v is True else 'salah' if v is False else 'tiada'] += 1
    return tiada, sh


def tulis_csv(path, baris, lajur):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=lajur, extrasaction='ignore')
        w.writeheader()
        for b in baris:
            w.writerow({k: ('' if b.get(k) is None else b.get(k)) for k in lajur})


def main(argv=None):
    ap = argparse.ArgumentParser(description='Saringan TradingView AS + pegangan ETF Shariah -> CSV')
    ap.add_argument('--keluar', required=True)
    ap.add_argument('--harga_min', type=float, default=5.0)
    a = ap.parse_args(argv)
    os.makedirs(a.keluar, exist_ok=True)
    status = {'dijana': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'sumber': URL}
    sesi = requests.Session()
    try:
        baris, jumlah = tarik_tv(a.harga_min, sesi=sesi)
        tiada, sh = ringkas(baris)
        if not baris:
            raise ValueError('tiada baris')
        tulis_csv(os.path.join(a.keluar, 'tv_us.csv'), baris, ['ticker', 'tv_simbol'] + MEDAN)
        status['tv'] = {'baris': len(baris), 'jumlah_padan': jumlah, 'harga_min': a.harga_min,
                        'medan_tiada_data': tiada, 'is_shariah_compliant': sh}
    except Exception as e:  # fail lama dikekalkan; status merekod ralat
        status['tv'] = {'ralat': f'{type(e).__name__}: {e}'[:500]}
    etf_baris, status['etf'] = [], {}
    for nama, url in ETF.items():
        try:
            t = tarik_etf(nama, url, sesi)
            etf_baris += [{'ticker': x, 'etf': nama} for x in t]
            status['etf'][nama] = {'pegangan': len(t)}
        except Exception as e:
            status['etf'][nama] = {'ralat': f'{type(e).__name__}: {e}'[:300]}
    if etf_baris:
        tulis_csv(os.path.join(a.keluar, 'etf_shariah.csv'), etf_baris, ['ticker', 'etf'])
    json.dump(status, open(os.path.join(a.keluar, 'status.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(status, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())

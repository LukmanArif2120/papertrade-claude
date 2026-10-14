"""Alat langkah beli 9:35 pagi NY.
  python3 beli_alat.py semak  --db DIR --quote FAIL_QUOTE [--quote FAIL2] --out pesanan.json
      -> pesanan.json: senarai saham unik untuk dibeli (1 unit) + baris dikongsi/langkau
  python3 beli_alat.py isian  --db DIR --pesanan pesanan.json --sejarah FAIL_ORDER_HISTORY [...] --out isian.json
      -> isian.json untuk 'scanner.py rekod'
"""
import json, argparse, os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scanner import baca_db


def jload(p):
    d = json.load(open(p))
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        d = json.loads(d[0]['text'])
    return d


def cmd_semak(a):
    db = baca_db(a.db); beli = db.get('meta/beli', {}).get('rows', [])
    pegang = set(db.get('meta/akaun', {}).get('saham', []))
    for k, d in db.items():
        if k.startswith('kaedah/'):
            pegang |= {p['saham'] for p in d.get('posisi', [])}
    q = {}
    for f in a.quote:
        for r in jload(f)['data']['quote_list']:
            q[r['code'].split('.', 1)[1]] = r
    tarikh = pd.Timestamp.now(tz='America/New_York').strftime('%Y-%m-%d')
    rows = []; beli_unik = []
    for b in beli:
        t = b['saham']; r = q.get(t)
        x = dict(kaedah=b['kaedah'], saham=t, tarikh_masuk=tarikh)
        if r is None:
            x.update(status='langkau', catatan='tiada sebut harga'); rows.append(x); continue
        harga = float(r.get('last_price') or 0); buka = float(r.get('open_price') or 0)
        if r.get('suspension') or harga <= 0:
            x.update(status='langkau', catatan='digantung / tiada harga'); rows.append(x); continue
        henti = b.get('henti')
        if henti is not None and buka and buka <= henti:
            x.update(status='langkau', catatan=f'buka {buka} <= henti {round(henti, 2)} (peraturan langkau backtest)'); rows.append(x); continue
        if t in pegang:
            x.update(status='dikongsi', harga_isian=buka or harga, catatan='sudah dipegang; direkod pada harga buka tanpa unit kedua')
        else:
            x.update(status='beli'); beli_unik.append(t); pegang.add(t)
        rows.append(x)
    json.dump(dict(tarikh=tarikh, beli=beli_unik, rows=rows), open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(pesanan_baharu=len(beli_unik), dikongsi=sum(r['status'] == 'dikongsi' for r in rows),
                          langkau=sum(r['status'] == 'langkau' for r in rows), senarai=beli_unik), ensure_ascii=False))


def cmd_senarai(a):
    """Senarai kod untuk quote_stock_quote: saham dalam baris gilir + pengisi supaya keputusan disimpan ke fail (>=120 kod)."""
    db = baca_db(a.db); t = []
    for b in db.get('meta/beli', {}).get('rows', []):
        if b['saham'] not in t: t.append(b['saham'])
    isi = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'univ.csv')).ticker.tolist()
    for x in isi:
        if len(t) >= max(120, len(t)): break
        if x not in t: t.append(x)
    kod = ['US.' + x for x in t]
    for i in range(0, len(kod), 390):
        print(json.dumps(kod[i:i + 390]))


def cmd_isian(a):
    P = json.load(open(a.pesanan)); isi = {}
    for f in a.sejarah:
        for o in jload(f)['data'].get('orders', []):
            if int(o.get('side', 0)) != 1: continue
            if not str(o.get('text', '')).startswith('PT'): continue
            t = o['symbol']; fp = o.get('avg_fill_price')
            if fp and float(o.get('cum_qty') or 0) > 0:
                isi.setdefault(t, dict(order_id=o['order_id'], harga=float(fp)))
    out = []
    for r in P['rows']:
        r = dict(r)
        if r['status'] == 'beli':
            f = isi.get(r['saham'])
            if f: r.update(status='diisi', harga_isian=f['harga'], order_id=f['order_id'])
            else: r.update(status='gagal', catatan='pesanan belum diisi / tiada dalam sejarah')
        out.append(r)
    # baris 'dikongsi' bagi saham yang dibeli hari ini oleh kaedah lain: guna harga isian sebenar
    for r in out:
        if r['status'] == 'dikongsi' and r['saham'] in isi:
            r['harga_isian'] = isi[r['saham']]['harga']
    json.dump(out, open(a.out, 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(json.dumps(Counter(r['status'] for r in out)))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd')
    s = sp.add_parser('semak'); s.add_argument('--db'); s.add_argument('--quote', nargs='+'); s.add_argument('--out')
    i = sp.add_parser('isian'); i.add_argument('--db'); i.add_argument('--pesanan'); i.add_argument('--sejarah', nargs='+'); i.add_argument('--out')
    n = sp.add_parser('senarai'); n.add_argument('--db')
    a = p.parse_args(); {'semak': cmd_semak, 'isian': cmd_isian, 'senarai': cmd_senarai}[a.cmd](a)

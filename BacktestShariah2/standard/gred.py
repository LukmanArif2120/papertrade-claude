# Gred calon dan posisi papertrade: Sektor, Industri, RS, Pemangkin, QR (jarak ke laporan suku/earnings).
# Peraturan dan bukti: standard/tugasan_v3.md §8. Gred direkod pada hari isyarat; prestasi setiap gred dinilai
# selepas >= 20 dagangan tertutup (dashboard Prestasi > Prestasi ikut gred).
#
# Guna (imbasan 8:02 malam):
#   python3 gred.py tambah --csv papertrade/senarai_beli.csv --harga <folder harga_A/B.csv> \
#       --sektor papertrade/sektor.csv --acara <market_events.json> --pemangkin <pemangkin.json> --tarikh YYYY-MM-DD
#   (ulang untuk papertrade/watchlist.csv; --pemangkin pilihan)
import sys, os, re, csv, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import date, timedelta

import numpy as np
import pandas as pd

GRED = ['A', 'B', 'C', 'D', 'E']
MATA = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
TIADA = '–'
LAJUR = ['sektor_us', 'industri_us', 'gred_sektor', 'skor_sektor', 'gred_industri', 'skor_industri', 'rs_rating', 'gred_rs',
         'gred_pemangkin', 'mata_pemangkin', 'pemangkin', 'pemangkin_url', 'tarikh_earnings', 'hari_ke_earnings', 'sumber_earnings', 'gred_qr',
         'gred_keseluruhan', 'gred_pada']


# ---------- RS rating (gaya IBD, 1–99) ----------
def rs_rating(close):
    """close: DataFrame (index tarikh, lajur ticker). Pulangkan Series RS 1–99 pada bar terakhir.
    Skor = 40% pulangan 63 hari terkini + 20% setiap satu daripada tiga suku sebelumnya; pangkat persentil
    berbanding semua saham dalam stor harga. Saham dengan < 253 bar tiada RS."""
    c = close.sort_index()
    if len(c) < 253:
        return pd.Series(dtype=float)
    a = c.iloc[-1]
    q = [c.iloc[-64], c.iloc[-127], c.iloc[-190], c.iloc[-253]]
    skor = 0.4 * (a / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1)
    skor = skor.replace([np.inf, -np.inf], np.nan).dropna()
    return (skor.rank(pct=True) * 98 + 1).round().astype(int).clip(1, 99)


def gred_rs(rs):
    """Ujian 2019–2026 (431 saham, pulangan 21 hari): RS 90+ purata +4.2% lawan +1.6–2.2% bagi gred lain,
    dan mendahului setiap tahun. Sempadan ikut ujian itu."""
    if rs is None or (isinstance(rs, float) and np.isnan(rs)):
        return TIADA
    return 'A' if rs >= 90 else 'B' if rs >= 80 else 'C' if rs >= 60 else 'D' if rs >= 40 else 'E'


# ---------- Sektor / Industri (skor panas SST, 0–100) ----------
def gred_kumpulan(skor):
    """Ujian 13 Okt 2026: skor panas/fasa sektor TIDAK meramal pulangan 1–3 bulan. Gred direkod untuk diuji
    semula dalam papertrade, bukan penapis."""
    if skor is None or (isinstance(skor, float) and np.isnan(skor)):
        return TIADA
    return 'A' if skor >= 80 else 'B' if skor >= 60 else 'C' if skor >= 40 else 'D' if skor >= 20 else 'E'


def peta_pasaran(path_csv):
    """sektor_pasaran.csv (seluruh pasaran AS) -> ({sektor: skor}, {industri: skor}) snapshot terkini."""
    return peta_sektor(path_csv)


def peta_sektor(path_csv):
    """sektor.csv -> ({sektor: skor_panas}, {industri: skor_panas}) bagi snapshot terkini."""
    rows = list(csv.DictReader(open(path_csv, newline='', encoding='utf-8')))
    if not rows:
        return {}, {}
    akhir = max(r['tarikh'] for r in rows)
    sek, ind = {}, {}
    for r in rows:
        if r['tarikh'] != akhir:
            continue
        try:
            v = float(r['skor_panas'])
        except (TypeError, ValueError):
            continue
        (sek if r['jenis'] == 'Sektor' else ind)[r['nama']] = v
    return sek, ind


# ---------- QR: jarak ke laporan suku (earnings) ----------
def hari_dagangan(dari, ke):
    """Bilangan hari bekerja (Isn–Jum) selepas `dari` hingga `ke` (anggaran hari dagangan; cuti diabaikan)."""
    if ke <= dari:
        return 0
    return int(np.busday_count(dari + timedelta(days=1), ke + timedelta(days=1)))


def gred_qr(hari):
    """Pegangan swing ~20 hari dagangan: makin jauh earnings, makin kecil risiko jurang harga semasa pegang.
    hari=None bermaksud tiada earnings dalam tetingkap 30 hari kalendar (≈ 21 hari dagangan) -> A."""
    if hari is None:
        return 'A'
    return 'A' if hari > 21 else 'B' if hari > 15 else 'C' if hari > 10 else 'D' if hari > 5 else 'E'


def peta_earnings(path_json, hari_ini):
    """Fail keputusan SST market_events (daysLookahead 30) -> {ticker: tarikh earnings terdekat >= hari ini}."""
    d = json.load(open(path_json, encoding='utf-8'))
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        d = json.loads(d[0]['text'])
    rows = d.get('data', {}).get('data', []) if isinstance(d, dict) else d
    out = {}
    for r in rows:
        if r.get('eventType') != 'EARNINGS':
            continue
        try:
            t = date.fromisoformat(r['eventDate'][:10])
        except (KeyError, ValueError):
            continue
        k = r.get('ticker')
        if k and t >= hari_ini and (k not in out or t < out[k]):
            out[k] = t
    return out


def ringkas_earnings(path_json, hari_ini):
    """Fail Moomoo quote_financials_earnings_price_history -> dict:
       earnings_lalu_tarikh, earnings_lalu_hari (hari dagangan sejak), earnings_gerak_pct (reaksi tutup hari
       pertama selepas pengumuman lawan tutup sebelumnya), earnings_anggaran (lalu + 91 hari)."""
    d = json.load(open(path_json, encoding='utf-8'))
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        d = json.loads(d[0]['text'])
    rec = d.get('data', {}).get('records', [])
    lalu = [r for r in rec if r.get('pub_trading_day_str') and r['pub_trading_day_str'] <= hari_ini.isoformat()]
    if not lalu:
        return {}
    pub = max(r['pub_trading_day_str'] for r in lalu)
    hari = {r['trading_day_str']: r for r in rec if r.get('pub_trading_day_str') == pub and r.get('trading_day_str')}
    jenis = next((r.get('pub_type') for r in hari.values()), None)
    # pub_type 2 = selepas tutup: reaksi pada hari dagangan berikutnya; selainnya pada hari pengumuman
    selepas = sorted(t for t in hari if (t > pub if jenis == 2 else t >= pub))
    out = {'earnings_lalu_tarikh': pub, 'earnings_lalu_hari': hari_dagangan(date.fromisoformat(pub), hari_ini),
           'earnings_anggaran': (date.fromisoformat(pub) + timedelta(days=91)).isoformat(), 'earnings_gerak_pct': None}
    if selepas:
        r = hari[selepas[0]]
        sebelum = r.get('last_close_price')
        if sebelum and r.get('close_price'):
            out['earnings_gerak_pct'] = round((r['close_price'] / sebelum - 1) * 100, 2)
    return out


# ---------- Pemangkin (kenapa saham bergerak) ----------
POSITIF = [r'\bupgrade', r'raises? (its )?(price )?target', r'initiates?.*\b(buy|outperform|overweight|strong buy)\b',
           r'\bbeats?\b', r'record (revenue|quarter|sales)', r'raises? (guidance|outlook)', r'\bwins?\b.*contract',
           r'\bapproval\b', r'\bbuyback\b']
NEGATIF = [r'\bdowngrade', r'(cuts?|lowers?) (its )?(price )?target', r'initiates?.*\b(sell|underperform|underweight)\b',
           r'\bmiss(es|ed)?\b', r'(cuts?|lowers?) (guidance|outlook)', r'\blawsuit\b', r'\boffering\b', r'\bprobe\b',
           r'\binvestigation\b', r'\brecall\b']


def nilai_tajuk(tajuk):
    t = (tajuk or '').lower()
    if any(re.search(p, t) for p in NEGATIF):
        return -1
    if any(re.search(p, t) for p in POSITIF):
        return 1
    return 0


def mata_pemangkin(p):
    """p: dict untuk satu saham (dikumpul oleh tugasan imbasan):
         berita: [{'tajuk': str, 'hari_lalu': int, 'url': str}]  (Moomoo quote_news_search + SST search_news, 10 hari)
         earnings_lalu_hari: int|None  (hari dagangan sejak earnings terakhir)
         earnings_gerak_pct: float|None (perubahan harga hari earnings, Moomoo earnings_price_history)
         volum_nisbah: float|None (volum 5 hari / purata 50 hari)  ; naik_5h: float|None (% 5 hari)
         institusi: 'kumpul'|'agih'|None (SST institutional_flow)
       Pulangkan (mata, ringkasan)."""
    m, ring = 0, []
    berita = [b for b in (p.get('berita') or []) if (b.get('hari_lalu') is None or b['hari_lalu'] <= 10)]
    pos = sum(1 for b in berita if nilai_tajuk(b.get('tajuk')) > 0)
    neg = sum(1 for b in berita if nilai_tajuk(b.get('tajuk')) < 0)
    m += min(pos, 2) - min(neg, 2)
    if pos: ring.append(f'{pos} berita positif')
    if neg: ring.append(f'{neg} berita negatif')
    if len(berita) >= 3:
        m += 1; ring.append(f'{len(berita)} berita/10 hari')
    eh, eg = p.get('earnings_lalu_hari'), p.get('earnings_gerak_pct')
    if eh is not None and eh <= 30 and eg is not None:
        if eg >= 3: m += 2; ring.append(f'earnings {eh} hari lalu +{eg:.1f}%')
        elif eg <= -3: m -= 2; ring.append(f'earnings {eh} hari lalu {eg:.1f}%')
    vn, n5 = p.get('volum_nisbah'), p.get('naik_5h')
    if vn is not None and vn >= 2 and (n5 or 0) > 0:
        m += 1; ring.append(f'volum {vn:.1f}× naik')
    ins = p.get('institusi')
    if ins == 'kumpul': m += 1; ring.append('institusi kumpul')
    elif ins == 'agih': m -= 1; ring.append('institusi agih')
    return m, '; '.join(ring) or 'tiada pemangkin dikesan'


def pautan_berita(berita, maks=2):
    """Pautan berita untuk dashboard: berita positif dahulu, kemudian terkini; hanya yang ada URL https.
    Pulangkan JSON [{"tajuk", "url"}] (maks 2) atau '' jika tiada."""
    b = [x for x in (berita or []) if str(x.get('url') or '').startswith('https://')
         and (x.get('hari_lalu') is None or x['hari_lalu'] <= 10)]
    b.sort(key=lambda x: (-nilai_tajuk(x.get('tajuk')), x.get('hari_lalu') if x.get('hari_lalu') is not None else 99))
    out = [{'tajuk': str(x.get('tajuk') or '')[:140], 'url': x['url']} for x in b[:maks]]
    return json.dumps(out, ensure_ascii=False) if out else ''


def gred_pemangkin(mata):
    if mata is None:
        return TIADA
    return 'A' if mata >= 4 else 'B' if mata == 3 else 'C' if mata >= 1 else 'D' if mata == 0 else 'E'


def gred_keseluruhan(gred):
    """Purata mata gred yang ada (A=4 … E=0) -> huruf. Belum diuji; untuk paparan sahaja."""
    v = [MATA[g] for g in gred if g in MATA]
    if not v:
        return TIADA
    x = sum(v) / len(v)
    return 'A' if x >= 3.5 else 'B' if x >= 2.5 else 'C' if x >= 1.5 else 'D' if x >= 0.5 else 'E'


# ---------- CLI ----------
def muat_harga(folder):
    fr = []
    for nm in ['harga_A.csv', 'harga_B.csv']:
        p = os.path.join(folder, nm)
        if os.path.exists(p):
            fr.append(pd.read_csv(p, usecols=['ticker', 'date', 'close', 'volume']))
    if not fr:
        raise SystemExit(f'Tiada harga_A.csv/harga_B.csv dalam {folder}')
    d = pd.concat(fr).drop_duplicates(['ticker', 'date'], keep='last')
    d['date'] = pd.to_datetime(d['date'].astype(str))
    c = d.pivot(index='date', columns='ticker', values='close').sort_index()
    v = d.pivot(index='date', columns='ticker', values='volume').sort_index()
    return c, v


def ambil(r, *k):
    for x in k:
        if x in r and r[x] not in (None, ''):
            return r[x]
    return None


def tambah(a):
    rows = list(csv.DictReader(open(a.csv, newline='', encoding='utf-8')))
    lajur = list(rows[0].keys()) if rows else []
    hari_ini = date.fromisoformat(a.tarikh)
    c, v = muat_harga(a.harga)
    rs = rs_rating(c)
    vn = (v.iloc[-5:].mean() / v.iloc[-50:].mean()) if len(v) >= 50 else pd.Series(dtype=float)
    n5 = (c.iloc[-1] / c.iloc[-6] - 1) * 100 if len(c) >= 6 else pd.Series(dtype=float)
    sek, ind = peta_sektor(a.sektor)
    # Utama: kekuatan seluruh pasaran AS (sektor_pasaran.py) dengan industri Moomoo setiap saham
    pusek, puind, pind = {}, {}, {}
    if a.pasaran and a.peta and os.path.exists(a.pasaran) and os.path.exists(a.peta):
        from sektor_pasaran import SEKTOR_INDUSTRI
        pusek, puind = peta_pasaran(a.pasaran)
        pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(a.peta, newline='', encoding='utf-8'))}
    ear = peta_earnings(a.acara, hari_ini) if a.acara else None
    pem = json.load(open(a.pemangkin, encoding='utf-8')) if a.pemangkin else {}
    for r in rows:
        t = ambil(r, 'saham', 'Saham')
        iu = pind.get(t); su = SEKTOR_INDUSTRI.get(iu) if iu else None
        r['industri_us'] = iu or ''; r['sektor_us'] = su or ''
        s1 = pusek.get(su) if su in pusek else sek.get(ambil(r, 'sektor', 'Sektor'))
        s2 = puind.get(iu) if iu in puind else ind.get(ambil(r, 'industri', 'Industri'))
        r['skor_sektor'] = '' if s1 is None else round(s1, 1); r['gred_sektor'] = gred_kumpulan(s1)
        r['skor_industri'] = '' if s2 is None else round(s2, 1); r['gred_industri'] = gred_kumpulan(s2)
        x = int(rs[t]) if t in rs.index else None
        r['rs_rating'] = '' if x is None else x; r['gred_rs'] = gred_rs(x)
        te, sumber = (ear or {}).get(t), 'SST'
        if te is None and (pem.get(t) or {}).get('earnings_anggaran'):
            te, sumber = date.fromisoformat(pem[t]['earnings_anggaran']), 'anggaran'
            if te < hari_ini:
                te = None
        if te is None and ear is None:
            r['tarikh_earnings'] = ''; r['hari_ke_earnings'] = ''; r['sumber_earnings'] = 'tiada data'; r['gred_qr'] = TIADA
        else:
            h = hari_dagangan(hari_ini, te) if te else None
            r['tarikh_earnings'] = te.isoformat() if te else ''
            r['hari_ke_earnings'] = '' if h is None else h
            r['sumber_earnings'] = sumber if te else 'tiada dalam 30 hari (SST)'
            r['gred_qr'] = gred_qr(h)
        if t in pem:
            p = dict(pem[t])
            p.setdefault('volum_nisbah', None if t not in vn.index or pd.isna(vn[t]) else float(vn[t]))
            p.setdefault('naik_5h', None if t not in n5.index or pd.isna(n5[t]) else float(n5[t]))
            m, ring = mata_pemangkin(p)
            r['mata_pemangkin'] = m; r['pemangkin'] = ring; r['gred_pemangkin'] = gred_pemangkin(m)
            r['pemangkin_url'] = pautan_berita(p.get('berita'))
        else:
            r['mata_pemangkin'] = ''; r['pemangkin'] = 'belum dikumpul'; r['gred_pemangkin'] = TIADA
            r['pemangkin_url'] = ''
        r['gred_keseluruhan'] = gred_keseluruhan([r['gred_sektor'], r['gred_industri'], r['gred_rs'],
                                                  r['gred_pemangkin'], r['gred_qr']])
        r['gred_pada'] = a.tarikh
    out = lajur + [k for k in LAJUR if k not in lajur]
    with open(a.csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out)
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    for k in ['gred_sektor', 'gred_industri', 'gred_rs', 'gred_pemangkin', 'gred_qr', 'gred_keseluruhan']:
        print(k, dict(sorted(Counter(r[k] for r in rows).items())))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Tambah lajur gred ke CSV calon (senarai_beli / watchlist)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    t = sp.add_parser('tambah')
    t.add_argument('--csv', required=True)
    t.add_argument('--harga', required=True, help='folder harga_A.csv / harga_B.csv (stor harga dashboard)')
    t.add_argument('--sektor', required=True, help='papertrade/sektor.csv (sandaran: snapshot SST)')
    t.add_argument('--pasaran', help='papertrade/sektor_pasaran.csv (utama: seluruh pasaran AS)')
    t.add_argument('--peta', help='papertrade/peta_industri.csv (ticker -> industri Moomoo)')
    t.add_argument('--acara', help='JSON SST market_events (daysLookahead 30)')
    t.add_argument('--pemangkin', help='JSON {ticker: {berita [{tajuk, hari_lalu, url}], earnings_lalu_hari, earnings_gerak_pct, institusi}}')
    t.add_argument('--tarikh', required=True, help='tarikh imbasan YYYY-MM-DD')
    e = sp.add_parser('earnings', help='ringkas fail Moomoo earnings_price_history -> JSON')
    e.add_argument('fail'); e.add_argument('--tarikh', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'tambah':
        tambah(a)
    elif a.cmd == 'earnings':
        print(json.dumps(ringkas_earnings(a.fail, date.fromisoformat(a.tarikh))))


if __name__ == '__main__':
    main()

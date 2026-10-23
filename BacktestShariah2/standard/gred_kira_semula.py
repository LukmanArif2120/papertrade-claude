# Kira semula gred dengan skema semasa bagi baris bergred dalam fail posisi, senarai_beli dan watchlist, pada tarikh
# rujukan asal (keputusan pengguna 18 Okt 2026: "semua dimensi + db"):
#   Sektor/Industri v2 : data/kumpulan/gred_kumpulan_sejarah.csv bagi sesi rujukan (tiada -> lajur tidak diubah, dikira)
#   RS skema 18 Okt    : rs_semua pada harga <= sesi rujukan (sama seperti gred_rs_semula.py)
#   QR                 : hari_ke_earnings asal + peraturan selepas QR (earnings lalu sebelum hari imbasan)
#   Pemangkin v3       : K1 daripada hari_ke_earnings asal; K2 daripada earnings lalu + harga <= sesi rujukan; veto
#                        berita hanya jika pemangkin.json ada entri yang dikumpul pada hari imbasan itu
#   Gred keseluruhan v2: Industri (kecuali kaedah pantulan), Pemangkin, QR
# Sesi rujukan D = tarikh_isyarat, atau tarikh_data (watchlist), atau sesi sebelum tarikh_beli; hari imbasan = tarikh
# gred_pada asal jika ada (selainnya sesi selepas D). Earnings lalu: data/pemangkin/sejarah/eps.csv (yfinance) dan
# kalendar Nasdaq. Lajur lain tidak disentuh; gred_pada ditambah catatan.
# Guna: python3 BacktestShariah2/standard/gred_kira_semula.py --harga <folder stor> [--folder papertrade] [--tarikh YYYY-MM-DD]
import argparse, csv, json, os, re, sys
from collections import Counter
from datetime import date, timedelta

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gred as G  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402
from sektor_pasaran import SEKTOR_INDUSTRI  # noqa: E402

BS2 = os.path.dirname(HERE)
TANDA = 'skema semasa'


def peta_kumpulan_sejarah(path):
    """gred_kumpulan_sejarah.csv -> {tarikh: ({sektor: (skor, gred)}, {industri: (skor, gred)})}"""
    out = {}
    if not os.path.exists(path):
        return out
    for r in csv.DictReader(open(path, newline='', encoding='utf-8')):
        if r['gred'] not in G.GRED:
            continue
        sek, ind = out.setdefault(r['tarikh'], ({}, {}))
        (sek if r['jenis'] == 'Sektor' else ind)[r['nama']] = (float(r['skor']), r['gred'])
    return out


def peta_earnings_lalu(eps_csv, nasdaq_json):
    """{ticker: [(tarikh, selepas_tutup True/False/None), ...] menaik} daripada eps.csv (masa New York) dan Nasdaq."""
    out = {}
    if eps_csv and os.path.exists(eps_csv):
        for r in csv.DictReader(open(eps_csv, newline='', encoding='utf-8')):
            jam = int(r['masa'][:2]) if (r.get('masa') or '')[:2].isdigit() else None
            st = None if jam is None or jam == 0 else True if jam >= 16 else False if jam < 10 else None
            out.setdefault(r['ticker'], {})[r['tarikh']] = st
    if nasdaq_json and os.path.exists(nasdaq_json):
        d = json.load(open(nasdaq_json, encoding='utf-8'))
        for t, e in (d.get('saham') or {}).items():
            if e.get('lalu'):
                m = e.get('lalu_masa') or ''
                st = True if m == 'time-after-hours' else False if m == 'time-pre-market' else None
                out.setdefault(t, {}).setdefault(e['lalu'], st)
    return {t: sorted(v.items()) for t, v in out.items()}


def lalu_sebelum(senarai, hari):
    """Earnings terakhir sebelum `hari` (date) -> (date, selepas_tutup) atau (None, None)."""
    x = [(d, s) for d, s in senarai or [] if d < hari.isoformat()]
    return (date.fromisoformat(x[-1][0]), x[-1][1]) if x else (None, None)


def kira_baris(r, D, hi, ctx, kira):
    """Kira semula satu baris pada sesi rujukan D (Timestamp) dan hari imbasan hi (date)."""
    t = G.ambil(r, 'saham', 'Saham')
    c, v, spy = ctx['c'], ctx['v'], ctx['spy']
    k = ctx['cache'].get(D)
    if k is None:
        cc = c[c.index <= D]
        k = ctx['cache'][D] = (G.rs_semua(cc, spy, ctx['rs']) if len(cc) else (pd.DataFrame(), None))
    rsd, atas = k
    G.isi_rs(r, rsd.loc[t] if t in rsd.index else None, atas)
    # Sektor / Industri v2
    kum = ctx['kum'].get(str(D.date()))
    if kum:
        iu = r.get('industri_us') or ctx['pind'].get(t) or ''
        su = SEKTOR_INDUSTRI.get(iu) if iu else None
        (s1, g1), (s2, g2) = kum[0].get(su, (None, G.TIADA)), kum[1].get(iu, (None, G.TIADA))
        if iu and g2 == G.TIADA and g1 != G.TIADA:   # industri < 3 saham: sandaran sektor (gred.SANDARAN_INDUSTRI)
            s2, g2 = s1, g1
            if G.SANDARAN_INDUSTRI not in (r.get('gred_pada') or ''):
                r['gred_pada'] = (r.get('gred_pada') or '') + '; ' + G.SANDARAN_INDUSTRI
        r['skor_sektor'] = '' if s1 is None else round(s1, 1); r['gred_sektor'] = g1
        r['skor_industri'] = '' if s2 is None else round(s2, 1); r['gred_industri'] = g2
    else:
        kira['sektor/industri tiada data sesi itu'] += 1
    # QR + Pemangkin v3
    h = int(float(r['hari_ke_earnings'])) if str(r.get('hari_ke_earnings') or '').strip() not in ('', '–') else None
    lalu, st = lalu_sebelum(ctx['ear'].get(t), hi)
    if r.get('gred_qr') not in ('', G.TIADA, None):
        sj = G.sejak_qr(lalu, hi)
        r['gred_qr'] = G.gred_qr(h, sj)
        r['sumber_earnings'] = G.tanda_pasca_qr(re.sub(r'; QR lalu \d+ hari$', '', r.get('sumber_earnings') or ''), sj)
    pe = ctx['pem'].get(t) or {}
    p = {'berita': pe.get('berita')} if pe.get('dikumpul') == hi.isoformat() else {}
    if lalu:
        p.update(earnings_lalu_tarikh=lalu.isoformat(), earnings_selepas_tutup=st)
    if r.get('gred_qr') in ('', G.TIADA, None) and not lalu and not p.get('berita'):
        r['mata_pemangkin'] = ''; r['pemangkin'] = 'tiada data'; r['gred_pemangkin'] = G.TIADA; r['pemangkin_url'] = ''
    else:
        ada = t in c.columns
        cc, vv = (c[t][c.index <= D], v[t][v.index <= D]) if ada else (None, None)
        m, g, ring = G.nilai_pemangkin(p, hi, h, cc, vv, spy[spy.index <= D] if spy is not None else None)
        r['mata_pemangkin'] = m; r['pemangkin'] = ring; r['gred_pemangkin'] = g
        r['pemangkin_url'] = G.pautan_berita(p.get('berita'), hari_ini=hi)
        if not p.get('berita'):
            kira['pemangkin tanpa berita (veto tidak disemak)'] += 1
    # Gred keseluruhan v2
    r['gred_keseluruhan'] = G.keseluruhan_baris(r, ctx['jenis'])
    gp = re.sub(r'; ' + TANDA + r' [^;]*$', '', r.get('gred_pada') or '')
    # "S/I v2" dalam gred_pada: dashboard Prestasi hanya mengira gred Sektor/Industri baris bertanda ini (konvensyen SKEMA)
    r['gred_pada'] = f'{gp}; {TANDA} {ctx["tarikh"]} ({"S/I v2, " if kum else ""}rujukan {D.date()})'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--harga', required=True, help='folder harga_A/B.csv + harga_idx.csv')
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--rs', default=os.path.join(BS2, 'data', 'rs'))
    ap.add_argument('--kumpulan', default=os.path.join(BS2, 'data', 'kumpulan', 'gred_kumpulan_sejarah.csv'))
    ap.add_argument('--eps', default=os.path.join(BS2, 'data', 'pemangkin', 'sejarah', 'eps.csv'))
    ap.add_argument('--nasdaq', default=os.path.join(BS2, 'data', 'pemangkin', 'earnings_nasdaq.json'))
    ap.add_argument('--tarikh', default=date.today().isoformat())
    a = ap.parse_args(argv)
    c, v = G.muat_harga(a.harga)
    sesi = list(c.index)
    peta = os.path.join(a.folder, 'peta_industri.csv')
    pem = os.path.join(a.folder, 'pemangkin.json')
    ctx = dict(c=c, v=v, spy=G.muat_spy(a.harga), rs=a.rs, cache={}, tarikh=a.tarikh,
               kum=peta_kumpulan_sejarah(a.kumpulan), ear=peta_earnings_lalu(a.eps, a.nasdaq),
               pind={r['ticker']: r['industri'] for r in csv.DictReader(open(peta, newline='', encoding='utf-8'))}
               if os.path.exists(peta) else {},
               pem=json.load(open(pem, encoding='utf-8')) if os.path.exists(pem) else {}, jenis=G.peta_jenis_kaedah())
    kira, n = Counter(), 0
    for p in fail_posisi(a.folder) + [os.path.join(a.folder, f) for f in ('senarai_beli.csv', 'watchlist.csv')]:
        if not os.path.exists(p):
            continue
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        if 'gred_keseluruhan' not in lajur:
            continue
        ubah = 0
        for r in rows:
            if not r.get('gred_pada'):
                continue
            ti = r.get('tarikh_isyarat') or r.get('tarikh_data') or ''
            if not ti and r.get('tarikh_beli'):
                sb = [x for x in sesi if x < pd.Timestamp(r['tarikh_beli'])]
                ti = str(sb[-1].date()) if sb else ''
            if not ti:
                kira['tiada tarikh rujukan'] += 1
                continue
            D = max([x for x in sesi if x <= pd.Timestamp(ti)], default=None)
            if D is None:
                kira['tiada harga sesi rujukan'] += 1
                continue
            gp = G._tarikh((r.get('gred_pada') or '')[:10])   # hari imbasan asal jika direkod
            sl = [x for x in sesi if x > D]
            hi = gp if gp and gp >= D.date() else sl[0].date() if sl else (D + pd.offsets.BDay(1)).date()
            kira_baris(r, D, hi, ctx, kira)
            kira[f"P {r['gred_pemangkin']}"] += 1
            ubah += 1
        if ubah:
            lajur += [k for k in G.LAJUR if k not in lajur]
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
        n += ubah
    print(json.dumps(dict(dikira_semula=n, **dict(sorted(kira.items()))), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())

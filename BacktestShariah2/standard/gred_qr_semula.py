# Betulkan lajur QR (audit 18 Okt 2026; keputusan pengguna) bagi baris bergred dalam fail posisi, senarai_beli dan
# watchlist, pada tarikh rujukan asal gred (gred_pada: "QR pada X", jika tiada tarikh pertama). Tarikh SST kerap salah
# (146/915 sepadan Nasdaq, 500/1,323 hujung minggu), jadi tarikh earnings diambil daripada kalendar Nasdaq: sejarah
# data/pemangkin/tarikh_pendapatan.csv + data/pemangkin/earnings_nasdaq.json (lalu/seterusnya). Saham yang tidak diliputi
# Nasdaq tidak disentuh. Peraturan selepas QR (gred_qr sejak) dipakai. Pemangkin v3: hanya K1 (earnings 1–21 hari lagi)
# dilaras ikut jarak baharu; baris dengan teks pemangkin bukan v3 tidak disentuh. gred_keseluruhan dikira semula bagi
# SEMUA baris bergred dengan peraturan v2 (G.keseluruhan_baris) supaya satu peraturan sahaja dipakai.
# Guna: python3 BacktestShariah2/standard/gred_qr_semula.py [--folder papertrade] [--tarikh YYYY-MM-DD] [--uji]
import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gred as G  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402

BS2 = os.path.dirname(HERE)
TANDA = 'QR Nasdaq 18 Okt'
K1 = re.compile(r'^earnings (\d+) hari dagangan lagi \(premium pengumuman\) \+(\d)$')
V3 = re.compile(r'^(reaksi earnings .*|earnings \d+ hari dagangan lagi .*|had [A-E]: .*|tiada pemangkin)$')
PANAS = '🔥 PANAS · '


def kalendar(pemangkin):
    """-> ({ticker: set(tarikh pengumuman)}, set ticker diliputi Nasdaq, tarikh hujung tetingkap Nasdaq)."""
    sb = defaultdict(set)
    with open(os.path.join(pemangkin, 'tarikh_pendapatan.csv'), newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            d = G._tarikh(r['d0'])
            if d:
                sb[r['ticker']].add(d)
    nas = json.load(open(os.path.join(pemangkin, 'earnings_nasdaq.json'), encoding='utf-8'))
    for t, e in (nas.get('saham') or {}).items():
        for k in ('lalu', 'seterusnya'):
            d = G._tarikh(e.get(k))
            if d:
                sb[t].add(d)
    return sb, set(sb), G._tarikh(nas.get('hingga'))


def tarikh_ruj(gp):
    m = re.search(r'QR pada (\d{4}-\d\d-\d\d)', gp or '') or re.search(r'(\d{4}-\d\d-\d\d)', gp or '')
    return G._tarikh(m.group(1)) if m else None


def laras_pemangkin(r, h):
    """Laras K1 pemangkin v3 ikut jarak QR baharu h. Pulang True jika baris dikemas kini, None jika bukan v3."""
    teks = r.get('pemangkin') or ''
    seg = [s for s in teks.replace(PANAS, '', 1).split('; ') if s]
    if r.get('mata_pemangkin') in (None, '') or not seg or not all(V3.match(s) for s in seg):
        return None
    lama = next((K1.match(s) for s in seg if K1.match(s)), None)
    k1_lama = int(lama.group(2)) if lama else 0
    k1 = (2 if h >= 6 else 1) if h is not None and 1 <= h <= 21 else 0
    seg = [s for s in seg if not K1.match(s) and s != 'tiada pemangkin']
    if k1:
        i = sum(1 for s in seg if s.startswith('reaksi earnings'))
        seg.insert(i, f'earnings {h} hari dagangan lagi (premium pengumuman) +{k1}')
    mata = int(float(r['mata_pemangkin'])) - k1_lama + k1
    g = G.gred_pemangkin(mata)
    for s in seg:
        m = re.match(r'had ([A-E]): ', s)
        if m and G.GRED.index(g) < G.GRED.index(m.group(1)):
            g = m.group(1)
    panas = any(s.startswith('reaksi earnings') for s in seg) and g == 'A'
    r['mata_pemangkin'] = mata
    r['gred_pemangkin'] = g
    r['pemangkin'] = (PANAS if panas else '') + ('; '.join(seg) or 'tiada pemangkin')
    return True


def betul(r, sb, liput, hingga):
    """Kira semula QR satu baris. Pulang (ubah_qr, status)."""
    t = G.ambil(r, 'saham', 'Saham')
    ref = tarikh_ruj(r.get('gred_pada'))
    if not t or not ref or t not in liput:
        return False, 'tidak diliputi'
    akan = sorted(d for d in sb[t] if d >= ref)
    te = akan[0] if akan and hingga and akan[0] <= hingga else None     # sama seperti gred.py: seterusnya dalam tetingkap
    if te is None and (not hingga or ref + timedelta(days=35) > hingga):
        return False, 'di luar tetingkap Nasdaq'
    ang = G._tarikh(r.get('tarikh_earnings'))
    if te is None and (r.get('sumber_earnings') or '').startswith('anggaran') and ang and ang > ref + timedelta(days=35):
        return False, 'anggaran di luar 35 hari (kekal)'
    lalu = [d for d in sb[t] if d < ref]
    sj = G.sejak_qr(max(lalu), ref) if lalu else None
    h = G.hari_dagangan(ref, te) if te else None
    baru = {'tarikh_earnings': te.isoformat() if te else '', 'hari_ke_earnings': '' if h is None else str(h),
            'sumber_earnings': G.tanda_pasca_qr('Nasdaq' if te else 'tiada dalam 35 hari (Nasdaq)', sj),
            'gred_qr': G.gred_qr(h, sj)}
    if all(str(r.get(k, '')) == v for k, v in baru.items()):
        return False, 'sama'
    h_lama = r.get('hari_ke_earnings')
    r.update(baru)
    pem = laras_pemangkin(r, h) if str(h_lama or '') != baru['hari_ke_earnings'] else True
    gp = r.get('gred_pada') or ''
    if TANDA not in gp:
        r['gred_pada'] = gp + '; ' + TANDA
    return True, 'dibetulkan' if pem else 'dibetulkan (pemangkin bukan v3, tidak dilaras)'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--pemangkin', default=os.path.join(BS2, 'data', 'pemangkin'))
    ap.add_argument('--uji', action='store_true', help='kira sahaja; jangan tulis fail')
    a = ap.parse_args(argv)
    sb, liput, hingga = kalendar(a.pemangkin)
    jenis = G.peta_jenis_kaedah()
    kira, ubah_gred, n_kes = Counter(), Counter(), 0
    fail = fail_posisi(a.folder) + [os.path.join(a.folder, f) for f in ('senarai_beli.csv', 'watchlist.csv')]
    for p in fail:
        if not os.path.exists(p):
            continue
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        if 'gred_qr' not in lajur:
            continue
        ubah = 0
        for r in rows:
            if not r.get('gred_keseluruhan') and not r.get('gred_qr'):
                continue
            q0, k0 = r.get('gred_qr'), r.get('gred_keseluruhan')
            ok, st = betul(r, sb, liput, hingga)
            kira[st] += 1
            if r.get('gred_keseluruhan'):
                r['gred_keseluruhan'] = G.keseluruhan_baris(r, jenis)
            if r.get('gred_qr') != q0:
                ubah_gred[f'QR {q0}->{r["gred_qr"]}'] += 1
            if r.get('gred_keseluruhan') != k0:
                n_kes += 1
            ubah += ok or r.get('gred_keseluruhan') != k0
        if ubah and not a.uji:
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
    print(json.dumps(dict(status=kira, ubah_gred_qr=dict(ubah_gred.most_common()), ubah_keseluruhan=n_kes,
                          uji=a.uji), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
